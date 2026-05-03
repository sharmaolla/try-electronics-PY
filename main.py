from gpiozero import Button, PWMLED
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import tkinter as tk

from task1 import show_task1
from task2 import show_task2
from task3 import show_task3
from menu import show_task_menu

DECOR_LED_PINS = [13, 19, 26]

# -------------------------------
# Helpers
# -------------------------------
def get_scale():
    root.update_idletasks()

    w = root.winfo_width()
    h = root.winfo_height()

    if w < 100:
        w = root.winfo_screenwidth()

    if h < 100:
        h = root.winfo_screenheight()

    scale = min(w / 1000, h / 600)

    if scale < 0.6:
        scale = 0.6

    if scale > 1.3:
        scale = 1.3

    return scale, w, h


def font(size, bold=False):
    scale, _, _ = get_scale()
    real_size = max(10, int(size * scale))

    if bold:
        return ("Arial", real_size, "bold")

    return ("Arial", real_size)


def cleanup_gpio():
    for name in [
        "sig_a",
        "sig_b",
        "btn_task1",
        "sensor",
        "adc3",
        "led_task2",
        "led_task3",
        "task2_device"
    ]:
        if hasattr(root, name):
            try:
                getattr(root, name).close()
            except:
                pass

            delattr(root, name)


def setup_menu_buttons():
    if not hasattr(root, "button_task1"):
        root.button_task1 = Button(2, pull_up=True, bounce_time=0.1)
        root.button_task1.when_pressed = lambda: root.after(
            0, lambda: show_task1(root, clear_screen, main_menu)
        )

    if not hasattr(root, "button_task2"):
        root.button_task2 = Button(3, pull_up=True, bounce_time=0.1)
        root.button_task2.when_pressed = lambda: root.after(
            0, lambda: show_task2(root, clear_screen, main_menu)
        )

    if not hasattr(root, "button_task3"):
        root.button_task3 = Button(4, pull_up=True, bounce_time=0.1)
        root.button_task3.when_pressed = lambda: root.after(
            0, lambda: show_task3(root, clear_screen, main_menu)
        )


def close_menu_buttons():
    for name in ["button_task1", "button_task2", "button_task3"]:
        if hasattr(root, name):
            try:
                getattr(root, name).close()
            except:
                pass

            delattr(root, name)


def english_selected():
    setup_menu_buttons()
    root.language = "en"

    show_task_menu(
        root,
        clear_screen,
        main_menu,
        show_task1,
        show_task2,
        show_task3
    )


def finnish_selected():
    setup_menu_buttons()
    root.language = "fi"

    show_task_menu(
        root,
        clear_screen,
        main_menu,
        show_task1,
        show_task2,
        show_task3
    )


def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()


def show_under_construction():
    clear_screen()

    scale, _, _ = get_scale()

    tk.Label(
        root,
        text="Under Construction",
        font=font(20),
        bg="white"
    ).pack(pady=int(50 * scale))

    tk.Button(
        root,
        text="Back",
        font=font(12),
        width=10,
        height=2,
        command=main_menu
    ).pack(pady=int(10 * scale))


def ask_day():
    while True:
        root.update_idletasks()
        root.lift()
        root.attributes("-topmost", True)
        root.focus_force()
        root.update()

        day = simpledialog.askstring(
            "Day / Päivä",
            "Enter day (1, 2 or 3)\nSyötä päivä (1, 2 tai 3)\n",
            parent=root
        )

        root.attributes("-topmost", False)

        if day in ["1", "2", "3"]:
            root.game_day = day
            return

        root.lift()
        root.attributes("-topmost", True)

        messagebox.showwarning(
            "Wrong day / Väärä päivä",
            "Please enter only 1, 2 or 3.\nSyötä vain 1, 2 tai 3.",
            parent=root
        )

        root.attributes("-topmost", False)


def go_back_to_main():
    if root.screen == "main":
        return

    root.cleanup_gpio()
    main_menu()


