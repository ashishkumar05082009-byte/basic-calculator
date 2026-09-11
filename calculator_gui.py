import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Calculator")
        self.root.geometry("320x400")
        self.root.resizable(False, False)
        
        self.expression = ""
        self.display_var = tk.StringVar()
        
        self.create_display()
        self.create_buttons()
        
    def create_display(self):
        display = tk.Entry(
            self.root,
            textvariable=self.display_var,
            font=("Arial", 24),
            bd=10,
            insertwidth=2,
            width=14,
            borderwidth=4,
            justify="right"
        )
        display.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
        
    def create_buttons(self):
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('Del', 5, 1)
        ]
        
        for (text, row, col) in buttons:
            if text == '=':
                btn = tk.Button(
                    self.root, text=text, padx=20, pady=20,
                    font=("Arial", 14), bg="#4CAF50", fg="white",
                    command=self.calculate
                )
            elif text == 'C':
                btn = tk.Button(
                    self.root, text=text, padx=20, pady=20,
                    font=("Arial", 14), bg="#f44336", fg="white",
                    command=self.clear
                )
            elif text == 'Del':
                btn = tk.Button(
                    self.root, text=text, padx=20, pady=20,
                    font=("Arial", 14), bg="#FF9800", fg="white",
                    command=self.delete
                )
            else:
                btn = tk.Button(
                    self.root, text=text, padx=20, pady=20,
                    font=("Arial", 14),
                    command=lambda t=text: self.on_click(t)
                )
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
            
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
            
    def on_click(self, char):
        self.expression += str(char)
        self.display_var.set(self.expression)
        
    def clear(self):
        self.expression = ""
        self.display_var.set("")
        
    def delete(self):
        self.expression = self.expression[:-1]
        self.display_var.set(self.expression)
        
    def calculate(self):
        try:
            result = str(eval(self.expression))
            self.display_var.set(result)
            self.expression = result
        except ZeroDivisionError:
            self.display_var.set("Error: Div by 0")
            self.expression = ""
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()