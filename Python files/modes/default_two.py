from . import led_mode
import numpy as np

x_points = np.linspace(0,550, num=2, endpoint=False)
y_points = np.linspace(0, 0.863, num=2, endpoint=False)

def led_function(Led_Handler):
        p=np.interp(Led_Handler.PM25.variable, x_points, y_points)
        rand_list = np.random.choice([False, True], size=(Led_Handler.n_dots,), p=[1-p, p])

        for i in range(Led_Handler.n_dots):
            if rand_list[i]:
                Led_Handler.dots[i] = (255, 255, 255)
            else:
                Led_Handler.dots[i] = (0, 0, 0)
        Led_Handler.dots.show()

mode = led_mode.Led_Mode(
    name="default two",
    pace=1,
    led_function = led_function
)