import router
import news
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import base64
import io
from datetime import datetime
import threading

nameg = None
pfp_path = None
background_path = None
background_photo = None
rendered_messages = 0
chosen_mode = None
found_servers = []
current_theme = "Red"

THEMES = {
    "Classic": {
        "BG": "#1e1e1e",
        "CARD": "#252526",
        "ENTRY": "#2d2d30",
        "ACCENT": "#6c6c6c",
        "ACCENT_HOVER": "#808080",
        "TEXT": "#ffffff",
        "SUBTEXT": "#b8b8b8",
        "PANEL": "#202020",
        "OTHER_BUBBLE": "#333333",
        "TOPBAR": "#252526",
        "BOTTOM": "#252526",
        "ENTRY_CHAT": "#303030",
        "GLOW1": "#333333",
        "GLOW2": "#2a2a2a",
        "GLOW3": "#3a3a3a",
        "BTN_STYLE": "flat"
    },
    "Red": {
        "BG": "#0f0f0f",
        "CARD": "#181818",
        "ENTRY": "#232323",
        "ACCENT": "#ff2b2b",
        "ACCENT_HOVER": "#ff4444",
        "TEXT": "#ffffff",
        "SUBTEXT": "#aaaaaa",
        "PANEL": "#141414",
        "OTHER_BUBBLE": "#242424",
        "TOPBAR": "#151515",
        "BOTTOM": "#181818",
        "ENTRY_CHAT": "#202020",
        "GLOW1": "#3a0000",
        "GLOW2": "#220000",
        "GLOW3": "#240000",
        "BTN_STYLE": "flat"
    },
    "Blue": {
        "BG": "#07111f",
        "CARD": "#0d1b2a",
        "ENTRY": "#14283d",
        "ACCENT": "#3a86ff",
        "ACCENT_HOVER": "#5c9cff",
        "TEXT": "#ffffff",
        "SUBTEXT": "#b8d4ff",
        "PANEL": "#091827",
        "OTHER_BUBBLE": "#1b263b",
        "TOPBAR": "#0b1d33",
        "BOTTOM": "#0b1d33",
        "ENTRY_CHAT": "#132842",
        "GLOW1": "#002855",
        "GLOW2": "#001d3d",
        "GLOW3": "#003566",
        "BTN_STYLE": "ridge"
    },
    "Light": {
        "BG": "#f2f2f2",
        "CARD": "#ffffff",
        "ENTRY": "#e8e8e8",
        "ACCENT": "#d62828",
        "ACCENT_HOVER": "#ff4444",
        "TEXT": "#111111",
        "SUBTEXT": "#555555",
        "PANEL": "#e6e6e6",
        "OTHER_BUBBLE": "#dddddd",
        "TOPBAR": "#ffffff",
        "BOTTOM": "#ffffff",
        "ENTRY_CHAT": "#eeeeee",
        "GLOW1": "#ffd6d6",
        "GLOW2": "#ffe6e6",
        "GLOW3": "#ffcccc",
        "BTN_STYLE": "groove"
    },
    "Fully Dark": {
        "BG": "#000000",
        "CARD": "#080808",
        "ENTRY": "#111111",
        "ACCENT": "#ffffff",
        "ACCENT_HOVER": "#cccccc",
        "TEXT": "#ffffff",
        "SUBTEXT": "#777777",
        "PANEL": "#050505",
        "OTHER_BUBBLE": "#111111",
        "TOPBAR": "#050505",
        "BOTTOM": "#050505",
        "ENTRY_CHAT": "#101010",
        "GLOW1": "#090909",
        "GLOW2": "#050505",
        "GLOW3": "#111111",
        "BTN_STYLE": "solid"
    }
}


