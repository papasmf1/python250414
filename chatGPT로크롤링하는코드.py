import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# 네이버 검색 URL
url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%B0%98%EB%8F%84%EC%B2%B4"

# HTTP 요청
response = requests.get(url)
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # 신문기사 제목 크롤링
    titles = []
    for title in soup.select('.news_tit'):  # 네이버 뉴스 제목 클래스
        titles.append(title.get('title'))

    # 결과를 엑셀 파일로 저장
    if titles:
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "News Titles"

        # 헤더 추가
        sheet.append(["번호", "제목"])

        # 데이터 추가
        for idx, title in enumerate(titles, start=1):
            sheet.append([idx, title])

        # 엑셀 파일 저장
        workbook.save("results.xlsx")
        print("크롤링 결과가 results.xlsx 파일에 저장되었습니다.")
    else:
        print("크롤링 결과가 없습니다.")
else:
    print(f"HTTP 요청 실패: {response.status_code}")