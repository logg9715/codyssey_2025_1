# crawling_KBS.py
#
# 이 스크립트는 KBS 뉴스 웹사이트의 메인 뉴스 페이지에서
# 주요 헤드라인 뉴스를 크롤링하여 화면에 출력하는 예제다.
# 외부 패키지는 사용하지 않고, Python 내장 모듈인 html.parser와
# requests만 활용한다.
#
# 개발환경: Python 3.x
# 스타일: PEP 8 규칙 준수
#


import requests
from html.parser import HTMLParser


class HeadlineParser(HTMLParser):
    """
    HTMLParser를 상속받아 KBS 뉴스 페이지의
    <p class="title"> 태그 안에 들어있는 텍스트를 추출하는 파서 클래스.
    """

    def __init__(self):
        super().__init__()
        self.in_title = False      # 현재 <p class="title"> 안에 있는지 여부
        self.headlines = []        # 최종적으로 수집된 헤드라인 텍스트 리스트
        self.current_data = ''     # 하나의 제목을 임시로 저장하는 버퍼

    def handle_starttag(self, tag, attrs):
        """
        HTML 시작 태그(<p ...>)를 만났을 때 호출된다.
        <p class="title"> 태그를 발견하면 in_title 플래그를 True로 설정한다.
        """
        if tag == 'p':
            for attr in attrs:
                if attr[0] == 'class' and 'title' in attr[1]:
                    self.in_title = True

    def handle_data(self, data):
        """
        태그 안의 텍스트 데이터를 만났을 때 호출된다.
        in_title이 True 상태라면, 즉 <p class="title"> 안쪽이면
        해당 텍스트를 current_data에 누적 저장한다.
        """
        if self.in_title:
            self.current_data += data.strip()

    def handle_endtag(self, tag):
        """
        HTML 종료 태그(</p>)를 만났을 때 호출된다.
        in_title이 True 상태라면 지금까지 모은 current_data를
        headlines 리스트에 추가하고 초기화한다.
        """
        if tag == 'p' and self.in_title:
            if self.current_data:
                # 불필요한 줄바꿈, 탭, 공백 제거
                clean_text = self.current_data.replace('\n', '').replace('\r', '').replace('\t', '').replace('  ', ' ')
                self.headlines.append(clean_text)

            # 상태 초기화
            self.current_data = ''
            self.in_title = False


def fetch_headlines(url):
    """
    지정된 URL에서 HTML을 요청하고, HeadlineParser를 이용해
    주요 헤드라인 텍스트를 추출하여 리스트로 반환한다.
    """
    response = requests.get(url)
    response.encoding = 'utf-8'   # 한글 깨짐 방지를 위해 UTF-8 인코딩 지정

    parser = HeadlineParser()
    parser.feed(response.text)    # HTML 내용을 파서에 전달
    return parser.headlines


def main():
    """
    프로그램의 시작점.
    KBS 뉴스 메인 페이지 URL을 호출하여
    헤드라인을 가져온 후 화면에 출력한다.
    """
    url = 'http://news.kbs.co.kr/news/pc/main/main.html'
    headlines = fetch_headlines(url)

    print('KBS 주요 헤드라인 뉴스:')
    for idx, headline in enumerate(headlines, start=1):
        print(f'{idx}. {headline}')


if __name__ == '__main__':
    main()
