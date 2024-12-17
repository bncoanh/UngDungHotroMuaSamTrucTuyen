import tkinter as tk
from tkinter import messagebox
import requests


class ChangePasswordApp(tk.Toplevel):
    def __init__(self, session):
        super().__init__()
        self.session = session  

        if not self.session:
            messagebox.showerror("Lỗi", "Session không tồn tại. Vui lòng đăng nhập lại.")
            self.destroy()  
            return
            
        self.title("Đổi mật khẩu")
        self.geometry("400x300")
        self.rowconfigure([0, 1, 2], weight=1)
        self.columnconfigure([0, 1], weight=1)

        tk.Label(self, text="Mật khẩu cũ:").grid(row=0, column=0, padx=10, pady=10, sticky='we')
        self.old_password_entry = tk.Entry(self, show="*")
        self.old_password_entry.grid(row=0, column=1, padx=10, pady=10, sticky='we')

        tk.Label(self, text="Mật khẩu mới:").grid(row=1, column=0, padx=10, pady=10, sticky='we')
        self.new_password_entry = tk.Entry(self, show="*")
        self.new_password_entry.grid(row=1, column=1, padx=10, pady=10, sticky='we')

        tk.Button(self, text="Đổi mật khẩu", command=self.change_password, width=15, bg='#007acc', fg='white').grid(row=2, columnspan=2, pady=20)

    def change_password(self):
        """Thực hiện đổi mật khẩu."""
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()

        if old_password and new_password:
            confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đổi mật khẩu?")
            if not confirm:
                return  

            # Cấu hình API
            url = "https://127.0.0.1:5000/api/auth/change_password"
            payload = {"oldPassword": old_password, "newPassword": new_password}
            headers = {'Content-Type': 'application/json'}

            try:
                response = self.session.patch(url, json=payload, headers=headers, verify=False)
                if response.status_code == 200:
                    messagebox.showinfo("Thành công", "Đổi mật khẩu thành công!")
                    self.destroy()  
                elif response.status_code == 401:
                    messagebox.showerror("Lỗi", "Mật khẩu cũ không đúng.")
                elif response.status_code == 400:
                    messagebox.showerror("Lỗi", "Dữ liệu không hợp lệ. Vui lòng kiểm tra lại.")
                else:
                    messagebox.showerror("Lỗi", f"Đổi mật khẩu thất bại: {response.text}")
            except requests.RequestException as e:
                messagebox.showerror("Lỗi", f"Lỗi kết nối: {e}")
        else:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin mật khẩu.")