def load_theme():
    global BG, CARD, ENTRY, ACCENT, ACCENT_HOVER, TEXT, SUBTEXT
    global PANEL, OTHER_BUBBLE, TOPBAR, BOTTOM, ENTRY_CHAT
    global GLOW1, GLOW2, GLOW3, BTN_STYLE

    theme = THEMES[current_theme]

    BG = theme["BG"]
    CARD = theme["CARD"]
    ENTRY = theme["ENTRY"]
    ACCENT = theme["ACCENT"]
    ACCENT_HOVER = theme["ACCENT_HOVER"]
    TEXT = theme["TEXT"]
    SUBTEXT = theme["SUBTEXT"]
    PANEL = theme["PANEL"]
    OTHER_BUBBLE = theme["OTHER_BUBBLE"]
    TOPBAR = theme["TOPBAR"]
    BOTTOM = theme["BOTTOM"]
    ENTRY_CHAT = theme["ENTRY_CHAT"]
    GLOW1 = theme["GLOW1"]
    GLOW2 = theme["GLOW2"]
    GLOW3 = theme["GLOW3"]
    BTN_STYLE = theme["BTN_STYLE"]


load_theme()

news_cards = []
news_labels = []


def on_enter(e, btn):
    btn.config(bg=ACCENT_HOVER)


def on_leave(e, btn):
    btn.config(bg=ACCENT)


def draw_background():
    canvas.delete("bg_shape")
    canvas.delete("bg_image")

    if background_path:
        try:
            global background_photo

            bg_img = Image.open(background_path)
            bg_img = bg_img.resize((540, 640))
            background_photo = ImageTk.PhotoImage(bg_img)

            canvas.create_image(
                0,
                0,
                image=background_photo,
                anchor="nw",
                tags="bg_image"
            )

            canvas.create_rectangle(
                0,
                0,
                540,
                640,
                fill=BG,
                stipple="gray50",
                outline="",
                tags="bg_shape"
            )

        except:
            pass

    canvas.create_oval(-100, -100, 180, 180, fill=GLOW1, outline="", tags="bg_shape")
    canvas.create_oval(300, 500, 550, 750, fill=GLOW2, outline="", tags="bg_shape")
    canvas.create_oval(250, 100, 550, 400, fill=GLOW3, outline="", tags="bg_shape")
    canvas.create_rectangle(40, 40, 470, 570, fill=CARD, outline="", tags="bg_shape")
    canvas.tag_lower("bg_image")
    canvas.tag_lower("bg_shape")


def choose_background():
    global background_path

    file_path = filedialog.askopenfilename(
        title="Choose Background",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg")
        ]
    )

    if file_path:
        background_path = file_path
        draw_background()


def open_theme_menu():
    theme_window = tk.Toplevel(root)
    theme_window.title("Themes")
    theme_window.geometry("330x420")
    theme_window.configure(bg=BG)

    title_label = tk.Label(
        theme_window,
        text="Choose Theme",
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 20, "bold")
    )

    title_label.pack(pady=(25, 15))

    for theme_name in THEMES:
        theme = THEMES[theme_name]

        btn = tk.Button(
            theme_window,
            text=theme_name,
            command=lambda t=theme_name: change_theme(t),
            bg=theme["ACCENT"],
            fg="white" if theme_name != "Fully Dark" else "#000000",
            activebackground=theme["ACCENT_HOVER"],
            relief=theme["BTN_STYLE"] if theme["BTN_STYLE"] != "solid" else "flat",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2"
        )

        btn.pack(fill="x", padx=35, pady=7, ipady=8)

    bg_btn = tk.Button(
        theme_window,
        text="Choose Custom Background",
        command=choose_background,
        bg=ACCENT,
        fg="white",
        activebackground=ACCENT_HOVER,
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        cursor="hand2"
    )

    bg_btn.pack(fill="x", padx=35, pady=(25, 8), ipady=8)


