from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import os

class MangazScraper:

    def __init__(self, url = "https://www.mangaz.com/book/detail/157901", save_dir = "project_mangaz", wait_time = 10):
        self.url = url
        self.save_dir = self._create_dir(save_dir)
        self.wait_time = wait_time
        self.options = self._create_options()
        self.driver = None
        self.wait_element = None

    @staticmethod
    def _create_options():
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        return options
    
    @staticmethod
    def _create_dir(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        return folder_path

    def open_browser(self):
        self.driver = webdriver.Chrome(options=self.options)
        self.wait_element = WebDriverWait(self.driver, self.wait_time)
        self.driver.get(self.url)
        self.wait_element.until(lambda d: len(d.title) > 0)
        print("網頁標題: ", self.driver.title)

    def open_reader(self):
        # Read FREE 按鈕
        button = self.wait_element.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.open-viewer.book-begin.ga')))
        button.click()

        # 切換到新視窗
        all_windows = self.driver.window_handles
        self.driver.switch_to.window(all_windows[-1])

        # すぐに読む 按鈕
        read_now = self.wait_element.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'すぐに読む')))
        read_now.click()

    def start_scrape(self):
        total_image_count = 0

        while True:
            # 搜刮頁面上有顯示的漫畫照片
            image_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.page_image img.image")
            for img_element in image_elements:
                if img_element.is_displayed():
                    file_path = f"manga_page_{total_image_count}.png"

                    img_element.screenshot(os.path.join(self.save_dir, file_path))
                    print(f"成功擷取頁面並儲存為: {file_path}")

                    total_image_count += 1

            # 點擊下一頁
            try:
                next_page = self.wait_element.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.flip.flip-left')))
                next_page.click()
                print("已點擊下一頁，等待畫面載入...")
                sleep(2)
            except TimeoutException:
                print("【系統提示】找不到下一頁按鈕，已達最後一頁，結束爬取迴圈。")
                break

    def close_browser(self):
        if self.driver:
            self.driver.quit()

    def run(self):
        try:
            self.open_browser()
            self.open_reader()
            self.start_scrape()
        finally:
            self.close_browser()