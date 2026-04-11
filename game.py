import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from gpiozero import Button, LED, PWMLED
import json
import os

TEXTS = {
    "en": {
        "main_title": "LET'S PLAY A GAME",
        "description_title": "DESCRIPTION of the game",
        "description_text": (
            "Complete Task 1, Task 2 and Task 3 in order.\n\n"
            "Enter your name and press START to begin.\n\n\n"
        ),
        "task1_title": "Task 1. Connect button",
        "task1_instructions": [
            "1. Find BUTTON connection point and BUTTON_1 on the green PCB board",
            "2. Take two jumper wires from the box (refer image)",
            "3. Connect BUTTON_1 and BUTTON connection points with wires",
            "4. Press the button"
        ],
        "task1_hint": "Hint: if you press the button and nothing happens, check wiring and connections",
        "task2_title": "Task 2. Connect resistor and turn LED light on",
        "task2_instructions": [
            "1. Find RESISTOR in the box (refer image)",
            "2. Insert it into the resistor connection point on the green PCB board",
            "3. If connected correctly the resistor will be detected"
        ],
        "task2_hint": "Hint: you can insert RESISTOR either way, try both ways.",
        "task2_connected": "CONNECTED ✅ 😊",
        "task2_not_connected": "NOT CONNECTED ❌ ☹️",
        "task3_title": "Task 3. Connect encoder and change LED brightness",
        "task3_instructions": [
            "1. Find ENCODER in the box (refer image)",
            "2. Insert it into the encoder connection point on the green PCB board",
            "3. Turn the knob left and right",
            "4. If connected correctly, the LED brightness will change"
        ],
        "task3_hint": "Hint: Encoder has a 4-wire cable",
        "brightness": "Brightness Level",
        "task1": "Task 1",
        "task2": "Task 2",
        "task3": "Task 3",
        "start": "START",
        "back": "Back",
        "enter_name": "Enter your name",
        "name_required": "Please enter your name.",
        "correct": "CORRECT!"
    },
    "fi": {
        "main_title": "PELATAAN PELIÄ",
        "description_title": "Pelin kuvaus",
        "description_text": (
            "Suorita Tehtävä 1, Tehtävä 2 ja Tehtävä 3 järjestyksessä.\n\n"
            "Kirjoita nimesi ja paina START."
        ),
        "task1_title": "Tehtävä 1. Yhdistä painike",
        "task1_instructions": [
            "1. Etsi BUTTON-liitäntäkohta ja BUTTON_1 vihreältä PCB-levyltä",
            "2. Ota kaksi hyppylankaa laatikosta (katso kuva)",
            "3. Yhdistä BUTTON_1 ja BUTTON-liitäntäkohta johdoilla",
            "4. Paina painiketta"
        ],
        "task1_hint": "Vinkki: Jos painat painiketta eikä mitään tapahdu, tarkista johdot ja liitännät",
        "task2_title": "Tehtävä 2. Kytke vastus ja sytytä LED-valo",
        "task2_instructions": [
            "1. Etsi vastus (RESISTOR) laatikosta (katso kuva)",
            "2. Aseta se vastuksen liitäntäkohtaan vihreällä PCB-levyllä",
            "3. Jos kytkentä on oikein, vastus tunnistetaan"
        ],
        "task2_hint": "Vinkki: Voit laittaa vastuksen kumpaan suuntaan tahansa – kokeile molempia",
        "task2_connected": "KYTKETTY ✅ 😊",
        "task2_not_connected": "EI KYTKETTY ❌ ☹️",
        "task3_title": "Tehtävä 3. Kytke ENCODER ja muuta valon kirkkautta",
        "task3_instructions": [
            "1. Etsi ENCODER laatikosta (katso kuva)",
            "2. Aseta se encoderin liitäntäkohtaan vihreällä PCB-levyllä",
            "3. Käännä nuppia vasemmalle ja oikealle",
            "4. Jos kytkentä on oikein, LED-valon kirkkaus muuttuu"
        ],
        "task3_hint": "Vinkki: Encoderissa on 4-johtiminen kaapeli",
        "brightness": "Kirkkaustaso",
        "task1": "Tehtävä 1",
        "task2": "Tehtävä 2",
        "task3": "Tehtävä 3",
        "start": "START",
        "back": "Takaisin",
        "enter_name": "Kirjoita nimesi",
        "name_required": "Kirjoita nimesi ensin.",
        "correct": "OIKEIN!"
    }
}


def save_player_name(player_name):
    file_path = "players.json"
    players = []

    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                players = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            players = []

    players.append({"name": player_name})

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(players, f, indent=4, ensure_ascii=False)