def change_theme(theme):
    global current_theme, rendered_messages

    current_theme = theme
    load_theme()

    root.configure(bg=BG)
    main_frame.configure(bg=BG)
    left_panel.configure(bg=PANEL)
    news_title.configure(bg=PANEL, fg=ACCENT)
    news_box.configure(bg=PANEL)
    right_panel.configure(bg=BG)
    canvas.configure(bg=BG)

    draw_background()

    for card in news_cards:
        card.configure(bg=CARD)

    for label in news_labels:
        label.configure(bg=CARD, fg=TEXT)

    choice_frame.configure(bg=CARD)
    choice_title.configure(bg=CARD, fg=TEXT)
    choice_subtitle.configure(bg=CARD, fg=SUBTEXT)

    server_choice_btn.configure(bg=ACCENT, activebackground=ACCENT_HOVER, relief=BTN_STYLE if BTN_STYLE != "solid" else "flat")
    client_choice_btn.configure(bg=OTHER_BUBBLE, fg=TEXT, relief=BTN_STYLE if BTN_STYLE != "solid" else "flat")

    config_frame.configure(bg=CARD)
    mode_title.configure(bg=CARD, fg=TEXT)
    server_ip_label.configure(bg=CARD, fg=ACCENT)
    pfp_frame.configure(bg=CARD)
    pfp_label.configure(bg=CARD)
    pfp_button.configure(bg=ACCENT, activebackground=ACCENT_HOVER, relief=BTN_STYLE if BTN_STYLE != "solid" else "flat")

    username_label.configure(bg=CARD, fg=TEXT)
    ip_label.configure(bg=CARD, fg=TEXT)
    port_label.configure(bg=CARD, fg=TEXT)

    name_entry.configure(bg=ENTRY, fg=TEXT)
    ip_entry.configure(bg=ENTRY, fg=TEXT)
    port_entry.configure(bg=ENTRY, fg=TEXT)

    scan_area.configure(bg=CARD)
    scan_btn.configure(bg=ACCENT, activebackground=ACCENT_HOVER, relief=BTN_STYLE if BTN_STYLE != "solid" else "flat")
    server_listbox.configure(bg=ENTRY_CHAT, fg=TEXT, selectbackground=ACCENT)

    confirm_btn.configure(bg=ACCENT, activebackground=ACCENT_HOVER, relief=BTN_STYLE if BTN_STYLE != "solid" else "flat")

    chat_frame.configure(bg=BG)
    topbar.configure(bg=TOPBAR)
    logo_label_chat.configure(bg=TOPBAR)
    chat_title.configure(bg=TOPBAR, fg=TEXT)
    online_label.configure(bg=TOPBAR)

    theme_btn.configure(bg=ACCENT, activebackground=ACCENT_HOVER, relief=BTN_STYLE if BTN_STYLE != "solid" else "flat")

    bottom_frame.configure(bg=BOTTOM)
    typing_label.configure(bg=BOTTOM)
    msg_entry.configure(bg=ENTRY_CHAT, fg=TEXT, highlightcolor=ACCENT)
    send_btn.configure(bg=ACCENT, activebackground=ACCENT_HOVER, relief=BTN_STYLE if BTN_STYLE != "solid" else "flat")

    canvas_chat.configure(bg=BG)
    messages_frame.configure(bg=BG)

    for widget in messages_frame.winfo_children():
        widget.destroy()

    rendered_messages = 0


def choose_pfp():
    global pfp_path, pfp_preview

    file_path = filedialog.askopenfilename(
        title="Choose Profile Picture",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg")
        ]
    )

    if file_path:
        pfp_path = file_path

        pfp_img = Image.open(file_path)
        pfp_img.thumbnail((70, 70))

        pfp_preview = ImageTk.PhotoImage(pfp_img)

        pfp_label.config(image=pfp_preview)
        pfp_label.image = pfp_preview


def select_server_mode():
    global chosen_mode

    chosen_mode = "Server"

    choice_frame.place_forget()
    config_frame.place(relx=0.5, rely=0.5, anchor="center")

    mode_title.config(text="Server Setup")
    scan_area.pack_forget()

    ip_entry.delete(0, tk.END)
    ip_entry.insert(0, router.get_local_ip())

    port_entry.delete(0, tk.END)
    port_entry.insert(0, "5000")

    server_ip_label.config(text="Your IP: " + router.get_local_ip())
    server_ip_label.pack(pady=(0, 10))


