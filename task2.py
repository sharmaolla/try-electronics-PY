import tkinter as tk
from PIL import Image, ImageTk
from gpiozero import Button, LED

TEXTS = {
    "en": {
        "title": "Task 2. Connect resistor and turn LED light on",
        "instructions": [
            "1. Find RESISTOR in the box (refer image)",
            "2. Insert it into the resistor connection point on the green PCB board",
            "3. If connected correctly the resistor will be detected"
        ],
        "hint": "Hint: you can insert RESISTOR either way, try both ways.",
        "back": "Back",
        "connected": "CONNECTED ✅ 😊",
        "not_connected": "NOT CONNECTED ❌ ☹️"

    },
    "fi": {
        "title": "Tehtävä 2. Kytke vastus ja sytytä LED-valo",
        "instructions": [
            "1. Etsi vastus (RESISTOR) laatikosta (katso kuva)",
            "2. Aseta se vastuksen liitäntäkohtaan vihreällä PCB-levyllä",
            "3. Jos kytkentä on oikein, vastus tunnistetaan"
        ],
        "hint": "Vinkki: Voit laittaa vastuksen kumpaan suuntaan tahansa – kokeile molempia",
        "back": "Takaisin",
        "connected": "KYTKETTY ✅ 😊",
        "not_connected": "EI KYTKETTY ❌ ☹️"
    }
}


def show_task2(root, clear_screen, go_to_menu):
    root.cleanup_gpio()
    clear_screen()

    lang = getattr(root, "language", "en")
    t = TEXTS[lang]
    root.update_idletasks()

    screen_width = root.winfo_width()
    if screen_width < 100:
        screen_width = root.winfo_screenwidth()

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

    tk.Label(
        root,
        text=t["title"],
        font=("Arial", 18, "bold"),
        bg="white"
    ).pack(pady=10)

    content_frame = tk.Frame(root, bg="white", width=banner_width)
    content_frame.pack(pady=10)

    left_frame = tk.Frame(content_frame, bg="white")
    left_frame.pack(side="left", anchor="n")

    spacer = tk.Frame(content_frame, bg="white", width=40)
    spacer.pack(side="left")

    right_frame = tk.Frame(content_frame, bg="white")
    right_frame.pack(side="left", anchor="n")

    text_width = int(banner_width * 0.5)

    for line in t["instructions"]:
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

    box_img = Image.open("box.png")
    box_target_width = int(banner_width * 0.4)
    bw2, bh2 = box_img.size
    box_target_height = int(bh2 * (box_target_width / bw2))

    box_img = box_img.resize((box_target_width, box_target_height))
    box_photo = ImageTk.PhotoImage(box_img)

    box_label = tk.Label(right_frame, image=box_photo, bg="white")
    box_label.image = box_photo
    box_label.pack()

    tk.Button(
        root,
        text=t["back"],
        width=10,
        height=2,
        command=go_to_menu
    ).pack(pady=20)

    status_label = tk.Label(
        root,
        text=t["not_connected"],
        font=("Arial", 14),
        bg="white"
    )
    status_label.pack(pady=10)

    sensor = Button(26, pull_up=True)
    root.sensor = sensor
    led_task2 = LED(21)
    root.led_task2 = led_task2

    def check_connection():
        if sensor.is_pressed:
            status_label.config(
                text=t["connected"],
                font=("Arial", 18, "bold"),
                fg="green",
                bg="white"
            )
            led_task2.on()


        else:
            status_label.config(
                text=t["not_connected"],
                font=("Arial", 18, "bold"),
                fg="red",
                bg="white"
            )
            led_task2.off()

        root.after(200, check_connection)

    check_connection()