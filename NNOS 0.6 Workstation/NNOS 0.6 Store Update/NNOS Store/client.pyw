import tkinter as tk
from tkinter import messagebox, simpledialog
import socket
import os
import threading

SERVER_PORT = 12345
TIMEOUT = 0.5  

def find_server_in_network():
    ranges = [
        "192.168.0.",   # Häufig bei Fritzbox
        "192.168.1.",   # Telekom Standard
        "192.168.2.",   # Manche Speedport/TP-Link etc.
        "192.168.178."  # AVM/Fritzbox Klassiker
    ]
    found_ip = []

    def check_ip_range(base):
        for i in range(1, 255):
            ip = f"{base}{i}"
            try:
                sock = socket.create_connection((ip, SERVER_PORT), timeout=TIMEOUT)
                sock.close()
                found_ip.append(ip)  
                break  
            except socket.error:
                continue 

    threads = []
    for base in ranges:
        t = threading.Thread(target=check_ip_range, args=(base,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()  

    return found_ip[0] if found_ip else None

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NNOS Workstation - File Client")
        self.root.geometry("400x300")
        self.root.attributes('-topmost', True)

        self.SERVER_HOST = '127.0.0.1'

        self.status_text = "🔄 Verbindung wird hergestellt..."
        self.status = tk.Label(root, text=self.status_text, fg="green")
        self.status.pack(pady=20)

        self.thread = threading.Thread(target=self.establish_connection)
        self.thread.start()

        tk.Button(root, text="📤 Datei senden", command=self.send_file_manual).pack(pady=10)
        tk.Button(root, text="📥 Datei empfangen", command=self.receive_file_manual).pack(pady=10)
        tk.Button(root, text="❌ Verbindung schließen", command=self.exit_client).pack(pady=10)

    def establish_connection(self):
        # Zuerst Verbindung zu localhost versuchen
        if self.connect_to_server(self.SERVER_HOST):
            self.update_status(f"✅ Verbunden mit Server: {self.SERVER_HOST}")
        else:
            found = find_server_in_network()
            if found:
                self.SERVER_HOST = found
                if self.connect_to_server(self.SERVER_HOST):
                    self.update_status(f"🌐 Verbunden mit Server im Netzwerk: {self.SERVER_HOST}")
                else:
                    self.update_status("❌ Verbindung zum gefundenen Server fehlgeschlagen.")
            else:
                self.update_status("❌ Kein Server im Netzwerk gefunden.")

    def update_status(self, text):
        self.status.config(text=text)

    def connect_to_server(self, server_ip):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, SERVER_PORT))
            welcome = self.client_socket.recv(1024).decode()
            print(welcome)
            return True  
        except Exception as e:
            print(f"Verbindung zu {server_ip} fehlgeschlagen: {str(e)}")
            return False  

    def send_file_manual(self):
        filepath = simpledialog.askstring("Datei senden", "Gib den **vollständigen Pfad** der Datei an:")
        if not filepath or not os.path.isfile(filepath):
            messagebox.showerror("Fehler", "Pfad ungültig oder Datei existiert nicht.")
            return

        filename = os.path.basename(filepath)
        self.client_socket.send("send".encode())
        self.client_socket.send(filename.encode())

        ack = self.client_socket.recv(1024).decode()
        if ack != "ACK":
            messagebox.showerror("Fehler", "Server konnte Datei nicht empfangen.")
            return

        filesize = os.path.getsize(filepath)
        self.client_socket.send(str(filesize).encode())
        self.client_socket.recv(1024)

        with open(filepath, 'rb') as f:
            while chunk := f.read(1024):
                self.client_socket.send(chunk)

        messagebox.showinfo("Erfolg", "Datei erfolgreich gesendet.")

    def receive_file_manual(self):
        self.client_socket.send("list_files".encode())
        files_list = self.client_socket.recv(4096).decode().splitlines()
        if not files_list:
            messagebox.showinfo("Info", "Keine Dateien auf dem Server.")
            return

        filename = simpledialog.askstring("Datei auswählen", "Verfügbare Dateien:\n" + "\n".join(files_list) + "\n\nDateiname eingeben:")
        if not filename:
            return

        save_dir = simpledialog.askstring("Speicherort", "Gib das Zielverzeichnis an (z.B. C:\\EmpfangeneDateien):")
        if not save_dir or not os.path.isdir(save_dir):
            messagebox.showerror("Fehler", "Ungültiges Verzeichnis.")
            return

        self.client_socket.send("receive".encode())
        self.client_socket.send(filename.encode())

        ack = self.client_socket.recv(1024).decode()
        if ack != "ACK":
            messagebox.showerror("Fehler", "Datei nicht gefunden auf Server.")
            return

        filesize = int(self.client_socket.recv(1024).decode())
        self.client_socket.send("ACK".encode())

        filepath = os.path.join(save_dir, filename)
        with open(filepath, 'wb') as f:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                f.write(data)
                if f.tell() >= filesize:
                    break

        messagebox.showinfo("Erfolg", f"Datei gespeichert unter:\n{filepath}")

    def exit_client(self):
        try:
            self.client_socket.send("exit".encode())
            self.client_socket.close()
        except:
            pass
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()