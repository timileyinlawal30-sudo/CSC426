import tkinter as tk
from tkinter import messagebox

class NordicCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("390x600")
        self.root.configure(bg="#f4f4f6")  # Premium off-white soft background
        self.root.resizable(False, False)

        self.expression = ""
        self.history_text = tk.StringVar()
        self.display_text = tk.StringVar()

        # Build UI Elements
        self.create_display()
        self.create_buttons()

    def create_display(self):
        """Creates a spacious, elegant dual-line display area"""
        display_frame = tk.Frame(self.root, bg="#ffffff", bd=0, highlightthickness=1, highlightbackground="#e5e7eb")
        display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=20, pady=(24, 14))

        # Line 1: Equation History (Top readout)
        history_label = tk.Label(
            display_frame, 
            textvariable=self.history_text, 
            font=("Helvetica", 13), 
            bg="#ffffff", 
            fg="#9ca3af",  # Soft muted silver grey
            anchor="e", 
            padx=18,
            pady=6
        )
        history_label.pack(fill=tk.X)
        self.history_text.set("")

        # Line 2: Active Input / Output (Main readout)
        display_label = tk.Label(
            display_frame, 
            textvariable=self.display_text, 
            font=("Helvetica", 34, "normal"),  # Fixed font weight config for Windows cross-compatibility
            bg="#ffffff", 
            fg="#111827",  # Deep charcoal gray (no pure black)
            anchor="e", 
            padx=18,
            pady=12
        )
        display_label.pack(fill=tk.X)
        self.display_text.set("0")

    def format_large_number(self, val_str):
        """Formats numbers exceeding display limits to classic scientific notation"""
        try:
            clean_str = val_str.replace('^', '').replace('\\', '')
            if not clean_str.replace('.','',1).isdigit():
                return val_str
                
            num = float(val_str)
            if len(val_str) > 11 or num >= 1e11:
                formatted = f"{num:.4E}"
                return formatted.replace("E+", "E")
            return val_str
        except ValueError:
            return val_str

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#f4f4f6")
        button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=16, pady=(0, 20))

        button_layout = [
            ['C', '^', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '\\', '=']
        ]

        for i in range(5):
            button_frame.rowconfigure(i, weight=1)
        for j in range(4):
            button_frame.columnconfigure(j, weight=1)

        for row_idx, row in enumerate(button_layout):
            for col_idx, char in enumerate(row):
                # Color Orchestra for Nordic Design
                if char == '=':
                    bg_color = "#111827"  # Deep slate focal button
                    fg_color = "#ffffff"
                    active_bg = "#374151"
                elif char in ['C', '^', '%', '/', '*', '-', '+', '\\']:
                    bg_color = "#e5e7eb"  # Balanced ash gray keys
                    fg_color = "#4b5563"  # Muted charcoal labels
                    active_bg = "#d1d5db"
                else:
                    bg_color = "#ffffff"  # Crisp white keycaps
                    fg_color = "#111827"  # Dark numbers
                    active_bg = "#f9fafb"

                btn = tk.Button(
                    button_frame, 
                    text=char, 
                    font=("Helvetica", 16),
                    bg=bg_color, 
                    fg=fg_color, 
                    activebackground=active_bg,
                    activeforeground=fg_color,
                    bd=0, 
                    relief="flat",
                    command=lambda x=char: self.on_button_click(x)
                )
                btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=5, pady=5)

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.history_text.set("")
            self.display_text.set("0")
        
        elif char == '=':
            try:
                if not self.expression:
                    return
                
                self.history_text.set(self.expression + " =")
                expr_to_eval = self.expression.replace('^', '**').replace('\\', '//')
                result = eval(expr_to_eval)
                
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                
                final_output = self.format_large_number(str(result))
                
                self.display_text.set(final_output)
                self.expression = str(result)
                
            except ZeroDivisionError:
                messagebox.showerror("Math Error", "Cannot divide by zero")
                self.expression = ""
                self.display_text.set("0")
                self.history_text.set("")
            except Exception:
                messagebox.showerror("Error", "Invalid Expression")
                self.expression = ""
                self.display_text.set("0")
                self.history_text.set("")
                
        else:
            if self.display_text.get() == "0" and char not in ['^', '%', '/', '*', '-', '+', '\\']:
                self.expression = char
            else:
                self.expression += char
            
            active_view = self.format_large_number(self.expression)
            self.display_text.set(active_view)

if __name__ == "__main__":
    root = tk.Tk()
    app = NordicCalculator(root)
    root.mainloop()