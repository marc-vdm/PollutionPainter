import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont



class display_handler():
    PM25 = 0
    status = "Booting"
    mode = "Standard"

    def __init__(self) -> None:
        #initialize display
        i2c = busio.I2C(board.SCL, board.SDA)
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
        self.oled.fill(0)
        self.oled.show()
        self.refresh()
    
    def refresh(self) -> None:
        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)

        font = ImageFont.load_default()
        text = f"PM25: {self.PM25}\nStatus: {self.status}\nMode: {self.mode}"
        draw.text((0.0,0.0),text,font=font, fill=255, spacing=0)

        self.oled.image(image)
        self.oled.show()




def main():
    display_handler()

    
    

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("Keyboard interrupt")