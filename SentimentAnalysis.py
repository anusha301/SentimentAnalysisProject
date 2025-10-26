import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from textblob import TextBlob
import pytesseract
from PyPDF2 import PdfReader
from PIL import Image, ImageTk
import os


# Specify the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class SentimentAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sentiment Analysis Tool")
        self.root.geometry("700x600")
        self.root.configure(bg='#EFE4B0')

        # Load images
        self.positive_image = self.load_image("positive1.png")
        self.negative_image = self.load_image("negative.png")
        self.neutral_image = self.load_image("neutral.png")

        # Title label
        self.title_label = tk.Label(self.root, text="Sentiment Analysis Tool", font=("Helvetica", 24, "bold"), bg='#22B14C', fg='#ffffff', bd=5, relief="solid")
        self.title_label.pack(pady=20)

        # Frame for input
        self.input_frame = tk.Frame(self.root, bg='#202569', bd=5)
        self.input_frame.pack(pady=10)

        self.input_label = tk.Label(self.input_frame, text="Enter text or choose a file:", font=("Helvetica", 14), bg='#202569', fg='#ffffff')
        self.input_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.text_entry = tk.Text(self.input_frame, height=8, width=60, font=("Helvetica", 12), bg='#ffffff', bd=3)
        self.text_entry.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        # File options buttons
        self.file_button_frame = tk.Frame(self.root, bg='#202569')
        self.file_button_frame.pack(pady=10)

        self.load_text_button = tk.Button(self.file_button_frame, text="Load Text File", command=self.load_text_file, font=("Helvetica", 12), bg='#2196f3', fg='#ffffff')
        self.load_text_button.grid(row=0, column=0, padx=5, pady=5)

        self.load_pdf_button = tk.Button(self.file_button_frame, text="Load PDF File", command=self.load_pdf_file, font=("Helvetica", 12), bg='#2196f3', fg='#ffffff')
        self.load_pdf_button.grid(row=0, column=1, padx=5, pady=5)

        self.load_image_button = tk.Button(self.file_button_frame, text="Load Image File", command=self.load_image_file, font=("Helvetica", 12), bg='#2196f3', fg='#ffffff')
        self.load_image_button.grid(row=0, column=2, padx=5, pady=5)

        # Analyze button
        self.analyze_button = tk.Button(self.root, text="Analyze Sentiment", command=self.analyze_sentiment, font=("Helvetica", 14), bg='#ff5722', fg='#ffffff', bd=2, highlightbackground='#961106')
        self.analyze_button.pack(pady=20)

        # Result frame
        self.result_frame = tk.Frame(self.root, bg='#ffffff', bd=5)
        self.result_frame.pack(pady=10)

        self.result_label = tk.Label(self.result_frame, text="Polarity:", font=("Helvetica", 14, "bold"), bg='#ffffff', fg='#000000')
        self.result_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.polarity_label = tk.Label(self.result_frame, text="", font=("Helvetica", 14), bg='#ffffff', fg='#000000')
        self.polarity_label.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.subjectivity_label = tk.Label(self.result_frame, text="", font=("Helvetica", 14), bg='#ffffff', fg='#000000')
        self.subjectivity_label.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        self.sentiment_label = tk.Label(self.result_frame, text="", font=("Helvetica", 14), bg='#ffffff', fg='#000000')
        self.sentiment_label.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        self.sentiment_image_label = tk.Label(self.result_frame, image=None, bg='#ffffff')
        self.sentiment_image_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def load_image(self, file_path):
        try:
            return tk.PhotoImage(file=file_path)
        except Exception as e:
            messagebox.showerror("Image Load Error", f"Failed to load image {file_path}: {e}")
            return None

    def load_text_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                text = file.read()
            self.text_entry.delete("1.0", tk.END)
            self.text_entry.insert(tk.END, text)

    def load_pdf_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            self.text_entry.delete("1.0", tk.END)
            self.text_entry.insert(tk.END, text)

    def load_image_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            text = pytesseract.image_to_string(Image.open(file_path))
            self.text_entry.delete("1.0", tk.END)
            self.text_entry.insert(tk.END, text)

    def analyze_sentiment(self):
        # Get the text from the entry widget
        user_text = self.text_entry.get("1.0", tk.END).strip()
        if not user_text:
            messagebox.showwarning("Input Error", "Please enter some text or load a file.")
            return

        # Analyze the sentiment
        analysis = TextBlob(user_text)
        sentiment = analysis.sentiment

        # Display the result
        self.polarity_label.config(text=f"{sentiment.polarity:.2f}")
        self.subjectivity_label.config(text=f"{sentiment.subjectivity:.2f}")
        if sentiment.polarity > 0:
            sentiment_text = "Positive 😊"
            self.sentiment_label.config(text=sentiment_text, foreground='green')
            self.sentiment_image_label.config(image=self.positive_image)
        elif sentiment.polarity < 0:
            sentiment_text = "Negative 😞"
            self.sentiment_label.config(text=sentiment_text, foreground='red')
            self.sentiment_image_label.config(image=self.negative_image)
        else:
            sentiment_text = "Neutral 😐"
            self.sentiment_label.config(text=sentiment_text, foreground='blue')
            self.sentiment_image_label.config(image=self.neutral_image)

if __name__ == "__main__":
    root = tk.Tk()

    app = SentimentAnalyzerApp(root)
    root.mainloop()
