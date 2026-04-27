import tkinter as tk
from gpiozero import Button
from PIL import Image, ImageTk
from task1 import show_task1
from game import show_game

TEXTS = {
    "en": {
        "title": "Choose Task",
        "task1": "Task 1",
        "task2": "Task 2",
        "task3": "Task 3",
        "game": "Game",
        "back": "Back"
    },
    "fi": {
        "title": "Valitse tehtävä",
        "task1": "Tehtävä 1",
        "task2": "Tehtävä 2",
        "task3": "Tehtävä 3",
        "game": "Peli",
        "back": "Takaisin"
    }
}


def show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3):
    root.screen = "menu"
    root.cleanup_gpio()
    clear_screen()
    lang = getattr(root, "language", "en")
    t = TEXTS[lang]

    # Screen size
    screen_width = root.winfo_width()
    if screen_width < 100:
        screen_width = root.winfo_screenwidth()

    # -------------------------------
    # Banner
    # -------------------------------
    banner_img = Image.open("task_banner.png")

    banner_width = int(screen_width * 0.5)

    bw, bh = banner_img.size
    scale = banner_width / bw
    height_boost = 1.2

    banner_height = int(bh * scale * height_boost)

    banner_img = banner_img.resize((banner_width, banner_height))
    banner_photo = ImageTk.PhotoImage(banner_img)

    banner_label = tk.Label(root, image=banner_photo, bg="white")
    banner_label.image = banner_photo
    banner_label.pack(pady=10)

    # ---- Title ----
    tk.Label(root, text=t["title"],
             font=("Arial", 20, "bold"),
             bg="white").pack(pady=15)

    # ---- Soft button: Task 1----
    tk.Button(root, text=t["task1"],
              font=("Arial", 16), width=15, height=2,
              command=lambda: show_task1(
                  root,
                  clear_screen,
                  lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
              )
              ).pack(pady=10)
    tk.Button(root, text=t["task2"],
              font=("Arial", 16), width=15, height=2,
              command=lambda: show_task2(
                  root,
                  clear_screen,
                  lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
              )
              ).pack(pady=10)

    tk.Button(root, text=t["task3"],
              font=("Arial", 16), width=15, height=2,
              command=lambda: show_task3(
                  root,
                  clear_screen,
                  lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
              )
              ).pack(pady=10)

    tk.Button(root, text=t["game"],
              font=("Arial", 16), width=15, height=2,
              command=lambda: show_game(
                  root,
                  clear_screen,
                  lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
              )
              ).pack(pady=10)

    tk.Button(root, text=t["back"],
              font=("Arial", 12), width=10, height=2,
              command=lambda: (root.cleanup_gpio(), main_menu())).pack(pady=20)

    # ---- hardware button: Task 1 ----
    # btn1 = Button(2, pull_up=True, bounce_time=0.3)
    # btn1.when_pressed = lambda: root.after(
    #     0, lambda: show_task1(
    #         root,
    #         clear_screen,
    #         lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
    #     )
    # )

    # root.btn1 = btn1

    # btn2 = Button(3, pull_up=True, bounce_time=0.3)
    # btn2.when_pressed = lambda: root.after(
    #     0, lambda: show_task2(
    #         root,
    #         clear_screen,
    #         lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
    #     )
    # )
    # root.btn2 = btn2

    # btn3 = Button(4, pull_up=True, bounce_time=0.3)
    # btn3.when_pressed = lambda: root.after(
    #     0, lambda: show_task3(
    #         root,
    #         clear_screen,
    #         lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
    #     )
    # )
    # root.btn3 = btn3

    # btn_back = Button(6, pull_up=True)
    # btn_back.when_pressed = lambda: root.after(
    #     0, lambda: (root.cleanup_gpio(), main_menu())
    # )

    # root.btn_back = btn_back
