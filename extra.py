from gpiozero import MCP3008
from time import sleep

# Test ADC
adc2 = MCP3008(channel=2)
adc3 = MCP3008(channel=3)

while True:
    ad2_value = adc2.value
    ad3_value = adc3.value


    print(
        f"AD2: {ad2_value:.3f}  |   "
        f"AD3: {ad3_value:.3f}"
    )

    sleep(0.5)