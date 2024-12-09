import re
import time
import csv
import pywhatkit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import keyboard
#uygulama sadece türkiyedeki yerler için çalışıyor çünkü html kodları değişebiliyor bu da hata almasını sağlar 
#wp web açık olmalı !!!!

#!!!!!scroll bar çalışmıyor 

# Telefon , mekan  ve ziyaret edilmişler listeleri
mekan_tel_list = []
mekan_name_list = []
visited_urls = []  

#driver ayarları
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized")




driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#çekilen telefon numaralarını temizliyor
def temizle_telefon(numara):
    temiz_numara = re.sub(r'[^\d+]', '', numara)
    return temiz_numara

def mekan_cek(arama_kelimesi, kordinat_x, kordinat_y, zoom):
    driver.get(f"https://www.google.com/maps/search/{arama_kelimesi}/@{kordinat_x},{kordinat_y},{zoom}z")
    time.sleep(2)


    #scrollbarı aşağı indirip mekanları html üzerinde görünür hale getirmeye çalışıyor    
    for _ in range(5):  
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "hfpxzc")))
            scrollable_div = driver.find_element(By.CLASS_NAME, "m6QErb")  # Google Maps için doğru sınıf
            driver.execute_script("arguments[0].scrollBy(0, 2000);", scrollable_div)

            time.sleep(1.5)
        except Exception as e:
            print(f"Kaydırma hatası: {e}")
            break
    #görünür tüm mekanları listeye ekler            
    mekan_page_list = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    print(f"Toplam restoran bulundu: {len(mekan_page_list)}")

    for mekan in mekan_page_list:
        
        try:
            mekan.click()
            time.sleep(1)
            current_url = driver.current_url

            if current_url in visited_urls:  
                print(f"Zaten ziyaret edilmiş: {current_url}")
                
                continue

            visited_urls.append(current_url)

            # Restoran detaylarını çekme
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//button[contains(@data-item-id, 'phone')]"))
            )
            mekan_name = driver.find_element(By.XPATH, "//h1[contains(@class, 
                                             'DUwDvf lfPIob')]").text
            if mekan_name not in mekan_name_list:
                mekan_name_list.append(mekan_name)
                print(f"Bulunan restoran: {mekan_name}")

                mekan_details = driver.find_elements(By.XPATH, "//button[contains(@data-item-id, 'phone')]")
                for detail in mekan_details:
                    if detail.is_displayed():
                        temiz_tel = temizle_telefon(detail.text)
                        if temiz_tel not in mekan_tel_list:
                            mekan_tel_list.append(temiz_tel)
                            print(f"Telefon: {temiz_tel}")
                            break
            
            
            time.sleep(2)
            

        except Exception as e:
            print(f"Restoran detay çekme hatası: {e}")
              
            time.sleep(2)
            continue

    print("Telefon Numaraları:", mekan_tel_list)
    print("Mekan İsimleri:", mekan_name_list)

def data_save():
    
    with open("map_data.csv", "w", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Mekan adı","Telefon numarası"])
        for isim, telefon in zip(mekan_name_list, mekan_tel_list):
            writer.writerow([isim, telefon])



    pass    

def message_send(message):
    
    Ntime = datetime.datetime.now()
    hour = Ntime.hour
    minute = Ntime.minute + 2  

   
    if minute >= 60:
        minute -= 60
        hour += 1

    
    if hour >= 24:
        hour -= 24

    n = 0
    with open("map_data.csv", "r", newline="", encoding='utf-8') as f:
        reader = csv.reader(f)
        for isim, tel in reader:
            Ntime = datetime.datetime.now()
            hour = Ntime.hour
            minute = Ntime.minute + 1  

   
            if minute >= 60:
                minute -= 60
                hour += 1

    
            if hour >= 24:
                hour -= 24

            if n == 0:  
                n += 1
                continue   

            print(f"Mesaj gönderiliyor: {isim}, {tel}")
            pywhatkit.sendwhatmsg(f"+9{tel}", message, hour, minute,tab_close=True,wait_time=10)

            time.sleep(2)  





mekan_cek("restaurant", 41, 29, 16)
data_save()
message_send(".")
driver.quit()
