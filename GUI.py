import router
import news
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
import shutil

nameg = None
pfp_path = None
rendered_messages = 0

BG = "#121212"
CARD = "#1e1e1e"
ENTRY = "#2b2b2b"
ACCENT = "#4a90ff"
TEXT = "#ffffff"
SUBTEXT = "#9f9f9f"

if not os.path.exists("pfps"):
    os.makedirs("pfps")


def choose_pfp():
    global pfp_path, pfp_preview

    file_path = filedialog.askopenfilename(
        title="Choose Profile Picture",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg")
        ]
    )

    if file_path:

        filename = os.path.basename(file_path)
        new_path = os.path.join("pfps", filename)

        shutil.copy(file_path, new_path)

        pfp_path = new_path

        pfp_img = Image.open(new_path)
        pfp_img.thumbnail((70, 70))

        pfp_preview = ImageTk.PhotoImage(pfp_img)

        pfp_label.config(image=pfp_preview)
        pfp_label.image = pfp_preview


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


def create_circle_pfp(path, size=(42, 42)):

    try:

        if path and os.path.exists(path):

            img = Image.open(path).convert("RGB")
            img.thumbnail(size)

            render = ImageTk.PhotoImage(img)
            return render

    except:
        pass

    fallback = Image.open("kototost.png").convert("RGB")
    fallback.thumbnail(size)

    return ImageTk.PhotoImage(fallback)


def update_chat():
    global rendered_messages

    try:

        messages = router.messages

        if len(messages) == rendered_messages:
            root.after(300, update_chat)
            return

        for msg_data in messages[rendered_messages:]:

            sender = msg_data.get("name")
            message = msg_data.get("message")
            pfp = msg_data.get("pfp")

            is_me = sender == nameg

            outer = tk.Frame(
                messages_frame,
                bg=BG
            )

            outer.pack(
                fill="x",
                pady=6,
                padx=14
            )

            row = tk.Frame(
                outer,
                bg=BG
            )

            row.pack(
                anchor="e" if is_me else "w"
            )

            bubble_color = ACCENT if is_me else "#242424"

            if not is_me:

                pfp_render = create_circle_pfp(pfp)

                pfp_label_chat = tk.Label(
                    row,
                    image=pfp_render,
                    bg=BG
                )

                pfp_label_chat.image = pfp_render

                pfp_label_chat.pack(
                    side="left",
                    padx=(0, 8)
                )

            bubble = tk.Frame(
                row,
                bg=bubble_color,
                padx=14,
                pady=10
            )

            bubble.pack(
                side="right" if is_me else "left"
            )

            sender_label = tk.Label(
                bubble,
                text=sender,
                bg=bubble_color,
                fg="#d6d6d6",
                font=("Segoe UI", 8, "bold")
            )

            sender_label.pack(anchor="w")

            msg_label = tk.Label(
                bubble,
                text=message,
                bg=bubble_color,
                fg="white",
                wraplength=300,
                justify="left",
                font=("Segoe UI", 10)
            )

            msg_label.pack(anchor="w")

            if is_me:

                pfp_render = create_circle_pfp(pfp)

                pfp_label_chat = tk.Label(
                    row,
                    image=pfp_render,
                    bg=BG
                )

                pfp_label_chat.image = pfp_render

                pfp_label_chat.pack(
                    side="right",
                    padx=(8, 0)
                )

        rendered_messages = len(messages)

        messages_frame.update_idletasks()

        canvas_chat.configure(
            scrollregion=canvas_chat.bbox("all")
        )

        canvas_chat.yview_moveto(1.0)

    except Exception as e:
        print("Error Updating:", e)

    root.after(300, update_chat)


def send_message(event=None):

    msg = msg_entry.get().strip()

    if msg:

        try:

            router.send_message(
                {
                    "name": nameg,
                    "message": msg,
                    "pfp": pfp_path
                }
            )

        except Exception as e:
            print("Send error:", e)

        msg_entry.delete(0, tk.END)


root = tk.Tk()
root.title("LAN Messenger")
root.geometry("760x640")
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

main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True)

left_panel = tk.Frame(
    main_frame,
    bg="#181818",
    width=220
)

left_panel.pack(side="left", fill="y")

news_title = tk.Label(
    left_panel,
    text="NEWS",
    bg="#181818",
    fg=ACCENT,
    font=("Segoe UI", 16, "bold")
)

news_title.pack(pady=(20, 12))

news_box = tk.Frame(
    left_panel,
    bg="#181818"
)

news_box.pack(fill="both", expand=True, padx=10)

for item in news.texts:

    news_card = tk.Frame(
        news_box,
        bg=CARD
    )

    news_card.pack(fill="x", pady=6)

    tk.Label(
        news_card,
        text=item,
        bg=CARD,
        fg=TEXT,
        wraplength=180,
        justify="left",
        padx=10,
        pady=10,
        font=("Segoe UI", 9)
    ).pack(anchor="w")

