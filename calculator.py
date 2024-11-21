import tkinter as tk
from tkinter import messagebox
import math

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.create_widgets()
        self.mainloop()

    def create_widgets(self):
        # Entry widget for the expression
        self.entry = tk.Entry(self, width=22, borderwidth=2, font=('Arial', 16))
        self.entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        # Button layout
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '√', '+',
            '(', ')', 'C', '='
        ]

        # Button configuration
        button_config = {'width': 4, 'height': 2, 'font': ('Arial', 14)}

        # Create and place buttons
        row = 1
        col = 0
        for button in buttons:
            tk.Button(self, text=button, **button_config,
                      command=lambda b=button: self.on_button_click(b)).grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def evaluate_expression(self, expression):
        try:
            # Replace square root function with math.sqrt
            expression = self.replace_sqrt(expression)
            # Evaluate the expression
            result = eval(expression, {"math": math})
            return result
        except Exception as e:
            messagebox.showerror("Error", f"Invalid expression: {e}")
            return None

    def replace_sqrt(self, expression):
        # Replace '√' with 'math.sqrt(...)' where '...' is the expression inside the square root
        while '√' in expression:
            # Find the position of the '√'
            index = expression.index('√')
            # Find the matching closing parenthesis for the square root
            open_paren = expression.find('(', index)
            if open_paren == -1:
                # If there is no opening parenthesis, assume the root is of the next term
                expression = expression[:index] + 'math.sqrt(' + expression[index+1:] + ')'
            else:
                # If there is an opening parenthesis, find the closing parenthesis
                close_paren = expression.find(')', open_paren)
                if close_paren == -1:
                    close_paren = len(expression)
                # Replace the square root part with 'math.sqrt(...)'
                expression = expression[:index] + 'math.sqrt(' + expression[open_paren+1:close_paren] + ')' + expression[close_paren:]
        return expression

    def on_button_click(self, char):
        current_text = self.entry.get()
        if char == '=':
            result = self.evaluate_expression(current_text)
            if result is not None:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
        elif char == 'C':
            self.entry.delete(0, tk.END)
        else:
            self.entry.insert(tk.END, char)

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()