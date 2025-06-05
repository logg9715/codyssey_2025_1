import zipfile
import time
from datetime import timedelta


class ZipBruteForcer:
    def __init__(self, zip_path, max_length=6):
        self.DIGITS = '0123456789abcdefghijklmnopqrstuvwxyz'
        self.zip_path = zip_path
        self.max_length = max_length
        self.max_tries = len(self.DIGITS) ** self.max_length
        self.start_time = None
        self.attempts = 0

    def increment_id(self, s):
        base = len(self.DIGITS)
        s_list = list(s)
        i = len(s_list) - 1

        while i >= 0:
            idx = self.DIGITS.index(s_list[i])
            if idx + 1 < base:
                s_list[i] = self.DIGITS[idx + 1]
                break
            else:
                s_list[i] = self.DIGITS[0]
                i -= 1
        else:
            s_list = [self.DIGITS[0]] + s_list

        return ''.join(s_list)

    def try_password(self, password):
        try:
            with zipfile.ZipFile(self.zip_path) as zf:
                zf.extractall(pwd=password.encode())
                print(f"[✓] 비밀번호 찾음: {password}")
                return True
        except:
            return False

    def print_status(self):
        elapsed = time.time() - self.start_time
        print("\n[완료]")
        print(f"총 시도 횟수: {self.attempts}")
        print(f"총 소요 시간: {timedelta(seconds=int(elapsed))}")

    def unlock_zip(self):
        pw = '000000'
        self.start_time = time.time()

        while len(pw) <= self.max_length:
            self.attempts += 1

            if self.try_password(pw):
                self.print_status()
                return

            if self.attempts % 100000 == 0:
                elapsed = time.time() - self.start_time
                print(
                    f"[진행 중] 시도: {self.attempts} | 비밀번호: {pw} | 경과: {timedelta(seconds=int(elapsed))}"
                )

            pw = self.increment_id(pw)

        print("비밀번호를 찾지 못했습니다.")


if __name__ == "__main__":
    brute_forcer = ZipBruteForcer(zip_path='emergency_storage_key.zip')
    brute_forcer.unlock_zip()
