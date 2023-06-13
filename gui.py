from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.clipboard import Clipboard
from kivy.core.audio import SoundLoader
from gtts import gTTS
from deep_translator import GoogleTranslator
import pytesseract


class GUI(MDApp):
    def __init__(self, gray, **kwargs):
        super().__init__(**kwargs)
        pytesseract.pytesseract.tesseract_cmd = '.\\Tesseract-OCR\\tesseract.exe'
        self.screen = Builder.load_file('gui.kv')
        self.language = "tr"
        self.translate_language = "en"
        self.tesseract_language = "tur"
        self.gray = gray
        self.menu_items = ListProperty()
        self.language_items = ListProperty()
        self.prompt = self.get_prompt()
        self.prompter = self.screen.ids.text_field
        self.prompter.text = self.prompt

    def get_prompt(self) -> str:
        return pytesseract.image_to_string(self.gray, lang=self.tesseract_language)

    def open_language_menu(self):
        self.menu_items = [
            {
                "text": "Türkçe",
                "height": dp(50),
                "viewclass": "OneLineListItem",
                "on_release": lambda: set_item("tr", "Türkçe"),
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
            if self.language == "tr":
                self.tesseract_language = "tur"
            self.prompter.text = self.get_prompt()
            dropdown_menu.dismiss()

    def copy_to_clipboard(self):
        Clipboard.copy(self.prompter.text)

    def simplify_text(self):
        self.prompter.text = self.prompt.replace("\n", " ")

    def translate_text(self):
        self.language_items = [
            {
                "text": "Türkçe",
                "height": dp(50),
                "viewclass": "OneLineListItem",
                "on_release": lambda: set_lang("tr", "Türkçe"),
            },
            {
                "text": "English",
                "height": dp(50),
                "viewclass": "OneLineListItem",
                "on_release": lambda: set_lang("en", "English"),
            }
        ]
        dropdown_menu = MDDropdownMenu(
            caller=self.root.ids.translation_button, items=self.language_items, width_mult=3,
        )
        dropdown_menu.open()

        def set_lang(to_lang, to_lang_name):
            button = self.screen.ids.language_button
            button.text = to_lang_name
            self.language = to_lang
            dropdown_menu.dismiss()
            translated_text = GoogleTranslator(source='auto', target=to_lang).translate(self.prompter.text)
            self.prompter.text = translated_text

    def read_text(self):
        tts = gTTS(text=self.prompter.text, lang=self.language)
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
