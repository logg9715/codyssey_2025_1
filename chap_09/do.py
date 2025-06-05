import os


class PasswordReader:
    def __init__(self, filename='password.txt'):
        # do.py랑 같은 경로 기준으로 파일 경로 구성
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(base_path, filename)

    def read_password(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                password = file.read().strip()
                print(f" password.txt 내용 읽음: {password}")
                return password
        except FileNotFoundError:
            print(f"[오류] 파일이 존재하지 않음: {self.file_path}")
        except Exception as e:
            print(f"[오류] 파일 읽기 실패: {e}")
        return None


def caesar_cipher_decode(target_text):
    """디코딩 시도"""
    results = []
    for shift in range(26):
        decoded = ''
        for char in target_text:
            if 'A' <= char <= 'Z':
                decoded += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            elif 'a' <= char <= 'z':
                decoded += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:
                decoded += char
        results.append((shift, decoded))
    return results

def main():
    # password.txt 읽기
    reader = PasswordReader()
    encrypted_text = reader.read_password()
    if not encrypted_text:
        return

    print('--- 카이사르 암호 해독 시도 ---\n')
    results = caesar_cipher_decode(encrypted_text)

    for shift, decoded in results:
        print(f'{shift:2d}: {decoded}')

    print('\n위에서 의미 있는 문장을 찾고 번호 입력')
    try:
        selected = int(input('시프트 번호 입력: '))
        if 0 <= selected < 26:
            final_text = results[selected][1]
            base_path = os.path.dirname(os.path.abspath(__file__))
            result_path = os.path.join(base_path, 'result.txt')
            with open(result_path, 'w', encoding='utf-8') as result_file:
                result_file.write(final_text)
            print('저장 완료')
        else:
            print('0부터 25 사이 숫자를 입력하시오.')
    except Exception as e:
        print('입력 오류:', e)


if __name__ == '__main__':
    main()
