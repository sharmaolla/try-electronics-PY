import tkinter as tk
from PIL import Image, ImageTk
from gpiozero import LED, MCP3008
import time

GREY_BG = "#EEEEEE"

# -------------------------------
# ADC + GPIO
# -------------------------------
ADC_CHANNEL = 3
ADC_THRESHOLD = 0.5
TASK2_LED_PIN = 18

TEXTS = {
    "en": {
        "title": "Task 2. Connect the resistor and turn LED2 on",
        "instructions": [
            "1. Find connection points J4 and J5, and LED2 on the green PCB board",
            "2. Find the RESISTOR in the box (see image)",
            "3. Insert the resistor between connection points J4 and J5 by following the white guide line printed on the PCB",
            "4. If connected correctly, the resistor will be detected and LED2 will turn ON"
        ],
        "hint": "Hint: you can insert the RESISTOR either way, try both ways.",
        "main": "Main",
        "task1": "Task 1",
        "task3": "Task 3",
        "connected": "CONNECTED ✅ 😊",
        "not_connected": "NOT CONNECTED ❌ ☹️"
    },
    "fi": {
        "title": "Tehtävä 2. Kytke vastus ja sytytä LED2",
        "instructions": [
            "1. Etsi liitäntäkohdat J4 ja J5 sekä LED2 vihreältä PCB-levyltä",
            "2. Etsi vastus (RESISTOR) laatikosta (katso kuva)",
            "3. Aseta vastus liitäntäkohtien J4 ja J5 väliin PCB-levyyn painetun valkoisen ohjeviivan mukaisesti",
            "4. Jos kytkentä on oikein, vastus tunnistetaan ja LED2 syttyy"
        ],
        "hint": "Vinkki: voit asettaa vastuksen kummin päin tahansa – kokeile molempia",
        "main": "Etusivu",
        "task1": "Tehtävä 1",
        "task3": "Tehtävä 3",
        "connected": "KYTKETTY ✅ 😊",
        "not_connected": "EI KYTKETTY ❌ ☹️"
    }
}

def read_adc_average(adc, samples=5):
    total = 0

    for _ in range(samples):
        total += adc.value
        time.sleep(0.01)

    return total / samples


def show_task2(root, clear_screen, go_to_menu):
    root.screen = "task2"
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
    left_frame.pack(
        side="left",
        anchor="n",
        padx=(0, int(banner_width * 0.03))
    )

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

    box_img = box_img.resize(
        (box_target_width, box_target_height),
        Image.LANCZOS
    )
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
        text=t["task1"],
        font=font(12),
        width=btn_width,
        height=btn_height,
        command=root.go_task1
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
    # Status
    # -------------------------------
    status_label = tk.Label(
        main_frame,
        text=t["not_connected"],
        font=font(14, bold=True),
        bg="white",
        fg="red"
    )
    status_label.pack(pady=int(6 * scale))

    # -------------------------------
    # ADC + LED2
    # -------------------------------
    try:
        adc3 = MCP3008(channel=ADC_CHANNEL)
        root.adc3 = adc3
    except Exception as e:
        status_label.config(
            text=f"ADC ERROR: {e}",
            font=font(14, bold=True),
            fg="red",
            bg="white"
        )
        return

    led_task2 = LED(TASK2_LED_PIN)
    root.led_task2 = led_task2

    led_task2.on()

    def check_connection():
        if not hasattr(root, "adc3") or root.adc3 != adc3:
            return

        if not status_label.winfo_exists():
            return

        try:
            ad3_value = read_adc_average(adc3)
        except Exception as e:
            print("ADC error:", e)
            return

        print("AD3:", round(ad3_value, 3))

        resistor_connected = ad3_value > ADC_THRESHOLD

        if resistor_connected:
            status_label.config(
                text=t["connected"],
                font=font(18, bold=True),
                fg="green",
                bg="white"
            )
        else:
            status_label.config(
                text=t["not_connected"],
                font=font(18, bold=True),
                fg="red",
                bg="white"
            )

        root.after(300, check_connection)

    check_connection()