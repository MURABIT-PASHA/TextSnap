from kivy.app import App
from kivy.graphics import Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
import pytesseract


class Scaffold(BoxLayout):
    def __init__(self, app, gray, **kwargs):
        super(Scaffold, self).__init__(**kwargs)
        self.app = app
        self.custom_width = 600
        self.custom_height = 100
        self.orientation = "horizontal"
        self.initial_language = "tur"
        self.prompt = pytesseract.image_to_string(gray, lang='tur')
        first_box = BoxLayout(size=(self.custom_width / 2, self.custom_height), orientation="vertical")
        self.add_widget(first_box)

        # Inside the first box
        first_box_first_box = BoxLayout(size=(self.custom_width / 2, self.custom_height * 3 / 5))
        first_box.add_widget(first_box_first_box)
        text_input = TextInput(text=self.prompt, multiline=True)
        first_box_first_box.add_widget(text_input)

        first_box_second_box = BoxLayout(size_hint=(1, 1 / 3))
        first_box.add_widget(first_box_second_box)
        dropdown = DropDown()

        tr_btn = Button(text='Türkçe', size_hint_y=None, height=44)
        tr_btn.bind(on_release=lambda button_lam: dropdown.select(tr_btn.text))
        dropdown.add_widget(tr_btn)
        en_btn = Button(text='English', size_hint_y=None, height=44)
        en_btn.bind(on_release=lambda button_lam: dropdown.select(en_btn.text))
        dropdown.add_widget(en_btn)
        main_button = Button(text='English')
        main_button.bind(on_release=dropdown.open)
        first_box_second_box.add_widget(main_button)
        dropdown.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))

        # Inside the second box
        second_box = BoxLayout(size_hint=(.5, 1), orientation="vertical")
        self.add_widget(second_box)
        copy_button = Button(text="Copy", size=(self.custom_width / 7, self.custom_height / 5))
        copy_button.canvas.after.add(Color(1, 1, 1, 0.2))
        second_box.add_widget(copy_button)
        simplify_button = Button(text="Simplify", size_hint=(1, 1))
        second_box.add_widget(simplify_button)
        listen_button = Button(text="Listen", size_hint=(1, 1))
        second_box.add_widget(listen_button)
        translate_button = Button(text="Translate", size_hint=(1, 1))
        second_box.add_widget(translate_button)



        # Inside the third box
        third_box = BoxLayout(size_hint=(.5, 1), orientation="vertical")
        self.add_widget(third_box)
        third_box_first_box = BoxLayout()
        third_box.add_widget(third_box_first_box)
        create_button = Button(text="+", size=(100, 200), on_press=self.create)
        third_box_first_box.add_widget(create_button)

    def create(self):
        pass
        # self.app.close()
        # from text_snap import NewWindow
        # window = NewWindow()

class TextSnapApp(App):
    def __init__(self, gray, **kwargs):
        super().__init__(**kwargs)
        self.gray = gray
        pytesseract.pytesseract.tesseract_cmd = '.\\Tesseract-OCR\\tesseract.exe'

    def build(self):
        self.title = 'TextSnap'
        self.icon = './icon.ico'
        return Scaffold(app=self, gray=self.gray)
