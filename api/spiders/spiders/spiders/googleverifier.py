from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
class GoogleVerifier:
    def __init__(self):
        print("verifier_initiated.....")
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome('api/spiders/spiders/driver/chromedriver',chrome_options=options)
        print("driver_intiated....")
        # self.driver.maximize_window()

    def _parse(self,name,releaseDate):
        search_string = "{} {}".format(name, releaseDate)
        search_string = search_string.replace(' ','+')
        self.driver.get('https://www.google.com/search?q='+search_string)
        
        try:
            glikes = int("".join([x for x in self.driver.find_element_by_xpath("//div[@class='srBp4 Vrkhme']").text if x.isdigit()]),10)
        except:
            glikes = 0
        return glikes
    
    def run(self,name,releaseDate):
      return self._parse(name,releaseDate)

    def __del__(self):
        self.driver.quit()