def select_client_mode():
    global chosen_mode

    chosen_mode = "Client"

    choice_frame.place_forget()
    config_frame.place(relx=0.5, rely=0.5, anchor="center")

    mode_title.config(text="Client Setup")

    ip_entry.delete(0, tk.END)
    port_entry.delete(0, tk.END)
    port_entry.insert(0, "5000")

    server_ip_label.pack_forget()
    scan_area.pack(fill="x", padx=35, pady=(5, 10))


def scan_servers():
    server_listbox.delete(0, tk.END)
    server_listbox.insert(tk.END, "Scanning Wi-Fi...")

    def worker():
        global found_servers

        found_servers = router.discover_servers()

        root.after(0, update_server_list)

    threading.Thread(target=worker, daemon=True).start()


def update_server_list():
    server_listbox.delete(0, tk.END)

    if not found_servers:
        server_listbox.insert(tk.END, "No servers found")
        return

    for server in found_servers:
        server_listbox.insert(
            tk.END,
            f"{server['name']}  |  {server['ip']}:{server['port']}"
        )


def server_selected(event=None):
    selected = server_listbox.curselection()

    if selected:
        index = selected[0]

        if index < len(found_servers):
            server = found_servers[index]

            ip_entry.delete(0, tk.END)
            ip_entry.insert(0, server["ip"])

            port_entry.delete(0, tk.END)
            port_entry.insert(0, server["port"])


def submit():
    global nameg

    ip = ip_entry.get()
    port = port_entry.get()
    name = name_entry.get()

    nameg = name

    router.messages.append(
        {
            "name": "SYSTEM",
            "message": f"{name} joined the chat",
            "pfp": None
        }
    )

    threading.Thread(
        target=router.start,
        args=(ip, port, name, chosen_mode),
        daemon=True
    ).start()

    open_chat()


def open_chat():
    main_frame.pack_forget()
    chat_frame.pack(fill="both", expand=True)
    update_chat()


def create_circle_pfp(image_data, size=(42, 42)):
    try:
        if image_data:
            decoded = base64.b64decode(image_data)

            img = Image.open(
                io.BytesIO(decoded)
            ).convert("RGB")

        else:
            img = Image.open("kototost.png").convert("RGB")

        img.thumbnail(size)

        return ImageTk.PhotoImage(img)

    except:
        fallback = Image.open("kototost.png").convert("RGB")
        fallback.thumbnail(size)

        return ImageTk.PhotoImage(fallback)


def update_chat():
    global rendered_messages

    try:
        messages = router.messages

        if len(messages) == rendered_messages:
            root.after(250, update_chat)
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

            bubble_color = ACCENT if is_me else OTHER_BUBBLE

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
                fg=TEXT if not is_me else "white",
                font=("Segoe UI", 8, "bold")
            )

            sender_label.pack(anchor="w")

            msg_label = tk.Label(
                bubble,
                text=message,
                bg=bubble_color,
                fg=TEXT if not is_me else "white",
                wraplength=300,
                justify="left",
                font=("Segoe UI", 10)
            )

            msg_label.pack(anchor="w")

            current_time = datetime.now().strftime("%H:%M")

            time_label = tk.Label(
                bubble,
                text=current_time,
                bg=bubble_color,
                fg=SUBTEXT if not is_me else "#f0f0f0",
                font=("Segoe UI", 7)
            )

            time_label.pack(anchor="e", pady=(4, 0))

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

    root.after(250, update_chat)