def hardware_back_pressed():
    root.after(0, go_back_to_main)


def start_decorative_leds():
    root.decor_leds = []

    for pin in DECOR_LED_PINS:
        try:
            led = PWMLED(pin)
            led.value = 0
            root.decor_leds.append(led)
        except Exception as e:
            print(f"Unavailable LED on GPIO {pin}: {e}")

    pattern = [
        [0.15, 0.00, 0.00],
        [0.45, 0.15, 0.00],
        [0.75, 0.35, 0.15],
        [0.45, 0.75, 0.35],
        [0.15, 0.45, 0.75],
        [0.00, 0.15, 0.45],
        [0.00, 0.00, 0.15],
        [0.00, 0.00, 0.00],
    ]

    root.decor_step = 0

    def animate():
        if not hasattr(root, "decor_leds"):
            return

        values = pattern[root.decor_step]

        for led, value in zip(root.decor_leds, values):
            try:
                led.value = value
            except:
                pass

        root.decor_step = (root.decor_step + 1) % len(pattern)
        root.after(450, animate)

    animate()


def on_close():
    if hasattr(root, "decor_leds"):
        for led in root.decor_leds:
            try:
                led.off()
                led.close()
            except:
                pass

    root.destroy()


def main_menu():
    root.screen = "main"
    root.cleanup_gpio()

    close_menu_buttons()
    clear_screen()

    scale, screen_width, screen_height = get_scale()

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(expand=True, fill="both")

    img = Image.open("banner.png")

    banner_width = int(root.winfo_screenwidth() * 0.50)

    w, h = img.size
    scale_img = banner_width / w
    banner_height = int(h * scale_img)

    img = img.resize((banner_width, banner_height), Image.LANCZOS)

    banner = ImageTk.PhotoImage(img)

    banner_label = tk.Label(main_frame, image=banner, bg="white")
    banner_label.image = banner
    banner_label.pack(pady=int(10 * scale))

    tk.Label(
        main_frame,
        text="Choose Language",
        font=font(16, bold=True),
        bg="white"
    ).pack(pady=int(15 * scale))

    tk.Label(
        main_frame,
        text=f"Day / Päivä: {root.game_day}",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="gray"
    ).pack(pady=(0, 10))

    # -------------------------------
    # Buttons
    # -------------------------------
    button_width = max(10, int(15 * scale))
    button_height = 2 if screen_height > 500 else 1

    tk.Button(
        main_frame,
        text="English",
        font=font(18),
        width=button_width,
        height=button_height,
        command=english_selected
    ).pack(pady=int(8 * scale))

    tk.Button(
        main_frame,
        text="Suomi",
        font=font(18),
        width=button_width,
        height=button_height,
        command=finnish_selected
    ).pack(pady=int(8 * scale))


# -------------------------------
# Main app
# -------------------------------
root = tk.Tk()

root.cleanup_gpio = cleanup_gpio
root.go_main = main_menu

root.go_task1 = lambda: show_task1(root, clear_screen, main_menu)
root.go_task2 = lambda: show_task2(root, clear_screen, main_menu)
root.go_task3 = lambda: show_task3(root, clear_screen, main_menu)

root.title("Electronics Game")
root.geometry("1000x600")
root.minsize(480, 320)
root.configure(bg="white")
root.screen = "main"

root.protocol("WM_DELETE_WINDOW", on_close)


# -------------------------------
# Hardware buttons
# -------------------------------
button_english = Button(5, pull_up=True)
button_suomi = Button(22, pull_up=True)
button_back = Button(6, pull_up=True)

button_english.when_pressed = lambda: root.after(
    0, lambda: english_selected() if root.screen == "main" else None
)

button_suomi.when_pressed = lambda: root.after(
    0, lambda: finnish_selected() if root.screen == "main" else None
)

button_back.when_pressed = hardware_back_pressed


start_decorative_leds()
ask_day()
main_menu()
root.mainloop()