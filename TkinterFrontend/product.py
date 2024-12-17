import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import io, json
from io import BytesIO
import customtkinter as ctk
from tkinter import messagebox
import os
from productDetailById import ProductDetailById
class ProductCard(tk.Tk):
    PRODUCTS_PER_PAGE = 35
    PRODUCTS_PER_ROW = 7
    def __init__(self, session, username):
        super().__init__()
        self.session = session # or requests.Session()
        self.username = username
        self.title(f"{username}")
        self.state('zoomed')

        # Tạo frame trên
        self.frame_top = tk.Frame(self)
        self.frame_top.grid(row=0)
        self.frame_combobox0 = tk.Frame(self)
        self.frame_combobox0.grid(row=1, sticky="ew")
        self.frame_combobox11 = tk.Frame(self.frame_combobox0, width=280)
        self.frame_combobox11.grid(row=0, column=0, sticky="w")
        self.frame_combobox1 = tk.Frame(self.frame_combobox0)
        self.frame_combobox1.grid(row=0, column=1, sticky="w")
        self.frame_combobox = tk.Frame(self.frame_combobox0)
        self.frame_combobox.grid(row=0, column=2, sticky="e")
        self.frame_combobox0.columnconfigure(1, weight=1)
        # Tạo frame dưới
        self.frame_bottom = tk.Frame(self)
        self.frame_bottom.grid(row=2, sticky="nsew")
        

        self.frame_bottom_left = tk.Frame(self.frame_bottom, width=400, bg="lightgrey")
        self.frame_bottom_left.grid(row=0, column=0, sticky="nsw", padx=30, pady=0)

        self.frame_bottom_right1 = tk.Frame(self.frame_bottom, width= 1000)
        self.frame_bottom_right1.grid(row=0, column=1)
        self.frame_bottom_right = tk.Frame(self.frame_bottom_right1, width= 1000)
        self.frame_bottom_right.grid(row=0)
        self.frame_page = tk.Frame(self.frame_bottom_right1)
        self.frame_page.grid(row=1, sticky='we')
        self.current_number = 1
        self.page = 1

        #Gọi 
       
        self.data_list =  []
        data = self.url_load_search_history1()
        self.data_list.extend([item["content"] for item in data["data"][:4]])
        # Load và hiển thị logo
        self.logo_frame = tk.Frame(self.frame_top)
        self.logo_frame.grid(row=0, column=0,  rowspan=2)
        image_path = os.path.join(os.path.dirname(__file__), "image", "ShoppingAssistant.png")  # Thay bằng đường dẫn ảnh
        img = Image.open(image_path)
        # img = img.resize((160,80))  # Thay đổi kích thước ảnh nếu cần
        self.logo_img = ImageTk.PhotoImage(img) 
        self.logo = tk.Label(self.logo_frame, image=self.logo_img)
        self.logo.grid(row=0, column=0, sticky='W', padx= 30)
        self.logo.bind("<Button-1>",self.load_search_history) #Khi click chọn vào frame logo, về phần đề xuất màng hình sản phẩm
        self.combobox_product()
        #Phần cho tài khoản đăng nhập
        self.tk_frame = tk.Frame(self.frame_top)
        self.tk_frame.grid(row=0, column=2,  rowspan=2)
        self.tk_img = self.tk_image()
        self.button_with_image = tk.Button(
            self.tk_frame,
            text=f"{username}",  # Văn bản trên nút
            image=self.tk_img,  # Hình ảnh
            compound="left",  # Văn bản nằm trên hoặc dưới hình ảnh
            width=100,
            height=50,
            command=self.open_login_window # Gọi hàm khi nhấn nút
        )
        self.button_with_image.pack()
        # Tạo ô tìm kiếm
        self.timkiem_frame = tk.Frame(self.frame_top)
        self.timkiem_frame.grid(row=0, column=1)
        self.lable_timkiem_frame = tk.Frame(self.frame_top)
        self.lable_timkiem_frame.grid(row=1, column=1)
        self.labels = []
        for i in range(4):
            lbl = tk.Label(self.lable_timkiem_frame, text="", width=15, anchor="center", bg="lightgray")
            lbl.grid(row=0, column=i, padx=5, sticky='w')
            self.labels.append(lbl)
        self.update_labels()
        self.timkiem = ctk.CTkEntry(
            self.timkiem_frame,
            width=600,
            height=35,
            placeholder_text='Tìm kiếm',
            border_color='#00FF99',
            border_width=2,
            corner_radius=10
        )
        self.timkiem.grid(row=0, column=1, padx=30)

        self.button = ctk.CTkButton(self.timkiem_frame,text="Tìm kiếm", command=self.load_search)
        self.button.grid(row=0, column=2, padx = 30)

        self.button_comnobox = ctk.CTkButton(self.frame_combobox,text="Lọc", command=self.load_search)    
        self.button_comnobox.grid_forget()
        self.button_comnobox1 = ctk.CTkButton(self.frame_combobox,text="Lọc", command=self.on_filter_click)    
        self.button_comnobox1.grid_forget()

        self.label_total_quantity = None
        self.btn_next = None
        self.btn_prev = None
        self.lable_page = None

        self.load_search_history()
        self.load_url()
        
    def url_load_search_history1(self):
        
        url = "https://127.0.0.1:5000/api/tracking/recently_browsed"

        try:
            response = self.session.get(url, verify=False)  # Use session for consistency
            if response.status_code == 200:
                data = response.json()
                return data

            else:
                messagebox.showerror("Error", f"Lỗi: {response.status_code}, {response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Lỗi yêu cầu: {e}")
        # print("Đang load lịch sửa ")    
    def update_labels(self):
        
        for i, lbl in enumerate(self.labels):
            lbl.config(text="")
        for i, lbl in enumerate(self.labels):
            if i < len(self.data_list):
                lbl.config(text=self.data_list[i])
        # print("Đang update lịch sửa ") 
    def load_url(self):
        try:
            url = "https://127.0.0.1:5000/api/product/tiki/get_categories"
            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload, verify=False)
            categories_data = json.loads(response.text)

            if categories_data['success']:
                categories = categories_data['data']
                second_level_categories = []
                
                for category in categories:
                    if 'children' in category:
                        for subcategory in category['children']:
                            second_level_categories.append(subcategory)

                self.display_categories(second_level_categories)

            else:
                print("Error fetching categories")

        except requests.RequestException as e:
            print(f"Error fetching categories: {e}")


    def bind_mousewheel(self, widget, canvas):
        # Gắn sự kiện cuộn chuột khi chuột vào vùng canvas
        widget.bind(
            "<Enter>",
            lambda _: canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * int(e.delta / 120), "units")),
        )
        # Hủy sự kiện khi chuột rời khỏi vùng canvas
        widget.bind("<Leave>", lambda _: canvas.unbind_all("<MouseWheel>"))

    def display_categories(self, categories):
        # Xóa các widget cũ
        for widget in self.frame_bottom_left.winfo_children():
            widget.destroy()

        # Tạo Canvas cho phần bên trái
        self.canvas_left = tk.Canvas(self.frame_bottom_left, width=200, height=700, highlightthickness=0)
        self.scrollbar_left = tk.Scrollbar(self.frame_bottom_left, orient="vertical", command=self.canvas_left.yview)
        self.scrollable_frame_left = tk.Frame(self.canvas_left)

        # Cập nhật scrollregion mỗi khi có thay đổi
        self.scrollable_frame_left.bind(
            "<Configure>",
            lambda e: self.canvas_left.configure(scrollregion=self.canvas_left.bbox("all"))
        )
        
        # Đặt frame vào trong canvas
        self.canvas_left.create_window((0, 0), window=self.scrollable_frame_left, anchor="nw")
        self.canvas_left.configure(yscrollcommand=self.scrollbar_left.set)

        # Hiển thị canvas và scrollbar
        self.canvas_left.pack(side="left", fill="both", expand=True)
        self.scrollbar_left.pack(side="right", fill="y")

        # Gắn sự kiện cuộn chuột
        self.bind_mousewheel(self.frame_bottom_left, self.canvas_left)

    
        # Thêm các nút cho từng danh mục
        for category in categories:
            name = category['name']
            button = tk.Button(
                self.scrollable_frame_left,
                text=name,
                width=80,
                height=2,
                anchor="w",  # Căn trái
                justify="left",  # Căn chữ trong nút về bên trái
                command=lambda c=category: self.on_category_click(c),
            )
            button.pack(pady=2, padx=4)  # Loại bỏ padx để sát trái
            

        
    def on_filter_click(self):
        if hasattr(self, 'selected_category') and self.selected_category:
            # Dùng danh mục đã lưu để thực hiện lọc
            

            # Logic thực hiện lọc dựa trên self.selected_category
            
            self.on_category_click(self.selected_category)
            # Thêm hành động lọc ở đây
        else:
            print("No category selected for filtering.")


    def on_category_click(self, category):
        self.button_comnobox.grid_forget()
        self.button_comnobox1.grid(row=0, column=5, padx=30)
        self.selected_category = category # tạo 1 biến nhớ khi click
        print(f"Clicked category: {category['name']}")
        for widget in self.frame_bottom_right.winfo_children():
            widget.destroy()
        categoryId = category['categoryId']
        try:
            order_by_display = self.order_by_combobox.get()
            if order_by_display == "Mặc định":
                order_by = "normal"
            if order_by_display == "Số lượng bán":
                order_by = "quantitySold"
            elif order_by_display == "Giá":
                order_by = "price"
            elif order_by_display == "Số đánh giá":
                order_by = "reviewCount"
            elif order_by_display == "Số sao":
                order_by = "rating"
                
            type_order_display = self.type_combobox.get()
            if type_order_display == "Tăng dần":
                type_order = "asc"
            elif type_order_display == "Giảm dần":
                type_order = "desc"
            url = f"https://127.0.0.1:5000/api/product/tiki/category/{categoryId}/1"

            payload = json.dumps({
            "order_by": order_by,
            "type": type_order
            })
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("GET", url, headers=headers, data=payload, verify=False)
            page_data = json.loads(response.text)
            if page_data["success"]:
                self.display_search_history(page_data["data"])
                total_products = page_data["total_products"]
                max_page = page_data["max_page"]
            
            # Cập nhật giao diện
                self.update_total_quantity_display(total_products, max_page)
            else:
                print("Error fetching search history")
        except requests.RequestException as e:
            print(f"Error fetching search history: {e}")
        
        self.current_number = 1
        self.page = page_data["max_page"]
        self.btn_next = tk.Button(self.frame_page, text="Next", command=lambda: self.go_next(self.page, categoryId), padx=40)
        self.btn_next.grid(row=0, column=2, sticky="e")
        self.lable_page = tk.Label(self.frame_page, text=str(self.current_number), padx=500)
        self.lable_page.grid(row=0, column=1)
        # Tạo nút Previous và disable khi khởi động
        self.btn_prev = tk.Button(self.frame_page, text="Previous", command=lambda: self.go_previous(categoryId), padx=40,state="disabled")
        self.btn_prev.grid(row=0, column=0, sticky="w")

    def go_next(self, page, categoryId):
        if self.current_number < page:  # Giới hạn không vượt quá 100
            self.current_number += 1
            self.load_url_page(categoryId, self.current_number)
            self.lable_page.config(text=str(self.current_number))
        if self.current_number == 100:
            self.btn_next.config(state="disabled")
        self.btn_prev.config(state="normal")

    def go_previous(self, categoryId):
        if self.current_number > 1:  # Giới hạn không nhỏ hơn 1
            self.current_number -= 1
            self.load_url_page(categoryId, self.current_number)
            self.lable_page.config(text=str(self.current_number))
        if self.current_number == 1:
            self.btn_prev.config(state="disabled")
        self.btn_next.config(state="normal")
    def load_url_page(self, categoryId,x):
        for widget in self.frame_bottom_right.winfo_children():
            widget.destroy()
        try:
            order_by_display = self.order_by_combobox.get()
            if order_by_display == "Mặc định":
                order_by = "normal"
            elif order_by_display == "Số lượng bán":
                order_by = "quantitySold"
            elif order_by_display == "Giá":
                order_by = "price"
            elif order_by_display == "Số đánh giá":
                order_by = "reviewCount"
            elif order_by_display == "Số sao":
                order_by = "rating"
                
            type_order_display = self.type_combobox.get()
            if type_order_display == "Tăng dần":
                type_order = "asc"
            elif type_order_display == "Giảm dần":
                type_order = "desc"
            url = f"https://127.0.0.1:5000/api/product/tiki/category/{categoryId}/{x}"

            payload = json.dumps({
            "order_by": order_by,
            "type": type_order
            })
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("GET", url, headers=headers, data=payload, verify=False)
            page_data = json.loads(response.text)
            if page_data["success"]:
                self.display_search_history(page_data["data"])
            else:
                print("Error fetching search history")
        except requests.RequestException as e:
            print(f"Error fetching search history: {e}")

    def load_image_from_url(self, url, size=(100, 100)):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            img_data = response.content
            img = Image.open(io.BytesIO(img_data))
            img.thumbnail(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except (requests.exceptions.RequestException, IOError) as e:
            print(f"Error loading image: {e}")
            # Hiển thị hình ảnh mặc định
            placeholder = Image.new("RGB", size, (200, 200, 200))  # Xám nhạt
            return ImageTk.PhotoImage(placeholder)
#load sản phẩm ở màng hình chính
    def load_search_history(self, event = None):
        self.button_comnobox.grid_forget()
        self.button_comnobox1.grid_forget()
        if self.label_total_quantity: self.label_total_quantity.config(text='')
        if self.btn_next: self.btn_next.config(state="disabled")
        if self.btn_prev: self.btn_prev.config(state="disabled")
        if self.lable_page: self.lable_page.config(text='1')
        try:
            url = "https://127.0.0.1:5000/api/product/recommend_products_by_history"
            payload = {}
            headers = {}

            response = self.session.request("GET", url, headers=headers, data=payload, verify=False)
            history_data = json.loads(response.text)
            if history_data["success"]:
                self.url_load_search_history1()
                self.display_search_history(history_data["data"])
            else:
                print("Error fetching search history")
        except requests.RequestException as e:
            print(f"Error fetching search history: {e}")
        
    def display_search_history(self, history_products):
        # Xóa các widget cũ
        for widget in self.frame_bottom_right.winfo_children():
            widget.destroy()
        # Tạo canvas cho phần hiển thị sản phẩm
        self.canvas = tk.Canvas(self.frame_bottom_right, bg="white", width=1250, height=660)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Tạo thanh cuộn dọc cho canvas
        self.scrollbar_y = tk.Scrollbar(self.frame_bottom_right, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        # Tạo một frame để chứa các sản phẩm
        self.frame_products = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.frame_products, anchor="nw")

        # Thêm các sản phẩm vào trong frame
        for idx, product in enumerate(history_products):
            product_frame = tk.Frame(self.frame_products, bg="white", bd=2, relief="groove", width=150, height=200)
            product_frame.grid_propagate(False)

            # Tải và hiển thị hình ảnh sản phẩm
            img = self.load_image_from_url(product["imgURL"], size=(150, 150))
            img_label = tk.Label(product_frame, image=img, bg="white")
            img_label.image = img
            img_label.pack()

            # Tên sản phẩm
            product_name = product["name"][:60] + "..." if len(product["name"]) > 60 else product["name"]
            name_label = tk.Label(product_frame, text=product_name, font=("Arial", 10, "bold"), wraplength=150, bg="white")
            name_label.pack()

            origin_label = tk.Label(product_frame, text=f"{product["origin"]}", font=("Arial", 11, "bold"), fg="red", bg="white")
            origin_label.pack(side="bottom", anchor='w')

            quantitySold_label = tk.Label(product_frame, text=f"Đã bán: {product["quantitySold"]} ", font=("Arial", 10, "italic"), fg="black", bg="white")
            quantitySold_label.pack(side="bottom", anchor='w')
            # Giá và xuất xứ
            price_label = tk.Label(product_frame, text=f"{product["price"]} VND", font=("Arial", 12, "bold"), fg="red", bg="white")
            price_label.pack(side = 'bottom')

            # Giá và xuất xứ
            rating_label = tk.Label(product_frame, text=f"{product["rating"]} ★", font=("Arial", 10), fg="black", bg="white")
            rating_label.pack(side="bottom", anchor="w")

            row = idx // self.PRODUCTS_PER_ROW
            col = idx % self.PRODUCTS_PER_ROW
            product_frame.grid(row=row, column=col, padx=10, sticky="nsew")
            name_label.bind("<Button-1>", lambda event, origin=product['origin'], productId=product['productId']: self.show_product_details(origin, productId))
            img_label.bind("<Button-1>", lambda event, origin=product['origin'], productId=product['productId']: self.show_product_details(origin, productId))

        # Cập nhật scrollregion của canvas
        self.frame_products.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Gắn sự kiện cuộn chuột vào canvas
        self.bind_mousewheel(self.frame_bottom_right, self.canvas)

    
    def show_product_details(self, origin, productId):
        product_detail_window = ProductDetailById(self.session, origin, productId)
        product_detail_window.focus()
    
    #Phần tìm kiếm
    def theodoitryvan(self, text):  
        """Gửi yêu cầu theo dõi tìm kiếm đến API"""
        url = "https://127.0.0.1:5000/api/tracking/browse"
        payload = json.dumps({
            "browse": text
        })
        
        headers = {
            "Content-Type": "application/json" 
        }
        try:
            response = self.session.post(url, headers=headers, data=payload, verify=False)
            if response.status_code == 200:
                res_json = response.json()
                if res_json.get("success", False):
                    print("Thành công")
                                        
                else:
                    print("Thất bại")
            else:
                print(f"Lỗi HTTP {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Lỗi kết nối: {e}")
    def load_search(self):
        self.button_comnobox.grid(row=0, column=5, padx=30)#Hiện button
        self.button_comnobox1.grid_forget()
        text = self.timkiem.get()
        
        order_by_display = self.order_by_combobox.get()
        if order_by_display == "Mặc định":
            order_by = "normal"
        elif order_by_display == "Số lượng bán":
            order_by = "quantitySold"
        elif order_by_display == "Giá":
            order_by = "price"
        elif order_by_display == "Số đánh giá":
            order_by = "reviewCount"
        elif order_by_display == "Số sao":
            order_by = "rating"
            
        type_order_display = self.type_combobox.get()
        if type_order_display == "Tăng dần":
            type_order = "asc"
        elif type_order_display == "Giảm dần":
            type_order = "desc"
        if text:
            
            try:
                url = f"https://127.0.0.1:5000/api/product/query/{text}"

                payload = json.dumps({
                "order_by": order_by,
                "type": type_order
                })
                headers = {
                'Content-Type': 'application/json'
                }

                response = self.session.request("GET", url, headers=headers, data=payload, verify=False)
                search_data = json.loads(response.text)
                if search_data["success"]:
                    self.display_search_history(search_data["data"])
                    self.theodoitryvan(text)
                    new_data = self.url_load_search_history1()  # Gọi API lấy dữ liệu mới
                    if new_data:
                        self.data_list = [item["content"] for item in new_data["data"][:4]]  # Cập nhật self.data_list
                    self.update_labels()
                else:
                    print("Error fetching search history")
            except requests.RequestException as e:
                print(f"Error fetching search history: {e}")
    def combobox_product(self):
        self.order_by_options_display = ["Mặc định","Số lượng bán", "Giá", "Số đánh giá", "Số sao"]
        self.order_by_options = ["normal","quantitySold", "price", "reviewCount", "rating"]
        self.type_options_display = ["Tăng dần", "Giảm dần"] 
        self.type_options = ["asc", "desc"]
        
        # self.order_by_label = tk.Label(self.frame_combobox, text="Order By:")
        # self.order_by_label.grid(row=0, column=0, padx=10, sticky="e")
        
        self.order_by_combobox = ttk.Combobox(self.frame_combobox, values=self.order_by_options_display, state = "readonly")
        self.order_by_combobox.set(self.order_by_options_display[0])
        self.order_by_combobox.grid(row=0, column=1, padx=10, sticky="e")
        
        self.type_label = tk.Label(self.frame_combobox, text="Sắp xếp")
        self.type_label.grid(row=0, column=2, padx=10, sticky="e")
        
        self.type_combobox = ttk.Combobox(self.frame_combobox, values=self.type_options_display, state = "readonly")
        self.type_combobox.set(self.type_options_display[0])  # Mặc định là "Tăng dần"
        self.type_combobox.grid(row=0, column=3, padx=10, sticky="e") 
    def tk_image(self):
        self.img_original = Image.open(os.path.join(os.path.dirname(__file__), "image", "user.png"))  # Đường dẫn tới file ảnh
        self.img_resized = self.img_original.resize((50, 50))  # Thay đổi kích thước nếu cần
        self.img = ImageTk.PhotoImage(self.img_resized)
        return self.img  

    def update_total_quantity_display(self, total_products, trang):
        # Xóa widget hiện tại trong `frame_combobox` trước khi cập nhật
        for widget in self.frame_combobox1.winfo_children():
            widget.destroy()
        
        # Thêm thông tin tổng số sản phẩm
        self.label_total_quantity = tk.Label(self.frame_combobox1, text=f"Tổng số sản phẩm: {total_products}|| Số trang: {trang}", font=("Arial", 9))
        self.label_total_quantity.grid(row=0, sticky='w')

    def open_login_window(self):
        from account import Account
        Account(self, self.session, self.username)
        
    def mainlop(self):
        pass
