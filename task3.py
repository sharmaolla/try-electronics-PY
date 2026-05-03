import tkinter as tk
from PIL import Image, ImageTk
from gpiozero import PWMLED, Button

GREY_BG = "#EEEEEE"

TEXTS = {
    "en": {
        "title": "Task 3. Connect the encoder and change LED3 brightness",
        "instructions": [
            "1. Find the ENCODER in the box (see image)",
            "2. Find the suitable connection point for the encoder on the green PCB board",
            "3. Connect the encoder cable to this connection point",
            "4. Turn the encoder knob left and right",
            "5. If connected correctly, LED3 brightness will change"
        ],
        "hint": "Hint: the encoder has a 4-wire cable",
        "brightness": "Brightness Level",
        "main": "Main",
        "task1": "Task 1",
        "task2": "Task 2",
    },
    "fi": {
        "title": "Tehtävä 3. Kytke encoder ja muuta LED3:n kirkkautta",
        "instructions": [
            "1. Etsi ENCODER laatikosta (katso kuva)",
            "2. Etsi encoderille sopiva liitäntäkohta vihreältä PCB-levyltä",
            "3. Kytke encoderin kaapeli tähän liitäntäkohtaan",
            "4. Käännä encoderin nuppia vasemmalle ja oikealle",
            "5. Jos kytkentä on oikein, LED3:n kirkkaus muuttuu"
        ],
        "hint": "Vinkki: encoderissa on 4-johtiminen kaapeli",
        "brightness": "Kirkkaustaso",
        "main": "Etusivu",
        "task1": "Tehtävä 1",
        "task2": "Tehtävä 2",
    }
}


def show_task3(root, clear_screen, go_to_menu):
    root.screen = "task3"
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
    # Title
    # -------------------------------
    tk.Label(
        main_frame,
        text=t["title"],
        font=font(18, bold=True),
        bg=GREY_BG

    ).pack(pady=(int(4 * scale), int(6 * scale)))

    # -------------------------------
    # Content
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
    # Brightness label
    # -------------------------------
    tk.Label(
        main_frame,
        text=t["brightness"],
        font=font(14, bold=True),
        bg="white"
    ).pack(pady=(int(4 * scale), int(3 * scale)))

    # -------------------------------
    # Brightness bar
    # -------------------------------
    bar_width_total = max(220, int(screen_width * 0.30))
    bar_height = max(24, int(30 * scale))

    bar_canvas = tk.Canvas(
        main_frame,
        width=bar_width_total,
        height=bar_height,
        bg="white",
        highlightthickness=0
    )
    bar_canvas.pack(pady=int(3 * scale))

    x1 = int(bar_width_total * 0.07)
    x2 = int(bar_width_total * 0.93)
    y1 = int(bar_height * 0.2)
    y2 = int(bar_height * 0.8)

    bar_canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2)
    fill_bar = bar_canvas.create_rectangle(x1, y1, x1, y2, fill="skyblue", outline="")

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
        command=lambda: (root.cleanup_gpio(), root.go_main())
    ).pack(side="left", padx=int(8 * scale))

    tk.Button(
        nav_frame,
        text=t["task1"],
        font=font(12),
        width=btn_width,
        height=btn_height,
        command=lambda: (root.cleanup_gpio(), root.go_task1())

    ).pack(side="left", padx=int(8 * scale))

    tk.Button(
        nav_frame,
        text=t["task2"],
        font=font(12),
        width=btn_width,
        height=btn_height,
        command=lambda: (root.cleanup_gpio(), root.go_task2())

    ).pack(side="left", padx=int(8 * scale))

    # -------------------------------
    # GPIO
    # -------------------------------
    led_task3 = PWMLED(12)
    led_task3.value = 0
    root.led_task3 = led_task3

    sig_a = Button(27, pull_up=True)
    sig_b = Button(17, pull_up=True)

    root.sig_a = sig_a
    root.sig_b = sig_b

    brightness = [0]

    def adjust_brightness():
        if sig_b.is_pressed:
            brightness[0] = min(1, brightness[0] + 0.05)
        else:
            brightness[0] = max(0, brightness[0] - 0.05)

        led_task3.value = brightness[0]

        bar_width = x1 + ((x2 - x1) * brightness[0])
        bar_canvas.coords(fill_bar, x1, y1, bar_width, y2)

        print("Brightness:", brightness[0])

    sig_a.when_pressed = adjust_brightness