def send_message(event=None):
    msg = msg_entry.get().strip()

    if msg:
        pfp_data = None

        try:
            if pfp_path:
                with open(pfp_path, "rb") as img_file:
                    pfp_data = base64.b64encode(
                        img_file.read()
                    ).decode("utf-8")

        except Exception as e:
            print("PFP encode error:", e)

        try:
            router.send_message(
                {
                    "name": nameg,
                    "message": msg,
                    "pfp": pfp_data
                }
            )

        except Exception as e:
            print("Send error:", e)

        msg_entry.delete(0, tk.END)
        typing_label.config(text="Ready to chat")


def typing_effect(event=None):
    text = msg_entry.get().strip()

    if text:
        typing_label.config(text="Typing...")
    else:
        typing_label.config(text="Ready to chat")


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
    bg=PANEL,
    width=220
)

left_panel.pack(side="left", fill="y")

news_title = tk.Label(
    left_panel,
    text="LIVE NEWS",
    bg=PANEL,
    fg=ACCENT,
    font=("Segoe UI", 17, "bold")
)

news_title.pack(pady=(20, 12))

news_box = tk.Frame(
    left_panel,
    bg=PANEL
)

news_box.pack(fill="both", expand=True, padx=10)

for item in news.texts:
    news_card = tk.Frame(
        news_box,
        bg=CARD
    )

    news_cards.append(news_card)

    news_card.pack(fill="x", pady=6)

    news_label = tk.Label(
        news_card,
        text=item,
        bg=CARD,
        fg=TEXT,
        wraplength=180,
        justify="left",
        padx=10,
        pady=10,
        font=("Segoe UI", 9)
    )

    news_labels.append(news_label)

    news_label.pack(anchor="w")

right_panel = tk.Frame(main_frame, bg=BG)
right_panel.pack(side="right", fill="both", expand=True)

canvas = tk.Canvas(
    right_panel,
    bg=BG,
    highlightthickness=0
)

canvas.place(relwidth=1, relheight=1)
draw_background()

choice_frame = tk.Frame(
    right_panel,
    bg=CARD
)

choice_frame.place(relx=0.5, rely=0.5, anchor="center", width=360, height=400)

choice_title = tk.Label(
    choice_frame,
    text="Choose Mode",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 24, "bold")
)

choice_title.pack(pady=(35, 10))

choice_subtitle = tk.Label(
    choice_frame,
    text="Start a server or join one on Wi-Fi",
    bg=CARD,
    fg=SUBTEXT,
    font=("Segoe UI", 10)
)

choice_subtitle.pack(pady=(0, 30))

server_choice_btn = tk.Button(
    choice_frame,
    text="Start Server",
    command=select_server_mode,
    bg=ACCENT,
    fg="white",
    activebackground=ACCENT_HOVER,
    relief=BTN_STYLE if BTN_STYLE != "solid" else "flat",
    font=("Segoe UI", 12, "bold"),
    cursor="hand2"
)

server_choice_btn.pack(fill="x", padx=45, ipady=12, pady=8)

client_choice_btn = tk.Button(
    choice_frame,
    text="Join as Client",
    command=select_client_mode,
    bg=OTHER_BUBBLE,
    fg=TEXT,
    relief=BTN_STYLE if BTN_STYLE != "solid" else "flat",
    font=("Segoe UI", 12, "bold"),
    cursor="hand2",
    activebackground=ACCENT_HOVER,
    activeforeground="white"
)

client_choice_btn.pack(fill="x", padx=45, ipady=12, pady=8)

theme_menu_btn = tk.Button(
    choice_frame,
    text="Themes",
    command=open_theme_menu,
    bg=ACCENT,
    fg="white",
    activebackground=ACCENT_HOVER,
    relief=BTN_STYLE if BTN_STYLE != "solid" else "flat",
    font=("Segoe UI", 10, "bold"),
    cursor="hand2"
)

theme_menu_btn.pack(fill="x", padx=45, ipady=9, pady=(18, 6))

