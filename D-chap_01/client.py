import socket
import threading
import sys


def recv_loop(sock: socket.socket) -> None:
    """서버로부터 수신하여 표준출력에 뿌린다."""
    try:
        file_r = sock.makefile('r', encoding='utf-8', newline='\n')
        for line in file_r:
            text = line.rstrip('\n').rstrip('\r')
            if text:
                print(text)
    except Exception:
        pass
    finally:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        sock.close()


def send_loop(sock: socket.socket, nickname: str) -> None:
    """표준입력에서 읽어 서버로 전송한다."""
    file_w = sock.makefile('w', encoding='utf-8', newline='\n')
    try:
        # 접속 즉시 닉네임 전송
        file_w.write(f'/nick {nickname}\n')
        file_w.flush()

        for line in sys.stdin:
            text = line.rstrip('\n').rstrip('\r')
            if not text:
                continue
            file_w.write(f'{text}\n')
            file_w.flush()
            if text.strip() == '/종료':
                break
    except Exception:
        pass
    finally:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        sock.close()


def main() -> None:
    if len(sys.argv) < 4:
        print('사용법: client.py <host> <port> <nickname>')
        print('예시:   client.py 127.0.0.1 5000 홍길동')
        sys.exit(1)

    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print('[SYSTEM] 포트는 정수여야 합니다.')
        sys.exit(1)
    nickname = sys.argv[3]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    t_recv = threading.Thread(target=recv_loop, args=(sock,), daemon=True)
    t_recv.start()

    try:
        send_loop(sock, nickname)
    except KeyboardInterrupt:
        try:
            sock.sendall('/종료\n'.encode('utf-8', errors='ignore'))
        except OSError:
            pass

    # 수신 스레드 종료 대기
    t_recv.join(timeout=1.0)


if __name__ == '__main__':
    main()
