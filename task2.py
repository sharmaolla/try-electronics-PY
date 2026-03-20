import tkinter as tk
from PIL import Image, ImageTk
from gpiozero import LED


def show_task2(root, clear_screen, go_to_menu):
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
    tk.Label(root, text="TASK 2: CONNECT RESISTOR and TURN LED LIGHT ON",
             font=("Arial", 18, "bold"), bg="white").pack(pady=10)

    # ---- Instructions ----
    instructions = [
        "1. Find RESISTOR in the box (refer image)",
        "2. Insert it into the resistor connection point on the green PCB board",
        "3. If connected correctly, the LED will turn ON",

    ]

    for line in instructions:
        tk.Label(root, text=line, font=("Arial", 14),
                 bg="white", anchor="w", justify="left"
                 ).pack(fill="x", padx=50, pady=2)

    tk.Label(root,
             text="Hint: you can insert RESISTOR either way. Try both ways.",
             font=("Arial", 12, "italic"),
             fg="gray",
             bg="white",
             justify="left",
             anchor="w",
             ).pack(fill="x", padx=50, pady=15)

    tk.Button(root, text="Back", width=10, height=2,
              command=go_to_menu).pack(pady=10)

# ---- Turn LED ON on GPIO26 ----
    led_task2 = LED(26)
    led_task2.on()

    root.led_task2 = led_task2

