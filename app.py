# app.py
import streamlit as st

# Подключаем страницы (Streamlit ≥1.10)
import analysis_and_model
import presentation

# Словарь с названием и функцией-обёрткой каждой страницы
PAGES = {
    "Анализ и модель": analysis_and_model.analysis_and_model_page,
    "Презентация": presentation.presentation_page
}

st.sidebar.title("Навигация")
selection = st.sidebar.radio("Перейти на страницу:", list(PAGES.keys()))
page_func = PAGES[selection]
page_func()
