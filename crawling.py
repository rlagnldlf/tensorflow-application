from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from openpyxl import Workbook
import pandas as pd
from bs4 import BeautifulSoup
import os

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://www.youtube.com/watch?v=tImOwFD9aCg"
driver.get(url)
driver.implicitly_wait(3)

time.sleep(1.5)

driver.execute_script("window.scrollTo(0, 800)")
time.sleep(3)

last_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1.5)

    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(1.5)

# "답글 보기" 버튼 클릭
try:
    driver.find_element(By.CSS_SELECTOR, "#dismiss-button > a").click()
except:
    pass

buttons = driver.find_elements(By.CSS_SELECTOR, "#more-replies > a")

for button in buttons:
    driver.execute_script("arguments[0].click();", button)
    time.sleep(1.5)

# BeautifulSoup을 사용해 댓글 추출
html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')

id_list = soup.select("ytd-comment-thread-renderer #author-text > span")
comment_list = soup.select("ytd-comment-thread-renderer #content-text")

channel_id_list = '채널 이름'
update_data_list = '로아온 날짜'
update_name_list = '로아온 이름'
video_date_list = '비디오 업로드 날짜'

id_final = []
comment_final = []

channel_id = []
update_date = []
update_name = []
video_date = []

# 댓글 내용과 ID 추출
for i in range(len(comment_list)):
    temp_id = id_list[i].text.strip()  # 불필요한 공백 제거
    id_final.append(temp_id)  # 댓글 작성자

    temp_comment = comment_list[i].text.strip()  # 불필요한 공백 제거
    comment_final.append(temp_comment)  # 댓글 내용

    channel_id.append(channel_id_list)
    update_date.append(update_data_list)
    update_name.append(update_name_list)
    video_date.append(video_date_list)


# Pandas DataFrame으로 변환 후 엑셀로 저장
pd_data = {"아이디": id_final, "댓글 내용": comment_final, '채널 이름': channel_id, '업데이트 날짜' : update_date, '업데이트 이름' : update_name, '동영상 업로드 날짜' : video_date}
youtube_pd = pd.DataFrame(pd_data)
file_path = 'result.xlsx'

# 기존 파일이 있을 경우 데이터를 읽어온다
if os.path.exists(file_path):
    existing_df = pd.read_excel(file_path)
    # 기존 데이터와 새 데이터를 합친다
    youtube_pd = pd.concat([existing_df, youtube_pd], ignore_index=True)

with pd.ExcelWriter(file_path, mode='w', engine='openpyxl') as writer: # 데이터를 엑셀 파일에 저장 (기존 파일에 추가하는 방식)
    youtube_pd.to_excel(writer, index=False)
# youtube_pd.to_excel('result.xlsx', index=False)  # 엑셀 파일 저장 , 초기 엑셀파일 생성시 사용
