from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from python3_anticaptcha import ImageToTextTask, CallbackClient
from PIL import Image
from time import sleep
import requests
import time

# 前臺開啟瀏覽器模式
def openChrome():
    # 加啟動配置
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    # 開啟chrome瀏覽器
    driver = webdriver.Chrome(chrome_options=option)
    return drivers

# 輸入查詢表單
def insertIDCardReissue(driver):
    url = "https://www.ris.gov.tw/app/portal/3043"
    driver.get(url)

    # 找到身分證字號輸入框並輸入查詢內容
    idnum = driver.find_element_by_id("idnum")
    idnum.send_keys("A234567890")

    # 找到發證日期 下拉選單
    applyTWY = Select(driver.find_element_by_id('applyTWY')
    applyTWY.select_by_value("105")
    applyMM = Select(driver.find_element_by_id('applyMM')
    applyMM.select_by_value("1")
    applyDD = Select(driver.find_element_by_id('applyDD')
    applyDD.select_by_value("27")
        
    #發證地點：
    siteId = Select(driver.find_element_by_id('siteId')
    siteId.select_by_value("68000")

    #領補換類別：
    applyReason = Select(driver.find_element_by_id('applyReason')
    applyReason.select_by_value("3")

    #圖片驗證
    captcha = driver.find_element_by_id("captchaImage_captcha-refresh")
    path = 'captchaImage.jpg'
    get_captcha(driver, captcha, path)
    captcha_key = parse_captcha(path)

    captchaInput_captcha = driver.find_element_by_id("captchaInput_captcha-refresh")
    captchaInput_captcha.send_keys(captcha_key)

    # 提交表單
    driver.find_element_by_xpath("//*[@id='su']").click()

    print('表單送出完畢！')

def get_captcha(driver, element, path):
    driver.save_screenshot(path)          # 先將目前的 screen 存起來
    location = element.location           # 取得圖片 element 的位置
    size = element.size                   # 取得圖片 element 的大小
    left = location['x']                  # 決定上下左右邊界
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    image = Image.open(path)              # 將 screen load 至 memory
    image = image.crop((left, top, right, bottom)) # 根據位置剪裁圖片
    image.save(path, 'png')               # 重新儲存圖片為 png 格式
    
def parse_captcha(image_path):
    # Load image into memory
    buffer = BytesIO()
    image = Image.open(image_path)
    image.save(buffer, format="PNG")
    # Use base64 to encode image buffer
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    # Anti-captcha API structure
    data = {
        "clientKey":"my-key",
        "task": {
            "type": "ImageToTextTask",
            "body": img_str,
            "phrase":False,
            "case": True,
            "numeric": 2,
            "math": 0,
            "minLength": 5,
            "maxLength": 5
        }
    }
    # Create a ImageToTextTask and retrieve taskId from response
    r = requests.post("https://api.anti-captcha.com/createTask", json=data)
    r.raise_for_status()
    task_id = r.json()['taskId']
    # Polling for task finish.
    ret = ""
    while True:
        data = {
            "clientKey":"my-key",
            'taskId': task_id
        }
        r = requests.post("https://api.anti-captcha.com/getTaskResult", json=data)
        r.raise_for_status()
        if r.json()['status'] == 'ready':
            ret = r.json()['solution']['text']
            break
        time.sleep(5)
    return ret

# 方法主入口
if __name__ == '__main__':
    # 加啟動配置
    driver = openChrome()
    insertIDCardReissue(driver)
