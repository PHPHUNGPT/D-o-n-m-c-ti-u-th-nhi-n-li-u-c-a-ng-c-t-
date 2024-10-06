import streamlit as st
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load các mô hình và scaler đã lưu
linear_model = joblib.load('models/linear_model.pkl')
ridge_model = joblib.load('models/ridge_model.pkl')
mlp_model = joblib.load('models/mlp_model.pkl')
bagging_linear = joblib.load('models/bagging_linear.pkl')
bagging_ridge = joblib.load('models/bagging_ridge.pkl')
bagging_mlp = joblib.load('models/bagging_mlp.pkl')
scaler = joblib.load('models/scaler.pkl')

# Giao diện ứng dụng Streamlit
st.title("Dự đoán mức tiêu thụ nhiên liệu của xe")
st.write("Nhập các thông số cần thiết để dự đoán mức tiêu thụ nhiên liệu (mpg).")

# Tạo form nhập liệu từ người dùng
cylinders = st.number_input("Số xi-lanh", min_value=3, max_value=12, value=6)
displacement = st.number_input("Displacement", min_value=60.0, max_value=500.0, value=200.0)
horsepower = st.number_input("Công suất (Horsepower)", min_value=50.0, max_value=300.0, value=100.0)
weight = st.number_input("Trọng lượng xe (Pounds)", min_value=1000.0, max_value=5000.0, value=3000.0)
acceleration = st.number_input("Tăng tốc (Seconds)", min_value=8.0, max_value=24.0, value=15.0)
model_year = st.number_input("Năm sản xuất", min_value=70, max_value=82, value=76)
origin = st.selectbox("Xuất xứ", [1, 2, 3], index=0)

# Chuyển đổi đầu vào thành mảng numpy
input_data = np.array([[cylinders, displacement, horsepower, weight, acceleration, model_year, origin]])

# Chuẩn hóa dữ liệu
input_data_scaled = scaler.transform(input_data)

# Cho phép người dùng chọn mô hình dự đoán
model_choice = st.selectbox("Chọn mô hình để dự đoán:", 
                            ("Linear Regression", "Ridge Regression", "MLP Regressor", "Combined Bagging Model"))

# Tính toán dự đoán dựa trên mô hình đã chọn
if st.button("Dự đoán"):
    if model_choice == "Linear Regression":
        prediction = linear_model.predict(input_data_scaled)
    elif model_choice == "Ridge Regression":
        prediction = ridge_model.predict(input_data_scaled)
    elif model_choice == "MLP Regressor":
        prediction = mlp_model.predict(input_data_scaled)
    elif model_choice == "Combined Bagging Model":
        # Dự đoán với từng mô hình Bagging
        y_pred_bagging_linear = bagging_linear.predict(input_data_scaled)
        y_pred_bagging_ridge = bagging_ridge.predict(input_data_scaled)
        y_pred_bagging_mlp = bagging_mlp.predict(input_data_scaled)

        # Trung bình các dự đoán từ 3 mô hình
        prediction = (y_pred_bagging_linear + y_pred_bagging_ridge + y_pred_bagging_mlp) / 3

    # Nếu kết quả dự đoán là âm, nhân với -1 để chuyển thành dương
    if prediction[0] < 0:
        prediction[0] = -prediction[0]
    
    # Hiển thị kết quả dự đoán
    st.success(f"Dự đoán mức tiêu thụ nhiên liệu (mpg): {prediction[0]:.2f}")

# Thông tin về độ tin cậy của mô hình
st.write("Chọn mô hình tốt nhất và nhập dữ liệu để dự đoán.")
st.write("Mô hình dự đoán sử dụng các phương pháp hồi quy: Linear, Ridge, MLP và Bagging.")
