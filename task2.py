import tkinter as tk
from PIL import Image, ImageTk

def show_task2(root, clear_screen, main_menu):
    clear_screen()

    # ---- Banner ----
    img = Image.open("task_banner.png")
    img = img.resize((900, 300))
    banner = ImageTk.PhotoImage(img)

    banner_label = tk.Label(root, image=banner, bg="white")
    banner_label.image = banner
    banner_label.pack(pady=5)

    # ---- Title ----
    title = tk.Label(root, text="TASK 2 : CONNECT SENSOR",
                     font=("Arial", 18, "bold"), bg="white")
    title.pack(pady=10)

    tk.Label(root, text="Under Construction 🚧",
             font=("Arial", 20), bg="white").pack(pady=50)

    tk.Button(root, text="Back", width=10, height=2,
              command=main_menu).pack(pady=10)
