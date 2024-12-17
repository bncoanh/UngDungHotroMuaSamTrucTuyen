import tkinter as tk
from tkinter import messagebox
import requests


class MaintenanceAccountApp(tk.Toplevel):
    def __init__(self, session):
        super().__init__()
        self.session = session

        if not self.session:
            messagebox.showerror("Lỗi", "Session không tồn tại. Vui lòng đăng nhập lại.")
            self.destroy()  
            return

        self.title("Quản lý người dùng")
        self.geometry("600x400")
        self.rowconfigure(4, weight=1)
        self.columnconfigure([0, 1, 2], weight=1)

        # Giao diện quản trị
        tk.Label(self, text="Tên người dùng:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='we')

        tk.Label(self, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self)
        self.password_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='we')

        self.add_button = tk.Button(self, text="Thêm người dùng", command=self.create_user, width=15, bg='#007acc', fg='white')
        self.update_button = tk.Button(self, text="Cập nhật mật khẩu", command=self.update_user, width=15, bg='#007acc', fg='white')
        self.delete_button = tk.Button(self, text="Xóa người dùng", command=self.delete_user, width=15, bg='#007acc', fg='white')

        # Sắp xếp các nút vào cùng một hàng (row 2)
        self.add_button.grid(row=2, column=0, padx=10, pady=5)
        self.update_button.grid(row=2, column=1, padx=10, pady=5)
        self.delete_button.grid(row=2, column=2, padx=10, pady=5)

        # Danh sách người dùng
        self.user_listbox = tk.Listbox(self)
        self.user_listbox.grid(row=4, column=0, columnspan=3, pady=10, sticky='nswe')

        tk.Button(self, text="Lấy danh sách", command=self.show_user_data, width=15, bg='#007acc', fg='white').grid(row=5, column=0, columnspan=3, pady=5)
        
        self.user_listbox.bind('<<ListboxSelect>>', self.on_user_select)

    def show_user_data(self):
        url = "https://127.0.0.1:5000/api/admin/manage_users"
        try:
            response = self.session.get(url, verify=False)
            if response.status_code == 200:
                self.user_listbox.delete(0, tk.END)
                user_data = response.json()
                for user in user_data.get('data', []):
                    self.user_listbox.insert(tk.END, f"{user['accountId']} - {user['username']}")
            elif response.status_code == 401:  
                messagebox.showerror("Lỗi", "Bạn chưa đăng nhập. Vui lòng đăng nhập trước khi tiếp tục.")
            else:
                messagebox.showerror("Lỗi", f"Không thể lấy danh sách người dùng: {response.text}")
        except requests.RequestException as e:
            messagebox.showerror("Lỗi", f"Lỗi kết nối: {e}")

    def create_user(self):
        # Lấy dữ liệu từ các textbox
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            
            user_payload = {
                "username": username,
                "password": password
            }

            
            try:
                response = self.session.post(
                    "https://127.0.0.1:5000/api/admin/manage_users",
                    json=user_payload,
                    verify=False
                )
                if response.status_code == 201:  
                    messagebox.showinfo("Thành công", "Người dùng mới đã được thêm.")
                    self.show_user_data()  
                elif response.status_code == 409: 
                    error_message = response.json().get('message', 'Lỗi không xác định')
                    if "already registered" in error_message:
                        messagebox.showerror("Lỗi", f"Người dùng {username} đã tồn tại.")
                    else:
                        messagebox.showerror("Lỗi", f"Lỗi khi thêm người dùng: {response.text}")
                else:
                    messagebox.showerror("Lỗi", f"Lỗi khi thêm người dùng: {response.status_code} - {response.text}")
            except requests.RequestException as e:
                messagebox.showerror("Lỗi", f"Lỗi khi kết nối tới server: {str(e)}")
        else:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin cho user mới.")

    def update_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Lấy accountId 
        selected_index = self.user_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            account_id, _ = self.user_listbox.get(selected_index).split(" - ")
        else:
            messagebox.showwarning("Lỗi", "Vui lòng chọn người dùng để cập nhật.")
            return

        if username and password:
            confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn cập nhật mật khẩu cho {username}?")
            if confirm:
                url = "https://127.0.0.1:5000/api/admin/manage_users"
                payload = {"accountId": account_id, "password": password}

                try:
                    response = self.session.patch(url, json=payload, verify=False)
                    if response.status_code == 200:
                        messagebox.showinfo("Thành công", "Cập nhật mật khẩu thành công.")
                        self.show_user_data()  
                    else:
                        messagebox.showerror("Lỗi", f"Lỗi khi cập nhật mật khẩu: {response.status_code} - {response.text}")
                except requests.RequestException as e:
                    messagebox.showerror("Lỗi", f"Lỗi kết nối: {str(e)}")
        else:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin mật khẩu mới.")


    def delete_user(self):
        selected_index = self.user_listbox.curselection()  # lay indẽ
        if selected_index:
            selected_index = selected_index[0] 
            account_id, _ = self.user_listbox.get(selected_index).split(" - ")

            confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa người dùng với ID: {account_id}?")
            if confirm:
                url = "https://127.0.0.1:5000/api/admin/manage_users"
                payload = {"accountId": account_id}  
                try:
                    response = self.session.delete(url, json=payload, verify=False)
                    if response.status_code == 200:
                        messagebox.showinfo("Thành công", f"Đã xóa người dùng ID: {account_id}")
                        self.show_user_data()  
                    else:
                        messagebox.showerror("Lỗi", f"Lỗi khi xóa người dùng: {response.status_code} - {response.text}")
                except requests.RequestException as e:
                    messagebox.showerror("Lỗi", f"Lỗi kết nối: {str(e)}")
        else:
            messagebox.showwarning("Chưa chọn người dùng", "Vui lòng chọn người dùng cần xóa.")



    def on_user_select(self, event):
        selected_index = self.user_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            account_id, username = self.user_listbox.get(selected_index).split(" - ")
            
            
            self.selected_account_id = account_id
            
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, username)
            self.password_entry.delete(0, tk.END)  
