import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score, confusion_matrix,
    classification_report, roc_auc_score, roc_curve
)

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    try:
        y_proba = model.predict_proba(X_test)[:, 1]
    except:
        y_proba = model.decision_function(X_test)

    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    cr = classification_report(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)

    st.write(f"**Accuracy:** {acc:.3f}")
    st.write("**Confusion Matrix:**")
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    st.pyplot(fig)

    st.write("**Classification Report:**")
    st.text(cr)

    st.write(f"**ROC-AUC:** {auc:.3f}")
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    plt.figure()
    plt.plot(fpr, tpr, label=f"{model.__class__.__name__} (AUC = {auc:.2f})")
    plt.plot([0, 1], [0, 1], "--", color="gray")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"ROC-кривая: {model.__class__.__name__}")
    plt.legend()
    st.pyplot(plt.gcf())
    plt.clf()

def analysis_and_model_page():
    st.title("Анализ данных и модель")
    st.write("**Цель:** предсказать отказ оборудования (Target = 1/0).")

    uploaded = st.file_uploader("Загрузите CSV-датасет", type="csv")
    if uploaded is None:
        st.info("Загрузите файл CSV с данными или перейдите на страницу Презентации для инструкции.")
        return

    df = pd.read_csv(uploaded)
    st.write("### Первые строки загруженных данных")
    st.dataframe(df.head())

    to_drop = ['UDI', 'Product ID', 'TWF', 'HDF', 'PWF', 'OSF', 'RNF']
    df = df.drop(columns=[c for c in to_drop if c in df.columns], errors='ignore')

    if 'Type' in df.columns:
        le = LabelEncoder()
        df['Type'] = le.fit_transform(df['Type'])

    if df.isna().sum().sum() > 0:
        st.warning("Найдены пропущенные значения. Они будут заполнены нулями.")
        df = df.fillna(0)

    num_feats = ['Air temperature [K]', 'Process temperature [K]',
                 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']
    present_num = [f for f in num_feats if f in df.columns]
    if present_num:
        scaler = StandardScaler()
        df[present_num] = scaler.fit_transform(df[present_num])

    if 'Machine failure' not in df.columns:
        st.error("В файле отсутствует столбец 'Machine failure'.")
        return

    X = df.drop(columns=['Machine failure'])
    y = df['Machine failure']

    # ⚙️ Создаем переменную session_state для модели, если её нет
    if 'rf_model' not in st.session_state:
        st.session_state.rf_model = None

    if st.button("Обучить модели"):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Фикс для XGBoost
        X_train.columns = X_train.columns.str.replace(r"[\[\]<]", "", regex=True)
        X_test.columns = X_test.columns.str.replace(r"[\[\]<]", "", regex=True)

        st.write("### LogisticRegression")
        logreg = LogisticRegression(max_iter=1000)
        logreg.fit(X_train, y_train)
        evaluate_model(logreg, X_test, y_test)

        st.write("---")
        st.write("### RandomForestClassifier")
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        evaluate_model(rf, X_test, y_test)

        # Сохраняем обученную модель в session_state
        st.session_state.rf_model = rf

        st.write("---")
        st.write("### XGBClassifier")
        xgb = XGBClassifier(n_estimators=100, learning_rate=0.1, use_label_encoder=False, eval_metric='logloss', random_state=42)
        xgb.fit(X_train, y_train)
        evaluate_model(xgb, X_test, y_test)

        st.write("---")
        st.write("### SVM (линейное ядро)")
        svm = SVC(kernel='linear', probability=True, random_state=42)
        svm.fit(X_train, y_train)
        evaluate_model(svm, X_test, y_test)

        st.success("Обучение и оценка моделей завершены.")

    st.write("---")
    st.subheader("Предсказание на новых данных")
    with st.form("prediction_form"):
        type_choice = st.selectbox("Type (L/M/H)", options=["L", "M", "H"])
        air_temp = st.number_input("Air temperature [K]", value=300.0)
        proc_temp = st.number_input("Process temperature [K]", value=310.0)
        rot_speed = st.number_input("Rotational speed [rpm]", value=1000)
        torque = st.number_input("Torque [Nm]", value=40.0)
        tool_wear = st.number_input("Tool wear [min]", value=50)

        submit = st.form_submit_button("Предсказать")
        if submit:
            type_mapping = {"L": 0, "M": 1, "H": 2}
            in_dict = {
                'Type': type_mapping[type_choice],
                'Air temperature K': (air_temp - 300) / 2,
                'Process temperature K': (proc_temp - 310) / 1,
                'Rotational speed rpm': rot_speed,
                'Torque Nm': torque,
                'Tool wear min': tool_wear
            }

            input_df = pd.DataFrame([in_dict])

            if st.session_state.rf_model is not None:
                model = st.session_state.rf_model
                pred = model.predict(input_df)[0]
                proba = model.predict_proba(input_df)[0][1]
                st.write(f"**Предсказание (Machine failure):** {pred}")
                st.write(f"**Вероятность отказа:** {proba:.2f}")
            else:
                st.error("Сначала обучите модели.")
