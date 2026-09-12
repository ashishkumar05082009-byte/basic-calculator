import tkinter as tk
from tkinter import messagebox
import random

class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        self.user_score = 0
        self.computer_score = 0
        self.choices = ['Rock', 'Paper', 'Scissors']
        
        self.setup_ui()
    
    def setup_ui(self):
        title = tk.Label(self.root, text="Rock Paper Scissors", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        self.score_label = tk.Label(self.root, text="You: 0  |  Computer: 0", font=("Arial", 14))
        self.score_label.pack(pady=10)
        
        self.result_label = tk.Label(self.root, text="Make your choice!", font=("Arial", 16), fg="blue")
        self.result_label.pack(pady=20)
        
        self.user_choice_label = tk.Label(self.root, text="Your choice: ", font=("Arial", 12))
        self.user_choice_label.pack(pady=5)
        
        self.computer_choice_label = tk.Label(self.root, text="Computer choice: ", font=("Arial", 12))
        self.computer_choice_label.pack(pady=5)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=30)
        
        for choice in self.choices:
            btn = tk.Button(button_frame, text=choice, font=("Arial", 14, "bold"),
                          width=10, height=2,
                          command=lambda c=choice: self.play(c))
            btn.pack(side=tk.LEFT, padx=10)
        
        reset_btn = tk.Button(self.root, text="Reset Score", font=("Arial", 12),
                            command=self.reset_score, bg="#ffcccc")
        reset_btn.pack(pady=20)
    
    def play(self, user_choice):
        computer_choice = random.choice(self.choices)
        
        self.user_choice_label.config(text=f"Your choice: {user_choice}")
        self.computer_choice_label.config(text=f"Computer choice: {computer_choice}")
        
        if user_choice == computer_choice:
            result = "It's a Tie!"
            color = "orange"
        elif (user_choice == 'Rock' and computer_choice == 'Scissors') or \
             (user_choice == 'Paper' and computer_choice == 'Rock') or \
             (user_choice == 'Scissors' and computer_choice == 'Paper'):
            result = "You Win! 🎉"
            color = "green"
            self.user_score += 1
        else:
            result = "Computer Wins! 😢"
            color = "red"
            self.computer_score += 1
        
        self.result_label.config(text=result, fg=color)
        self.score_label.config(text=f"You: {self.user_score}  |  Computer: {self.computer_score}")
    
    def reset_score(self):
        self.user_score = 0
        self.computer_score = 0
        self.score_label.config(text="You: 0  |  Computer: 0")
        self.result_label.config(text="Make your choice!", fg="blue")
        self.user_choice_label.config(text="Your choice: ")
        self.computer_choice_label.config(text="Computer choice: ")

if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissors(root)
    root.mainloop()