
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import random

HOST = '127.0.0.1'
PORT = 55555

class CosmicChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("🌌 Cosmic Chat")
        self.master.geometry("500x600")
        self.master.configure(bg="#0b0f29")  

        self.nickname = simpledialog.askstring("Ник", "Введите ваше космическое имя:", parent=master)
        if not self.nickname:
            messagebox.showerror("Ошибка", "Имя обязательно!")
            master.destroy()
            return

        self.chat_area = scrolledtext.ScrolledText(master, bg="#0e153a", fg="#00ffcc",
                                                   font=("Consolas", 11), wrap=tk.WORD)
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(master, bg="#1a1f4b", fg="#00ffff", insertbackground="#00ffff",
                              font=("Consolas", 12))
        self.entry.pack(padx=10, pady=5, fill=tk.X)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="🚀 Отправить", command=self.send_message,
                                     bg="#162447", fg="#00ffcc", font=("Consolas", 11, "bold"))
        self.send_button.pack(padx=10, pady=5, fill=tk.X)

        

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((HOST, PORT))
            self.receive_thread = threading.Thread(target=self.receive)
            self.receive_thread.daemon = True
            self.receive_thread.start()
        except Exception as e:
            messagebox.showerror("Ошибка подключения", str(e))
            master.destroy()

    def create_stars(self):
        """Создаем фон со звездами"""
        canvas = tk.Canvas(self.master, bg="#0b0f29", highlightthickness=0)
        canvas.place(relwidth=1, relheight=1)
        for _ in range(100):
            x, y = random.randint(0, 500), random.randint(0, 600)
            r = random.choice([1, 2])
            canvas.create_oval(x, y, x + r, y + r, fill="#ffffff", outline="")
        

    def receive(self):
        """Прием сообщений от сервера"""
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    self.display_message(message)
            except:
                self.display_message("⚠️ Соединение потеряно.")
                self.client.close()
                break

    def display_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def send_message(self, event=None):
        message = self.entry.get()
        if message.strip():
            full_message = f"{self.nickname}: {message}"
            self.client.send(full_message.encode('utf-8'))
            self.entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CosmicChatClient(root)
    root.mainloop()
