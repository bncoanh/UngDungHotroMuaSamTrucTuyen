# Shopping-assistant-desktop-app

# Kiến trúc hệ thống
![image](https://github.com/user-attachments/assets/4484f069-c489-4b20-a1ee-cc2f2dc02c88)

# Biểu đồ các lớp
![image](https://github.com/user-attachments/assets/5c853c3b-baf2-43cc-8fb3-d8de6acbc00c)

# Biểu đồ thực thể liên kết
![image](https://github.com/user-attachments/assets/06a967e3-1df6-482f-9b96-f1604bf285b3)


# Các bước chạy project
1. Tạo môi trường ảo:
- Mở FlaskBackend bằng VSCode
- Từ VSCode, nhấn Ctrl + P, nhập ">Python: Create Environment" và chọn mục
- Chọn Venv, phiên bản Python và tích vào ô "requirements.txt"
- Đợi VSCode tạo, kích hoạt môi trường ảo và cài đặt thư viện cần thiết
2. Tạo cơ sở dữ liệu:
- Cài đặt MySQL
- Tạo người dùng với tên người dùng là "root" và mật khẩu là "12345"
- Chạy MySQL Workbench, kết nối với localinstance bằng tên người dùng và mật khẩu đã tạo ở trên
- Chọn Data Import/Restore
- Chọn Import from Self-Contained File và chọn tệp Dump.sql từ thư mục này
- Tạo một Schema mới có tên là "ShoppingAssistant"
- Nhấp vào "Start Import"
3. Chạy máy chủ
- Từ thiết bị đầu cuối VSCode (môi trường ảo đã được kích hoạt), nhập "flask run --cert=cert.pem --key=key.pem --debug"

# Link chạy thử trên postman
https://red-zodiac-742421.postman.co/workspace/My-Workspace~8fd581cf-ea94-44f1-8282-f142b96a6821/collection/39630068-889a5ed0-9e74-42dd-9da9-8af8f862e0e0?action=share&creator=39630068&active-environment=39630068-c79c7a93-f91c-4c8e-96a5-4ba260f5cafb
