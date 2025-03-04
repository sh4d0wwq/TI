from sys import argv, exit
from math import gcd
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QComboBox, QFileDialog

ALPHABET_EN = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET_RU = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def is_coprime(a, b):
    return gcd(a, b) == 1

def decimation_cipher(text, key, decrypt=False):
    text = text.upper()
    result = ""
    m = len(ALPHABET_EN)
    if not is_coprime(key, m):
        return "Ошибка: Ключ и размер алфавита должны быть взаимно простыми числами."
    inv_key = pow(key, -1, m) if decrypt else key
    for char in text:
        if char in ALPHABET_EN:
            idx = ALPHABET_EN.index(char)
            new_idx = (idx * inv_key) % m
            result += ALPHABET_EN[new_idx]
        else:
            result += char
    return result

def vigenere_cipher(text, key, decrypt=False):
    text = text.upper()
    key = ''.join([c for c in key.upper() if c in ALPHABET_RU])
    result = ""
    key_length = len(key)
    key_indices = [ALPHABET_RU.index(k) for k in key]
    i = 0
    for _, char in enumerate(text):
        if char in ALPHABET_RU:
            text_idx = ALPHABET_RU.index(char)
            key_idx = key_indices[i % key_length]
            new_idx = (text_idx - key_idx) % len(ALPHABET_RU) if decrypt else (text_idx + key_idx) % len(ALPHABET_RU)
            result += ALPHABET_RU[new_idx]
            i += 1
        else:
            result += char
    return result

class CipherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Шифрование текста")
        self.setGeometry(100, 100, 480, 270)

        self.layout = QVBoxLayout()

        self.text_input = QTextEdit()
        self.layout.addWidget(QLabel("Введите текст:"))
        self.layout.addWidget(self.text_input)

        self.load_file_button = QPushButton("Загрузить из файла")
        self.load_file_button.clicked.connect(self.load_from_file)
        self.layout.addWidget(self.load_file_button)

        self.language_selector = QComboBox()
        self.language_selector.addItems(['Алгоритм "децимации"', "Шифр Виженера"])
        self.layout.addWidget(self.language_selector)

        self.key_input = QLineEdit()
        self.layout.addWidget(QLabel("Ключ:"))
        self.layout.addWidget(self.key_input)

        self.encrypt_button = QPushButton("Зашифровать")
        self.encrypt_button.clicked.connect(self.encrypt_text)
        self.layout.addWidget(self.encrypt_button)
        
        self.decrypt_button = QPushButton("Расшифровать")
        self.decrypt_button.clicked.connect(self.decrypt_text)
        self.layout.addWidget(self.decrypt_button)
        
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.layout.addWidget(QLabel("Результат:"))
        self.layout.addWidget(self.result_output)

        self.save_button = QPushButton("Сохранить в файл")
        self.save_button.clicked.connect(self.save_file)
        self.layout.addWidget(self.save_button)
        
        self.setLayout(self.layout)
    
    def load_from_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "Текстовые файлы (*.txt);;Все файлы (*)")
        if file_name:
            with open(file_name, "r", encoding="utf-8") as file:
                self.text_input.setText(file.read())
    
    def encrypt_text(self):
        self.process_text(decrypt=False)
    
    def decrypt_text(self):
        self.process_text(decrypt=True)

    def save_file(self, result):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить результат", "", "Текстовые файлы (*.txt);;Все файлы (*)")
        if file_name:
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(result)

    
    def process_text(self, decrypt):
        text = self.text_input.toPlainText()
        language = self.language_selector.currentIndex()
        key = self.key_input.text()

        if language == 0: 
            filtered_key = ''.join([c for c in key if c.isdigit()])
            if not filtered_key:
                result = "Ошибка: Ключ должен содержать хотя бы одну цифру."
                self.result_output.setText(result)
                return
            else:
                try:
                    key = int(filtered_key)
                    result = decimation_cipher(text, key, decrypt)
                except ValueError:
                    result = "Ошибка: Ключ должен быть числом."
                    self.result_output.setText(result)
                    return
        else: 
            key = ''.join([c for c in key.upper() if c in ALPHABET_RU])
            if key:
                result = vigenere_cipher(text, key, decrypt)
            else:
                result = "Ошибка: Ключ должен содержать хотя бы одну русскую букву."
                self.result_output.setText(result)
                return 
        
        self.result_output.setText(result)

if __name__ == "__main__":
    app = QApplication(argv)
    window = CipherApp()
    window.show()
    exit(app.exec())
