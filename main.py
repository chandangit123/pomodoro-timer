import tkinter as tk
import time
import threading
from plyer import notification

# ---------------------------- NOTIFICATION ------------------------------- #
def notify(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=5  # seconds
    )

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, timer
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg="#333")
    checkmarks_label.config(text="")
    reps = 0

# ---------------------------- TIMER START ------------------------------- #
def start_timer():
    global reps
    reps += 1

    work_min = int(work_min_var.get())
    short_break = int(short_break_min_var.get())
    long_break = int(long_break_min_var.get())

    if reps % 8 == 0:
        count = long_break * 60
        title_label.config(text="Long Break", fg="#e7305b")
        notify("Break Time", "Take a long break!")
    elif reps % 2 == 0:
        count = short_break * 60
        title_label.config(text="Short Break", fg="#e2979c")
        notify("Break Time", "Take a short break!")
    else:
        count = work_min * 60
        title_label.config(text="Work", fg="#9bdeac")
        notify("Focus", "Time to work!")

    count_down(count)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer
    minutes = count // 60
    seconds = count % 60
    if seconds < 10:
        seconds = f"0{seconds}"
    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")

    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = reps // 2
        for _ in range(work_sessions):
            marks += "✓"
        checkmarks_label.config(text=marks)

# ---------------------------- THREAD WRAPPER ------------------------------- #
def start_thread():
    t = threading.Thread(target=start_timer)
    t.start()

# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50, bg="#f7f5dd")

title_label = tk.Label(text="Timer", fg="#333", bg="#f7f5dd", font=("Courier", 40, "bold"))
title_label.grid(column=1, row=0)

canvas = tk.Canvas(width=200, height=224, bg="#f7f5dd", highlightthickness=0)
timer_text = canvas.create_text(100, 112, text="00:00", fill="#333", font=("Courier", 35, "bold"))
canvas.grid(column=1, row=1)

start_button = tk.Button(text="Start", command=start_thread, highlightthickness=0)
start_button.grid(column=0, row=2)

reset_button = tk.Button(text="Reset", command=reset_timer, highlightthickness=0)
reset_button.grid(column=2, row=2)

checkmarks_label = tk.Label(fg="#9bdeac", bg="#f7f5dd", font=("Courier", 15))
checkmarks_label.grid(column=1, row=3)

# Input Fields for Custom Times
work_min_var = tk.StringVar(value="25")
short_break_min_var = tk.StringVar(value="5")
long_break_min_var = tk.StringVar(value="15")

tk.Label(text="Work (min)", bg="#f7f5dd").grid(column=0, row=4)
tk.Entry(textvariable=work_min_var, width=5).grid(column=0, row=5)

tk.Label(text="Short Break", bg="#f7f5dd").grid(column=1, row=4)
tk.Entry(textvariable=short_break_min_var, width=5).grid(column=1, row=5)

tk.Label(text="Long Break", bg="#f7f5dd").grid(column=2, row=4)
tk.Entry(textvariable=long_break_min_var, width=5).grid(column=2, row=5)

# Globals
reps = 0
timer = None

window.mainloop()
