import zipfile
import time
import string
import os
import multiprocessing
import threading
from io import BytesIO

zip_filename = 'chap_08/emergency_storage_key.zip'
output_password_file = 'password.txt'
charset = string.digits + string.ascii_lowercase
base = len(charset)
threads_per_process = 10  # 최적 병렬 설정

def index_to_password(index):
    password = ''
    for _ in range(6):
        password = charset[index % base] + password
        index //= base
    return password

def worker(sub_start, sub_end, zip_data, counter, found_flag):
    try:
        zip_bytes = BytesIO(zip_data)
        zf = zipfile.ZipFile(zip_bytes)
        target_file = zf.namelist()[0] if zf.namelist() else None
        for i in range(sub_start, sub_end):
            if found_flag.value or not target_file:
                zf.close()
                return
            pwd = index_to_password(i)
            try:
                zf.setpassword(pwd.encode())
                zf.read(target_file)
                found_flag.value = True
                with open(output_password_file, 'w') as f:
                    f.write(pwd)
                zf.close()
                return
            except:
                counter.value += 1
        zf.close()
    except zipfile.BadZipFile:
        pass

def try_password_range(start, end, zip_data, counter, found_flag):
    total_range = end - start
    step = total_range // threads_per_process
    threads = []

    for t in range(threads_per_process):
        sub_start = start + t * step
        sub_end = end if t == threads_per_process - 1 else start + (t + 1) * step
        thread = threading.Thread(target=worker, args=(sub_start, sub_end, zip_data, counter, found_flag))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

def progress_monitor(counter, total, start_time, found_flag):
    while not found_flag.value:
        time.sleep(1)
        attempted = counter.value
        elapsed = time.time() - start_time
        print('경과 시간: {:.2f}초, 시도한 비밀번호 수: {:,} / {:,}'.format(elapsed, attempted, total))

def unlock_zip():
    if not os.path.exists(zip_filename):
        print('에러: zip 파일이 존재하지 않음')
        return

    try:
        with open(zip_filename, 'rb') as f:
            zip_data = f.read()

        total = base ** 6
        process_count = multiprocessing.cpu_count() * 2  # 최적 병렬 설정
        step = total // process_count
        start_time = time.time()

        counter = multiprocessing.Value('i', 0)
        found_flag = multiprocessing.Value('b', False)

        monitor = multiprocessing.Process(target=progress_monitor, args=(counter, total, start_time, found_flag))
        monitor.start()

        args_list = []
        for i in range(process_count):
            start = i * step
            end = total if i == process_count - 1 else (i + 1) * step
            args_list.append((start, end, zip_data, counter, found_flag))

        processes = []
        for args in args_list:
            p = multiprocessing.Process(target=try_password_range, args=args)
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        monitor.join()

        if not found_flag.value:
            print('비밀번호 찾지 못함')
    except zipfile.BadZipFile:
        print('에러: 유효하지 않은 ZIP 파일입니다.')

if __name__ == '__main__':
    unlock_zip()