background_choice_btn = tk.Button(
    choice_frame,
    text="Custom Background",
    command=choose_background,
    bg=OTHER_BUBBLE,
    fg=TEXT,
    activebackground=ACCENT_HOVER,
    activeforeground="white",
    relief=BTN_STYLE if BTN_STYLE != "solid" else "flat",
    font=("Segoe UI", 10, "bold"),
    cursor="hand2"
)

background_choice_btn.pack(fill="x", padx=45, ipady=9, pady=6)

server_choice_btn.bind("<Enter>", lambda e: on_enter(e, server_choice_btn))
server_choice_btn.bind("<Leave>", lambda e: on_leave(e, server_choice_btn))

theme_menu_btn.bind("<Enter>", lambda e: on_enter(e, theme_menu_btn))
theme_menu_btn.bind("<Leave>", lambda e: on_leave(e, theme_menu_btn))

config_frame = tk.Frame(
    right_panel,
    bg=CARD
)

mode_title = tk.Label(
    config_frame,
    text="Setup",
    font=("Segoe UI", 22, "bold"),
    bg=CARD,
    fg=TEXT
)

mode_title.pack(pady=(20, 5))

server_ip_label = tk.Label(
    config_frame,
    text="",
    bg=CARD,
    fg=ACCENT,
    font=("Segoe UI", 10, "bold")
)

pfp_frame = tk.Frame(
    config_frame,
    bg=CARD
)

pfp_frame.pack(pady=(5, 10))

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
    activebackground=ACCENT_HOVER,
    relief=BTN_STYLE if BTN_STYLE != "solid" else "flat",
    font=("Segoe UI", 9, "bold"),
    cursor="hand2"
)

pfp_button.pack(pady=6)

username_label = tk.Label(
    config_frame,
    text="Username",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 10)
)

username_label.pack(anchor="w", padx=35)

name_entry = tk.Entry(
    config_frame,
    bg=ENTRY,
    fg=TEXT,
    insertbackground="white",
    relief="flat",
    font=("Segoe UI", 11)
)

name_entry.pack(fill="x", padx=35, pady=(5, 10), ipady=7)

ip_label = tk.Label(
    config_frame,
    text="IP Address",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 10)
)

ip_label.pack(anchor="w", padx=35)

ip_entry = tk.Entry(
    config_frame,
    bg=ENTRY,
    fg=TEXT,
    insertbackground="white",
    relief="flat",
    font=("Segoe UI", 11)
)

ip_entry.pack(fill="x", padx=35, pady=(5, 10), ipady=7)

port_label = tk.Label(
    config_frame,
    text="Port",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 10)
)

port_label.pack(anchor="w", padx=35)

port_entry = tk.Entry(
    config_frame,
    bg=ENTRY,
    fg=TEXT,
    insertbackground="white",
    relief="flat",
    font=("Segoe UI", 11)
)

port_entry.pack(fill="x", padx=35, pady=(5, 10), ipady=7)

scan_area = tk.Frame(
    config_frame,
    bg=CARD
)

scan_btn = tk.Button(
    scan_area,
    text="Scan Wi-Fi For Servers",
    command=scan_servers,
    bg=ACCENT,
    fg="white",
    activebackground=ACCENT_HOVER,
    relief=BTN_STYLE if BTN_STYLE != "solid" else "flat",
    font=("Segoe UI", 9, "bold"),
    cursor="hand2"
)

scan_btn.pack(fill="x", pady=(0, 8), ipady=6)

server_listbox = tk.Listbox(
    scan_area,
    bg=ENTRY_CHAT,
    fg=TEXT,
    selectbackground=ACCENT,
    selectforeground="white",
    relief="flat",
    font=("Segoe UI", 9),
    height=4
)

server_listbox.pack(fill="x")
server_listbox.bind("<<ListboxSelect>>", server_selected)

confirm_btn = tk.Button(
    config_frame,
    text="Confirm",
    command=submit,
    bg=ACCENT,
    fg="white",
    activebackground=ACCENT_HOVER,
    relief=BTN_STYLE if BTN_STYLE != "solid" else "flat",
    font=("Segoe UI", 11, "bold"),
    cursor="hand2"
)

