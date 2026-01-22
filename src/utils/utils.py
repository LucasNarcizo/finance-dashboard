import requests
import streamlit as st
import streamlit.components.v1 as components

def get_usd_rate():
    try:
        url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
        response = requests.get(url).json()
        return float(response["USDBRL"]["bid"])
    except:
        return 5.0

def load_custom_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def load_custom_html(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        html_code = f.read()
        components.html(html_code, height=150)