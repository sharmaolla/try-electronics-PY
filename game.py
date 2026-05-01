import tkinter as tk
from PIL import Image, ImageTk
from gpiozero import Button, LED, PWMLED, MCP3008
import json
import os
import time

TASK_BLOCK_BG = "#EEEEEE"
TASK_DONE_BG = "#87CEEB"
result_bg = "white"
result_fg = "#0B3D91"  # dark blue
GREY_BG = "#EEEEEE"

# -------------------------------
# PCB pins
# -------------------------------
TASK1_PIN = 14
LED_PIN = 12
ROT_A_PIN = 27
ROT_B_PIN = 17

TASK2_ADC_CHANNEL = 3
TASK2_ADC_THRESHOLD = 0.5
TASK2_LED_PIN = 18

TEXTS = {
    "en": {
        "main_title": "LET'S PLAY A GAME",
        "description_title": "DESCRIPTION of the game",
        "description_text": (
            "Complete Task 1, Task 2 and Task 3 in order.\n\n"
            "Enter your name and press START to begin.\n"
            "(use a unique name or add numbers, e.g. John1)"
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
            "3. Turn the knob right until LED reaches full brightness",
            "4. Then turn it back until LED is off again",
            "5. If connected correctly, the LED brightness will change"
        ],
        "task3_hint": "Hint: Encoder has a 4-wire cable",
        "brightness": "Brightness Level",
        "task1": "Task 1",
        "task2": "Task 2",
        "task3": "Task 3",
        "start": "START",
        "back": "Back",
        "enter_name": "Enter your name",
        "correct": "CORRECT!",
        "result_time": "\n{name}, your time:   {time}",
        "rank": "Rank",
        "name": "Name",
        "time": "Time",
        "anonymous": "Anonymous",
        "today_results": "★ DAY {day} TOP 5 ★",
        "overall_results": "★ OVERALL TOP 5 ★",
        "player_ranks": "Day rank: #{day_rank}    Overall rank: #{overall_rank}\n"
    },

    "fi": {
        "main_title": "PELATAAN PELIÄ",
        "description_title": "Pelin kuvaus",
        "description_text": (
            "Suorita Tehtävä 1, Tehtävä 2 ja Tehtävä 3 järjestyksessä.\n\n"
            "Kirjoita nimesi ja paina START.\n"
            "(käytä yksilöllistä nimeä tai lisää numero, esim. Ulla1)"
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
            "3. Käännä nuppia oikealle, kunnes LED saavuttaa täyden kirkkauden",
            "4. Käännä sitten takaisin, kunnes LED sammuu",
            "5. Jos kytkentä on oikein, LED-valon kirkkaus muuttuu"
        ],
        "task3_hint": "Vinkki: Encoderissa on 4-johtiminen kaapeli",
        "brightness": "Kirkkaustaso",
        "task1": "Tehtävä 1",
        "task2": "Tehtävä 2",
        "task3": "Tehtävä 3",
        "start": "START",
        "back": "Takaisin",
        "enter_name": "Kirjoita nimesi",
        "correct": "OIKEIN!",
        "result_time": "\n{name}, aikasi:   {time}",
        "rank": "Sija",
        "name": "Nimi",
        "time": "Aika",
        "anonymous": "Anonyymi",
        "today_results": "★ PÄIVÄN {day} - TOP 5 ★",
        "overall_results": "★ KOKONAISTULOKSET – TOP 5 ★",
        "player_ranks": "Päivän sijoitus: #{day_rank}    Kokonaissijoitus: #{overall_rank}\n",
    }
}


def clean_player_list(players):
    valid_players = []

    if not isinstance(players, list):
        return valid_players

    for p in players:
        if isinstance(p, dict) and "name" in p and "time" in p:
            valid_players.append({
                "name": p["name"],
                "time": float(p["time"])
            })

    return valid_players


def top_5(players):
    players = clean_player_list(players)
    players = sorted(players, key=lambda x: x["time"])
    return players[:5]


