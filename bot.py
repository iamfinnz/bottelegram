import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Fungsi untuk mengambil screenshot dari elemen tertentu
def take_screenshot(url: str, filename: str):
    options = Options()
    options.headless = True  # Menjalankan browser di background
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Atur ukuran jendela browser ke 2K
    driver.set_window_size(2560, 1440)  # Ganti dengan resolusi yang diinginkan
    
    driver.get(url)
    time.sleep(5)  # Tunggu sebentar agar halaman sepenuhnya dimuat

    # Atur zoom level ke 80%
    driver.execute_script("document.body.style.zoom='80%'")
    
    time.sleep(5)  # Tunggu sebentar setelah mengatur zoom

    # Temukan elemen yang ingin diambil gambarnya
    element = driver.find_element(By.CSS_SELECTOR, '.ng2-canvas-container')  # Ganti dengan selector yang sesuai

    # Ambil screenshot dari elemen
    element.screenshot(filename)
    
    driver.quit()

# Fungsi untuk command /radiologi
async def radiologi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = 'https://lookerstudio.google.com/reporting/b9e7ad80-5fde-489f-b2d9-b6e56ecef215/page/p_2k8dn15dnd'  # Ganti dengan URL website Anda
    screenshot_path = 'screenshot.png'
    
    take_screenshot(url, screenshot_path)
    
    # Kirim screenshot ke Telegram
    with open(screenshot_path, 'rb') as photo:
        await update.message.reply_photo(photo=photo)
    
    # Hapus file screenshot setelah dikirim
    os.remove(screenshot_path)

def main():
    # Ganti 'YOUR_TOKEN' dengan token bot Anda
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    # Daftarkan command handler
    application.add_handler(CommandHandler("radiologi", radiologi))

    # Mulai bot
    application.run_polling()

if __name__ == '__main__':
    main()
