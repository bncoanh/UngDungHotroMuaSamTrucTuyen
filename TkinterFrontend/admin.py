import tkinter as tk
from tkinter import messagebox
import requests

class AdminApp(tk.Tk):
    def __init__(self, session, username):
        super().__init__()
        self.session = session  # lay ss sdung
        self.username = username
        if not self.session:
            messagebox.showerror("Lỗi", "Session không tồn tại. Vui lòng đăng nhập lại.")
            self.destroy()  
            return

        self.title("Trang Admin")
        self.geometry("400x300")
        self.rowconfigure([0, 1, 2], weight=1)
        self.columnconfigure([0, 1], weight=1)

        self.admin_button = tk.Button(self, text=self.username, command=self.toggle_admin_options, width=15, bg='#007acc', fg='white')
        self.admin_button.grid(row=0, column=0, columnspan=2, pady=10)

        self.maintenance_button = tk.Button(self, text="Bảo trì tài khoản", command=self.maintenance_account, width=15, bg='#007acc', fg='white')
        self.maintenance_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.update_button = tk.Button(self, text="Cập nhật dữ liệu", command=self.update_data, width=15, bg='#007acc', fg='white')
        self.update_button.grid(row=2, column=0, columnspan=2, pady=10)

    def toggle_admin_options(self):
        from account import Account
        Account(self, self.session, self.username)

    def maintenance_account(self):
        """Chuyển sang trang bảo trì tài khoản"""
         
        import manageusers  
        manageusers_window = manageusers.MaintenanceAccountApp(self.session)
        manageusers_window.mainloop()

    def update_data(self):
        """Chuyển sang trang cập nhật dữ liệu"""
        import update
        update.UpdateApp(self.session).mainloop()

        

    def open_login_page(self):
        """Mở lại trang đăng nhập"""
        import auth 
        auth.LoginApp().mainloop() 

