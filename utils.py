import streamlit as st

def get_whatsapp_bot():
    """Streamlit session_state-də WhatsApp botunu saxlayır."""
    if "whatsapp_bot" not in st.session_state:
        from bot import WhatsAppAutomation
        st.session_state.whatsapp_bot = WhatsAppAutomation()
    return st.session_state.whatsapp_bot
