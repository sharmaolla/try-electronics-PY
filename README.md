# Electronics Game

Electronics Game is an interactive Raspberry Pi 4 project for learning and practicing basic electronics.
The user completes three hardware tasks using a custom PCB/HAT.

## Game Description

The game has three tasks:

1. **Task 1:** Connect jumper wires between J2 and J3 and press BUTTON1.
2. **Task 2:** Insert a resistor between J4 and J5. The ADC detects the resistor connection and LED2 turns on.
3. **Task 3:** Connect the encoder and rotate it to control LED3 brightness.

In the game mode, the application measures the player's completion time and saves the results.  
The result screen shows the player's time, day rank, overall rank, the TOP 5 day table, and the TOP 5 overall table.

## Hardware Requirements

- Raspberry Pi 4 Starter Kit
- Monitor
- Mouse
- Keyboard
- Custom Try Electronics HAT / PCB with MCP3008 ADC chip soldered
- Jumper wires
- Resistor
- Rotary encoder with 4-wire cable and Grove-style connector
- LEDs, buttons and connection points soldered on the PCB/HAT
- Case, screws and spacers

## Software Requirements

- Raspberry Pi OS
- Python 3
- Tkinter
- GPIO Zero
- Pillow
- SPI enabled (for MCP3008)

## Files Included

```text
main.py
menu.py
task1.py
task2.py
task3.py
game.py

banner.png
task_banner.png
box.png
ready_pcb.png

requirements.txt
README.md
```


## Quick Start

1. Unzip and copy this folder to Raspberry Pi 4.

2. Install required packages:

```bash
sudo apt update
sudo apt install python3-tk python3-gpiozero python3-pil python3-spidev
```

3. Enable SPI for the MCP3008 ADC:

```bash
sudo raspi-config
```

Then choose:

```text
Interface Options -> SPI -> Enable
```

4. Reboot the Raspberry Pi:

```bash
sudo reboot
```

5. Open `main.py` in Thonny.

6. Run `main.py`.

7. Enter the day: `1`, `2` or `3`.

8. Select language and choose individual tasks or run the game.


## Results

Game results are saved automatically in:

```text
players.json
```

To clear all results, delete `players.json` from the project folder.  
A new file will be created automatically when new results are saved.

## Notes

- Keep all `.py` files and `.png` image files in the same folder.
- Task 2 requires SPI to be enabled because it uses the MCP3008 ADC.
- The HAT should be fixed firmly to the Raspberry Pi using screws and spacers for stable GPIO behavior.

