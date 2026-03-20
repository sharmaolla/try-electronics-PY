import tkinter as tk
from gpiozero import Button
from PIL import Image, ImageTk
from task1 import show_task1


def show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3):
    root.cleanup_gpio()
    clear_screen()

    # ---- Banner ----
    img = Image.open("task_banner.png")
    img = img.resize((900, 220))
    banner = ImageTk.PhotoImage(img)

    banner_label = tk.Label(root, image=banner, bg="white")
    banner_label.image = banner
    banner_label.pack(pady=5)

    # ---- Title ----
    tk.Label(root, text="Choose Task",
             font=("Arial", 20, "bold"),
             bg="white").pack(pady=15)

    # ---- Soft button: Task 1 only ----
    tk.Button(root, text="Task 1",
              font=("Arial", 16), width=15, height=2,
              command=lambda: show_task1(
                  root,
                  clear_screen,
                  lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
              )
              ).pack(pady=10)
    tk.Button(root, text="Task 2",
              font=("Arial", 16), width=15, height=2,
              command=lambda: show_task2(
                  root,
                  clear_screen,
                  lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
              )
              ).pack(pady=10)

    tk.Button(root, text="Task 3",
              font=("Arial", 16), width=15, height=2,
              command=lambda: show_task3(
                  root,
                  clear_screen,
                  lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
              )
              ).pack(pady=10)

    tk.Button(root, text="Back",
              font=("Arial", 12), width=10, height=2,
              command=main_menu).pack(pady=20)

    # ---- Real hardware button: Task 1 only ----
    btn1 = Button(9, pull_up=True)
    btn1.when_pressed = lambda: root.after(
        0, lambda: show_task1(
            root,
            clear_screen,
            lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
        )
    )

    root.btn1 = btn1

    btn2 = Button(6, pull_up=True)
    btn2.when_pressed = lambda: root.after(
        0, lambda: show_task2(
            root,
            clear_screen,
            lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
        )
    )
    root.btn2 = btn2

    btn3 = Button(19, pull_up=True)
    btn3.when_pressed = lambda: root.after(
        0, lambda: show_task3(
            root,
            clear_screen,
            lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
        )
    )
    root.btn3 = btn3
