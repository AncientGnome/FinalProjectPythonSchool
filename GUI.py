import router
import tkinter as tk

from tkinter import ttk
nameg = None
def submit():
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
            chat_text.insert(tk.END, msg + "\n")

        chat_text.config(state="disabled")
        chat_text.yview(tk.END)

    except Exception as e:
        print("Error Updating:", e)

    root.after(1000, update_chat)

def send_message(event=None):
    msg = msg_entry.get().strip()
    if msg:
        try:
            router.send_message(msg, nameg)
        except Exception as e:
            print("Send error:", e)
        msg_entry.delete(0, tk.END)


root = tk.Tk()
root.title("Network Config")
root.geometry("400x400")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("default")

style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
style.configure("TRadiobutton", background="#1e1e1e", foreground="#ffffff")

main_frame = tk.Frame(root, bg="#1e1e1e")
main_frame.pack(fill="both", expand=True)

tk.Label(main_frame, text="IP address:", bg="#1e1e1e", fg="white").pack()
ip_entry = tk.Entry(main_frame, bg="#2b2b2b", fg="white", insertbackground="white")
ip_entry.pack()

tk.Label(main_frame, text="Port:", bg="#1e1e1e", fg="white").pack()
port_entry = tk.Entry(main_frame, bg="#2b2b2b", fg="white", insertbackground="white")
port_entry.pack()

tk.Label(main_frame, text="Name:", bg="#1e1e1e", fg="white").pack()
name_entry = tk.Entry(main_frame, bg="#2b2b2b", fg="white", insertbackground="white")
name_entry.pack()

mode_var = tk.StringVar(value="Client")

tk.Label(main_frame, text="Mode:", bg="#1e1e1e", fg="white").pack()

ttk.Radiobutton(main_frame, text="Client", variable=mode_var, value="Client").pack()
ttk.Radiobutton(main_frame, text="Server", variable=mode_var, value="Server").pack()

tk.Button(main_frame, text="Confirm", command=submit,
          bg="#3a3a3a", fg="white", activebackground="#505050").pack(pady=10)

chat_frame = tk.Frame(root, bg="#1e1e1e")

chat_text = tk.Text(chat_frame,
                    bg="#1e1e1e",
                    fg="#d4d4d4",
                    insertbackground="white",
                    state="disabled")
chat_text.pack(fill="both", expand=True)

bottom_frame = tk.Frame(chat_frame, bg="#1e1e1e")
bottom_frame.pack(fill="x")


msg_entry = tk.Entry(bottom_frame,
                     bg="#2b2b2b",
                     fg="white",
                     insertbackground="white")
msg_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
msg_entry.bind("<Return>", send_message)

root.mainloop()