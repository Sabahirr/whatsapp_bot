import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time


class WhatsAppAutomation:
    
    def __init__(self):
        self.stop_flag = False

    def start_driver(self):
        """Chrome driver-i işə salır."""
        if "driver" not in st.session_state:
            options = Options()
            options.add_argument("--log-level=3")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--start-maximized")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get("https://web.whatsapp.com")
            st.session_state.driver = driver
            st.success("Driver işə salındı. QR kodunu oxut və gözlə.")
        else:
            st.warning("Driver artıq işə salınıb.")
    
    def stop_driver(self):
        """Driver-i dayandırır."""
        if "driver" in st.session_state and st.session_state.driver:
            st.session_state.driver.quit()
            del st.session_state.driver
            st.success("Driver dayandırıldı.")
        else:
            st.warning("Driver artıq dayandırılıb.")
    
    def get_contacts(self):
        """WhatsApp kontaktlarını alır."""
        try:
            contacts = []
            driver = st.session_state.driver
            time.sleep(2)
            div_class = "x1c4vz4f x3nfvp2 xuce83p x1bft6iq x1i7k8ik xq9mrsl x6s0dn4"
            contact_elements = driver.find_elements(By.XPATH, f"//div[@class='{div_class}']/span[@title]")
            # contact_elements = driver.find_elements(By.XPATH, '//span[@title]')
            for element in contact_elements:
                contact_name = element.get_attribute("title")
                if contact_name and contact_name not in contacts:
                    contacts.append(contact_name)
            return contacts
        except Exception as e:
            st.error(f"Kontaktlar alınarkən xəta baş verdi: {str(e)}")
            return []

    def search_contact(self, contact_name):
        """WhatsApp-da kontaktı axtarır."""
        try:
            driver = st.session_state.driver
            search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.click()
            search_box.clear()
            search_box.send_keys(contact_name)
            search_box.send_keys(Keys.ENTER)
            time.sleep(1)
            return True
        except Exception as e:
            st.error(f"{contact_name} tapılmadı! Xəta: {str(e)}")
            return False

    def send_message(self, message):
        """Mesaj göndərir."""
        try:
            driver = st.session_state.driver
            message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            message_box.send_keys(message)
            time.sleep(0.5)
            message_box.send_keys(Keys.ENTER)
            st.success("Mesaj göndərildi!")
        except Exception as e:
            st.error(f"Mesaj göndərmək mümkün olmadı: {str(e)}")
    
        
    def send_message_to_multiple(self, contacts, message, delay):
        """Seçilən bir neçə kontakta təkrar-təkrar mesaj göndərir."""
        self.stop_flag = False
        while not self.stop_flag:
            
            if message.lower() == "stop":
                st.warning("Mesaj göndərmə dayandırıldı!")
                self.stop_flag = True
                break
                    
            for contact_name in contacts:
                if self.search_contact(contact_name):
                    self.send_message(message)
                else:
                    st.warning(f"{contact_name} tapılmadı və mesaj göndərilmədi.")
            # Gözləmə intervalı
            time.sleep(delay)