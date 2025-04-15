import os
import shutil

# 원본 폴더 (다운로드 폴더)
download_folder = r'C:\Users\student\Downloads'

# 이동 대상 폴더들
destination_folders = {
    'images': ['.jpg', '.jpeg'],
    'data': ['.csv', '.xlsx'],
    'docs': ['.txt', '.doc', '.pdf'],
    'archive': ['.zip']
}

# 대상 폴더들이 없으면 생성
for folder in destination_folders:
    path = os.path.join(download_folder, folder)
    if not os.path.exists(path):
        os.makedirs(path)

# 파일 이동
for filename in os.listdir(download_folder):
    file_path = os.path.join(download_folder, filename)

    # 폴더는 무시
    if os.path.isdir(file_path):
        continue

    # 파일 확장자 확인 (소문자로 변환)
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    # 확장자에 따라 해당 폴더로 이동
    for folder, extensions in destination_folders.items():
        if ext in extensions:
            destination_path = os.path.join(download_folder, folder, filename)
            shutil.move(file_path, destination_path)
            print(f"{filename} -> {folder} 폴더로 이동됨")
            break
