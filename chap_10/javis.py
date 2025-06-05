import os
import wave
import pyaudio
import datetime

def create_records_folder():    # 'records' 폴더 없음 생성
    if not os.path.exists('records'):
        os.mkdir('records')

def generate_filename(): # 현재 시간을 기반으로 파일 이름 생성
    now = datetime.datetime.now()
    filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
    return os.path.join('records', filename)

def record_audio(seconds):
    # PyAudio 초기화
    audio = pyaudio.PyAudio()

    # 오디오 스트림 설정
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=50100,
                        input=True,
                        frames_per_buffer=1024)

    print('녹음 시작...')
    frames = []

    # 오디오 녹음
    for _ in range(0, int(50100 / 1024 * seconds)):
        data = stream.read(1024)
        frames.append(data)

    print('녹음 종료.')

    # 스트림 정리(멈추고 닫고 끝내기)
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 파일 저장이요
    create_records_folder()
    filename = generate_filename()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(50100)
        wf.writeframes(b''.join(frames))

    print('파일 저장:', filename)

if __name__ == '__main__':
    record_audio(7)  # n초
