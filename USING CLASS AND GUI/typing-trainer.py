import tkinter as tk
from tkinter import messagebox
import json
import time


class TypingTrainer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Typing Speed Test")
        self.geometry("600x400")

        self.text_samples = ["Sample text 1", "Sample text 2", "Sample text 3"]
        self.current_sample_index = 0
        self.current_word_index = 0
        self.current_sample = ""
        self.user_profile = ""
        self.high_scores = {}  # Store high scores for all users

        self.load_high_scores()

        self.username_label = tk.Label(self, text="Enter your username:")
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        self.start_button = tk.Button(self, text="Start Typing Test", command=self.start_typing_test)
        self.start_button.pack(pady=10)

        self.sample_text_display = tk.Label(self, text="", font=("Arial", 12), justify="center", wraplength=500)
        self.sample_text_display.pack(pady=20)

        self.typing_area = tk.Entry(self, font=("Arial", 14))
        self.typing_area.pack(pady=10)

        self.result_label = tk.Label(self, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.high_score_label = tk.Label(self, text="", font=("Arial", 14))
        self.high_score_label.pack(pady=10)

        self.start_time = None
        self.end_time = None

    def load_high_scores(self):
        try:
            with open("high_scores.json", "r") as file:
                self.high_scores = json.load(file)
        except FileNotFoundError:
            pass

    def save_high_scores(self):
        with open("high_scores.json", "w") as file:
            json.dump(self.high_scores, file)

    def start_typing_test(self):
        self.user_profile = self.username_entry.get()
        if not self.user_profile:
            messagebox.showerror("Error", "Please enter a username.")
            return

        if self.current_sample_index != len(self.text_samples):
            self.current_sample = self.text_samples[self.current_sample_index]
            self.sample_text_display.config(text=self.current_sample)
            self.typing_area.delete(0, tk.END)
            self.result_label.config(text="Type the text below:")
            self.typing_area.bind("<Return>", self.check_typing)
            self.start_time = time.time()
        else:
            self.result_label.config(text="Typing test completed!")
            self.end_time = time.time()
            elapsed_time = self.end_time - self.start_time
            total_words = len(self.current_sample.split()) * self.current_sample_index + self.current_word_index
            words_per_minute = int((total_words / elapsed_time) * 60)

            if self.user_profile not in self.high_scores or words_per_minute > self.high_scores[self.user_profile]:
                self.high_scores[self.user_profile] = words_per_minute
                self.save_high_scores()

            self.current_word_index = 0
            self.current_sample_index = 0
            self.load_high_scores()
            messagebox.showinfo("Typing Test Result", f"Your score: {words_per_minute} words per minute")
            self.high_score_label.config(text=f"High Score: {self.high_scores.get(self.user_profile, 0)}")

    def check_typing(self, event):
        typed_text = self.typing_area.get()
        expected_word = self.current_sample.split()[self.current_word_index]

        if typed_text.strip() == expected_word:
            self.typing_area.delete(0, tk.END)
            self.current_word_index += 1

            if self.current_word_index == len(self.current_sample.split()):
                self.current_word_index = 0
                self.current_sample_index += 1
                self.start_typing_test()
        else:
            self.result_label.config(text="Incorrect word. Try again.")


if __name__ == "__main__":
    app = TypingTrainer()
    app.mainloop()
