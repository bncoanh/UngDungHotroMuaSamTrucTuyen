import tkinter as tk
from tkinter import messagebox
import requests
import json

class RegisterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Đăng ký tài khoản")
        self.geometry("400x250")
        self.rowconfigure([0, 1, 2, 3, 4], weight=1)
        self.columnconfigure([0, 1], weight=1)

        tk.Label(self, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="Xác nhận Password:").grid(row=2, column=0, padx=10, pady=10)
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self, text="Đăng ký", command=self.register, width=15, bg='#007acc', fg='white').grid(row=3, columnspan=2, pady=10)

        tk.Button(self, text="Quay lại", command=self.open_login_page, width=15, bg='#007acc', fg='white').grid(row=4, columnspan=2, pady=10)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            return

        if password != confirm_password:
            messagebox.showwarning("Lỗi", "Mật khẩu xác nhận không khớp.")
            return

        url = "https://127.0.0.1:5000/api/auth/register"
        payload = json.dumps({
            "username": username,
            "password": password
        })
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)

            if response.status_code == 201:
                data = response.json()
                if data.get("success"):
                    messagebox.showinfo("Thành công", "Đăng ký thành công!")
                    self.open_login_page()
                else:
                    messagebox.showerror("Lỗi", f"Đăng ký thất bại: {data.get('message', 'Không rõ lý do.')}")
            elif response.status_code == 409:
                messagebox.showerror("Lỗi", "Tài khoản đã tồn tại. Vui lòng chọn tên tài khoản khác.")
            else:
                messagebox.showerror("Lỗi", f"Lỗi kết nối: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            messagebox.showerror("Lỗi", f"Lỗi kết nối: {e}")

    def open_login_page(self):
        """Mở lại trang đăng nhập"""
        self.destroy()
        import auth  
        auth.LoginApp().mainloop()  

