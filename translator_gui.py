# coding: utf-8

import tkinter as tk
from tkinter import messagebox
from translator import load_mapping, translate

def on_input_change(event=None):
    text = input_text.get("1.0", tk.END).strip()
    result = translate(text, mapping)
    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    output_text.config(state='disabled')

root = tk.Tk()
root.title("Переводчик wasd=цфыв")
mapping = load_mapping()


THEMES = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "input_bg": "#ffffff",
        "input_fg": "#000000",
        "output_bg": "#f5f5f5",
        "output_fg": "#000000",
        "label_fg": "#000000"
    },
    "dark": {
        "bg": "#23272e",
        "fg": "#ffffff",
        "input_bg": "#2d323b",
        "input_fg": "#ffffff",
        "output_bg": "#23272e",
        "output_fg": "#ffffff",
        "label_fg": "#ffffff"
    }
}

current_theme = "light"

def apply_theme(theme):
    t = THEMES[theme]
    root.configure(bg=t["bg"])
    frame.configure(bg=t["bg"])
    label_row.configure(bg=t["bg"])
    input_label.configure(bg=t["bg"], fg=t["label_fg"])
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Label) and widget != input_label:
            widget.configure(bg=t["bg"], fg=t["label_fg"])
        elif isinstance(widget, tk.Text):
            if widget == input_text:
                widget.configure(bg=t["input_bg"], fg=t["input_fg"], insertbackground=t["input_fg"])
            else:
                widget.configure(bg=t["output_bg"], fg=t["output_fg"])
    settings_btn_row.configure(bg=t["bg"], fg=t["fg"], activebackground=t["bg"], activeforeground=t["fg"])

def open_settings():
    settings_win = tk.Toplevel(root)
    settings_win.title("Настройки")
    settings_win.resizable(False, False)
    settings_win.grab_set()
    settings_win.configure(bg=THEMES[current_theme]["bg"])

    tk.Label(settings_win, text="Тема:", bg=THEMES[current_theme]["bg"], fg=THEMES[current_theme]["label_fg"], font=("Arial", 11)).pack(padx=15, pady=(15, 5), anchor="w")

    def set_theme(theme):
        nonlocal settings_win
        global current_theme
        current_theme = theme
        apply_theme(theme)
        settings_win.destroy()

    btn_light = tk.Button(settings_win, text="Светлая", width=12, command=lambda: set_theme("light"))
    btn_dark = tk.Button(settings_win, text="Тёмная", width=12, command=lambda: set_theme("dark"))
    btn_light.pack(padx=15, pady=5)
    btn_dark.pack(padx=15, pady=(0, 15))

    if current_theme == "light":
        btn_light.config(font=("Arial", 10, "bold"))
    else:
        btn_dark.config(font=("Arial", 10, "bold"))

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

label_row = tk.Frame(frame, bg=THEMES[current_theme]["bg"])
label_row.pack(fill=tk.X, pady=(0, 0))

input_label = tk.Label(label_row, text="Введите текст на английской раскладке:", bg=THEMES[current_theme]["bg"], fg=THEMES[current_theme]["label_fg"])
input_label.pack(side=tk.LEFT)

settings_btn_row = tk.Button(label_row, text="⚙", font=("Arial", 9), bd=0, command=open_settings, cursor="hand2", padx=2, pady=0, height=1, width=2)
settings_btn_row.pack(side=tk.RIGHT, padx=2)

input_text = tk.Text(frame, width=50, height=5)
input_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

input_text.bind("<KeyRelease>", on_input_change)

def paste_event(event=None):
    try:
        input_text.event_generate("<<Paste>>")
    except Exception:
        pass
    return "break"

input_text.bind("<Control-v>", paste_event)
input_text.bind("<Control-V>", paste_event)
input_text.bind("<Shift-Insert>", paste_event)
input_text.bind("<Control-Insert>", paste_event)

def copy_event(event=None):
    try:
        widget = event.widget
        if widget.tag_ranges("sel"):
            widget.event_generate("<<Copy>>")
    except Exception:
        pass
    return "break"

def select_all_event(event=None):
    try:
        widget = event.widget
        widget.tag_add("sel", "1.0", "end-1c")
        return "break"
    except Exception:
        pass
    return "break"

def ctrl_key_handler(event):
    if event.state & 0x4:
        if (hasattr(event, "char") and event.char and event.char.lower() == "v") or \
           (hasattr(event, "keysym") and event.keysym.lower() == "v") or \
           (hasattr(event, "keycode") and event.keycode == 86):
            return paste_event()
        elif (hasattr(event, "char") and event.char and event.char.lower() == "c") or \
             (hasattr(event, "keysym") and event.keysym.lower() == "c") or \
             (hasattr(event, "keycode") and event.keycode == 67):
            return copy_event()
        elif (hasattr(event, "char") and event.char and event.char.lower() == "a") or \
             (hasattr(event, "keysym") and event.keysym.lower() == "a") or \
             (hasattr(event, "keycode") and event.keycode == 65):
            return select_all_event(event)
    return

input_text.bind("<Control-Key>", ctrl_key_handler)
input_text.bind("<Control-c>", copy_event)
input_text.bind("<Control-C>", copy_event)
tk.Label(frame, text="Результат:").pack(anchor='w')
output_text = tk.Text(frame, width=50, height=5, state='disabled')
output_text.pack(fill=tk.BOTH, expand=True)

output_text.bind("<Control-Key>", ctrl_key_handler)
output_text.bind("<Control-c>", copy_event)
output_text.bind("<Control-C>", copy_event)
output_text.bind("<Control-a>", select_all_event)
output_text.bind("<Control-A>", select_all_event)
input_text.bind("<Control-a>", select_all_event)
input_text.bind("<Control-A>", select_all_event)

apply_theme(current_theme)

root.mainloop()
