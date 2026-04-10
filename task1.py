import tkinter as tk
from PIL import Image, ImageTk
from gpiozero import Button

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
        "back": "Back",
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
        "back": "Takaisin",
        "correct": "OIKEIN!"
    }
}


def show_task1(root, clear_screen, go_to_menu):
    root.cleanup_gpio()
    clear_screen()
    lang = getattr(root, "language", "en")
    t = TEXTS[lang]
    root.update_idletasks()

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

    # -------------------------------
    # Title
    # -------------------------------
    tk.Label(
        root,
        text=t["title"],
        font=("Arial", 18, "bold"),
        bg="white"
    ).pack(pady=10)

    # -------------------------------

    # -------------------------------
    content_frame = tk.Frame(root, bg="white", width=banner_width)
    content_frame.pack(pady=10)

    left_frame = tk.Frame(content_frame, bg="white")
    left_frame.pack(side="left", anchor="n")

    spacer = tk.Frame(content_frame, bg="white", width=40)
    spacer.pack(side="left")

    right_frame = tk.Frame(content_frame, bg="white")
    right_frame.pack(side="left", anchor="n")

    # -------------------------------
    # Instructions
    # -------------------------------
    instructions = t["instructions"]

    text_width = int(banner_width * 0.5)

    for line in instructions:
        tk.Label(
            left_frame,
            text=line,
            font=("Arial", 14),
            bg="white",
            anchor="w",
            justify="left",
            wraplength=text_width
        ).pack(anchor="w", pady=4)

    tk.Label(
        left_frame,
        text=t["hint"],
        font=("Arial", 12, "italic"),
        fg="gray",
        bg="white",
        anchor="w",
        justify="left",
        wraplength=text_width
    ).pack(anchor="w", pady=15)

    # -------------------------------
    # Box image
    # -------------------------------
    box_img = Image.open("box.png")

    box_target_width = int(banner_width * 0.4)
    bw2, bh2 = box_img.size
    box_target_height = int(bh2 * (box_target_width / bw2))

    box_img = box_img.resize((box_target_width, box_target_height))
    box_photo = ImageTk.PhotoImage(box_img)

    box_label = tk.Label(right_frame, image=box_photo, bg="white")
    box_label.image = box_photo
    box_label.pack()

    # -------------------------------
    # Back button
    # -------------------------------
    tk.Button(
        root,
        text=t["back"],
        width=10,
        height=2,
        command=go_to_menu
    ).pack(pady=20)

    # -------------------------------
    def show_popup(root):
        popup = tk.Toplevel(root)
        popup.overrideredirect(True)

        width = 320
        height = 200

        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        popup.geometry(f"{width}x{height}+{x}+{y}")
        popup.configure(bg="white")

        canvas = tk.Canvas(popup, width=width, height=height,
                           bg="white", highlightthickness=0)
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
            (width // 2) - 30, height // 2,
            text=t["correct"],
            font=("Arial", 20, "bold"),
            fill="white"
        )

        popup.after(1000, popup.destroy)

    def on_task1_pressed():
        print("GP 17 pressed")
        root.after(0, lambda: show_popup(root))

    btn_task1 = Button(17, pull_up=True)

    btn_task1.when_pressed = on_task1_pressed

    root.btn_task1 = btn_task1