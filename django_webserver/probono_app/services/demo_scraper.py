import os
from datetime import datetime
from pytz import timezone

# DemoScraper modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import olefile
import re
import zlib
import struct

from probono_app.models import Demo


class DemoInfo():
    
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        # self.__download_path = '/Users/limhs/Downloads/'
        self.__download_path  = '/Users/choijeongheum/Downloads/'
        self.__site_url       = "https://www.smpa.go.kr/user/nd54882.do"

    def _crawling_demo(self):
        print('Initializing demo crawling.. ', end='')
        self.__get_date_info()
        if self.__check_file():
            print('OK')
            return
        self.__start_driver()
        self.__navigate_to_site()
        self.__click_on_today_demo()
        self.__download_hwp()
        self.__update_demo()
        self.__close_driver()
        print('OK')
        return

    def __check_file(self):  # 파일명에서 한글 없애기(파일경로 수정 요망)
        new_filename = self.date + 'data.hwp'
        new_file_path = self.__download_path+new_filename
        # print(new_file_path)
        return os.path.exists(new_file_path)

    def __start_driver(self):
        # self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def __navigate_to_site(self):
        self.driver.get(self.__site_url)

    def __get_date_info(self):
        current_date = datetime.now(timezone('Asia/Seoul'))
        year = current_date.strftime("%y")
        today = current_date.weekday()
        days = ["월", "화", "수", "목", "금", "토", "일"]
        day = days[today]
        self.date = year + current_date.strftime("%m%d")
        self.day = day

    def __click_on_today_demo(self):
        link_text = "오늘의 집회"
        blank = " "
        xpath_expression = f"//a[contains(text(),'{link_text}{blank}{self.date}{blank}{self.day}')]"
        element = self.driver.find_element(By.XPATH, xpath_expression)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()

    def __download_hwp(self):
        file_name_text = "인터넷집회"
        target_filename = self.date + \
            "(" + self.day + ")" + " " + file_name_text + ".hwp"
        xpath_expression = f"//a[contains(text(), '{target_filename}')]"
        links = self.driver.find_elements(By.XPATH, f"//a[@class='doc_link']")
        download_link = None
        for link in links:
            if target_filename in link.text:
                download_link = link
                break
        if download_link:
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", download_link)
            download_link.click()
            self.wait.until(
                lambda driver: target_filename in os.listdir(self.__download_path))

    def __process_hwp_file(self):

        # 파일명에서 한글 없애기(파일경로 수정 요망)
        file_path = self.__download_path + self.date + \
            "(" + self.day + ")" + " " + "인터넷집회.hwp"
        new_filename = self.date + 'data.hwp'
        new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
        os.rename(file_path, new_file_path)

        # HWP 파일 처리
        with olefile.OleFileIO(new_file_path) as f:
            dirs = f.listdir()

            # HWP 파일 검증
            if ["FileHeader"] not in dirs or \
                    ["\x05HwpSummaryInformation"] not in dirs:
                raise Exception("Not Valid HWP.")

            # 문서 포맷 압축 여부 확인
            header = f.openstream("FileHeader")
            header_data = header.read()
            is_compressed = (header_data[36] & 1) == 1

            # Body Sections 불러오기
            nums = []
            for d in dirs:
                if d[0] == "BodyText":
                    nums.append(int(d[1][len("Section"):]))
            sections = ["BodyText/Section"+str(x) for x in sorted(nums)]

            # 전체 text 추출
            text = ""
            for section in sections:

                bodytext = f.openstream(section)
                data = bodytext.read()
                if is_compressed:
                    unpacked_data = zlib.decompress(data, -15)
                else:
                    unpacked_data = data

                # 각 Section 내 text 추출
                section_text = ""
                i = 0
                size = len(unpacked_data)
                while i < size:
                    header = struct.unpack_from("<I", unpacked_data, i)[0]
                    rec_type = header & 0x3ff
                    rec_len = (header >> 20) & 0xfff

                    if rec_type in [67]:
                        rec_data = unpacked_data[i+4:i+4+rec_len]
                        section_text += rec_data.decode('utf-16')
                        section_text += "\n"

                    i += 4 + rec_len

                text += section_text
                text += "\n"

            to_insert = []
            date = re.search(r'\d{4}\. \d{2}\. \d{2}', text)
            cnt = len(re.findall(r'(\d{2}:\d{2})[∼~](\d{2}:\d{2})', text))
            text = text.replace('\r', '').replace('\n', '')
            for i in range(cnt+1):
                match = re.search(r'(\d{2}:\d{2})[∼~](\d{2}:\d{2})', text)
                if match:
                    time = text[match.start():match.end()]
                    text = text[match.end():]
                    # print(time)

                i = 0
                while (1):
                    if text[i].isalnum() and not 0x4E00 <= ord(text[i]) <= 0x9FFF:
                        break
                    i += 1

                match = re.search(r'<[^>]+>', text)
                if match:
                    place = text[i:match.end()]
                    text = text[match.end():]
                    # print(place)

                match = re.search(r'\d{1,3}(,\d{3})*', text)
                if match:
                    amount = text[match.start():match.end()]
                    text = text[match.end():]
                    # print(amount)

                result = {
                    'location': place,
                    'date': date,
                    'time': time,
                    'amount': amount
                }
                to_insert.append(result)
                i += 1

        return to_insert

    def __update_demo(self):
        # 모든 Demo 객체를 삭제
        Demo.objects.all().delete()

        new_data = []
        new_data.extend(self.__process_hwp_file())
        for idx, target in enumerate(new_data):
            formatted_date = datetime.strptime(target['date'].group(), "%Y. %m. %d").date()
            new_data[idx]['date'] = formatted_date
        
        # 새로운 데이터를 Demo 모델에 추가
        demo_instances = [Demo(**item) for item in new_data]
        Demo.objects.bulk_create(demo_instances)

    def __close_driver(self):
        self.driver.quit()