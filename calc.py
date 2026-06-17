#assignment: create a menu driven(GUI) Calculator using function for:
# addition, subtration, multiplication and division
#MUTEESASIRA TENDO SHAMMA 2400707480

import tkinter as tk

#  Arithmetic Functions 
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

# Calculator State 
first_num = None      # stores first operand once an operator is pressed
operator = None        # stores the pending operator (+, -, x, /)
reset_screen = False    # True means the next digit should start a fresh number

# Button Actions 
def click_digit(digit):
    global reset_screen
    current = display_var.get()
    if current == "0" or reset_screen:
        current = digit
        reset_screen = False
    else:
        current += digit
    display_var.set(current)

def click_decimal():
    global reset_screen
    current = display_var.get()
    if reset_screen:
        current = "0"
        reset_screen = False
    if "." not in current:
        display_var.set(current + ".")

def click_operator(op):
    global first_num, operator, reset_screen
    
    # if an operator is already pending, solve it first (allows chaining: 5+3x2)
    if first_num is not None and operator is not None and not reset_screen:
        click_equals()
    first_num = float(display_var.get())
    operator = op
    reset_screen = True

def click_equals():
    global first_num, operator, reset_screen
    if first_num is None or operator is None:
        return
    second_num = float(display_var.get())
    try:
        # call the matching function based on the chosen operator
        if operator == "+":
            result = add(first_num, second_num)
        elif operator == "-":
            result = subtract(first_num, second_num)
        elif operator == "x":
            result = multiply(first_num, second_num)
        elif operator == "/":
            result = divide(first_num, second_num)
        if result == int(result):   # show 8 instead of 8.0
            result = int(result)
        display_var.set(str(result))
        first_num = result
    except ZeroDivisionError:
        display_var.set("Error")
        first_num = None
    operator = None
    reset_screen = True

def click_clear():
    global first_num, operator, reset_screen
    first_num, operator, reset_screen = None, None, False
    display_var.set("0")

def click_backspace():
    current = display_var.get()
    display_var.set(current[:-1] if len(current) > 1 else "0")

def click_toggle_sign():
    current = display_var.get()
    if current.startswith("-"):
        display_var.set(current[1:])
    elif current != "0":
        display_var.set("-" + current)

#  GUI Setup
window = tk.Tk()
window.title("Calculator")
window.geometry("320x480")
window.resizable(False, False)
window.configure(bg="#000080")

display_var = tk.StringVar(value="0")
display = tk.Label(window, textvariable=display_var, font=("Arial", 48),
                    bg="#8B4DB8", fg="white", anchor="e", padx=20)
display.pack(fill="both", pady=(60, 20))

button_frame = tk.Frame(window, bg="#000080")
button_frame.pack(expand=True, fill="both")

# (label, row, column, columnspan, bg color, text color, action)
buttons = [
    ("C", 0, 0, 1, "#4B0082", "white", click_clear),
    ("+/-", 0, 1, 1, "#4B0082", "white", click_toggle_sign),
    ("DEL", 0, 2, 1, "#4B0082", "white", click_backspace),
    ("/", 0, 3, 1, "#8B4DB8", "white", lambda: click_operator("/")),
    ("7", 1, 0, 1, "#000080", "white", lambda: click_digit("7")),
    ("8", 1, 1, 1, "#000080", "white", lambda: click_digit("8")),
    ("9", 1, 2, 1, "#000080", "white", lambda: click_digit("9")),
    ("x", 1, 3, 1, "#8B4DB8", "white", lambda: click_operator("x")),
    ("4", 2, 0, 1, "#000080", "white", lambda: click_digit("4")),
    ("5", 2, 1, 1, "#000080", "white", lambda: click_digit("5")),
    ("6", 2, 2, 1, "#000080", "white", lambda: click_digit("6")),
    ("-", 2, 3, 1, "#8B4DB8", "white", lambda: click_operator("-")),
    ("1", 3, 0, 1, "#000080", "white", lambda: click_digit("1")),
    ("2", 3, 1, 1, "#000080", "white", lambda: click_digit("2")),
    ("3", 3, 2, 1, "#000080", "white", lambda: click_digit("3")),
    ("+", 3, 3, 1, "#8B4DB8", "white", lambda: click_operator("+")),
    ("0", 4, 0, 2, "#000080", "white", lambda: click_digit("0")),
    (".", 4, 2, 1, "#000080", "white", click_decimal),
    ("=", 4, 3, 1, "#8B4DB8", "white", click_equals),
]

for (text, row, col, colspan, bg, fg, cmd) in buttons:
    tk.Button(button_frame, text=text, font=("Arial", 22), bg=bg, fg=fg,
              activebackground=bg, bd=0, command=cmd
              ).grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)

# make all rows/columns resize evenly so buttons fill the window
for i in range(4):
    button_frame.columnconfigure(i, weight=1)
for i in range(5):
    button_frame.rowconfigure(i, weight=1)

window.mainloop()