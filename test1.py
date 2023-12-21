import os
import tkinter as tk
from tkinter import filedialog, simpledialog
import pygame

class SoundboardApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Soundboard App")
        self.master.geometry("800x600")

        self.buttons = []
        self.sound_files = []

        # Initialize Pygame
        pygame.mixer.init()

        # Load sound files from the saved file
        self.load_sound_files()

        # Create UI elements
        self.create_widgets()

        # Bind the closing event to save sound files
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Button to add sound files
        add_button = tk.Button(self.master, text="Add Sound", command=self.add_sound, bg="#4CAF50", fg="white", padx=10, pady=5)
        add_button.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

        # Create buttons for each sound in a grid layout
        row, col = 1, 0
        for i in range(9):
            button = tk.Button(self.master, text=f"Sound {i+1}", command=lambda idx=i: self.play_sound(idx),
                               bg="#2196F3", fg="white", padx=20, pady=15, font=("Helvetica", 10, "bold"))
            button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.buttons.append(button)

            col += 1
            if col > 2:
                col = 0
                row += 1

        # Configure grid weights to make buttons expand with the window
        for i in range(3):
            self.master.grid_columnconfigure(i, weight=1)
        for i in range(row):
            self.master.grid_rowconfigure(i, weight=1)

        # Update button names based on loaded sound files
        for idx, button in enumerate(self.buttons):
            if idx < len(self.sound_files):
                title = self.sound_files[idx][1]  # Custom name stored at index 1
                button.configure(text=f"Sound {idx + 1}\n{title}")

    def add_sound(self):
        file_path = filedialog.askopenfilename(filetypes=[("Sound files", "*.wav;*.mp3")])

        if file_path:
            custom_name = self.ask_for_custom_name()
            self.sound_files.append((file_path, custom_name))
            idx = len(self.sound_files) - 1
            title = self.sound_files[idx][1]  # Custom name stored at index 1
            self.buttons[idx].configure(text=f"Sound {idx + 1}\n{title}")

            # Save the updated sound files to the file
            self.save_sound_files()

    def play_sound(self, idx):
        if 0 <= idx < len(self.sound_files):
            pygame.mixer.music.load(self.sound_files[idx][0])  # File path stored at index 0
            pygame.mixer.music.play()

    def on_closing(self):
        # Save sound files when closing the program
        self.save_sound_files()
        self.master.destroy()

    def save_sound_files(self):
        with open("sound_files.txt", "w") as file:
            for sound_file in self.sound_files:
                file.write(f"{sound_file[0]}\t{sound_file[1]}\n")

    def load_sound_files(self):
        try:
            with open("sound_files.txt", "r") as file:
                lines = file.readlines()
                self.sound_files = [tuple(line.strip().split('\t')) for line in lines]
        except FileNotFoundError:
            pass  # File doesn't exist, ignore and use an empty list

    def ask_for_custom_name(self):
        return simpledialog.askstring("Custom Name", "Enter a custom name for the sound:")

if __name__ == "__main__":
    root = tk.Tk()
    app = SoundboardApp(root)
    root.mainloop()