def show_game(root, clear_screen, go_to_menu):
    root.cleanup_gpio()
    clear_screen()

    lang = getattr(root, "language", "en")
    t = TEXTS[lang]
    root.update_idletasks()

    screen_width = root.winfo_width()
    if screen_width < 100:
        screen_width = root.winfo_screenwidth()

    # -------------------------------
    # Banner
    # -------------------------------
    banner_img = Image.open("task_banner.png")
    banner_width = int(screen_width * 0.7)

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
    # Main title
    # -------------------------------
    tk.Label(
        root,
        text=t["main_title"],
        font=("Arial", 18, "bold"),
        bg="white"
    ).pack(pady=(0, 12))

    # -------------------------------
    # Horizontal task blocks
    # -------------------------------
    tasks_frame = tk.Frame(root, bg="white")
    tasks_frame.pack(pady=(0, 18))

    task1_box = tk.Label(
        tasks_frame,
        text=t["task1"],
        font=("Arial", 16, "bold"),
        bg="light gray",
        width=10,
        height=1,
        bd=1,
        relief="solid"
    )
    task1_box.pack(side="left", padx=10)

    task2_box = tk.Label(
        tasks_frame,
        text=t["task2"],
        font=("Arial", 16, "bold"),
        bg="light gray",
        width=10,
        height=1,
        bd=1,
        relief="solid"
    )
    task2_box.pack(side="left", padx=10)

    task3_box = tk.Label(
        tasks_frame,
        text=t["task3"],
        font=("Arial", 16, "bold"),
        bg="light gray",
        width=10,
        height=1,
        bd=1,
        relief="solid"
    )
    task3_box.pack(side="left", padx=10)

    # -------------------------------
    # Main dynamic content area
    # -------------------------------
    content_frame = tk.Frame(root, bg="white")
    content_frame.pack(pady=10)

    # -------------------------------
    # Helper functions
    # -------------------------------
    def clear_content():
        for widget in content_frame.winfo_children():
            widget.destroy()

    def show_description():
        clear_content()

        desc_frame = tk.Frame(content_frame, bg="white")
        desc_frame.pack()

        tk.Label(
            desc_frame,
            text=t["description_title"],
            font=("Arial", 16, "bold"),
            bg="white",
            anchor="nw",
            justify="left"
        ).pack(anchor="nw", padx=12, pady=(12, 8))

        tk.Label(
            desc_frame,
            text=t["description_text"],
            font=("Arial", 13),
            bg="white",
            anchor="nw",
            justify="left",
            wraplength=520
        ).pack(anchor="nw", padx=12, pady=(0, 18))

        controls_frame = tk.Frame(desc_frame, bg="white")
        controls_frame.pack(anchor="w", padx=12, pady=(0, 10))

        tk.Label(
            controls_frame,
            text=t["enter_name"],
            font=("Arial", 13),
            bg="white"
        ).pack(side="left", padx=(0, 10))

        name_var = tk.StringVar()

        name_entry = tk.Entry(
            controls_frame,
            textvariable=name_var,
            font=("Arial", 14),
            width=22,
            justify="center"
        )
        name_entry.pack(side="left", padx=(0, 15))
        name_entry.focus_set()

        def on_start():
            player_name = name_var.get().strip()

            if not player_name:
                messagebox.showwarning("Warning", t["name_required"])
                return

            root.player_name = player_name
            save_player_name(player_name)

            show_task1()

        tk.Button(
            controls_frame,
            text=t["start"],
            font=("Arial", 16, "bold"),
            width=10,
            height=1,
            command=on_start
        ).pack(side="left")

    def show_popup():
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

    root.task1_done = False
    root.task2_done = False
    root.task3_done = False

    def on_task1_pressed():
        if root.task1_done:
            return

        root.task1_done = True
        print("GPIO 17 pressed")
        root.after(0, show_popup)
        root.after(0, lambda: task1_box.config(bg="#ADD8E6"))
        root.after(1500, lambda: (root.cleanup_gpio(), show_task2()))

    def show_task1():
        clear_content()

        task1_box.config(bg="light gray")
        task2_box.config(bg="light gray")
        task3_box.config(bg="light gray")


        task1_frame = tk.Frame(content_frame, bg="white")
        task1_frame.pack()

        tk.Label(
            task1_frame,
            text=t["task1_title"],
            font=("Arial", 18, "bold"),
            bg="white"
        ).pack(pady=10)

        row_frame = tk.Frame(task1_frame, bg="white")
        row_frame.pack(pady=10)

        left_frame = tk.Frame(row_frame, bg="white")
        left_frame.pack(side="left", anchor="n")

        spacer = tk.Frame(row_frame, bg="white", width=40)
        spacer.pack(side="left")

        right_frame = tk.Frame(row_frame, bg="white")
        right_frame.pack(side="left", anchor="n")

        text_width = int(banner_width * 0.5)

        for line in t["task1_instructions"]:
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
            text=t["task1_hint"],
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

        btn_task1 = Button(17, pull_up=True)
        btn_task1.when_pressed = on_task1_pressed
        root.btn_task1 = btn_task1

    def show_task2():
        clear_content()

        task2_frame = tk.Frame(content_frame, bg="white")
        task2_frame.pack()

        tk.Label(
            task2_frame,
            text=t["task2_title"],
            font=("Arial", 18, "bold"),
            bg="white"
        ).pack(pady=10)

        row_frame = tk.Frame(task2_frame, bg="white")
        row_frame.pack(pady=10)

        left_frame = tk.Frame(row_frame, bg="white")
        left_frame.pack(side="left", anchor="n")

        spacer = tk.Frame(row_frame, bg="white", width=40)
        spacer.pack(side="left")

        right_frame = tk.Frame(row_frame, bg="white")
        right_frame.pack(side="left", anchor="n")

        text_width = int(banner_width * 0.5)

        for line in t["task2_instructions"]:
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
            text=t["task2_hint"],
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

        status_label = tk.Label(
            task2_frame,
            text=t["task2_not_connected"],
            font=("Arial", 14),
            bg="white",
            fg="red"
        )
        status_label.pack(pady=10)

        sensor = Button(26, pull_up=True)
        root.sensor = sensor

        led_task2 = LED(21)
        root.led_task2 = led_task2

        def check_connection():
            if not status_label.winfo_exists():
                return

            if sensor.is_pressed:
                status_label.config(
                    text=t["task2_connected"],
                    font=("Arial", 18, "bold"),
                    fg="green",
                    bg="white"
                )
                led_task2.on()

                if not root.task2_done:
                    root.task2_done = True
                    task2_box.config(bg="#ADD8E6")
                    root.after(2000, lambda: (root.cleanup_gpio(), show_task3()))
                    return

            else:
                status_label.config(
                    text=t["task2_not_connected"],
                    font=("Arial", 18, "bold"),
                    fg="red",
                    bg="white"
                )
                led_task2.off()

            root.after(200, check_connection)

        check_connection()