confirm_btn.pack(fill="x", padx=35, pady=(10, 20), ipady=10)

pfp_button.bind("<Enter>", lambda e: on_enter(e, pfp_button))
pfp_button.bind("<Leave>", lambda e: on_leave(e, pfp_button))

confirm_btn.bind("<Enter>", lambda e: on_enter(e, confirm_btn))
confirm_btn.bind("<Leave>", lambda e: on_leave(e, confirm_btn))

scan_btn.bind("<Enter>", lambda e: on_enter(e, scan_btn))
scan_btn.bind("<Leave>", lambda e: on_leave(e, scan_btn))

chat_frame = tk.Frame(root, bg=BG)

topbar = tk.Frame(
    chat_frame,
    bg=TOPBAR,
    height=70,
    highlightbackground="#262626",
    highlightthickness=1
)

topbar.pack(fill="x")

logo_label_chat = tk.Label(
    topbar,
    image=logo_chat,
    bg=TOPBAR
)

logo_label_chat.pack(side="left", padx=15, pady=5)

chat_title = tk.Label(
    topbar,
    text="LAN Messenger",
    font=("Segoe UI", 15, "bold"),
    bg=TOPBAR,
    fg=TEXT
)

chat_title.pack(side="left")

online_label = tk.Label(
    topbar,
    text="● Online",
    bg=TOPBAR,
    fg="#44ff44",
    font=("Segoe UI", 9)
)

online_label.pack(side="left", padx=10)

theme_btn = tk.Button(
    topbar,
    text="Themes",
    command=open_theme_menu,
    bg=ACCENT,
    fg="white",
    activebackground=ACCENT_HOVER,
    relief=BTN_STYLE if BTN_STYLE != "solid" else "flat",
    font=("Segoe UI", 8, "bold"),
    cursor="hand2"
)

theme_btn.pack(side="right", padx=8)

bottom_frame = tk.Frame(
    chat_frame,
    bg=BOTTOM,
    height=90
)

bottom_frame.pack(
    side="bottom",
    fill="x"
)

typing_label = tk.Label(
    bottom_frame,
    text="Ready to chat",
    bg=BOTTOM,
    fg="#888888",
    font=("Segoe UI", 9)
)

typing_label.pack(anchor="w", padx=20, pady=(8, 0))

msg_entry = tk.Entry(
    bottom_frame,
    bg=ENTRY_CHAT,
    fg=TEXT,
    insertbackground="white",
    relief="flat",
    font=("Segoe UI", 11),
    bd=0
)

msg_entry.config(highlightthickness=1)
msg_entry.config(highlightbackground="#2f2f2f")
msg_entry.config(highlightcolor=ACCENT)

msg_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(15, 10),
    pady=15,
    ipady=12
)

msg_entry.bind("<Return>", send_message)
msg_entry.bind("<KeyRelease>", typing_effect)

send_btn = tk.Button(
    bottom_frame,
    text="SEND",
    command=send_message,
    bg=ACCENT,
    fg="white",
    activebackground=ACCENT_HOVER,
    relief=BTN_STYLE if BTN_STYLE != "solid" else "flat",
    font=("Segoe UI", 10, "bold"),
    cursor="hand2",
    activeforeground="white",
    bd=0
)

send_btn.pack(
    side="right",
    padx=(0, 15),
    pady=15,
    ipady=8,
    ipadx=10
)

send_btn.bind("<Enter>", lambda e: on_enter(e, send_btn))
send_btn.bind("<Leave>", lambda e: on_leave(e, send_btn))

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

messages_window = canvas_chat.create_window(
    (0, 0),
    window=messages_frame,
    anchor="nw"
)


def resize_messages_frame(event):
    canvas_chat.itemconfig(messages_window, width=event.width)


canvas_chat.bind("<Configure>", resize_messages_frame)

root.mainloop()