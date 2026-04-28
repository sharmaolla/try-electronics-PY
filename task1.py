import tkinter as tk
from PIL import Image, ImageTk
from gpiozero import Button

GREY_BG = "#EEEEEE"



TEXTS = {
    "en": {
        "title": "Task 1. Connect button",
        "instructions": [
            "1. Find BUTTON connection point and BUTTON_1 on the green PCB board",
            "2. Take two jumper wires from the box (refer image)",
            "3. Connect BUTTON_1 and BUTTON connection points with wires",
            "4. Press the button"
        ],
        "hint": "Hint: if you press the button and nothing happens, check wiring and connections",
        "main": "Main",
        "task2": "Task 2",
        "task3": "Task 3",
        "correct": "CORRECT!"
    },
    "fi": {
        "title": "Tehtävä 1. Yhdistä painike",
        "instructions": [
            "1. Etsi BUTTON-liitäntäkohta ja BUTTON_1 vihreältä PCB-levyltä",
            "2. Ota kaksi hyppylankaa laatikosta (katso kuva)",
            "3. Yhdistä BUTTON_1 ja BUTTON-liitäntäkohta johdoilla",
            "4. Paina painiketta"
        ],
        "hint": "Vinkki: Jos painat painiketta eikä mitään tapahdu, tarkista johdot ja liitännät",
        "main": "Etusivu",
        "task2": "Tehtävä 2",
        "task3": "Tehtävä 3",
        "correct": "OIKEIN!"
    }
}


def show_task1(root, clear_screen, go_to_menu):
    root.screen = "task1"
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

    def font(size, bold=False, italic=False):
        real_size = max(9, int(size * scale))

        style = []
        if bold:
            style.append("bold")
        if italic:
            style.append("italic")

        if style:
            return ("Arial", real_size, " ".join(style))

        return ("Arial", real_size)

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(expand=True, fill="both")

    # -------------------------------
    # Banner - same style as menu
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
    # Title
    # -------------------------------
    tk.Label(
        main_frame,
        text=t["title"],
        font=font(18, bold=True),
        bg=GREY_BG
    ).pack(pady=(int(4 * scale), int(6 * scale)))

   # -------------------------------
    # Content aligned with banner
    # -------------------------------
    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(pady=int(5 * scale), padx=int(screen_width * 0.25))

    text_width = int(banner_width * 0.50)

    left_frame = tk.Frame(content_frame, bg="white")
    left_frame.pack(side="left", anchor="n", padx=(0, int(banner_width * 0.03)))

    right_frame = tk.Frame(content_frame, bg="white")
    right_frame.pack(side="left", anchor="n")

    for line in t["instructions"]:
        tk.Label(
            left_frame,
            text=line,
            font=font(14),
            bg="white",
            anchor="w",
            justify="left",
            wraplength=text_width
        ).pack(anchor="w", pady=int(3 * scale))

    tk.Label(
        left_frame,
        text=t["hint"],
        font=font(12, italic=True),
        fg="gray",
        bg="white",
        anchor="w",
        justify="left",
        wraplength=text_width
    ).pack(anchor="w", pady=int(12 * scale))

    # -------------------------------
    # Box image
    # -------------------------------
    box_img = Image.open("box.png")

    max_box_height = int(screen_height * 0.40)

    bw2, bh2 = box_img.size
    box_target_width = int(banner_width * 0.52)

    box_scale = box_target_width / bw2
    box_target_height = int(bh2 * box_scale)

    if box_target_height > max_box_height:
        box_scale = max_box_height / bh2
        box_target_width = int(bw2 * box_scale)
        box_target_height = max_box_height

    box_img = box_img.resize((box_target_width, box_target_height), Image.LANCZOS)
    box_photo = ImageTk.PhotoImage(box_img)

    box_label = tk.Label(right_frame, image=box_photo, bg="white")
    box_label.image = box_photo
    box_label.pack()

    # -------------------------------
    # Buttons
    # -------------------------------
    nav_frame = tk.Frame(main_frame, bg="white")
    nav_frame.pack(pady=int(14 * scale))

    btn_width = max(8, int(10 * scale))
    btn_height = 2 if screen_height > 500 else 1

    tk.Button(
        nav_frame,
        text=t["main"],
        font=font(12),
        width=btn_width,
        height=btn_height,
        bg="skyblue",
        command=root.go_main
    ).pack(side="left", padx=int(8 * scale))

    tk.Button(
        nav_frame,
        text=t["task2"],
        font=font(12),
        width=btn_width,
        height=btn_height,
        command=root.go_task2
    ).pack(side="left", padx=int(8 * scale))

    tk.Button(
        nav_frame,
        text=t["task3"],
        font=font(12),
        width=btn_width,
        height=btn_height,
        command=root.go_task3
    ).pack(side="left", padx=int(8 * scale))

    # -------------------------------
    # Popup
    # -------------------------------
    def show_popup(root):
        popup = tk.Toplevel(root)
        popup.overrideredirect(True)

        width = 320
        height = 200

        screen_w = popup.winfo_screenwidth()
        screen_h = popup.winfo_screenheight()

        x = int((screen_w / 2) - (width / 2))
        y = int((screen_h / 2) - (height / 2))

        popup.geometry(f"{width}x{height}+{x}+{y}")
        popup.configure(bg="white")

        canvas = tk.Canvas(
            popup,
            width=width,
            height=height,
            bg="white",
            highlightthickness=0
        )
        canvas.pack()

        points = [
            40, 100, 70, 80, 50, 50, 95, 55, 110, 25,
            145, 45, 185, 20, 180, 55, 230, 35, 205, 65,
            255, 70, 220, 90, 245, 120, 200, 110, 210, 145,
            165, 130, 150, 165, 120, 145, 85, 160, 80, 125
        ]

        canvas.create_polygon(
            points,
            fill="#4FC3F7",
            outline="#08394a",
            width=2
        )

        canvas.create_text(
            (width // 2) - 30,
            height // 2,
            text=t["correct"],
            font=("Arial", 20, "bold"),
            fill="white"
        )

        popup.after(1000, popup.destroy)

    def on_task1_pressed():
        print("GP 14 pressed")
        root.after(0, lambda: show_popup(root))

    btn_task1 = Button(14, pull_up=True)
    btn_task1.when_pressed = on_task1_pressed
    root.btn_task1 = btn_task1


