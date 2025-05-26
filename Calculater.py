import tkinter as tk
from tkinter import messagebox

def calculate(operation):
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                result_label.config(text="Error: Divide by 0")
                return
            result = num1 / num2
        elif operation == '%':
            
            result = (num1 / 100) * num2

        result_label.config(text=f"Result: {result:.2f}")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers.")

root = tk.Tk()
root.title("Calculator")
root.geometry("400x450")
root.configure(bg="#0f4069")

tk.Label(root, text="Simple Calculator", font=("Helvetica", 18, "bold"), bg="#1e1e1e", fg="#ffee00").pack(pady=10)

entry1 = tk.Entry(root, font=("Helvetica", 14), bg="#2b2b2b", fg="white", justify='center')
entry1.pack(pady=10)

entry2 = tk.Entry(root, font=("Helvetica", 14), bg="#2b2b2b", fg="white", justify='center')
entry2.pack(pady=10)

btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=20)

btn_style = {"font": ("Helvetica", 14), "bg": "#333", "fg": "white", "width": 6, "bd": 0, "relief": "ridge"}

tk.Button(btn_frame, text="+", command=lambda: calculate('+'), **btn_style).grid(row=0, column=0, padx=10, pady=5)
tk.Button(btn_frame, text="-", command=lambda: calculate('-'), **btn_style).grid(row=0, column=1, padx=10, pady=5)
tk.Button(btn_frame, text="×", command=lambda: calculate('*'), **btn_style).grid(row=1, column=0, padx=10, pady=5)
tk.Button(btn_frame, text="÷", command=lambda: calculate('/'), **btn_style).grid(row=1, column=1, padx=10, pady=5)
tk.Button(btn_frame, text="%", command=lambda: calculate('%'), **btn_style).grid(row=2, column=0, columnspan=2, pady=5)

result_label = tk.Label(root, text="Result: ", font=("Helvetica", 16), bg="#1e1e1e", fg="#00ffd5")
result_label.pack(pady=30)
root.mainloop()
