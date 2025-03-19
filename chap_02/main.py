# init
ROOTPATH = 'D:\\workspace\\학교\\codyssey_2025_1\\chap_02\\' # 프로젝트 루트 디렉터리

# 파일 읽기 및 리스트 변환
file_path = ROOTPATH + "Mars_Base_Inventory_List.csv"
inventory_list = []

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
        
        # 첫 번째 줄(헤더) 제외하고 데이터 변환
        for line in content[1:]:
            parts = line.strip().split(',')
            
            # 인화성 지수를 숫자로 변환 (예외 처리 포함)
            try:
                flammability = float(parts[-1])
            except ValueError:
                flammability = 0.0
            
            inventory_list.append([parts[0], flammability])
except Exception as e:
    print(f"파일을 읽는 중 오류 발생: {e}")

# 인화성 지수 기준으로 정렬
sorted_inventory = sorted(inventory_list, key=lambda x: x[1], reverse=True)

# 인화성 지수가 0.7 이상인 목록 추출
dangerous_materials = [item for item in sorted_inventory if item[1] >= 0.7]

# 위험 물질 목록을 CSV 파일로 저장
dangerous_file_path = ROOTPATH + "Mars_Base_Inventory_danger.csv"
try:
    with open(dangerous_file_path, 'w', encoding='utf-8') as file:
        file.write("Substance,Flammability\n")
        for item in dangerous_materials:
            file.write(f"{item[0]},{item[1]}\n")
except Exception as e:
    print(f"CSV 저장 중 오류 발생: {e}")


