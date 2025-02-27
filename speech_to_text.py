"""import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import threading
from bag_of_words import load_bag_of_words
from knowledge_graphs import query_similar_terms
from Main import detect_sensitive_data

# Load Bag of Words
bag_of_words = load_bag_of_words()

def start_speech_recognition():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            status_label.config(text="Processing text...")
            text_area.insert(tk.END, text + "\n")
            process_text(text)
        except sr.WaitTimeoutError:
            status_label.config(text="No speech detected. Try again.")
        except sr.UnknownValueError:
            status_label.config(text="Could not understand audio.")
        except sr.RequestError:
            status_label.config(text="Speech Recognition service unavailable.")

def process_text(text):
    similar_terms = query_similar_terms(text)
    detected_data = detect_sensitive_data_from_text(text)
    result = "Similar Terms:\n" + '\n'.join(f"{t['term']} ({t['category']})" for t in similar_terms)
    result += "\n\nDetected Sensitive Data:\n" + '\n'.join(f"{d['word']} ({d['category']})" for d in detected_data)
    text_area.insert(tk.END, "\n" + result + "\n")

def detect_sensitive_data_from_text(text):
    output_file = "speech_sensitive_data.docx"  # Temporary file to store detected results
    with open("speech_text.txt", "w", encoding="utf-8") as file:
        file.write(text)  # Save speech-to-text output to a temporary file

    detect_sensitive_data("speech_text.txt", output_file)  # Call with proper arguments
    return []  # Avoid breaking the flow; actual results are saved in the DOCX file


def on_speech_button_click():
    threading.Thread(target=start_speech_recognition).start()

# GUI Setup
root = tk.Tk()
root.title("Speech-to-Text Sensitive Data Detector")
root.geometry("800x600")

status_label = tk.Label(root, text="Press the button to speak", font=("Times Roman", 12))
status_label.pack(pady=10)

speech_button = tk.Button(root, text="Start Speech Recognition", command=on_speech_button_click, font=("Times Roman", 12))
speech_button.pack(pady=10)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, font=("Times Roman", 10))
text_area.pack(pady=10)

root.mainloop"""


""" PyQT """
import sys
import speech_recognition as sr
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QLabel
from PyQt6.QtGui import QTextCursor
from bag_of_words import load_bag_of_words
from knowledge_graphs import query_similar_terms
from Main import detect_sensitive_data  # Uses your existing detection system

class SpeechToTextApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the GUI layout"""
        self.setWindowTitle("Speech-to-Text Sensitive Data Detector")
        self.setGeometry(100, 100, 600, 400)

        # UI Elements
        self.label = QLabel("Press the button and speak", self)
        self.text_area = QTextEdit(self)
        self.text_area.setPlaceholderText("Detected text will appear here...")

        self.speech_button = QPushButton("Start Speech Recognition", self)
        self.speech_button.clicked.connect(self.start_speech_recognition)

        self.detect_button = QPushButton("Detect Sensitive Data", self)
        self.detect_button.clicked.connect(self.detect_sensitive_info)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_area)
        layout.addWidget(self.speech_button)
        layout.addWidget(self.detect_button)
        self.setLayout(layout)

    def start_speech_recognition(self):
        """Capture speech input and display recognized text"""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.label.setText("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce background noise
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=20)  
                text = recognizer.recognize_google(audio)
                self.text_area.setText(text)
                self.label.setText("Processing completed.")
            except sr.WaitTimeoutError:
                self.label.setText("No speech detected. Try again.")
            except sr.UnknownValueError:
                self.label.setText("Could not understand audio.")
            except sr.RequestError:
                self.label.setText("Speech Recognition service unavailable.")

    def detect_sensitive_info(self):
        """Detect sensitive data in the recognized text"""
        text = self.text_area.toPlainText().strip()
        if not text:
            self.label.setText("No text to analyze.")
            return

        # Process using your existing detection system
        output_file = "speech_sensitive_data.docx"
        with open("speech_text.txt", "w", encoding="utf-8") as file:
            file.write(text)

        # Call your existing sensitive data detection function
        detected_data = detect_sensitive_data("speech_text.txt", output_file)

        # Display results in the UI
        result = "\nDetected Sensitive Data:\n" + "\n".join(f"{d['word']} ({d['category']})" for d in detected_data)
        self.text_area.insertPlainText("\n\n" + result)
        self.text_area.moveCursor(QTextCursor.MoveOperation.End)
        self.label.setText("Analysis completed.")

# Run the PyQt Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeechToTextApp()
    window.show()
    sys.exit(app.exec())
