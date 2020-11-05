import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import urllib.request, urllib


class Crawling(object):

    def __init__(self, searchData):
        # 검색 데이터
        self.searchData = searchData

        self.option = webdriver.FirefoxOptions()
        self.option.add_argument('--no-sandbox')
        self.option.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Firefox(options=self.option)

        self.setupGoogle()

        # delay
        time.sleep(1)

        self.imageCrawling()

    def setupGoogle(self):
        ## Setup Login URL
        url = 'https://www.google.com/'
        self.browser.get(url)

        searchBox = self.browser.find_element_by_xpath("//input[@class='gLFyf gsfi']")
        searchBox.send_keys(self.searchData)  # 대장암 내시경 이미지 검색
        searchBox.submit()

        self.browser.implicitly_wait(1)

    def fetch_detail_url(self):
        image_urls = set()
        sleep_between_interactions = 0.1
        results_start = 0

        thumbnail_results = self.browser.find_elements_by_class_name("rg_i")
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]:
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception as e:
                print("[WARNING] THUMBNAIL_RESULTS : " + e)
                continue

            actual_images = self.browser.find_elements_by_class_name("n3VNCb")
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))
                    print(actual_image.get_attribute('src'))

        # 이미지 개수 출력
        print(len(image_urls))

        for idx, p in enumerate(image_urls):
            try:
                urllib.request.urlretrieve(p, "C:\\Users\\ChoiJuwon\\Desktop\\Mycampus\\image\\" + str(idx) + ".jpg")
            except Exception as e:
                print("[WARNING] URLLIB_REQUEST : ", e)
                continue

        print("Success !")

    def imageCrawling(self):
        # 전체 -> 이미지 검색모드 전환
        searchImg = self.browser.find_element_by_xpath("//a[@class='q qs']")
        searchImg.click()

        # 50번 스크롤 하강! (window.scrollBy(0, 10000) Script Execute 로 대체 가능)
        num_of_pagedown = 50

        for n in range(num_of_pagedown):
            # 페이지 다운키를 클릭한다.
            body = self.browser.find_element_by_xpath("//body[@id='yDmH0d']")
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

            try:
                viewMore = self.browser.find_element_by_xpath("//div[@class='YstHxe']")
                if "결과 더보기" in viewMore.text:
                    viewMore.click()
            except NoSuchElementException:
                # 해당 예외가 발생했다는 것은, "결과 더보기" 메뉴가 존재하지 않을 경우.
                continue

            # 더 이상 표시할 콘텐츠가 없습니다. -> 처리
            try:
                nonContents = self.browser.find_element_by_xpath("//div[@class='OuJzKb Yu2Dnd']")
                if "더 이상 표시할 콘텐츠가 없습니다." in nonContents.text:
                    break
            except NoSuchElementException:
                # 해당 예외가 발생했다는 것은, 아직 표시할 콘텐츠가 남아있는 경우.
                continue

        time.sleep(3)
        self.fetch_detail_url()


if __name__ == "__main__":
    try:
        searchData = input("Enter Link : ")
        ImageCrawling = Crawling(searchData)
    except IOError:
        print("Error")