def load_results():
    file_path = "players.json"

    empty_results = {
        "days": {
            "1": [],
            "2": [],
            "3": []
        },
        "overall": []
    }

    if not os.path.exists(file_path):
        return empty_results

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return empty_results

    if isinstance(data, list):
        empty_results["overall"] = top_5(data)
        return empty_results

    if not isinstance(data, dict):
        return empty_results

    days = data.get("days", {})
    overall = data.get("overall", [])

    for day in ["1", "2", "3"]:
        empty_results["days"][day] = sorted(
            clean_player_list(days.get(day, [])),
            key=lambda x: x["time"]
        )

    empty_results["overall"] = sorted(
        clean_player_list(overall),
        key=lambda x: x["time"]
    )

    return empty_results


def save_result(player_name, game_time, game_day):
    file_path = "players.json"

    results = load_results()
    game_day = str(game_day)

    if game_day not in ["1", "2", "3"]:
        game_day = "1"

    new_player = {
        "name": player_name,
        "time": round(game_time, 1)
    }

    results["days"][game_day].append(new_player)
    results["overall"].append(new_player)

    results["days"][game_day] = sorted(
        clean_player_list(results["days"][game_day]),
        key=lambda x: x["time"]
    )

    results["overall"] = sorted(
        clean_player_list(results["overall"]),
        key=lambda x: x["time"]
    )

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


def format_game_time(seconds):
    total_seconds = int(round(float(seconds)))

    minutes = total_seconds // 60
    remaining_seconds = total_seconds % 60

    return f"{minutes}m {remaining_seconds:02d}s"


def get_player_rank(players, player_name, player_time):
    player_time = round(player_time, 1)

    for index, player in enumerate(players, start=1):
        if player["name"] == player_name and round(player["time"], 1) == player_time:
            return index

    return "-"


def read_adc_average(adc, samples=5):
    total = 0

    for _ in range(samples):
        total += adc.value
        time.sleep(0.01)

    return total / samples


