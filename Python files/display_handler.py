import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import state
import handler



class Display_Handler(handler.Handler):
    darkened = False

    def __init__(self) -> None:
        self.STATUS.change("Starting display")
        #initialize display
        i2c = busio.I2C(board.SCL, board.SDA)
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
        self.oled.fill(0)
        self.oled.show()

        #hooking into states
        self.PM25.hook(self.set_PM25)
        self.STATUS.hook(self.set_status)
        self.MODE.hook(self.set_mode)
    
    def refresh(self) -> None:
        if self.darkened: return
        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)

        font = ImageFont.load_default()
        text = f"{self.STATUS.variable}\nPM25: {self.PM25.variable}\nMode: {self.MODE.variable}"
        draw.text((0.0,0.0),text,font=font, fill=255, spacing=0)

        self.oled.image(image)
        self.oled.show()
    
    def restart(self) -> None:
        self.darkened = False
        self.refresh()
    
    def darken(self) -> None:
        self.darkened = True
        i2c = busio.I2C(board.SCL, board.SDA)
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
        self.oled.fill(0)
        self.oled.show()
    
    def set_PM25(self, PM25):
        #self.PM25 = PM25
        self.refresh()
    
    def set_status(self, status):
        #self.status = status
        self.refresh()
    
    def set_mode(self, mode):
        #self.mode = mode
        self.refresh()

def main():
    Display_Handler()

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("Keyboard interrupt")