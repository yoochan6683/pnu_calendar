from selenium import webdriver # webdriver를 이용해 해당 브라우저를 열기 위해
from selenium.webdriver import ActionChains # 일련의 작업들을(ex.아이디 입력, 비밀번호 입력, 로그인 버튼 클릭...) 연속적으로 실행할 수 있게 하기 위해
from selenium.webdriver.common.keys import Keys # 키보드 입력을 할 수 있게 하기 위해
from selenium.webdriver.common.by import By # html요소 탐색을 할 수 있게 하기 위해
from selenium.webdriver.support.ui import WebDriverWait # 브라우저의 응답을 기다릴 수 있게 하기 위해
from selenium.webdriver.support import expected_conditions as EC # html요소의 상태를 체크할 수 있게 하기 위해
from selenium.webdriver.chrome.options import Options
from time import sleep
from dotenv import dotenv_values
import os
import getpass

secrets = dotenv_values("secret.env")

ID = secrets["ID"]
PW = secrets["PW"]

data = []

chrome_options = Options()
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
print (driver.title)
pnuUrl = 'https://onestop.pusan.ac.kr/login.do?status=logout'
driver.get(pnuUrl)

schedules = driver.find_elements(By.CSS_SELECTOR, ".schedule-list li")
for i in schedules: 
    data.append(i.text)

# icloud calender 접속
appleCalenderUrl = 'https://www.icloud.com/calendar/'
driver.get(appleCalenderUrl)

# 로그인 버튼 클릭
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".push.primary.sign-in-button.icloud-mouse")))
loginButton = driver.find_element(By.CSS_SELECTOR, ".push.primary.sign-in-button.icloud-mouse")
loginButton.click()

#document 로그인 폼으로 변경
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"aid-auth-widget-iFrame")))
aid_auth_widget_iFrame = driver.find_element(By.ID, "aid-auth-widget-iFrame")
driver.switch_to.frame(aid_auth_widget_iFrame)

#이메일 입력 후 화살표 버튼 클릭
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "account_name_text_field")))
driver.find_element(By.ID, "account_name_text_field").send_keys(ID)
driver.find_element(By.CSS_SELECTOR, ".shared-icon.icon_sign_in").click()

#암호로 입력하기 버튼 클릭 
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "continue-password")))
driver.find_element(By.ID, "continue-password").click()

#패스워드 입력 후 화살표 버튼 클릭
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password_text_field")))
driver.find_element(By.ID, "password_text_field").send_keys(PW)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".shared-icon.icon_sign_in")))
driver.find_element(By.CSS_SELECTOR, ".shared-icon.icon_sign_in").click()

#이중보안 비밀번호
double_key_pass = getpass.getpass('이중보안 비밀번호를 입력해주세요(6자리) : ')

#이중보안 비밀번호 화면에 입력
# for i in range(1, 7):
#     driver.find_element(By.XPATH, "//*[@id=\"stepEl\"]/div/hsa2-sk7/div/div[2]/div[1]/div/div/input[{i}]").send_keys(double_key_pass[i-1])
driver.find_element(By.XPATH, "//*[@id=\"stepEl\"]/div/hsa2-sk7/div/div[2]/div[1]/div/div/input[1]").send_keys(double_key_pass[0])
driver.find_element(By.XPATH, "//*[@id=\"stepEl\"]/div/hsa2-sk7/div/div[2]/div[1]/div/div/input[2]").send_keys(double_key_pass[1])
driver.find_element(By.XPATH, "//*[@id=\"stepEl\"]/div/hsa2-sk7/div/div[2]/div[1]/div/div/input[3]").send_keys(double_key_pass[2])
driver.find_element(By.XPATH, "//*[@id=\"stepEl\"]/div/hsa2-sk7/div/div[2]/div[1]/div/div/input[4]").send_keys(double_key_pass[3])
driver.find_element(By.XPATH, "//*[@id=\"stepEl\"]/div/hsa2-sk7/div/div[2]/div[1]/div/div/input[5]").send_keys(double_key_pass[4])
driver.find_element(By.XPATH, "//*[@id=\"stepEl\"]/div/hsa2-sk7/div/div[2]/div[1]/div/div/input[6]").send_keys(double_key_pass[5])

#이 브라우저를 신뢰함 버튼 클릭
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.button-rounded-rectangle")))
driver.find_element(By.CSS_SELECTOR, ".button.button-rounded-rectangle").click()

#애플 로그인 iframe -> 디폴트 드라이버로 전환
driver.switch_to.parent_frame()

# #디폴트 드라이버 -> 캘린더 iframe으로 전환
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".child-application.fade-in")))
calender_iFrame = driver.find_element(By.CSS_SELECTOR, ".child-application.fade-in")
driver.switch_to.frame(calender_iFrame)

#새로운 캘린더 추가
driver.find_element(By.CSS_SELECTOR, ".push.css-1ro814.icloud-mouse").click()
action = ActionChains(driver)
action.send_keys("부산대 학과일정 캘린더", Keys.ENTER)
action.perform()

#새로운 캘린더 선택
driver.find_elements(By.CSS_SELECTOR, ".css-64xuo2")[-1].click()

#학과일정 데이터 삽입
for i in data:
    duration, event = i.split('\n')
    startDuration, __, wave, endDuration, __ = duration.split()

    startYear, startMonth, startDate = startDuration.split('-')
    endYear, endMonth, endDate = endDuration.split('-')

    # 이벤트 추가 + 버튼 클릭
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".push.primary.css-1onyv69.create-event-button.icloud-mouse")))
    driver.find_element(By.CSS_SELECTOR, ".push.primary.css-1onyv69.create-event-button.icloud-mouse").click()

    #새로운 이벤트 input 입력

    new_event = driver.find_element(By.CSS_SELECTOR, ".standard.css-10gkp18.icloud-tint.icloud-mouse.contains-text")
    new_event.send_keys(Keys.COMMAND, "a")
    new_event.send_keys(Keys.BACKSPACE)
    new_event.send_keys(event)

    #시작, 종료 input 입력
    startMonthPicker, startDatePicker, startYearPicker, endMonthPicker, endDatePicker, endYearPicker = driver.find_elements(By.CSS_SELECTOR, "div[role = \"spinbutton\"]")
    startMonthPicker.send_keys(startMonth)
    startDatePicker.send_keys(startDate)
    startYearPicker.send_keys(startYear)
    endMonthPicker.send_keys(endMonth)
    endDatePicker.send_keys(endDate)
    endYearPicker.send_keys(endYear)

    #추가 버튼 클릭
    driver.find_element(By.CSS_SELECTOR, ".primary.css-ffuchb.block.icloud-mouse").click()


