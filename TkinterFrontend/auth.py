import tkinter as tk
from tkinter import Checkbutton
from tkinter import messagebox
import requests


class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.session = requests.Session()  

        self.title("Đăng nhập hệ thống")
        self.geometry('300x300')
        self.rowconfigure([0, 1, 2, 3, 4], weight=1)
        self.columnconfigure([0, 1], weight=1)

        #đag nhập
        tk.Label(self, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky='we')
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky='we')

        tk.Label(self, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky='we')
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky='we')

        self.is_admin_var = tk.BooleanVar()
        self.admin_check = tk.Checkbutton(self, text="Đăng nhập với quyền Admin", variable=self.is_admin_var)
        self.admin_check.grid(row=2, column=0, columnspan=2, pady=10, sticky='we')

       
        tk.Button(self, text="Đăng nhập", command=self.login, width=15, bg='#007acc', fg='white').grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(self, text="Đăng ký", command=self.open_register_page, width=15, bg='#007acc', fg='white').grid(row=4, column=0, columnspan=2, pady=10)

    def login(self):
        self.username = self.username_entry.get()
        password = self.password_entry.get()

        if self.username and password:
            login_url = "https://127.0.0.1:5000/api/auth/admin_login" if self.is_admin_var.get() else "https://127.0.0.1:5000/api/auth/login"
            payload = {"username": self.username, "password": password}
            headers = {'Content-Type': 'application/json'}

            try:
                response = self.session.post(login_url, headers=headers, json=payload, verify=False)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        
                        messagebox.showinfo("Thành công", "Đăng nhập thành công!")
                        self.open_admin_panel() if self.is_admin_var.get() else self.open_user_panel()
                    else:
                        messagebox.showerror("Lỗi", f"Đăng nhập thất bại: {data.get('message', 'Không rõ lý do.')}")
                elif response.status_code == 401: 
                    messagebox.showerror("Lỗi", "Sai tên tài khoản hoặc mật khẩu.")
                else:
                    messagebox.showerror("Lỗi", f"Đăng nhập thất bại: {response.status_code} - {response.text}") 
            except requests.RequestException as e:
                messagebox.showerror("Lỗi", f"Lỗi kết nối: {e}")
        else:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin đăng nhập.")

    def open_admin_panel(self):
        """Chuyển sang giao diện admin."""
        self.destroy()  # dong mh
        import admin #import mod admin
        admin.AdminApp(self.session, self.username)  # truyen session admin

    def open_user_panel(self):
        """Chuyển sang giao diện người dùng."""
        self.destroy()

        import product  
        product.ProductCard(self.session, self.username)

    def open_register_page(self):
        """Chuyển sang trang đăng ký."""
        self.destroy()  
        import register
        register.RegisterApp() 


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
