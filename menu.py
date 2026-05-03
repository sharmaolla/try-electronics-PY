import tkinter as tk
from PIL import Image, ImageTk
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

    root.update_idletasks()

    screen_width = root.winfo_width()
    screen_height = root.winfo_height()

    if screen_width < 100:
        screen_width = root.winfo_screenwidth()

    if screen_height < 100:
        screen_height = root.winfo_screenheight()

    scale = min(screen_width / 1000, screen_height / 600)
    scale = max(0.55, min(scale, 1.25))

    def font(size, bold=False):
        real_size = max(10, int(size * scale))
        if bold:
            return ("Arial", real_size, "bold")
        return ("Arial", real_size)

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(expand=True, fill="both")

    # -------------------------------
    # Banner
    # -------------------------------
    banner_img = Image.open("task_banner.png")

    banner_width = int(screen_width * 0.50)

    bw, bh = banner_img.size
    img_scale = banner_width / bw
    banner_height = int(bh * img_scale * 1.25)

    max_banner_height = int(screen_height * 0.4)

    if banner_height > max_banner_height:
        img_scale = max_banner_height / bh
        banner_width = int(bw * img_scale)
        banner_height = max_banner_height

    banner_img = banner_img.resize((banner_width, banner_height), Image.LANCZOS)
    banner_photo = ImageTk.PhotoImage(banner_img)

    banner_label = tk.Label(main_frame, image=banner_photo, bg="white")
    banner_label.image = banner_photo
    banner_label.pack(pady=(int(6 * scale), int(4 * scale)))


    # -------------------------------
    # Buttons
    # -------------------------------
    buttons_frame = tk.Frame(main_frame, bg="white")
    buttons_frame.pack(expand=True)

    tk.Label(
        buttons_frame,
        text=t["title"],
        font=font(20, bold=True),
        bg="white"
    ).pack(pady=(0, int(10 * scale)))


    btn_width = max(12, int(15 * scale))
    btn_height = 2 if screen_height >= 520 else 1
    btn_pady = max(3, int(6 * scale))

    def menu_button(text, command, size=16):
        tk.Button(
            buttons_frame,
            text=text,
            font=font(size),
            width=btn_width,
            height=btn_height,
            command=command
        ).pack(pady=btn_pady)

    menu_button(
        t["task1"],
        lambda: show_task1(
            root,
            clear_screen,
            lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
        )
    )

    menu_button(
        t["task2"],
        lambda: show_task2(
            root,
            clear_screen,
            lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
        )
    )

    menu_button(
        t["task3"],
        lambda: show_task3(
            root,
            clear_screen,
            lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
        )
    )

    menu_button(
        t["game"],
        lambda: show_game(
            root,
            clear_screen,
            lambda: show_task_menu(root, clear_screen, main_menu, show_task1, show_task2, show_task3)
        )
    )

    tk.Button(
        buttons_frame,
        text=t["back"],
        font=font(12),
        width=max(9, int(10 * scale)),
        height=btn_height,
        command=lambda: (root.cleanup_gpio(), main_menu())
    ).pack(pady=(btn_pady, int(10 * scale)))