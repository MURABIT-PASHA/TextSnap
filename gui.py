from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
import pytesseract
import win32clipboard as clipboard
from gtts import gTTS
from kivy.core.audio import SoundLoader
from googletrans import Translator


class GUI(MDApp):
    def __init__(self, gray, **kwargs):
        super().__init__(**kwargs)
        pytesseract.pytesseract.tesseract_cmd = '.\\Tesseract-OCR\\tesseract.exe'
        self.screen = Builder.load_file('gui.kv')
        self.language = "tur"
        self.translate_language = "en"
        self.gray = gray
        self.menu_items = ListProperty()
        self.prompt = self.get_prompt()
        self.prompter = self.screen.ids.text_field
        self.prompter.text = self.prompt

    def get_prompt(self) -> str:
        return pytesseract.image_to_string(self.gray, lang=self.language)

    def open_language_menu(self):
        self.menu_items = [
            {
                "text": "Türkçe",
                "height": dp(50),
                "viewclass": "OneLineListItem",
                "on_release": lambda: set_item("tur", "Türkçe"),
            },
            {
                "text": "English",
                "height": dp(50),
                "viewclass": "OneLineListItem",
                "on_release": lambda: set_item("en", "English"),
            }
        ]
        dropdown_menu = MDDropdownMenu(
            caller=self.root.ids.language_button, items=self.menu_items, width_mult=3,
        )
        dropdown_menu.open()

        def set_item(text_item, lang_text):
            button = self.screen.ids.language_button
            button.text = lang_text
            self.language = text_item
            self.prompter.text = self.get_prompt()
            dropdown_menu.dismiss()

    def copy_to_clipboard(self):
        clipboard.OpenClipboard()
        clipboard.EmptyClipboard()
        clipboard.SetClipboardText(self.prompter.text)
        clipboard.CloseClipboard()

    def simplify_text(self):
        pass

    def translate_text(self):
        translator = Translator()
        translated_text = translator.translate(self.prompter.text, dest=self.translate_language)
        self.prompter.language = translated_text
        self.language = self.translate_language

    def read_text(self):
        tts = gTTS(text=self.prompter.text, lang='tr')
        tts.save("prompter_text.mp3")
        sound = SoundLoader.load('prompter_text.mp3')
        if sound:
            if sound.state == 'play':
                sound.stop()
            else:
                sound.play()

    def add_new(self):
        self.stop()
        from text_snap import NewWindow
        NewWindow()

    def build(self):
        self.title = 'TextSnap'
        self.icon = './icon.ico'
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        return self.screen
