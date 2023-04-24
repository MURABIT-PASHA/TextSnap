import sys

import pytesseract
from PyQt5 import QtWidgets, QtCore, QtGui
from PIL import ImageGrab
import numpy as np
import cv2
import tkinter as tk
from tkinter.constants import LEFT, RIGHT
import tkinter.messagebox as mbox


class SnipTool(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Capture the screen...')
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        pytesseract.pytesseract.tesseract_cmd = '.\Tesseract-OCR\tesseract.exe'

        text = pytesseract.image_to_string(gray, lang='tur')
        window.close()
        my_gui = GUI(text)
        my_gui.start()


class GUI:
    def __init__(self, prompt: str):
        self.root = tk.Tk()
        self.root.title("TextSnap")
        self.root.geometry("1024x576")
        self.root.iconbitmap('./icon.ico')
        self.prompt = prompt
        self.answer = None
        self.text_box_1 = tk.Text(self.root, height=20, width=50)
        self.text_box_1.pack(pady=10)

        self.correction_button = tk.Button(self.root, height=3, width=20, text="Correction", command=self.correction)
        self.correction_button.pack(pady=10, side=LEFT)

        self.copy_button = tk.Button(self.root, height=3, width=20, text="Copy", command=self.copy_to_clipboard)
        self.copy_button.pack(pady=10, side=LEFT, padx=250)

        self.create_button = tk.Button(self.root, height=3, width=20, text="New One", command=self.create)
        self.create_button.pack(pady=10, side=RIGHT)

    def correction(self):
        self.prompt = self.prompt.replace("\n", " ")
        self.text_box_1.delete('1.0', tk.END)
        self.text_box_1.insert(tk.END, self.prompt)

    def create(self):
        self.root.quit()

    def copy_to_clipboard(self):
        content = self.text_box_1.get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            mbox.showinfo("Başarılı", "Metin kopyalandı!")
        else:
            mbox.showerror("Hata", "Kopyalanacak metin yok!")

    def start(self):
        self.text_box_1.insert(tk.END, self.prompt)
        self.root.mainloop()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SnipTool()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())
