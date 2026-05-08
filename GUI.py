import router
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

nameg = None

BG = "#121212"
CARD = "#1e1e1e"
ENTRY = "#2b2b2b"
ACCENT = "#4a90ff"
TEXT = "#ffffff"
SUBTEXT = "#9f9f9f"


def submit():
    global nameg
    ip = ip_entry.get()
    port = port_entry.get()
    name = name_entry.get()
    mode = mode_var.get()
    nameg = name

    import threading
    threading.Thread(
        target=router.start,
        args=(ip, port, name, mode),
        daemon=True
    ).start()

    open_chat()


def open_chat():
    main_frame.pack_forget()
    chat_frame.pack(fill="both", expand=True)
    update_chat()


def update_chat():
    try:
        messages = router.messages

        chat_text.config(state="normal")
        chat_text.delete("1.0", tk.END)

        for msg in messages:
            chat_text.insert(tk.END, "  " + msg + "\n\n")

        chat_text.config(state="disabled")
        chat_text.yview(tk.END)

    except Exception as e:
        print("Error Updatin:", e)

    root.after(500, update_chat)


def send_message(event=None):
    msg = msg_entry.get().strip()

    if msg:
        try:
            router.send_message(msg, nameg)
        except Exception as e:
            print("Send error: ", e)

        msg_entry.delete(0, tk.END)


root = tk.Tk()
root.title("LAN Messenger")
root.geometry("430x620")
root.configure(bg=BG)

img = Image.open("kototost.png")

img_main = img.copy()
img_main.thumbnail((130, 130))

img_chat = img.copy()
img_chat.thumbnail((55, 55))

logo_main = ImageTk.PhotoImage(img_main)
logo_chat = ImageTk.PhotoImage(img_chat)

root.iconphoto(False, logo_main)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TRadiobutton",
    background=CARD,
    foreground=TEXT,
    font=("Segoe UI", 10)
)

main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(
    main_frame,
    bg=BG,
    highlightthickness=0
)
canvas.place(relwidth=1, relheight=1)

canvas.create_oval(-100, -100, 180, 180, fill="#1d3557", outline="")
canvas.create_oval(300, 500, 550, 750, fill="#16213e", outline="")
canvas.create_rectangle(40, 40, 390, 570, fill=CARD, outline="")

logo_label_main = tk.Label(
    main_frame,
    image=logo_main,
    bg=CARD
)
logo_label_main.place(relx=0.5, y=90, anchor="center")

title = tk.Label(
    main_frame,
    text="LAN Messenger",
    font=("Segoe UI", 22, "bold"),
    bg=CARD,
    fg=TEXT
)
title.place(relx=0.5, y=180, anchor="center")

subtitle = tk.Label(
    main_frame,
    text="Fast local communication",
    font=("Segoe UI", 10),
    bg=CARD,
    fg=SUBTEXT
)
subtitle.place(relx=0.5, y=210, anchor="center")

tk.Label(
    main_frame,
    text="IP Address",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 10)
).place(x=75, y=260)

ip_entry = tk.Entry(
    main_frame,
    bg=ENTRY,
    fg=TEXT,
    insertbackground="white",
    relief="flat",
    font=("Segoe UI", 11)
)
ip_entry.place(x=75, y=285, width=280, height=35)

tk.Label(
    main_frame,
    text="Port",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 10)
).place(x=75, y=335)

port_entry = tk.Entry(
    main_frame,
    bg=ENTRY,
    fg=TEXT,
    insertbackground="white",
    relief="flat",
    font=("Segoe UI", 11)
)
port_entry.place(x=75, y=360, width=280, height=35)

tk.Label(
    main_frame,
    text="Username",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 10)
).place(x=75, y=410)

name_entry = tk.Entry(
    main_frame,
    bg=ENTRY,
    fg=TEXT,
    insertbackground="white",
    relief="flat",
    font=("Segoe UI", 11)
)
name_entry.place(x=75, y=435, width=280, height=35)

mode_var = tk.StringVar(value="Client")

mode_frame = tk.Frame(main_frame, bg=CARD)
mode_frame.place(relx=0.5, y=500, anchor="center")

client_btn = tk.Radiobutton(
    mode_frame,
    text="Client",
    variable=mode_var,
    value="Client",
    bg=CARD,
    fg=TEXT,
    selectcolor=ENTRY,
    activebackground=CARD,
    activeforeground=TEXT,
    font=("Segoe UI", 10)
)
client_btn.pack(side="left", padx=10)

server_btn = tk.Radiobutton(
    mode_frame,
    text="Server",
    variable=mode_var,
    value="Server",
    bg=CARD,
    fg=TEXT,
    selectcolor=ENTRY,
    activebackground=CARD,
    activeforeground=TEXT,
    font=("Segoe UI", 10)
)
server_btn.pack(side="left", padx=10)

confirm_btn = tk.Button(
    main_frame,
    text="Confirm",
    command=submit,
    bg=ACCENT,
    fg="white",
    activebackground="#3578e5",
    activeforeground="white",
    relief="flat",
    font=("Segoe UI", 11, "bold"),
    cursor="hand2"
)
confirm_btn.place(relx=0.5, y=550, anchor="center", width=280, height=40)

chat_frame = tk.Frame(root, bg=BG)

topbar = tk.Frame(chat_frame, bg=CARD, height=65)
topbar.pack(fill="x")

logo_label_chat = tk.Label(
    topbar,
    image=logo_chat,
    bg=CARD
)
logo_label_chat.pack(side="left", padx=15, pady=5)

chat_title = tk.Label(
    topbar,
    text="LAN Messenger",
    font=("Segoe UI", 15, "bold"),
    bg=CARD,
    fg=TEXT
)
chat_title.pack(side="left")

chat_text = tk.Text(
    chat_frame,
    bg="#181818",
    fg="#e5e5e5",
    insertbackground="white",
    relief="flat",
    font=("Consolas", 11),
    state="disabled",
    padx=15,
    pady=15,
    wrap="word"
)
chat_text.pack(fill="both", expand=True, padx=10, pady=10)

bottom_frame = tk.Frame(chat_frame, bg=BG)
bottom_frame.pack(fill="x", padx=10, pady=(0, 10))

msg_entry = tk.Entry(
    bottom_frame,
    bg=ENTRY,
    fg="white",
    insertbackground="white",
    relief="flat",
    font=("Segoe UI", 11)
)
msg_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))
msg_entry.bind("<Return>", send_message)

send_btn = tk.Button(
    bottom_frame,
    text="Send",
    command=send_message,
    bg=ACCENT,
    fg="white",
    activebackground="#3578e5",
    activeforeground="white",
    relief="flat",
    font=("Segoe UI", 10, "bold"),
    cursor="hand2"
)
send_btn.pack(side="right", ipadx=15, ipady=8)

root.mainloop()