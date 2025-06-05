# javis.py

import os
import wave
import pyaudio
import datetime
import csv
import speech_recognition as sr

def create_records_folder():
    if not os.path.exists('records'):
        os.mkdir('records')

def generate_filename():
    now = datetime.datetime.now()
    filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
    return os.path.join('records', filename)

def record_audio(seconds):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)

    print('녹음 시작...')
    frames = []

    for _ in range(0, int(44100 / 1024 * seconds)):
        data = stream.read(1024)
        frames.append(data)

    print('녹음 종료.')

    stream.stop_stream()
    stream.close()
    audio.terminate()

    create_records_folder()
    filename = generate_filename()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))

    print('파일 저장:', filename)

def list_audio_files():
    # records 폴더 내 .wav 파일 목록 반환
    return [f for f in os.listdir('records') if f.endswith('.wav')]

def convert_speech_to_text(filename):
    recognizer = sr.Recognizer()
    filepath = os.path.join('records', filename)

    with sr.AudioFile(filepath) as source:
        print('음성 파일 불러오는 중:', filename)
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language='ko-KR')
        print('인식된 텍스트:', text)
        return [(0.0, text)]  # 시간정보가 없으므로 0초 기준으로 기록
    except sr.UnknownValueError:
        print('음성을 인식할 수 없습니다:', filename)
        return []
    except sr.RequestError:
        print('STT 서비스에 연결할 수 없습니다.')
        return []

def save_text_as_csv(filename, text_data):
    base_name = os.path.splitext(filename)[0]
    csv_filename = base_name + '.csv'
    csv_path = os.path.join('records', csv_filename)

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['시간(초)', '인식된 텍스트'])
        for timestamp, text in text_data:
            writer.writerow([timestamp, text])

    print('CSV 저장 완료:', csv_path)

def process_all_audio_files():
    create_records_folder()
    audio_files = list_audio_files()

    for audio_file in audio_files:
        text_data = convert_speech_to_text(audio_file)
        if text_data:
            save_text_as_csv(audio_file, text_data)

if __name__ == '__main__':
    # 예시: 5초간 녹음 후 STT 실행
    record_audio(10)
    process_all_audio_files()
