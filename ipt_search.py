# 파일을 C:\Domain\ipt에 다운로드 받습니다.
import requests
import os
def download_csv(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print("\n최신 전화번호 csv 파일을 다운로드 중 입니다.")
        print("\n다운로드 완료!!")
    else:
        print("\n파일을 다운로드할 수 없습니다.\n")

url = "http://<주소입력>/ipt/DBTable/user_profile.csv"
save_path = "c:/domain/ipt/user_profile.csv"

download_csv(url, save_path)

import pandas as pd

def search_phone_number(csv_path, search_value):
    df = pd.read_csv(csv_path, encoding='ANSI')
    columns_to_exclude = ['v_port', 'MAC addr', 'mode', 'attached UC phone', 'Detail Type']
    search_result = df[df['Phone Number'].astype(str).str.contains(str(search_value))].drop(columns=columns_to_exclude)
    return search_result


def search_ip(csv_path, search_value):
    df = pd.read_csv(csv_path, encoding='ANSI')
    columns_to_exclude = ['v_port', 'MAC addr', 'mode', 'attached UC phone', 'Detail Type']
    search_result = df[df['IP address'].astype(str).str.contains(str(search_value))].drop(columns=columns_to_exclude)
    return search_result


def search_directory(csv_path, search_value):
    df = pd.read_csv(csv_path, encoding='ANSI')
    columns_to_exclude = ['v_port', 'MAC addr', 'mode', 'attached UC phone', 'Detail Type']
    search_result = df[df['Directory'].astype(str).str.contains(str(search_value))]
    search_result = search_result.drop(columns=columns_to_exclude)
    return search_result

csv_path = "c:/domain/ipt/user_profile.csv"
df = pd.read_csv(csv_path, encoding='ANSI')

# # 화면 지우고 프로그램 시작하기
# os.system('cls' if os.name == 'nt' else 'clear')

while True:
    
# 프로그램에 대한 정보
    os.system('cls' if os.name == 'nt' else 'clear')
    print('''
=========================================================

전화번호 / IP / 사용자 검색 프로그램 입니다.

1. 전화번호 검색

2. IP검색

3. 디렉토리 (사용자) 검색

9. 종료

=========================================================
''')
    
    option = input("\n검색 옵션을 선택하세요. : ")
    
    if option == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        search_value = input("\n전화번호 : ")
        result = search_phone_number(csv_path, search_value)
        if len(result) > 0:
            print("검색 결과:")
            print(result.to_string(index=False))  # 모든 행 데이터를 출력하기 위해 index를 제외하고 출력합니다.
        else:
            print("\n검색 결과가 없습니다.\n")
        
        input("\n계속하려면 엔터 키를 눌러주세요.\n")

    elif option == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        search_value = input("\nIP Address : ")
        result = search_ip(csv_path, search_value)
        if len(result) > 0:
            print("검색 결과:")
            print(result.to_string(index=False))  # 모든 행 데이터를 출력하기 위해 index를 제외하고 출력합니다.
        else:
            print("\n검색 결과가 없습니다.\n")
        
        input("\n계속하려면 엔터 키를 눌러주세요.\n")

    elif option == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        search_value = input("\n디렉토리 : ")
        result = search_directory(csv_path, search_value)
        if len(result) > 0:
            print("검색 결과:")
            print(result.to_string(index=False))  # 모든 행 데이터를 출력하기 위해 index를 제외하고 출력합니다.
        else:
            print("\n검색 결과가 없습니다.\n")
        
        input("\n계속하려면 엔터 키를 눌러주세요.\n")

    elif option == "9":
        print("\n프로그램을 종료합니다.\n")
        break
    
    else:
        print("\n올바른 옵션을 선택해주세요.\n")
