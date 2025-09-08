#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import sys
from typing import Dict, Tuple, Optional


class ChatServer:
    """멀티스레드 TCP 채팅 서버."""

    def __init__(self, host: str = '0.0.0.0', port: int = 5000) -> None:
        self.host = host
        self.port = port
        self.server_sock: Optional[socket.socket] = None
        self.clients: Dict[socket.socket, str] = {}
        self.lock = threading.Lock()
        self.running = False

    def start(self) -> None:
        """서버 소켓을 열고 클라이언트 접속을 수락한다."""
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 재시작 시 TIME_WAIT 포트 즉시 재사용
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen()
        self.running = True
        print(f'[SYSTEM] 서버 시작: {self.host}:{self.port}')

        try:
            while self.running:
                try:
                    client_sock, addr = self.server_sock.accept()
                except OSError:
                    break
                threading.Thread(
                    target=self._handle_client,
                    args=(client_sock, addr),
                    daemon=True
                ).start()
        except KeyboardInterrupt:
            print('\n[SYSTEM] 서버 종료 중...')
        finally:
            self._shutdown()

    def _shutdown(self) -> None:
        """서버 및 클라이언트 소켓 정리."""
        self.running = False
        with self.lock:
            for sock in list(self.clients.keys()):
                try:
                    sock.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                sock.close()
            self.clients.clear()
        if self.server_sock:
            try:
                self.server_sock.close()
            except OSError:
                pass
        print('[SYSTEM] 서버가 종료되었습니다.')

    def _register_client(self, sock: socket.socket, nickname: str) -> None:
        with self.lock:
            self.clients[sock] = nickname

    def _remove_client(self, sock: socket.socket) -> Optional[str]:
        with self.lock:
            nickname = self.clients.pop(sock, None)
        try:
            sock.close()
        except OSError:
            pass
        return nickname

    def _broadcast(self, message: str, except_sock: Optional[socket.socket] = None) -> None:
        """모든 접속자에게 메시지 전송."""
        data = f'{message}\n'.encode('utf-8', errors='ignore')
        with self.lock:
            targets = [s for s in self.clients.keys() if s is not except_sock]
        for s in targets:
            try:
                s.sendall(data)
            except OSError:
                # 보낼 수 없는 소켓은 정리
                self._remove_client(s)

    def _send_to_user(self, target_nick: str, message: str) -> bool:
        """특정 닉네임에게만 전송. 성공 여부 반환."""
        with self.lock:
            for s, nick in self.clients.items():
                if nick == target_nick:
                    try:
                        s.sendall(f'{message}\n'.encode('utf-8', errors='ignore'))
                        return True
                    except OSError:
                        self._remove_client(s)
                        return False
        return False

    def _parse_first_line_as_nick(self, line: str) -> str:
        """첫 줄에서 닉네임을 파싱한다. 클라이언트는 접속 후 바로 닉네임을 보낸다."""
        # 허용 포맷: /nick 닉네임  또는  NICK 닉네임  또는  그냥 닉네임
        line = line.strip()
        if not line:
            return '익명'
        if line.lower().startswith('/nick '):
            return line[6:].strip() or '익명'
        if line.lower().startswith('nick '):
            return line[5:].strip() or '익명'
        return line

    def _handle_client(self, client_sock: socket.socket, addr: Tuple[str, int]) -> None:
        """개별 클라이언트 스레드."""
        file_r = client_sock.makefile('r', encoding='utf-8', newline='\n')
        file_w = client_sock.makefile('w', encoding='utf-8', newline='\n')
        try:
            # 1) 닉네임 받기
            file_w.write('[SYSTEM] 닉네임을 입력하세요. 예) /nick 홍길동\n')
            file_w.flush()
            nick_line = file_r.readline()
            if not nick_line:
                file_w.close()
                file_r.close()
                client_sock.close()
                return
            nickname = self._parse_first_line_as_nick(nick_line)

            # 등록 및 입장 방송
            self._register_client(client_sock, nickname)
            join_msg = f'[SYSTEM] {nickname}님이 입장하셨습니다.'
            print(f'[JOIN] {nickname} from {addr[0]}:{addr[1]}')
            self._broadcast(join_msg)

            # 사용법 안내
            file_w.write('[SYSTEM] 채팅에 참여하셨습니다. 종료: /종료\n')
            file_w.write('[SYSTEM] 귓속말: /w 대상닉 메시지\n')
            file_w.flush()

            # 2) 메시지 루프
            for line in file_r:
                text = line.rstrip('\n').rstrip('\r')
                if not text:
                    continue

                if text.strip() == '/종료':
                    break

                if text.startswith('/w '):
                    # 포맷: /w 닉 메시지
                    parts = text.split(' ', 2)
                    if len(parts) < 3:
                        file_w.write('[SYSTEM] 사용법: /w 대상닉 메시지\n')
                        file_w.flush()
                        continue
                    _, target, msg = parts
                    if not target or not msg:
                        file_w.write('[SYSTEM] 사용법: /w 대상닉 메시지\n')
                        file_w.flush()
                        continue
                    sent = self._send_to_user(target, f'(귓속말) {nickname}> {msg}')
                    if sent:
                        file_w.write(f'(귓속말 발신) {nickname} -> {target}> {msg}\n')
                    else:
                        file_w.write(f'[SYSTEM] 대상 사용자를 찾을 수 없습니다: {target}\n')
                    file_w.flush()
                    continue

                # 일반 방송
                self._broadcast(f'{nickname}> {text}')

        except Exception as exc:
            print(f'[ERROR] client handler: {exc}')
        finally:
            file_w.close()
            file_r.close()
            leaver = self._remove_client(client_sock)
            if leaver:
                self._broadcast(f'[SYSTEM] {leaver}님이 퇴장하셨습니다.')
                print(f'[LEAVE] {leaver} disconnected')


def main() -> None:
    host = '0.0.0.0'
    port = 5000
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print('[SYSTEM] 포트는 정수여야 합니다.')
            sys.exit(1)

    server = ChatServer(host=host, port=port)
    server.start()


if __name__ == '__main__':
    main()
