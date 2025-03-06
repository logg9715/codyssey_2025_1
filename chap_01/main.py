# ======================= DEFINE ============================
COL = 0

TIMESTAMP = 0
EVENT = 1
MESSAGE = 2

# ======================== HELLO WORLD ====================================
print('Hello World')

# ========================= FILE OUT ===================================

with open('mission_computer_main.log', 'r', encoding='utf-8') as file:
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
with open('log_analysis.md', 'w', encoding='utf-8') as f:
    # >> start for <<
    for time, entries in sorted(time_dict.items()):
        f.write(f'## {time}\n')
     
        # >> start for <<
        for entry in entries:
            f.write(f'- {', '.join(entry)}\n')
        # >> end for <<
        
        f.write('\n') # escape
    # >> end for <<
    


