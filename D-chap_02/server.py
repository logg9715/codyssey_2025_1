from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import os


class SpacePirateHandler(BaseHTTPRequestHandler):
    """HTTP 요청을 처리하는 핸들러 클래스"""

    def do_GET(self):
        """GET 요청 처리 메서드"""
        if self.path == '/':
            self.send_response(200)  # 200 OK 헤더
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # index.html 파일 읽기
            file_path = os.path.join(os.path.dirname(__file__), 'index.html')   # html
            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())

            # 접속 시간 및 IP 주소 출력
            client_ip = self.client_address[0]
            access_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'접속 시간: {access_time}, 클라이언트 IP: {client_ip}')
        else:
            self.send_error(404, 'File Not Found')


def run_server():
    """8085 포트에서 HTTP 서버를 실행"""
    port = 8085
    server_address = ('', port)
    httpd = HTTPServer(server_address, SpacePirateHandler)
    print(f'HTTP 서버가 {port} 포트에서 시작되었습니다.')
    print('브라우저에서 http://localhost:8085 로 접속하세요.')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