right_panel = tk.Frame(main_frame, bg=BG)
right_panel.pack(side="right", fill="both", expand=True)

canvas = tk.Canvas(
    right_panel,
    bg=BG,
    highlightthickness=0
)

canvas.place(relwidth=1, relheight=1)

canvas.create_oval(-100, -100, 180, 180, fill="#1d3557", outline="")
canvas.create_oval(300, 500, 550, 750, fill="#16213e", outline="")
canvas.create_rectangle(40, 40, 470, 570, fill=CARD, outline="")

pfp_frame = tk.Frame(
    right_panel,
    bg=CARD
)

pfp_frame.place(relx=0.5, y=90, anchor="center")

pfp_label = tk.Label(
    pfp_frame,
    image=logo_main,
    bg=CARD
)

pfp_label.pack()

pfp_button = tk.Button(
    pfp_frame,
    text="Choose PFP",
    command=choose_pfp,
    bg=ACCENT,
    fg="white",
    relief="flat",
    font=("Segoe UI", 9, "bold"),
    cursor="hand2"
)

pfp_button.pack(pady=8)

title = tk.Label(
    right_panel,
    text="LAN Messenger",
    font=("Segoe UI", 22, "bold"),
    bg=CARD,
    fg=TEXT
)

title.place(relx=0.5, y=210, anchor="center")

subtitle = tk.Label(
    right_panel,
    text="Fast local communication",
    font=("Segoe UI", 10),
    bg=CARD,
    fg=SUBTEXT
)

subtitle.place(relx=0.5, y=240, anchor="center")

tk.Label(
    right_panel,
    text="IP Address",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 10)
).place(x=75, y=280)

ip_entry = tk.Entry(
    right_panel,
    bg=ENTRY,
    fg=TEXT,
    insertbackground="white",
    relief="flat",
    font=("Segoe UI", 11)
)

ip_entry.place(x=75, y=305, width=320, height=35)

tk.Label(
    right_panel,
    text="Port",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 10)
).place(x=75, y=355)

port_entry = tk.Entry(
    right_panel,
    bg=ENTRY,
    fg=TEXT,
    insertbackground="white",
    relief="flat",
    font=("Segoe UI", 11)
)

port_entry.place(x=75, y=380, width=320, height=35)

tk.Label(
    right_panel,
    text="Username",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 10)
).place(x=75, y=430)

name_entry = tk.Entry(
    right_panel,
    bg=ENTRY,
    fg=TEXT,
    insertbackground="white",
    relief="flat",
    font=("Segoe UI", 11)
)

name_entry.place(x=75, y=455, width=320, height=35)

mode_var = tk.StringVar(value="Client")

mode_frame = tk.Frame(right_panel, bg=CARD)

mode_frame.place(relx=0.5, y=520, anchor="center")

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
    right_panel,
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

confirm_btn.place(relx=0.5, y=570, anchor="center", width=320, height=40)

chat_frame = tk.Frame(root, bg=BG)

topbar = tk.Frame(
    chat_frame,
    bg="#181818",
    height=65
)

topbar.pack(fill="x")

logo_label_chat = tk.Label(
    topbar,
    image=logo_chat,
    bg="#181818"
)

logo_label_chat.pack(side="left", padx=15, pady=5)

chat_title = tk.Label(
    topbar,
    text="LAN Messenger",
    font=("Segoe UI", 15, "bold"),
    bg="#181818",
    fg=TEXT
)

chat_title.pack(side="left")

chat_container = tk.Frame(
    chat_frame,
    bg=BG
)

chat_container.pack(
    fill="both",
    expand=True
)

canvas_chat = tk.Canvas(
    chat_container,
    bg=BG,
    highlightthickness=0
)

canvas_chat.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar = tk.Scrollbar(
    chat_container,
    orient="vertical",
    command=canvas_chat.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)

canvas_chat.configure(
    yscrollcommand=scrollbar.set
)

messages_frame = tk.Frame(
    canvas_chat,
    bg=BG
)

canvas_chat.create_window(
    (0, 0),
    window=messages_frame,
    anchor="nw"
)

bottom_frame = tk.Frame(
    chat_frame,
    bg="#181818",
    height=80
)

bottom_frame.pack(
    side="bottom",
    fill="x"
)

msg_entry = tk.Entry(
    bottom_frame,
    bg="#242424",
    fg="white",
    insertbackground="white",
    relief="flat",
    font=("Segoe UI", 11)
)

msg_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(15, 10),
    pady=15,
    ipady=12
)

msg_entry.bind("<Return>", send_message)

send_btn = tk.Button(
    bottom_frame,
    text="➜",
    command=send_message,
    bg=ACCENT,
    fg="white",
    relief="flat",
    font=("Segoe UI", 14, "bold"),
    cursor="hand2",
    width=3
)

send_btn.pack(
    side="right",
    padx=(0, 15),
    pady=15,
    ipady=4
)

root.mainloop()