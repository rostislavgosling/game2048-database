import tkinter as tk

def button_click(button_text):
    print(f"Button {button_text} clicked")


root = tk.Tk()
root.title("Button Interface")

button_names = ["up", "down", "left", "right", "Start", "EndGame"]

for i, button_text in enumerate(button_names):
    button = tk.Button(root, text=button_text, command=lambda text=button_text: button_click(text))
    button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

root.mainloop()
