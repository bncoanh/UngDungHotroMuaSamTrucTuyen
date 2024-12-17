import tkinter as tk
from tkinter import messagebox
import requests
import json
from PIL import ImageTk, Image
from urllib.request import urlopen
import webbrowser

class ProductDetailById(tk.Toplevel):
    def __init__(self, session, origin, productId):
        # self.title('Product Detail By Id')
        super().__init__()
        self.state("zoomed")
        self.session = session
        self.origin = origin
        self.productId = productId

        def openInBrowser() -> None:
            url = "https://127.0.0.1:5000/api/tracking/product/{}/{}".format(self.origin, self.productId)

            payload = {}
            headers = {}

            response = self.session.request("POST", url, headers=headers, data=payload, verify=False)
            
            webbrowser.open(data['link'])

        def suggestedProduct():
            url = "https://127.0.0.1:5000/api/product/recommend_products_by_product_id/{}/{}".format(self.origin, self.productId)

            payload = {}
            headers = {}

            response = self.session.request("GET", url, headers=headers, data=payload, verify=False)
            res_json = json.loads(response.text)
            data = res_json['data']

            for next_product in data:
                frame = tk.Frame(master=self.frame2, height=55, width=300)
                frame.pack(padx=5, pady=5, fill=tk.X)
                label_image = tk.Label(master=frame)
                frame_info = tk.Frame(master=frame)
                label_name = tk.Label(master=frame_info)
                label_price = tk.Label(master=frame_info)
                button_product = tk.Button(master=frame_info, text='Xem sản phẩm',
                                           command=lambda origin=next_product['origin'], productId=next_product['productId']: ProductDetailById(self.session, origin, productId))

                label_image.pack(side=tk.LEFT, padx=5)
                frame_info.pack(side=tk.LEFT, padx=5)
                label_name.pack(padx=5)
                label_price.pack(padx=5, side=tk.LEFT)
                button_product.pack(padx=5, side=tk.LEFT)

                image = Image.open(urlopen(next_product['imgURL']))
                resized_image = image.resize((45, 45))

                photo = ImageTk.PhotoImage(resized_image)

                # Hiển thị ảnh trên label
                label_image.config(image=photo)
                label_name.image = photo
                label_name.config(text=next_product['name'], justify='left')
                label_price.config(text=next_product['price'], justify='left')

        self.frame1 = tk.Frame(self, width=900)
        self.frame2 = tk.Frame(self, width=600)
        self.sub_frame = tk.Frame(self.frame1)
        self.sub_frame2 = tk.Frame(self.frame1)
        self.label_name = tk.Label(self.frame1)
        self.label_image = tk.Label(self.sub_frame2)
        self.label_price = tk.Label(self.sub_frame)
        self.button_origin = tk.Button(self.sub_frame, text='Đến nơi bán', command=openInBrowser)
        self.label_information1 = tk.Label(self.sub_frame2)

        url = "https://127.0.0.1:5000/api/product/{}/product/{}".format(self.origin, self.productId)

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)

        res_json = json.loads(response.text)
        data = res_json['data']

        self.title(f'{data['name']}')
        self.frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.frame2.pack(fill=tk.BOTH, side=tk.LEFT)
        self.frame1.rowconfigure([0, 1, 2], weight=1)
        self.frame1.columnconfigure([0], weight=1)
        self.label_name.grid(row=0, column=0, pady=(10, 0), padx=15, sticky='w')

        self.sub_frame.grid(row=2, column=0, sticky='nw')
        self.sub_frame2.grid(row=1, column=0, padx=15, sticky='nw')
        self.label_image.pack(side=tk.LEFT, padx=(15, 30))
        self.label_price.pack(side=tk.LEFT, padx=(15, 30))
        self.button_origin.pack(side=tk.LEFT)
        self.label_information1.pack(side=tk.LEFT, padx=(15, 30))

        image_url = data['imgURL']
        with urlopen(image_url) as u:
            raw_data = u.read()
        photo = ImageTk.PhotoImage(data=raw_data, size=(300, 300))

        # if res_json['success'] == True:
        self.label_name.config(text=data['name'], font=("Arial", 14))

        self.label_image.config(image=photo)
        self.label_image.image = photo

        self.label_price.config(text=data['price'] + 'đ', fg='red', font=("Arial", 14))
        review = data['reviewSummary']
        review = review.split('<br>')

        information1 = ('Tên hãng: {}\nSố lượng bán: {}\n'
                        'Tỷ lệ đánh giá: {}\nNơi bán: {}\n'
                        'Số lượng đánh giá: {}').format(data['brandName'], data['quantitySold'], data['rating'],
                                                        data['sellerName'], data['reviewCount'])

        self.label_information1.config(text=information1, font=("Arial", 14), justify='left', pady=10)

        # else:
        #     self.label_name.config(text='Không tìm thấy sản phẩm')

        label_suggestion = tk.Label(master=self.frame2, text='Các sản phẩm liên quan',
                                    font=("Arial", 14), justify='left')
        label_suggestion.pack(pady=5)

        suggestedProduct()
# a = ProductDetailById()
# a.gui()
