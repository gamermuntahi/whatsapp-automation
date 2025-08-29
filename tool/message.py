# message.py
import os
import time
import pyautogui as pg
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys as key

base_dir = os.path.dirname(os.path.abspath(__file__))
console_file_path = os.path.join(base_dir, "requests", "console.txt")
def log_console(msg):
    with open(console_file_path, "a", encoding="utf-8") as console_file:
        console_file.write(f"[console:] {msg}\n")

class WhatsAppMessenger:
    def __init__(self, waittime=25):
        self.waittime = waittime

        # Store Chrome session to avoid QR scan every time
        self.user_data_dir = os.path.join(os.getcwd(), "whatsapp_session")
        if not os.path.exists(self.user_data_dir):
            os.makedirs(self.user_data_dir)

        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={self.user_data_dir}")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.get("https://web.whatsapp.com/")
        print("Please wait for WhatsApp Web to load...")
        log_console("Please wait for WhatsApp Web to load...")

        # Wait for the page to load fully
        WebDriverWait(self.driver, self.waittime).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @spellcheck="true"]'))
        )
        print("WhatsApp Web loaded successfully!")
        log_console("WhatsApp Web loaded successfully!")

    def send_message(self, number, message):
        try:
            # Open chat
            url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
            self.driver.get(url)
            
            # Wait until input box loads
            input_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @spellcheck="true"]'))
            )
            log_console(" WhatsApp request loaded...")
            input_box.click()
            time.sleep(2)
            pg.press("escape")
            time.sleep(2)
            pg.press("enter")  # Press Enter to send
            time.sleep(10)
            print(f"✅ Message sent to {number}")
            log_console(f"✅ Message sent to {number}")
        except Exception as e:
            print(f"❌ Failed to send to {number}: {e}")
            log_console(f"❌ Failed to send to {number}: {e}")

    def quit(self):
        self.driver.quit()

# Example usage
def whatsapp(number,msg):
    messenger = WhatsAppMessenger(waittime=25)
    messenger.send_message(number,msg) # Wait between messages
    messenger.quit()