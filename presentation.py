# presentation.py
import streamlit as st
import reveal_slides as rs

def presentation_page():
    st.title("Презентация проекта: Predictive Maintenance")
    presentation_md = """
# Прогнозирование отказов оборудования  
---

## Введение  
- **Цель проекта**: построить модель машинного обучения для бинарной классификации (Machine failure = 1 / 0).  
- **Данные**: AI4I 2020 Predictive Maintenance (10 000 записей, 14 признаков).  
---

## Этапы работы  
1. Загрузка и предобработка данных  
2. Разбиение на train/test (80/20)  
3. Обучение моделей: Logistic Regression, Random Forest, XGBoost, SVM  
4. Оценка: Accuracy, Confusion Matrix, Classification Report, ROC-AUC  
5. Разработка Streamlit-приложения + презентация  
---

## Архитектура приложения  
- `app.py` – точка входа, навигация  
- `analysis_and_model.py` – загрузка данных, обучение, оценка, предсказания  
- `presentation.py` – слайды с описанием  
---

## Результаты  
- Лучшие метрики (пример): RF: Accuracy=0.95, ROC-AUC=0.98  
- Возможные улучшения: подбор гиперпараметров, расширенная предобработка, ансамбли  
---

## Заключение  
- Проект демонстрирует полный цикл: от данных до готового веб-приложения  
- Streamlit позволяет быстро разрабатывать интерактивный интерфейс  
- Дальнейшие шаги: расширение функционала, деплой на Heroku/Streamlit Cloud  
"""
    with st.sidebar:
        st.header("Настройки презентации")
        theme = st.selectbox("Тема Reveal.js", ["black", "white", "league", "beige", "sky", "night", "serif", "simple", "solarized"])
        height = st.number_input("Высота слайдов (px)", value=600)
        transition = st.selectbox("Тип перехода", ["slide", "convex", "concave", "zoom", "none"])
        plugins = st.multiselect("Плагины", ["highlight", "katex", "mathjax2", "mathjax3", "notes", "search", "zoom"], default=[])

    rs.slides(
        presentation_md,
        height=height,
        theme=theme,
        config={"transition": transition, "plugins": plugins},
        markdown_props={"data-separator-vertical": "^--$"}
    )
