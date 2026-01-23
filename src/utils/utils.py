import requests
import streamlit as st

def get_usd_rate():
    try:
        url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
        response = requests.get(url).json()
        return float(response["USDBRL"]["bid"])
    except:
        return 5.20 # Valor padrão caso a API falhe

def ui_css(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)