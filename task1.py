import tkinter as tk
from PIL import Image, ImageTk
from gpiozero import Button


def show_task1_success(root, clear_screen, go_to_menu):
    root.cleanup_gpio()
    clear_screen()

    tk.Label(root, text="Correct!",
             font=("Arial", 24, "bold"),
             bg="white", fg="green").pack(pady=40)

    tk.Label(root, text="Button pressed successfully.",
             font=("Arial", 18),
             bg="white").pack(pady=10)

    tk.Label(root, text="Good job!",
             font=("Arial", 18),
             bg="white").pack(pady=10)

    tk.Button(root, text="Back to Menu",
              width=15, height=2,
              command=go_to_menu).pack(pady=30)


def show_task1(root, clear_screen, go_to_menu):
    clear_screen()

    # ---- Banner ----
    img = Image.open("task_banner.png")
    img = img.resize((800, 270))
    banner = ImageTk.PhotoImage(img)

    banner_label = tk.Label(root, image=banner, bg="white")
    banner_label.image = banner
    banner_label.pack(pady=5)

    # ---- Title ----
    tk.Label(root, text="TASK 1: CONNECT BUTTON",
             font=("Arial", 18, "bold"), bg="white").pack(pady=10)

    # ---- Instructions ----
    instructions = [
        "1. Find button connector on green PCB board",
        "2. Connect BLACK wire from button → GND on PCB board",
        "3. Connect RED wire from button → GP17 on PCB board",
        "4. Press the button"
    ]

    for line in instructions:
        tk.Label(root, text=line, font=("Arial", 14),
                 bg="white", anchor="w", justify="left"
                 ).pack(fill="x", padx=50, pady=2)

    tk.Label(root,
             text="Hint: If you press the button and nothing happens, check wiring and connections",
             font=("Arial", 12, "italic"),
             fg="gray",
             bg="white",
             justify="left",
             anchor="w",
             ).pack(fill="x", padx=50, pady=15)

    tk.Button(root, text="Back", width=10, height=2,
              command=go_to_menu).pack(pady=10)

    # ---- Real hardware button on GPIO17 ----
    def show_popup(root):
        popup = tk.Toplevel(root)
        popup.overrideredirect(True)  # remove normal window border

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
            text="CORRECT!",
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