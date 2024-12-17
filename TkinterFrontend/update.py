import tkinter as tk
from tkinter import messagebox
import requests

class UpdateApp(tk.Toplevel):
    def __init__(self, session):
        super().__init__()
        self.session = session

        if not self.session:
            messagebox.showerror("Lỗi", "Session không tồn tại. Vui lòng đăng nhập lại.")
            self.destroy()  
            return
            
        self.title("Cập nhật dữ liệu")
        self.geometry("400x600")
        self.rowconfigure([0,1], weight=1)
        self.columnconfigure(0, weight=1)

        self.crawl_frame = tk.Frame(self, padx=20, pady=20)
        self.crawl_frame.grid(row=0, column=0, sticky='nsew')
        self.crawl_frame.rowconfigure([0, 1, 2], weight=1)
        self.crawl_frame.columnconfigure(0, weight=1)

        self.crawl_label = tk.Label(self.crawl_frame, text="Crawl Dữ liệu", font=("Arial", 16, "bold"))
        self.crawl_label.grid(row=0, column=0, padx=10, pady=10, sticky='we')

        self.tiki_button = tk.Button(self.crawl_frame, text="Crawl Tiki", command=self.crawl_tiki_action, width=15, bg='#007acc', fg='white')
        self.tiki_button.grid(row=1, column=0, padx=10, pady=5)

        self.lazada_button = tk.Button(self.crawl_frame, text="Crawl Lazada", command=self.crawl_lazada_action, width=15, bg='#007acc', fg='white')
        self.lazada_button.grid(row=2, column=0, padx=10, pady=5)

        self.update_frame = tk.Frame(self, padx=20, pady=20)
        self.update_frame.grid(row=1, column=0, sticky='nsew')
        self.update_frame.rowconfigure([0, 1, 2, 3], weight=1)
        self.update_frame.columnconfigure(0, weight=1)

        self.update_label = tk.Label(self.update_frame, text="Cập nhật dữ liệu", font=("Arial", 16, "bold"))
        self.update_label.grid(row=0, column=0, padx=10, pady=10, sticky='we')

        self.update_tiki_button = tk.Button(self.update_frame, text="Cập nhật Tiki", command=self.update_tiki_action, width=15, bg='#007acc', fg='white')
        self.update_tiki_button.grid(row=1, column=0, pady=10)

        self.update_lazada_button = tk.Button(self.update_frame, text="Cập nhật Lazada", command=self.update_lazada_action, width=15, bg='#007acc', fg='white')
        self.update_lazada_button.grid(row=2, column=0, pady=10)

        self.update_both_button = tk.Button(self.update_frame, text="Cập nhật tất cả", command=self.update_both_action, width=15, bg='#007acc', fg='white')
        self.update_both_button.grid(row=3, column=0, pady=10)

    def crawl_tiki_action(self):
        print("Crawl Tiki")
        self.perform_request("https://127.0.0.1:5000/api/data/crawl_tiki", "crawl", "Tiki")

    def crawl_lazada_action(self):
        print("Crawl Lazada")
        self.perform_request("https://127.0.0.1:5000/api/data/crawl_lazada", "crawl", "Lazada")

    def update_tiki_action(self):
        self.perform_request("https://127.0.0.1:5000/api/data/load_tiki", "cập nhật", "Tiki")
        self.perform_request("https://127.0.0.1:5000/api/data/create_index", "cập nhật index", "Tiki")

    def update_lazada_action(self):
        self.perform_request("https://127.0.0.1:5000/api/data/load_lazada", "cập nhật", "Lazada")
        self.perform_request("https://127.0.0.1:5000/api/data/create_index", "cập nhật index", "Lazada")

    def update_both_action(self):
        self.perform_request("https://127.0.0.1:5000/api/data/load_tiki", "cập nhật", "Tiki")
        self.perform_request("https://127.0.0.1:5000/api/data/load_lazada", "cập nhật", "Lazada")
        self.perform_request("https://127.0.0.1:5000/api/data/create_index", "cập nhật index", "Tiki, Lazada")

    def perform_request(self, url, action, source):
        try:
            payload = {}  
            headers = {}  
            response = self.session.post(url, headers=headers, json=payload, verify=False)

            if response.status_code == 200:
                data = response.json()  
                if data.get("success") == True:  
                    messagebox.showinfo("Thành công", f"Đã {action} dữ liệu từ {source} thành công.")
                else:
                    messagebox.showerror("Lỗi", f"Không thể {action} dữ liệu từ {source}. Lý do: {data.get('message', 'Không xác định')}")
            elif response.status_code == 500:
                messagebox.showerror("Lỗi máy chủ", f"Không thể {action} dữ liệu từ {source}.")
            elif response.status_code in [404, 409]:
                messagebox.showerror("Lỗi", f"Lỗi khi {action} dữ liệu từ {source}: {response.text}")
            else:
                messagebox.showerror("Lỗi", f"Lỗi khi {action} dữ liệu từ {source}: {response.text}")
        except requests.RequestException as e:
            messagebox.showerror("Lỗi kết nối", f"Lỗi kết nối: {e}")
