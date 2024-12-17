import tkinter as tk
from tkinter import messagebox
import requests

class Account(tk.Toplevel):
    def __init__(self, window,session, username):
        super().__init__()
        self.window = window
        self.session = session  # lay ss sdung
        self.username = username
        self.title(self.username)
        self.geometry("400x300")
        self.rowconfigure([0, 1], weight=1)
        self.columnconfigure(0, weight=1)

        self.change_password_button = tk.Button(self, text="Đổi mật khẩu", command=self.open_change_password, width=15, bg='#007acc', fg='white')
        self.change_password_button.grid(row=0, column=0, pady=5)

        self.logout_button = tk.Button(self, text="Đăng xuất", command=self.logout, width=15, bg='#007acc', fg='white')
        self.logout_button.grid(row=1, column=0, pady=5)
    
    def open_change_password(self):
        """Mở giao diện đổi mật khẩu."""
        from changepassword import ChangePasswordApp
        ChangePasswordApp(self.session)
        self.destroy()
    
    def logout(self):
        """Đăng xuất khỏi hệ thống."""
        logout_url = "https://127.0.0.1:5000/api/auth/logout"
        headers = {} 
        try:
            response = self.session.get(logout_url, headers=headers, verify=False)
            if response.status_code == 200:
                messagebox.showinfo("Thành công", "Đăng xuất thành công!")
                self.destroy()
                self.window.destroy()
                import auth
                auth.LoginApp().mainloop()  #quay lai dangnhap
            else:
                messagebox.showerror("Lỗi", f"Đăng xuất thất bại: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            messagebox.showerror("Lỗi", f"Lỗi kết nối: {e}")