def show_game(root, clear_screen, go_to_menu):
    root.screen = "game"
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

    banner_width = int(screen_width * 0.45)

    bw, bh = banner_img.size
    img_scale = banner_width / bw
    banner_height = int(bh * img_scale * 1.25)

    max_banner_height = int(screen_height * 0.28)

    if banner_height > max_banner_height:
        img_scale = max_banner_height / bh
        banner_width = int(bw * img_scale)
        banner_height = max_banner_height

    banner_img = banner_img.resize((banner_width, banner_height), Image.LANCZOS)
    banner_photo = ImageTk.PhotoImage(banner_img)

    banner_row = tk.Frame(main_frame, bg="white")
    banner_row.pack(pady=(int(6 * scale), int(3 * scale)))

    left_score_area = tk.Frame(banner_row, bg="white")
    left_score_area.pack(side="left", padx=(0, int(10 * scale)), anchor="n")

    banner_label = tk.Label(banner_row, image=banner_photo, bg="white")
    banner_label.image = banner_photo
    banner_label.pack(side="left", anchor="n")

    right_score_area = tk.Frame(banner_row, bg="white")
    right_score_area.pack(side="left", padx=(int(10 * scale), 0), anchor="n")

    # -------------------------------
    # Main title
    # -------------------------------
    tk.Label(
        main_frame,
        text=t["main_title"],
        font=font(18, bold=True),
        bg="white"
    ).pack(pady=(0, int(8 * scale)))

    # -------------------------------
    # Task boxes
    # -------------------------------
    tasks_frame = tk.Frame(main_frame, bg="white")
    tasks_frame.pack(pady=(0, int(8 * scale)))

    box_width = max(8, int(10 * scale))

    task1_box = tk.Label(
        tasks_frame,
        text=t["task1"],
        font=font(14, bold=True),
        bg=TASK_BLOCK_BG,
        width=box_width,
        height=1,
        bd=1,
        relief="solid"
    )
    task1_box.pack(side="left", padx=int(8 * scale))

    task2_box = tk.Label(
        tasks_frame,
        text=t["task2"],
        font=font(14, bold=True),
        bg=TASK_BLOCK_BG,
        width=box_width,
        height=1,
        bd=1,
        relief="solid"
    )
    task2_box.pack(side="left", padx=int(8 * scale))

    task3_box = tk.Label(
        tasks_frame,
        text=t["task3"],
        font=font(14, bold=True),
        bg=TASK_BLOCK_BG,
        width=box_width,
        height=1,
        bd=1,
        relief="solid"
    )
    task3_box.pack(side="left", padx=int(8 * scale))

    # -------------------------------
    # Bottom area
    # -------------------------------
    bottom_frame = tk.Frame(main_frame, bg="white")
    bottom_lift = max(14, int(screen_height * 0.04))
    bottom_frame.pack(side="bottom", fill="x", pady=(0, bottom_lift))

    timer_job = [None]

    def stop_timer():
        if timer_job[0] is not None:
            try:
                root.after_cancel(timer_job[0])
            except:
                pass

            timer_job[0] = None

    tk.Button(
        bottom_frame,
        text=t["back"],
        font=font(11),
        width=max(8, int(10 * scale)),
        height=1,
        command=lambda: (stop_timer(), root.cleanup_gpio(), go_to_menu())
    ).pack(pady=(0, int(2 * scale)))

    timer_label = tk.Label(
        bottom_frame,
        text="Time: 0.0 s",
        font=font(15, bold=True),
        bg="white",
        fg="black"
    )

    # -------------------------------
    # Content area
    # -------------------------------
    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(fill="both", expand=True, pady=(0, int(3 * scale)))

    # -------------------------------
    # Helpers
    # -------------------------------
    def clear_content():
        for widget in content_frame.winfo_children():
            widget.destroy()

    def clear_start_tables():
        for widget in left_score_area.winfo_children():
            widget.destroy()

        for widget in right_score_area.winfo_children():
            widget.destroy()

    def make_start_score_table(parent, title, players):
        table_width = max(180, int(screen_width * 0.17))
        table_height = banner_height

        outer_border = tk.Frame(
            parent,
            bg="#87CEEB",
            width=table_width,
            height=table_height
        )
        outer_border.pack(anchor="n")
        outer_border.pack_propagate(False)

        middle_gap = tk.Frame(outer_border, bg="white")
        middle_gap.pack(fill="both", expand=True, padx=3, pady=3)
        middle_gap.pack_propagate(False)

        inner_border = tk.Frame(middle_gap, bg="#87CEEB")
        inner_border.pack(fill="both", expand=True, padx=2, pady=2)
        inner_border.pack_propagate(False)

        frame = tk.Frame(inner_border, bg="white")
        frame.pack(fill="both", expand=True, padx=3, pady=3)

        for row in range(7):
            frame.grid_rowconfigure(row, weight=1)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=3)
        frame.grid_columnconfigure(2, weight=2)

        title_font = font(8, bold=True)
        header_font = font(7, bold=True)
        row_font = font(7)

        tk.Label(
            frame,
            text=title,
            font=title_font,
            bg="#E6F7FF",
            anchor="center",
            wraplength=table_width - 20
        ).grid(row=0, column=0, columnspan=3, padx=2, pady=2, sticky="nsew")

        tk.Label(
            frame,
            text=t["rank"],
            font=header_font,
            bg="#E6F7FF"
        ).grid(row=1, column=0, padx=1, pady=1, sticky="nsew")

        tk.Label(
            frame,
            text=t["name"],
            font=header_font,
            bg="#E6F7FF"
        ).grid(row=1, column=1, padx=1, pady=1, sticky="nsew")

        tk.Label(
            frame,
            text=t["time"],
            font=header_font,
            bg="#E6F7FF"
        ).grid(row=1, column=2, padx=1, pady=1, sticky="nsew")

        for i in range(1, 6):
            if i <= len(players):
                player = players[i - 1]
                name_text = player["name"]
                time_text = format_game_time(player["time"])
            else:
                name_text = ""
                time_text = ""

            tk.Label(
                frame,
                text=str(i),
                font=row_font,
                bg="white"
            ).grid(row=i + 1, column=0, padx=1, pady=1, sticky="nsew")

            tk.Label(
                frame,
                text=name_text,
                font=row_font,
                bg="white"
            ).grid(row=i + 1, column=1, padx=1, pady=1, sticky="nsew")

            tk.Label(
                frame,
                text=time_text,
                font=row_font,
                bg="white"
            ).grid(row=i + 1, column=2, padx=1, pady=1, sticky="nsew")

    def show_start_tables():
        clear_start_tables()

        game_day = getattr(root, "game_day", "1")
        results = load_results()

        day_players = results["days"].get(str(game_day), [])
        overall_players = results["overall"]

        make_start_score_table(
            left_score_area,
            t["today_results"].format(day=game_day),
            day_players
        )

        make_start_score_table(
            right_score_area,
            t["overall_results"],
            overall_players
        )

    def make_task_content(title, instructions, hint):
        clear_content()

        tk.Label(
            content_frame,
            text=title,
            font=font(17, bold=True),
            bg=GREY_BG
        ).pack(pady=(int(2 * scale), int(5 * scale)))

        row_frame = tk.Frame(content_frame, bg="white")
        row_frame.pack(pady=int(5 * scale))

        text_width = int(banner_width * 0.50)

        left_frame = tk.Frame(row_frame, bg="white")
        left_frame.pack(
            side="left",
            anchor="n",
            padx=(0, int(banner_width * 0.03))
        )

        right_frame = tk.Frame(row_frame, bg="white")
        right_frame.pack(side="left", anchor="n")

        for line in instructions:
            tk.Label(
                left_frame,
                text=line,
                font=font(13),
                bg="white",
                anchor="w",
                justify="left",
                wraplength=text_width
            ).pack(anchor="w", pady=int(2 * scale))

        tk.Label(
            left_frame,
            text=hint,
            font=font(10, italic=True),
            fg="gray",
            bg="white",
            anchor="w",
            justify="left",
            wraplength=text_width
        ).pack(anchor="w", pady=int(8 * scale))

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

        return row_frame

    def update_timer():
        if hasattr(root, "start_time") and root.start_time is not None:
            if not timer_label.winfo_exists():
                return

            elapsed = time.time() - root.start_time
            timer_label.config(text=f"Time: {elapsed:.1f} s")

            timer_job[0] = root.after(100, update_timer)

    def show_result_screen(player_name, total_time):
        clear_content()

        game_day = getattr(root, "game_day", "1")
        results = load_results()

        day_players = results["days"].get(str(game_day), [])
        overall_players = results["overall"]

        day_rank = get_player_rank(day_players, player_name, total_time)
        overall_rank = get_player_rank(overall_players, player_name, total_time)

        tk.Label(
            content_frame,
            text=t["result_time"].format(
                name=player_name,
                time=format_game_time(total_time)
            ),
            font=font(18, bold=True),
            bg=result_bg,
            fg=result_fg,
        ).pack(pady=(int(8 * scale), int(8 * scale)))

        tk.Label(
            content_frame,
            text=t["player_ranks"].format(
                day_rank=day_rank,
                overall_rank=overall_rank
            ),
            font=font(14, bold=True),
            bg=result_bg,
            fg=result_fg,
        ).pack(pady=(0, int(8 * scale)))

        tables_outer_frame = tk.Frame(content_frame, bg="white")
        tables_outer_frame.pack(pady=int(4 * scale))

        def make_table(parent, title, players):
            outer_border = tk.Frame(parent, bg="#87CEEB")
            outer_border.pack(side="left", padx=int(16 * scale), anchor="n")

            middle_gap = tk.Frame(outer_border, bg="white")
            middle_gap.pack(padx=3, pady=3)

            inner_border = tk.Frame(middle_gap, bg="#87CEEB")
            inner_border.pack(padx=2, pady=2)

            frame = tk.Frame(inner_border, bg="white")
            frame.pack(padx=3, pady=3)

            tk.Label(
                frame,
                text=title,
                font=font(14, bold=True),
                bg="#E6F7FF",
                fg="black",
                width=34
            ).grid(row=0, column=0, columnspan=3, padx=4, pady=(4, 6), sticky="ew")

            tk.Label(
                frame,
                text=t["rank"],
                font=font(11, bold=True),
                bg="#E6F7FF",
                width=7
            ).grid(row=1, column=0, padx=4, pady=4)

            tk.Label(
                frame,
                text=t["name"],
                font=font(11, bold=True),
                bg="#E6F7FF",
                width=14
            ).grid(row=1, column=1, padx=4, pady=4)

            tk.Label(
                frame,
                text=t["time"],
                font=font(11, bold=True),
                bg="#E6F7FF",
                width=9
            ).grid(row=1, column=2, padx=4, pady=4)

            for i in range(1, 6):
                if i <= len(players):
                    player = players[i - 1]
                    name_text = player["name"]
                    time_text = format_game_time(player["time"])
                else:
                    name_text = ""
                    time_text = ""

                tk.Label(
                    frame,
                    text=str(i),
                    font=font(10),
                    bg="white",
                    width=7
                ).grid(row=i + 1, column=0, padx=4, pady=3)

                tk.Label(
                    frame,
                    text=name_text,
                    font=font(10),
                    bg="white",
                    width=14
                ).grid(row=i + 1, column=1, padx=4, pady=3)

                tk.Label(
                    frame,
                    text=time_text,
                    font=font(10),
                    bg="white",
                    width=9
                ).grid(row=i + 1, column=2, padx=4, pady=3)

        make_table(
            tables_outer_frame,
            t["today_results"].format(day=game_day),
            day_players
        )

        make_table(
            tables_outer_frame,
            t["overall_results"],
            overall_players
        )

    def show_description():
        clear_content()
        show_start_tables()

        timer_label.pack_forget()
        stop_timer()

        desc_frame = tk.Frame(content_frame, bg="white")
        desc_frame.pack(pady=int(8 * scale))

        tk.Label(
            desc_frame,
            text=t["description_title"],
            font=font(16, bold=True),
            bg=GREY_BG,
            anchor="center",
            justify="center"
        ).pack(anchor="center", padx=int(12 * scale), pady=(0, int(8 * scale)))

        tk.Label(
            desc_frame,
            text=t["description_text"],
            font=font(12),
            bg="white",
            anchor="nw",
            justify="left",
            wraplength=int(screen_width * 0.55)
        ).pack(anchor="nw", padx=int(12 * scale), pady=(0, int(12 * scale)))

        controls_frame = tk.Frame(desc_frame, bg="white")
        controls_frame.pack(anchor="w", padx=int(12 * scale), pady=(0, int(6 * scale)))

        tk.Label(
            controls_frame,
            text=t["enter_name"],
            font=font(12),
            bg="white"
        ).pack(side="left", padx=(0, int(8 * scale)))

        name_var = tk.StringVar()

        name_entry = tk.Entry(
            controls_frame,
            textvariable=name_var,
            font=font(13),
            width=22,
            justify="center"
        )
        name_entry.pack(side="left", padx=(0, int(12 * scale)))
        name_entry.focus_set()

        def on_start():
            player_name = name_var.get().strip()

            if not player_name:
                player_name = t["anonymous"]

            root.player_name = player_name
            root.start_time = time.time()

            timer_label.pack(pady=(0, int(2 * scale)))
            update_timer()

            clear_start_tables()
            show_task1()

        name_entry.bind("<Return>", lambda event: on_start())

        tk.Button(
            controls_frame,
            text=t["start"],
            font=font(15, bold=True),
            width=max(8, int(10 * scale)),
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

        print("GPIO 14 pressed")

        root.after(0, show_popup)
        root.after(0, lambda: task1_box.config(bg=TASK_DONE_BG))
        root.after(1500, lambda: (root.cleanup_gpio(), show_task2()))

    def show_task1():
        root.screen = "game_task1"

        task1_box.config(bg=TASK_BLOCK_BG)
        task2_box.config(bg=TASK_BLOCK_BG)
        task3_box.config(bg=TASK_BLOCK_BG)

        make_task_content(
            t["task1_title"],
            t["task1_instructions"],
            t["task1_hint"]
        )

        btn_task1 = Button(TASK1_PIN, pull_up=True)
        btn_task1.when_pressed = on_task1_pressed
        root.btn_task1 = btn_task1

    def show_task2():
        root.screen = "game_task2"

        make_task_content(
            t["task2_title"],
            t["task2_instructions"],
            t["task2_hint"]
        )

        status_label = tk.Label(
            content_frame,
            text=t["task2_not_connected"],
            font=font(14, bold=True),
            bg="white",
            fg="red"
        )
        status_label.pack(pady=int(4 * scale))

        try:
            adc3 = MCP3008(channel=TASK2_ADC_CHANNEL)
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

        # GPIO18 stays ON always

        led_task2.on()

        def check_connection():
            if not status_label.winfo_exists():
                return

            if not hasattr(root, "adc3") or root.adc3 != adc3:
                return

            try:
                ad3_value = read_adc_average(adc3)
            except Exception as e:
                print("ADC read error:", e)
                return

            print("Game Task 2 AD3:", round(ad3_value, 3))

            resistor_connected = ad3_value > TASK2_ADC_THRESHOLD

            if resistor_connected:
                status_label.config(
                    text=t["task2_connected"],
                    font=font(17, bold=True),
                    fg="green",
                    bg="white"
                )

                if not root.task2_done:
                    root.task2_done = True
                    task2_box.config(bg=TASK_DONE_BG)

                    root.after(
                        2000,
                        lambda: (root.cleanup_gpio(), show_task3())
                    )
                    return

            else:
                status_label.config(
                    text=t["task2_not_connected"],
                    font=font(17, bold=True),
                    fg="red",
                    bg="white"
                )

            root.after(300, check_connection)

        check_connection()

    def show_task3():
        root.screen = "game_task3"

        make_task_content(
            t["task3_title"],
            t["task3_instructions"],
            t["task3_hint"]
        )

        tk.Label(
            content_frame,
            text=t["brightness"],
            font=font(14, bold=True),
            bg="white"
        ).pack(pady=(int(4 * scale), int(3 * scale)))

        bar_width_total = max(220, int(screen_width * 0.30))
        bar_height = max(24, int(30 * scale))

        bar_canvas = tk.Canvas(
            content_frame,
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

        led_task3 = PWMLED(LED_PIN)
        led_task3.value = 0
        root.led_task3 = led_task3

        sig_a = Button(ROT_A_PIN, pull_up=True)
        sig_b = Button(ROT_B_PIN, pull_up=True)

        root.sig_a = sig_a
        root.sig_b = sig_b

        brightness = [0]
        reached_full = [False]
        returned_to_zero = [False]
        task3_completed = [False]

        def adjust_brightness():
            if sig_b.is_pressed:
                brightness[0] = min(1, brightness[0] + 0.05)
            else:
                brightness[0] = max(0, brightness[0] - 0.05)

            led_task3.value = brightness[0]

            bar_width = x1 + ((x2 - x1) * brightness[0])
            bar_canvas.coords(fill_bar, x1, y1, bar_width, y2)

            print("Brightness:", brightness[0])

            if brightness[0] >= 1:
                reached_full[0] = True

            if reached_full[0] and brightness[0] <= 0.0:
                returned_to_zero[0] = True

            if reached_full[0] and returned_to_zero[0] and not task3_completed[0]:
                task3_completed[0] = True
                root.task3_done = True
                task3_box.config(bg=TASK_DONE_BG)

                root.end_time = time.time()
                total_time = root.end_time - root.start_time

                player_name = getattr(root, "player_name", "Player")
                game_day = getattr(root, "game_day", "1")

                save_result(player_name, total_time, game_day)

                stop_timer()
                timer_label.pack_forget()

                root.cleanup_gpio()

                show_result_screen(player_name, total_time)

        sig_a.when_pressed = adjust_brightness

    show_description()