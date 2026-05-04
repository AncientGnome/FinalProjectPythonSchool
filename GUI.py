import router
import tkinter as tk
from tkinter import ttk

def submit():
    ip = ip_entry.get()
    port = port_entry.get()
    name = name_entry.get()
    mode = mode_var.get()
    router.start(ip, port, name, mode)
    result_label.config(
        text=f"IP: {ip}\nPort: {port}\nName: {name}\nMode: {mode}"
    )

root = tk.Tk()
root.title("Network Config")
root.geometry("300x300")

tk.Label(root, text="IP adress:").pack()
ip_entry = tk.Entry(root)
ip_entry.pack()

tk.Label(root, text="Port:").pack()
port_entry = tk.Entry(root)
port_entry.pack()

tk.Label(root, text="Name:").pack()
name_entry = tk.Entry(root)
name_entry.pack()

mode_var = tk.StringVar(value="Client")

tk.Label(root, text="Mode:").pack()

ttk.Radiobutton(root, text="Client", variable=mode_var, value="Client").pack()
ttk.Radiobutton(root, text="Server", variable=mode_var, value="Server").pack()

tk.Button(root, text="Confirm", command=submit).pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()