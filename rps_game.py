import tkinter as tk
from tkinter import messagebox
import random

class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("✊ Rock Paper Scissors ✂️")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")
        
        self.user_score = 0
        self.computer_score = 0
        self.choices = ['Rock', 'Paper', 'Scissors']
        self.choice_emojis = {'Rock': '✊', 'Paper': '✋', 'Scissors': '✂️'}
        self.choice_colors = {'Rock': '#e74c3c', 'Paper': '#3498db', 'Scissors': '#f39c12'}
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title with gradient effect
        title_frame = tk.Frame(self.root, bg="#1a1a2e")
        title_frame.pack(pady=30)
        
        tk.Label(title_frame, text="✊", font=("Segoe UI Emoji", 48), bg="#1a1a2e").pack(side=tk.LEFT)
        tk.Label(title_frame, text="ROCK PAPER SCISSORS", font=("Segoe UI", 28, "bold"), 
                 fg="#eee", bg="#1a1a2e").pack(side=tk.LEFT, padx=10)
        tk.Label(title_frame, text="✂️", font=("Segoe UI Emoji", 48), bg="#1a1a2e").pack(side=tk.LEFT)
        
        # Score board with modern cards
        score_frame = tk.Frame(self.root, bg="#1a1a2e")
        score_frame.pack(pady=20)
        
        self.user_score_card = self.create_score_card(score_frame, "YOU", self.user_score, "#27ae60", 0)
        self.computer_score_card = self.create_score_card(score_frame, "CPU", self.computer_score, "#c0392b", 1)
        
        # VS divider
        vs_label = tk.Label(score_frame, text="VS", font=("Segoe UI", 16, "bold"), 
                           fg="#7f8c8d", bg="#1a1a2e")
        vs_label.grid(row=0, column=1, padx=30)
        
        # Result display area
        self.result_frame = tk.Frame(self.root, bg="#16213e", relief=tk.RAISED, bd=3)
        self.result_frame.pack(pady=30, padx=40, fill=tk.X)
        
        self.result_emoji = tk.Label(self.result_frame, text="🎮", font=("Segoe UI Emoji", 64), 
                                     bg="#16213e")
        self.result_emoji.pack(pady=20)
        
        self.result_text = tk.Label(self.result_frame, text="MAKE YOUR MOVE", 
                                    font=("Segoe UI", 20, "bold"), fg="#f1c40f", bg="#16213e")
        self.result_text.pack(pady=10)
        
        self.detail_text = tk.Label(self.result_frame, text="", 
                                    font=("Segoe UI", 12), fg="#bdc3c7", bg="#16213e")
        self.detail_text.pack(pady=(0, 20))
        
        # Choice display
        choice_frame = tk.Frame(self.root, bg="#1a1a2e")
        choice_frame.pack(pady=10)
        
        self.user_display = tk.Label(choice_frame, text="", font=("Segoe UI Emoji", 32), 
                                     bg="#1a1a2e")
        self.user_display.grid(row=0, column=0, padx=30)
        
        tk.Label(choice_frame, text="→", font=("Segoe UI", 24), fg="#7f8c8d", bg="#1a1a2e").grid(row=0, column=1)
        
        self.computer_display = tk.Label(choice_frame, text="", font=("Segoe UI Emoji", 32), 
                                         bg="#1a1a2e")
        self.computer_display.grid(row=0, column=2, padx=30)
        
        # Buttons with modern styling
        btn_frame = tk.Frame(self.root, bg="#1a1a2e")
        btn_frame.pack(pady=30)
        
        for i, choice in enumerate(self.choices):
            btn = self.create_modern_button(btn_frame, choice, self.choice_emojis[choice], 
                                            self.choice_colors[choice], 
                                            lambda c=choice: self.play(c))
            btn.grid(row=0, column=i, padx=15)
        
        # Reset button
        reset_frame = tk.Frame(self.root, bg="#1a1a2e")
        reset_frame.pack(pady=20)
        
        reset_btn = tk.Button(reset_frame, text="🔄 RESET SCORE", font=("Segoe UI", 12, "bold"),
                             bg="#34495e", fg="#ecf0f1", activebackground="#2c3e50",
                             activeforeground="#ecf0f1", bd=0, padx=30, pady=12,
                             cursor="hand2", command=self.reset_score)
        reset_btn.pack()
        
        # Footer
        tk.Label(self.root, text="Built with Python & Tkinter", font=("Segoe UI", 9), 
                 fg="#555", bg="#1a1a2e").pack(side=tk.BOTTOM, pady=10)
    
    def create_score_card(self, parent, label, score, color, col):
        card = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=3)
        card.grid(row=0, column=col, padx=10)
        
        tk.Label(card, text=label, font=("Segoe UI", 11, "bold"), fg="#fff", bg=color).pack(padx=20, pady=(10, 0))
        score_label = tk.Label(card, text=str(score), font=("Segoe UI", 36, "bold"), 
                               fg="#fff", bg=color)
        score_label.pack(padx=20, pady=(0, 10))
        return score_label
    
    def create_modern_button(self, parent, text, emoji, color, command):
        btn_frame = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=4)
        
        btn = tk.Button(btn_frame, text=f"{emoji}\n{text}", font=("Segoe UI Emoji", 18, "bold"),
                       fg="#fff", bg=color, activebackground=self.darken_color(color),
                       activeforeground="#fff", bd=0, padx=25, pady=20,
                       cursor="hand2", width=6, height=3, command=command)
        btn.pack()
        
        # Hover effects
        btn.bind("<Enter>", lambda e: btn.config(bg=self.darken_color(color)))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        
        return btn_frame
    
    def darken_color(self, color):
        color_map = {
            '#e74c3c': '#c0392b',
            '#3498db': '#2980b9',
            '#f39c12': '#d35400'
        }
        return color_map.get(color, color)
    
    def play(self, user_choice):
        computer_choice = random.choice(self.choices)
        
        # Animate choices
        self.user_display.config(text=self.choice_emojis[user_choice])
        self.computer_display.config(text=self.choice_emojis[computer_choice])
        
        # Determine result
        if user_choice == computer_choice:
            result = "DRAW!"
            emoji = "🤝"
            color = "#f39c12"
            detail = f"Both chose {user_choice}"
        elif (user_choice == 'Rock' and computer_choice == 'Scissors') or \
             (user_choice == 'Paper' and computer_choice == 'Rock') or \
             (user_choice == 'Scissors' and computer_choice == 'Paper'):
            result = "YOU WIN! 🎉"
            emoji = "🏆"
            color = "#27ae60"
            detail = f"{user_choice} beats {computer_choice}"
            self.user_score += 1
            self.user_score_card.config(text=str(self.user_score))
        else:
            result = "YOU LOSE! 😢"
            emoji = "💀"
            color = "#e74c3c"
            detail = f"{computer_choice} beats {user_choice}"
            self.computer_score += 1
            self.computer_score_card.config(text=str(self.computer_score))
        
        # Update result display with animation
        self.result_frame.config(bg=color)
        self.result_emoji.config(text=emoji, bg=color)
        self.result_text.config(text=result, fg="#fff", bg=color)
        self.detail_text.config(text=detail, fg="#fff", bg=color)
        
        # Flash effect
        self.root.after(100, lambda: self.result_frame.config(bg="#16213e"))
        self.root.after(100, lambda: self.result_emoji.config(bg="#16213e"))
        self.root.after(100, lambda: self.result_text.config(bg="#16213e"))
        self.root.after(100, lambda: self.detail_text.config(bg="#16213e"))
    
    def reset_score(self):
        self.user_score = 0
        self.computer_score = 0
        self.user_score_card.config(text="0")
        self.computer_score_card.config(text="0")
        self.user_display.config(text="")
        self.computer_display.config(text="")
        self.result_frame.config(bg="#16213e")
        self.result_emoji.config(text="🎮", bg="#16213e")
        self.result_text.config(text="MAKE YOUR MOVE", fg="#f1c40f", bg="#16213e")
        self.detail_text.config(text="", bg="#16213e")

if __name__ == "__main__":
    root = tk.Tk()
    # Set window icon (optional)
    try:
        root.iconbitmap(default='')
    except:
        pass
    app = RockPaperScissors(root)
    root.mainloop()