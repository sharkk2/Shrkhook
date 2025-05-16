import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import ImageTk, Image
from io import BytesIO
import config


# i'd literally do anything but use files
ico = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xc8\x00\x00\x00\xc8\x01\x00\x00\x00\x00\x85#\x933\x00\x00\x00\xfaIDATx\x9c\xed\x97\xcb\n\x840\x10\x04\xab\xc5\xff\xff\xe5\xde\xc3L\xa2\x0b\xeb\x82QL\x02\xe6\xe4\xd0\x97j\xe6\xa9\xcc\xc1[\x8e\x84WyPYA\xf1e\x19\xb9F\x03\xb05\xfa\xc1\x00\xc2a%\xa3\x01\xd8Z\xfd\xa0t\x11\x8e2\xea\xcfvQ\x11\xf2o\xe5)\x82\xbb\x15K\x9d\t.++d\xb1\x01\xb2\xb6\xa8?[\xab\x9f\x92\x94\xda>\x83\xb0\xb5(\xbb\x96\xd1\x96\xa8'\t\xee\xdf?\xceJ\xb3(#[\xb3\xee\x9f%l\x18G\xa5\xd9\xc6\x92\x07akS\x84\x90\xc3S\x9d\x08\x83\xb0\x9dWdc\x95\xb3\xc08&\xc3\x10l\xad\x8a\xb2w\x8a\xab\x91\xd8N)\xfb\xf9f\x14\x89\xd2\xd4\xf7h\xbd\xa8\x89j\x93a\xday\x10?\t\xd4D):i\xday\xbd\xbb\xafc\x03\xe1\xf4\xd4\x9f\xad\xd9O\xbc\xf2\xcb\xe0\xb8\xb4\xfb\xb3]\xf4S\x8aO3\xef\x9f\xaf\xfb:\xadx\x10\xb6\x16\x05\x1739\xdf\xb0\xc1\xd8\xfd\xd9.\xee\x9fN\x04\xaf\xf2O\xf9\x00)\xbbW\x8d\xcf:\x1fZ\x00\x00\x00\x00IEND\xaeB`\x82"


def generate_qr():
    data = entry.get()
    if not data.strip():
        messagebox.showerror("Error", "Please enter text or a URL.")
        return

    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png")],
        title="Save QR Code As"
    )

    if img_path:
        img.save(img_path)
        show_qr(img)

def show_qr(img):
    img = img.resize((200, 200))
    tk_img = ImageTk.PhotoImage(img)
    qr_label.config(image=tk_img)
    qr_label.image = tk_img 
    
    
def start():     
  root = tk.Tk()
  root.title("Fast QRCode")
  root.geometry("400x400")
  root.configure(bg="#f0f0f0")
  image = Image.open(BytesIO(ico))
  icon = ImageTk.PhotoImage(image)
  root.iconphoto(False, icon)
  title = tk.Label(root, text="Fast QRCode", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
  title.pack(pady=10)
  
  global entry
  entry = tk.Entry(root, font=("Helvetica", 12), width=30)
  entry.pack(pady=10)
  gen_button = tk.Button(root, text="Generate QR Code", font=("Helvetica", 12), command=generate_qr)
  gen_button.pack(pady=10)
  global qr_label
  qr_label = tk.Label(root, bg="#f0f0f0")
  qr_label.pack(pady=10)
  verlabel = tk.Label(root, text={config.version.replace(" NOSOCKET", "")}, font=("Helvetica", 8), bg="#f0f0f0", fg="#888888")
  verlabel.place(relx=1.0, rely=1.0, anchor="se", x=-5, y=-5)
  root.mainloop()
  