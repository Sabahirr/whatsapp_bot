import streamlit as st
from utils import get_whatsapp_bot

# Streamlit interfeysi
st.title("WhatsApp Avtomatlaşdırma")
st.sidebar.title("İdarə Paneli")

whatsapp_bot = get_whatsapp_bot()

if st.sidebar.button("Start Driver"):
    whatsapp_bot.start_driver()

if st.sidebar.button("Stop Driver"):
    whatsapp_bot.stop_driver()

# Gecikmə ölçü vahidi seçimi
time_unit = st.sidebar.radio("Gecikmə ölçü vahidini seçin", ["Saniyə", "Dəqiqə", "Saat"])

# Slider dəyərini ölçü vahidinə uyğunlaşdırma
if time_unit == "Saniyə":
    delay = st.sidebar.slider("Mesaj göndərilmə gecikməsi", min_value=1, max_value=60, value=1)
elif time_unit == "Dəqiqə":
    delay_minutes = st.sidebar.slider("Mesaj göndərilmə gecikməsi (dəqiqə)", min_value=1, max_value=60, value=1)
    delay = delay_minutes * 60  # Dəqiqələri saniyəyə çevir
elif time_unit == "Saat":
    delay_hours = st.sidebar.slider("Mesaj göndərilmə gecikməsi (saat)", min_value=1, max_value=24, value=1)
    delay = delay_hours * 3600  # Saatları saniyəyə çevir

# Kontakların siyahısını göstərmək və seçimi
if "driver" in st.session_state:
    st.header("Kontakt Siyahısı")
    if st.button("Kontaktlar"):
        st.session_state.contacts = whatsapp_bot.get_contacts()
        if st.session_state.contacts:
            st.success("Kontaktlar uğurla yükləndi!")
        else:
            st.error("Kontaktlar yüklənmədi. Zəhmət olmasa, WhatsApp Web-in tam yüklənməsini gözləyin.")

    if "contacts" in st.session_state and st.session_state.contacts:
        selected_contacts = st.multiselect("Mesaj göndərmək üçün şəxsləri seçin", st.session_state.contacts)
        message = st.text_area("Göndəriləcək mesaj")
        if st.button("Mesaj Göndər"):
            if selected_contacts and message.strip():
                whatsapp_bot.send_message_to_multiple(selected_contacts, message, delay)
            else:
                st.warning("Zəhmət olmasa, kontaktları seçin və mesaj yazın.")
    else:
        st.info("Əvvəlcə 'Kontaktlar' düyməsinə basın.")
else:
    st.warning("Əvvəlcə 'Start Driver' düyməsinə basın və QR kodunu oxudun.")