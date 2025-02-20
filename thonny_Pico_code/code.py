import time
import board
import busio
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import usb_cdc  # Biblioteca para comunicação Serial

# Configurar o display OLED
displayio.release_displays()
i2c = busio.I2C(board.GP1, board.GP0)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Criar grupo de elementos
splash = displayio.Group()
display.root_group = splash

# Criar fundo preto
bg_bitmap = displayio.Bitmap(128, 64, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0x000000
bg_sprite = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
splash.append(bg_sprite)

# Criar barra de progresso
bar_width = 100
bar_height = 2
bar_x = 14
bar_y = 50
bar_bitmap = displayio.Bitmap(bar_width, bar_height, 1)
bar_palette = displayio.Palette(1)
bar_palette[0] = 0xFFFFFF
bar_sprite = displayio.TileGrid(bar_bitmap, pixel_shader=bar_palette, x=bar_x, y=bar_y)
splash.append(bar_sprite)

# Criar círculo do progresso
circle_radius = 2
circle_bitmap = displayio.Bitmap(circle_radius * 2, circle_radius * 2, 1)
circle_palette = displayio.Palette(1)
circle_palette[0] = 0xFFFF00
circle_sprite = displayio.TileGrid(circle_bitmap, pixel_shader=circle_palette, x=bar_x, y=bar_y - 1)
splash.append(circle_sprite)

# Criar label para exibir a música
track_label = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=5, y=20)
splash.append(track_label)

# Abrir a comunicação Serial
serial = usb_cdc.data

while True:
    if serial.in_waiting:
        data = serial.readline().decode("utf-8").strip()
        parts = data.split("|")

        if len(parts) == 3:
            track_name, duration, progress = parts
            duration = int(duration)
            progress = int(progress)

            # Atualizar nome da música
            track_label.text = track_name

            # Atualizar a posição do círculo
            progress_ratio = progress / duration
            circle_x = int(bar_x + (progress_ratio * bar_width)) - circle_radius
            circle_sprite.x = circle_x

    time.sleep(0.1)

