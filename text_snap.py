import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.lang import Builder
from kivy.graphics.texture import Texture
import os

from win32api import Sleep

Window.hide()
os.environ['KIVY_NO_ARGS'] = '1'

Builder.load_file("./text_snap.kv")


class SnipTool(App):
    def __init__(self, captured_image, **kwargs):
        super().__init__(**kwargs)
        self.start_pos = [0, 0]
        self.end_pos = [0, 0]
        self.widget = None
        self.is_drawing = False
        self.desktop_image = captured_image
        self.bg_path = self.save_path(self.desktop_image)

    def build(self):
        self.title = 'TextSnap'
        self.icon = './icon.ico'
        layout = Builder.load_file("./text_snap.kv")
        background_image = layout.ids.background_image
        texture = self.convert_to_texture(self.desktop_image)
        background_image.texture = texture
        return layout

    def save_path(self, image):
        image_filename = "bg_image.jpg"
        cv2.imwrite(image_filename, image)
        return image_filename

    def convert_to_texture(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 0)
        h, w, _ = image.shape
        image_with_alpha = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
        texture = Texture.create(size=(w, h))
        texture.blit_buffer(image_with_alpha.flatten(), colorfmt='rgba', bufferfmt='ubyte')
        return texture

    def on_touch_down(self, touch):
        if not self.is_drawing:
            self.is_drawing = True
            self.start_pos[0] = touch.pos[0]
            self.start_pos[1] = Window.size[1] - touch.pos[1]
            self.end_pos[0] = self.start_pos[0]
            self.end_pos[1] = self.start_pos[1]

    def on_touch_move(self, touch):
        if self.is_drawing:
            self.widget.canvas.clear()
            with self.widget.canvas:
                Color(rgba=(1, 1, 1, .1))
                Rectangle(pos=(self.start_pos[0], Window.size[1] - self.start_pos[1]),
                          size=(touch.pos[0] - self.start_pos[0], self.start_pos[1] - self.end_pos[1]))
            self.end_pos[0] = touch.pos[0]
            self.end_pos[1] = Window.size[1] - touch.pos[1]

    def on_touch_up(self, touch):
        if self.is_drawing:
            self.is_drawing = False
            with self.widget.canvas:
                Rectangle(pos=(self.start_pos[0], Window.size[1] - self.start_pos[1]),
                          size=(touch.pos[0] - self.start_pos[0], self.start_pos[1] - self.end_pos[1]))
            x1 = min(self.start_pos[0], self.end_pos[0])
            y1 = min(self.start_pos[1], self.end_pos[1])
            x2 = max(self.start_pos[0], self.end_pos[0])
            y2 = max(self.start_pos[1], self.end_pos[1])
            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))

            img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.stop()
            Window.set_system_cursor('arrow')
            self.root_window.fullscreen = False
            from gui import GUI
            GUI(gray).run()

    def on_start(self):
        Window.show()
        self.root_window.fullscreen = 'auto'
        Window.set_system_cursor('crosshair')
        self.widget = self.root.ids.rectangle
        self.widget.on_touch_down = self.on_touch_down
        self.widget.on_touch_move = self.on_touch_move
        self.widget.on_touch_up = self.on_touch_up


def capture_desktop():
    screenshot = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return image


if __name__ == '__main__':
    try:
        Sleep(500)
        get_image = capture_desktop()
        SnipTool(captured_image=get_image).run()
    except cv2.error:
        exit(0)