# task 3
#-----------------------------------------------------
    def show_task3():
        clear_content()

        task3_frame = tk.Frame(content_frame, bg="white")
        task3_frame.pack()

        tk.Label(
            task3_frame,
            text=t["task3_title"],
            font=("Arial", 18, "bold"),
            bg="white"
        ).pack(pady=10)

        row_frame = tk.Frame(task3_frame, bg="white")
        row_frame.pack(pady=10)

        left_frame = tk.Frame(row_frame, bg="white")
        left_frame.pack(side="left", anchor="n")

        spacer = tk.Frame(row_frame, bg="white", width=40)
        spacer.pack(side="left")

        right_frame = tk.Frame(row_frame, bg="white")
        right_frame.pack(side="left", anchor="n")

        text_width = int(banner_width * 0.5)

        for line in t["task3_instructions"]:
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
            text=t["task3_hint"],
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

        tk.Label(
            task3_frame,
            text=t["brightness"],
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(pady=(10, 5))

        bar_canvas = tk.Canvas(
            task3_frame,
            width=300,
            height=30,
            bg="white",
            highlightthickness=0
        )
        bar_canvas.pack(pady=5)

        bar_canvas.create_rectangle(20, 5, 280, 25, outline="black", width=2)
        fill_bar = bar_canvas.create_rectangle(20, 5, 20, 25, fill="skyblue", outline="")

        led_task3 = PWMLED(21)
        led_task3.value = 0
        root.led_task3 = led_task3

        sig_a = Button(20, pull_up=True)
        sig_b = Button(16, pull_up=True)

        root.sig_a = sig_a
        root.sig_b = sig_b

        brightness = [0]
        encoder_used = [False]

        def adjust_brightness():
            if sig_b.is_pressed:
                brightness[0] = min(1, brightness[0] + 0.05)
            else:
                brightness[0] = max(0, brightness[0] - 0.05)

            led_task3.value = brightness[0]

            bar_width = 20 + (260 * brightness[0])
            bar_canvas.coords(fill_bar, 20, 5, bar_width, 25)

            print("Brightness:", brightness[0])

            if not encoder_used[0]:
                encoder_used[0] = True
                root.task3_done = True
                task3_box.config(bg="#ADD8E6")

        sig_a.when_pressed = adjust_brightness


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

    # first screen
    show_description()