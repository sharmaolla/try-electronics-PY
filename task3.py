import tkinter as tk
from PIL import Image, ImageTk
from gpiozero import PWMLED, Button


def show_task3(root, clear_screen, go_to_menu):
    root.cleanup_gpio()
    clear_screen()

    # ---- Banner ----
    img = Image.open("task_banner.png")
    img = img.resize((800, 270))
    banner = ImageTk.PhotoImage(img)

    banner_label = tk.Label(root, image=banner, bg="white")
    banner_label.image = banner
    banner_label.pack(pady=5)

    # ---- Title ----
    tk.Label(root, text="TASK 3: CONNECT ENCODER AND CHANGE LED BRIGHTNESS",
             font=("Arial", 18, "bold"), bg="white").pack(pady=10)

    instructions = [
        "1. Find the ENCODER in the box (refer image)",
        "2. Insert it into the encoder connection point on the green PCB board",
        "3. Turn the knob left and right",
        "4. If connected correctly, the LED brightness will change"
    ]

    for line in instructions:
        tk.Label(root, text=line, font=("Arial", 14),
                 bg="white", anchor="w", justify="left"
                 ).pack(fill="x", padx=50, pady=2)

    tk.Label(root,
             text="Hint: Encoder has a 4-wire cable",
             font=("Arial", 12, "italic"),
             fg="gray",
             bg="white",
             justify="left",
             anchor="w",
             ).pack(fill="x", padx=50, pady=15)

    tk.Label(root, text="Brightness Level",
             font=("Arial", 14, "bold"), bg="white").pack(pady=(10, 5))

    bar_canvas = tk.Canvas(root, width=300, height=30,
                           bg="white", highlightthickness=0)
    bar_canvas.pack(pady=5)

    bar_canvas.create_rectangle(20, 5, 280, 25, outline="black", width=2)
    fill_bar = bar_canvas.create_rectangle(20, 5, 150, 25, fill="skyblue", outline="")

    tk.Button(root, text="Back", width=10, height=2,
              command=go_to_menu).pack(pady=10)

    # ---- Turn LED ON on GPIO 21 ----
    led_task3 = PWMLED(21)
    led_task3.value = 0.5
    root.led_task3 = led_task3

    sig_a = Button(20, pull_up=True)
    sig_b = Button(16, pull_up=True)

    root.sig_a = sig_a
    root.sig_b = sig_b
    brightness = [0.5]

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




