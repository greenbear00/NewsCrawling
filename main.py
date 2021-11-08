from pathlib import Path
import os
from selenium import webdriver

def print_hi(name):
    path = Path(__file__).parent
    chrome_path = os.path.join(path, *["driver", "osx_chromedriver"])
    print(f"chrome path = {chrome_path}")

    driver = webdriver.Chrome(executable_path=chrome_path)

    driver.get("http://www.daum.net")

    # os.path



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
