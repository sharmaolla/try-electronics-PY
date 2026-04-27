from gpiozero import Button
from PIL import Image, ImageTk
import tkinter as tk
from task1 import show_task1
from task2 import show_task2
from task3 import show_task3
from menu import show_task_menu


def cleanup_gpio():
    for name in ["btn2", "btn3", "sig_a", "sig_b", "btn_task1", "sensor", "led_task2", "led_task3", "task2_device"]:
        if hasattr(root, name):
            try:
                getattr(root, name).close()
            except:
                pass
            delattr(root, name)


def setup_menu_buttons():
    if not hasattr(root, "button_task1"):
        root.button_task1 = Button(2, pull_up=True)
        root.button_task1.when_pressed = lambda: root.after(
            0, lambda: show_task1(root, clear_screen, main_menu)
        )

    if not hasattr(root, "button_task2"):
        root.button_task2 = Button(3, pull_up=True)
        root.button_task2.when_pressed = lambda: root.after(
            0, lambda: show_task2(root, clear_screen, main_menu)
        )

    if not hasattr(root, "button_task3"):
        root.button_task3 = Button(4, pull_up=True)
        root.button_task3.when_pressed = lambda: root.after(
            0, lambda: show_task3(root, clear_screen, main_menu)
        )


def close_menu_buttons():
    for name in ["button_task1", "button_task2", "button_task3"]:
        if hasattr(root, name):
            try:
                getattr(root, name).close()
            except:
                pass
            delattr(root, name)


def english_selected():
    setup_menu_buttons()
    root.language = "en"
    show_task_menu(root, clear_screen, main_menu,
                   show_task1, show_task2, show_task3)


def finnish_selected():
    setup_menu_buttons()
    root.language = "fi"
    show_task_menu(root, clear_screen, main_menu,
                   show_task1, show_task2, show_task3)


button_english = Button(5, pull_up=True)
button_suomi = Button(22, pull_up=True)
button_back = Button(6, pull_up=True)

button_english.when_pressed = lambda: root.after(
    0, lambda: english_selected() if root.screen == "main" else None
)

button_suomi.when_pressed = lambda: root.after(
    0, lambda: finnish_selected() if root.screen == "main" else None
)
button_back.when_pressed = lambda: root.after(0, main_menu)


def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()


def show_under_construction():
    clear_screen()
    tk.Label(root, text="Under Construction",
             font=("Arial", 20), bg="white").pack(pady=50)

    tk.Button(root, text="Back",
              width=10, height=2,
              command=main_menu
              ).pack(pady=10)


def main_menu():
    root.screen = "main"
    close_menu_buttons()
    clear_screen()

    img = Image.open("banner.png")
    img = img.resize((800, 500))
    banner = ImageTk.PhotoImage(img)

    banner_label = tk.Label(root, image=banner, bg="white")
    banner_label.image = banner
    banner_label.pack(pady=10)

    tk.Label(root, text="Choose Language",
             font=("Arial", 16, "bold"), bg="white").pack(pady=20)

    tk.Button(root, text="English",
              font=("Arial", 18), width=15, height=2,
              command=english_selected
              ).pack(pady=10)

    tk.Button(root, text="Suomi",
              font=("Arial", 18), width=15, height=2,
              command=finnish_selected
              ).pack(pady=10)


root = tk.Tk()
root.cleanup_gpio = cleanup_gpio
root.go_main = main_menu
root.go_task1 = lambda: show_task1(root, clear_screen, main_menu)
root.go_task2 = lambda: show_task2(root, clear_screen, main_menu)
root.go_task3 = lambda: show_task3(root, clear_screen, main_menu)

root.title("Electronics Game")
root.geometry("1000x600")
root.configure(bg="white")

main_menu()
root.mainloop()