# ======================= DEFINE ============================
COL = 0 # 데이터 필드
TIMESTAMP = 0 # 레코드[0] = 타임스탬프
ROOTPATH = 'D:\workspace\학교\codyssey_2025_1\chap_01' # 프로젝트 루트 디렉터리

# ======================== HELLO WORLD ====================================
print('Hello World')

# ========================= FILE OUT ===================================

with open( ROOTPATH + '\mission_computer_main.log', 'r', encoding='utf-8') as file:
    lines = file.read().split('\n')

column = lines[COL].split(',')
data = [line.split(',') for line in lines[1:] if line]

time_dict = {}
# >> start for <<
for row in data:
    time = row[TIMESTAMP]
    if time not in time_dict:
        time_dict[time] = []
    time_dict[time].append(row[1:])
# >> end for <<

#out
with open( ROOTPATH + '\log_analysis.md', 'w', encoding='utf-8') as f:
    # >> start for <<
    for time, entries in sorted(time_dict.items()):
        f.write(f'## {time}\n')
        print(f'============== {time} ==============')

        # >> start for <<
        for entry in entries:
            f.write(f'- {', '.join(entry)}\n')
            print(entry)
        # >> end for <<

        print('\n')
        f.write('\n') # escape
    # >> end for <<
    


