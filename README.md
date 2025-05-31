# Проект: Бинарная классификация для предиктивного обслуживания оборудования

## Описание  
Цель проекта – разработать модель, которая по данным о состоянии оборудования (температура, скорость, крутящий момент, износ и др.) предсказывает, произойдет ли отказ (Machine failure = 1) или нет (0). Результаты оформлены в виде Streamlit-приложения с двумя страницами:  
- **Анализ и модель** – загрузка данных, обучение, метрики, предсказание на новых данных.  
- **Презентация** – слайды с описанием этапов проекта.  

## Датасет  
Используется «AI4I 2020 Predictive Maintenance Dataset» (10 000 записей, 14 признаков).  
- Источник: https://archive.ics.uci.edu/dataset/601/predictive+maintenance+dataset  
- Основные признаки:  
  - `Type` (L/M/H)  
  - `Air temperature [K]`  
  - `Process temperature [K]`  
  - `Rotational speed [rpm]`  
  - `Torque [Nm]`  
  - `Tool wear [min]`  
  - `Machine failure` (целевая переменная).  

## Установка и запуск  
1. Клонируйте репозиторий:  
   ```bash
   git clone <https://github.com/Jinede/DSFinal>
   cd .\DSFinal\
   python -m pip install  -r .\requirements.txt --user
   python -m  streamlit run app.py
