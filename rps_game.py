import tkinter as tk
from tkinter import messagebox
import random

class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("420x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        
        self.user_score = 0
        self.computer_score = 0
        self.choices = ['Rock', 'Paper', 'Scissors']
        self.emojis = {'Rock': '🪨', 'Paper': '📄', 'Scissors': '✂️'}
        self.colors = {'Rock': '#e74c3c', 'Paper': '#3498db', 'Scissors': '#f39c12'}
        
        self.build_ui()
    
    def build_ui(self):
        # Title
        tk.Label(self.root, text="🪨  ROCK  PAPER  SCISSORS  ✂️", 
                 font=("Arial", 18, "bold"), fg="#ecf0f1", bg="#2c3e50").pack(pady=20)
        
        # Score board
        score_frame = tk.Frame(self.root, bg="#2c3e50")
        score_frame.pack(pady=10)
        
        self.user_score_lbl = tk.Label(score_frame, text="YOU: 0", font=("Arial", 16, "bold"), 
                                        fg="#2ecc71", bg="#2c3e50", width=12)
        self.user_score_lbl.grid(row=0, column=0, padx=20)
        
        tk.Label(score_frame, text="VS", font=("Arial", 16, "bold"), fg="#95a5a6", bg="#2c3e50").grid(row=0, column=1)
        
        self.comp_score_lbl = tk.Label(score_frame, text="CPU: 0", font=("Arial", 16, "bold"), 
                                        fg="#e74c3c", bg="#2c3e50", width=12)
        self.comp_score_lbl.grid(row=0, column=2, padx=20)
        
        # Result area
        self.result_frame = tk.Frame(self.root, bg="#34495e", relief=tk.RIDGE, bd=3)
        self.result_frame.pack(pady=20, padx=30, fill=tk.X)
        
        self.result_emoji = tk.Label(self.result_frame, text="❓", font=("Segoe UI Emoji", 50), bg="#34495e")
        self.result_emoji.pack(pady=15)
        
        self.result_text = tk.Label(self.result_frame, text="Choose below!", font=("Arial", 18, "bold"), 
                                     fg="#f1c40f", bg="#34495e")
        self.result_text.pack(pady=5)
        
        self.detail_text = tk.Label(self.result_frame, text="", font=("Arial", 12), fg="#bdc3c7", bg="#34495e")
        self.detail_text.pack(pady=(0, 15))
        
        # Choice display
        choice_frame = tk.Frame(self.root, bg="#2c3e50")
        choice_frame.pack(pady=10)
        
        self.user_choice_lbl = tk.Label(choice_frame, text="", font=("Segoe UI Emoji", 30), bg="#2c3e50")
        self.user_choice_lbl.grid(row=0, column=0, padx=30)
        
        tk.Label(choice_frame, text="→", font=("Arial", 20), fg="#7f8c8d", bg="#2c3e50").grid(row=0, column=1)
        
        self.comp_choice_lbl = tk.Label(choice_frame, text="", font=("Segoe UI Emoji", 30), bg="#2c3e50")
        self.comp_choice_lbl.grid(row=0, column=2, padx=30)
        
        # Buttons
        btn_frame = tk.Frame(self.root, bg="#2c3e50")
        btn_frame.pack(pady=25)
        
        for i, choice in enumerate(self.choices):
            self.make_button(btn_frame, choice, i)
        
        # Reset
        tk.Button(self.root, text="🔄 Reset Score", font=("Arial", 11, "bold"),
                  bg="#95a5a6", fg="#2c3e50", activebackground="#7f8c8d",
                  bd=0, padx=20, pady=8, cursor="hand2",
                  command=self.reset).pack(pady=15)
    
    def make_button(self, parent, choice, col):
        color = self.colors[choice]
        emoji = self.emojis[choice]
        
        btn = tk.Button(parent, text=f"{emoji}\n{choice}", font=("Arial", 14, "bold"),
                        fg="white", bg=color, activebackground=self.darken(color),
                        activeforeground="white", bd=0, width=8, height=3,
                        cursor="hand2",
                        command=lambda c=choice: self.play(c))
        btn.grid(row=0, column=col, padx=8)
        
        btn.bind("<Enter>", lambda e: btn.config(bg=self.darken(color)))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
    
    def darken(self, hex_color):
        return {'#e74c3c': '#c0392b', '#3498db': '#2980b9', '#f39c12': '#d35400'}.get(hex_color, hex_color)
    
    def play(self, user):
        comp = random.choice(self.choices)
        
        self.user_choice_lbl.config(text=f"{self.emojis[user]}  You")
        self.comp_choice_lbl.config(text=f"CPU  {self.emojis[comp]}")
        
        if user == comp:
            msg, emoji, color, detail = "DRAW!", "🤝", "#f39c12", f"Both picked {user}"
        elif (user == 'Rock' and comp == 'Scissors') or \
             (user == 'Paper' and comp == 'Rock') or \
             (user == 'Scissors' and comp == 'Paper'):
            msg, emoji, color, detail = "YOU WIN!", "🎉", "#27ae60", f"{user} beats {comp}"
            self.user_score += 1
        else:
            msg, emoji, color, detail = "YOU LOSE!", "😵", "#e74c3c", f"{comp} beats {user}"
            self.computer_score += 1
        
        self.result_frame.config(bg=color)
        self.result_emoji.config(text=emoji, bg=color)
        self.result_text.config(text=msg, fg="white", bg=color)
        self.detail_text.config(text=detail, fg="white", bg=color)
        
        self.user_score_lbl.config(text=f"YOU: {self.user_score}")
        self.comp_score_lbl.config(text=f"CPU: {self.computer_score}")
        
        # Flash back to normal after 150ms
        self.root.after(150, lambda: self.result_frame.config(bg="#34495e"))
        self.root.after(150, lambda: self.result_emoji.config(bg="#34495e"))
        self.root.after(150, lambda: self.result_text.config(bg="#34495e", fg="#f1c40f"))
        self.root.after(150, lambda: self.detail_text.config(bg="#34495e", fg="#bdc3c7"))
    
    def reset(self):
        self.user_score = 0
        self.computer_score = 0
        self.user_score_lbl.config(text="YOU: 0")
        self.comp_score_lbl.config(text="CPU: 0")
        self.user_choice_lbl.config(text="")
        self.comp_choice_lbl.config(text="")
        self.result_frame.config(bg="#34495e")
        self.result_emoji.config(text="❓", bg="#34495e")
        self.result_text.config(text="Choose below!", fg="#f1c40f", bg="#34495e")
        self.detail_text.config(text="", bg="#34495e")

if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissors(root)
    root.mainloop()