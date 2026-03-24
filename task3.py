import tkinter as tk
from PIL import Image, ImageTk
from gpiozero import PWMLED, Button


def show_task3(root, clear_screen, go_to_menu):
    root.cleanup_gpio()
    clear_screen()
    root.update_idletasks()

    # Screen size
    screen_width = root.winfo_width()
    if screen_width < 100:
        screen_width = root.winfo_screenwidth()

    # -------------------------------
    # Banner (dynamic size)
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
    # Title (center)
    # -------------------------------
    tk.Label(
        root,
        text="TASK 3: CONNECT ENCODER AND CHANGE LED BRIGHTNESS",
        font=("Arial", 18, "bold"),
        bg="white"
    ).pack(pady=10)

    # -------------------------------
    # Main row under title
    # same width as banner
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
    # Instructions (left)
    # -------------------------------
    instructions = [
        "1. Find the ENCODER in the box (refer image)",
        "2. Insert it into the encoder connection point on the green PCB board",
        "3. Turn the knob left and right",
        "4. If connected correctly, the LED brightness will change"
    ]

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
        text="Hint: Encoder has a 4-wire cable",
        font=("Arial", 12, "italic"),
        fg="gray",
        bg="white",
        anchor="w",
        justify="left",
        wraplength=text_width
    ).pack(anchor="w", pady=15)

    # -------------------------------
    # Box image (right)
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

    # Brightness bar
    tk.Label(root, text="Brightness Level",
             font=("Arial", 14, "bold"), bg="white").pack(pady=(10, 5))

    bar_canvas = tk.Canvas(root, width=300, height=30,
                           bg="white", highlightthickness=0)
    bar_canvas.pack(pady=5)

    bar_canvas.create_rectangle(20, 5, 280, 25, outline="black", width=2)
    fill_bar = bar_canvas.create_rectangle(20, 5, 20, 25, fill="skyblue", outline="")

    # -------------------------------
    # Back button (center)
    # -------------------------------
    tk.Button(
        root,
        text="Back",
        width=10,
        height=2,
        command=go_to_menu
    ).pack(pady=20)

    # -------------------------------
    # ---- Turn LED ON on GPIO 21 ----
    led_task3 = PWMLED(21)
    led_task3.value = 0
    root.led_task3 = led_task3

    sig_a = Button(20, pull_up=True)
    sig_b = Button(16, pull_up=True)

    root.sig_a = sig_a
    root.sig_b = sig_b
    brightness = [0]

    def adjust_brightness():
        if sig_b.is_pressed:
            brightness[0] = min(1, brightness[0] + 0.05)
        else:
            brightness[0] = max(0, brightness[0] - 0.05)

        led_task3.value = brightness[0]

        bar_width = 20 + (260 * brightness[0])
        bar_canvas.coords(fill_bar, 20, 5, bar_width, 25)

        print("Brightness:", brightness[0])

    sig_a.when_pressed = adjust_brightness