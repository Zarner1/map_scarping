from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_options = Options()
chrome_options.add_argument(r"--user-data-dir=C:\Users\yildi\AppData\Local\Google\Chrome\User Data\muhammed")
chrome_options.add_argument(r"--profile-directory=Default")  # Varsayılan profil
chrome_options.add_argument("--remote-debugging-port=9222")  # DevTools hatası çözümü
chrome_options.add_argument("--disable-gpu")  # GPU hatalarını önlemek için
chrome_options.add_argument("--no-sandbox")  # Sandbox modunu devre dışı bırak
chrome_options.add_argument("--disable-dev-shm-usage")  # Büyük dosyalar için paylaşımı devre dışı bırak

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://web.whatsapp.com")
time.sleep(15)


driver.quit()