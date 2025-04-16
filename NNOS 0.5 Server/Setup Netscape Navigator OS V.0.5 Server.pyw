import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import time

def maximize_console_window():
    """Maximiert das Konsolenfenster und setzt den Titel."""
    import ctypes
    user32 = ctypes.windll.user32
    user32.ShowWindow(user32.GetForegroundWindow(), 3)  # SW_MAXIMIZE

def create_directory(path):
    """Erstellt ein Verzeichnis, falls es noch nicht existiert."""
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Verzeichnis erstellt: {path}")
        else:
            print(f"Verzeichnis existiert bereits: {path}")
    except Exception as e:
        print(f"Fehler beim Erstellen des Verzeichnisses: {e}")

def create_html_file(path):
    """Erstellt eine HTML-Datei im angegebenen Verzeichnis."""
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Welcome to Netscape Navigator OS Server</title>
</head>
<body>
    <h1>Welcome to Netscape Navigator OS Server</h1>
    <p>Thank you for using our Server OS, this is Netscape Navigator OS 0.5 Beta 1 Server Edition</p>
    <p>This page is only for NNOS-Server</p>
   <a href="https://www.google.de/">Google Suche</a>

</body>
</html>"""

    html_file_path = os.path.join(path, "index.html")
    try:
        with open(html_file_path, 'w') as html_file:
            html_file.write(html_content)
        print(f"HTML-Datei erstellt: {html_file_path}")
    except Exception as e:
        print(f"Fehler beim Erstellen der HTML-Datei: {e}")

def copy_file(source, destination):
    """Kopiert eine Datei vom Quell- zum Zielpfad."""
    try:
        if not os.path.isfile(source):
            raise FileNotFoundError(f"Die Quelldatei wurde nicht gefunden: {source}")
        shutil.copy(source, destination)
        print(f"Datei kopiert von {source} nach {destination}")
    except FileNotFoundError as e:
        print(str(e))
    except PermissionError:
        print(f"Fehler: Keine Berechtigung zum Kopieren der Datei {source}.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

def show_welcome_page(root):
    """Zeigt die Willkommensseite im Hauptfenster an."""
    root.attributes('-fullscreen', True)
    root.title("Netscape Navigator OS V.0.5 Beta 1 with, Server Edition Setup")

    welcome_frame = tk.Frame(root, bg="darkblue")
    welcome_frame.pack(fill="both", expand=True, padx=18, pady=18)

    welcome_label = tk.Label(welcome_frame, text="Willkommen zum Netscape Navigator OS V.0.5 Beta 1, Server Edition Setup", bg="darkblue", fg="yellow", font=("Arial", 20, "bold"))
    welcome_label.pack(pady=18)

    license_label = tk.Label(welcome_frame, text="Lizenzvereinbarung:", bg="darkblue", fg="yellow", font=("Arial", 18, "bold"))
    license_label.pack(pady=10)

    license_text = tk.Text(welcome_frame, wrap="word", bg="white", fg="black", font=("Arial", 12), height=20, width=90)
    license_text.insert("1.0", "EULA für Netscape Navigator OS 0.5 Beta 1 Server Edition: Dies ist ein Produkt von Alte F1 Games, Sie sind nur zur Nutzung berechtigt. Jede Weiterverbreitung ist strafbar, das Copyright liegt ausschließlich bei AF1G/New Netscape! Sie als als Beta Tester dürfen Verbesserungsvorschläge senden, aber nicht selbst den Code verändern. Sie haben die Erlaubnis das OS zu installieren oder neuzuinstallieren! Da dies eine Beta ist tragen sie die Verantwortung der Wartung ihres eigenen Systems, es wird nicht garnatiert das für diese Beta ohne eine neue Version auch Patches erscheinen.")
    license_text.config(state="disabled")  # Nur-Lese-Modus
    license_text.pack(pady=10)

    button_frame = tk.Frame(welcome_frame, bg="darkblue")
    button_frame.pack(pady=10)

    accept_button = tk.Button(button_frame, text="Akzeptieren", command=lambda: show_install_options(root), bg="green", fg="black", font=("Arial", 14, "bold"))
    accept_button.pack(side="left", padx=10)

    cancel_button = tk.Button(button_frame, text="Abbrechen", command=root.quit, bg="red", fg="white", font=("Arial", 14, "bold"))
    cancel_button.pack(side="right", padx=10)

def show_install_options(root):
    """Zeigt die Installationsoptionen im Hauptfenster an."""
    clear_window(root)

    options_frame = tk.Frame(root, bg="darkblue")
    options_frame.pack(fill="both", expand=True, padx=20, pady=20)

    instruction_label = tk.Label(options_frame, text="Installationsverzeichnis:", bg="darkblue", fg="yellow", font=("Arial", 16))
    instruction_label.pack(pady=5)

    # Fester Pfad
    fixed_dir = "C:\\NNOS-Server"
    dir_entry = tk.Entry(options_frame, width=40, font=("Arial", 14))
    dir_entry.insert(0, fixed_dir)
    dir_entry.config(state='disabled')  # Deaktiviert das Bearbeiten des Pfads
    dir_entry.pack(pady=5)

    install_button = tk.Button(options_frame, text="Installieren", command=lambda: start_installation(root, fixed_dir), bg="green", fg="white", font=("Arial", 14, "bold"))
    install_button.pack(pady=10)

    cancel_button = tk.Button(options_frame, text="Abbrechen", command=root.quit, bg="red", fg="white", font=("Arial", 14, "bold"))
    cancel_button.pack(pady=10)

def clear_window(root):
    """Leert das Hauptfenster."""
    for widget in root.winfo_children():
        widget.destroy()

def show_progress(root, message, total_steps):
    """Zeigt den Fortschritt im Hauptfenster an."""
    clear_window(root)

    progress_frame = tk.Frame(root, bg="darkblue")
    progress_frame.pack(fill="both", expand=True, padx=20, pady=20)

    progress_label = tk.Label(progress_frame, text=message, bg="darkblue", fg="yellow", font=("Arial", 16))
    progress_label.pack(pady=20)

    progress_bar = ttk.Progressbar(progress_frame, length=600, mode="determinate")
    progress_bar.pack(pady=20)

    for i in range(total_steps + 1):
        progress_bar["value"] = (i / total_steps) * 100
        root.update_idletasks()
        time.sleep(0.02)

def start_installation(root, base_dir):
    """Startet die Installation, erstellt Verzeichnisse und kopiert die Dateien."""
    system_dir = os.path.join(base_dir, "system")
    document_dir = os.path.join(base_dir, "document")
    server_page_dir = os.path.join(base_dir, "Server Page")  # Neuer Ordner für Server Page
    programms_dir = os.path.join(base_dir, "programms")  # Hier wird das neue Verzeichnis für Programme definiert

    create_directory(base_dir)
    create_directory(system_dir)
    create_directory(document_dir)
    create_directory(server_page_dir)
    create_directory(programms_dir)  # Jetzt wird das Verzeichnis für Programme erstellt

    create_html_file(server_page_dir)  # HTML-Datei im neuen Ordner erstellen

    show_progress(root, "Erstelle Verzeichnisse", 160)

    desktop_path = r"C:/Users/User/Desktop/Netscape Navigator OS V.0.5 Beta 1.pyw"
    onedrive_path = r"C:/Users/User/OneDrive/Desktop/Netscape Navigator OS V.0.5 Beta 1 Server.pyw"
    destination_file = os.path.join(system_dir, "Netscape Navigator OS.sys.pyw")

    source_file = None
    if os.path.isfile(desktop_path):
        source_file = desktop_path
    elif os.path.isfile(onedrive_path):
        source_file = onedrive_path

    if not source_file:
        source_file = select_file(root)
        if not source_file:
            messagebox.showerror("Fehler", "Keine Datei ausgewählt. Beende Installation.")
            root.destroy()
            return

    copy_file(source_file, destination_file)
    show_progress(root, "Kopiere Dateien", 160)

    # Rufe die Funktion zum Kopieren in den Autostart auf
    copy_to_startup(destination_file)

    show_completion_message(root)

def copy_to_startup(file_path):
    """Kopiert die Datei in den Autostart-Ordner."""
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    destination = os.path.join(startup_folder, os.path.basename(file_path))

    try:
        shutil.copy(file_path, destination)
        print(f"Datei in den Autostart kopiert: {destination}")
    except Exception as e:
        print(f"Fehler beim Kopieren in den Autostart: {e}")

def select_file(root):
    """Öffnet den Windows-Explorer, um eine Datei auszuwählen."""
    file_path = filedialog.askopenfilename()
    return file_path

def show_completion_message(root):
    """Zeigt eine Abschlussnachricht nach der Installation an."""
    clear_window(root)

    completion_frame = tk.Frame(root, bg="darkblue")
    completion_frame.pack(fill="both", expand=True, padx=20, pady=20)

    completion_label = tk.Label(completion_frame, text="Installation abgeschlossen!", bg="darkblue", fg="yellow", font=("Arial", 24, "bold"))
    completion_label.pack(pady=20)

    exit_button = tk.Button(completion_frame, text="Beenden", command=root.quit, bg="green", fg="black", font=("Arial", 14, "bold"))
    exit_button.pack(pady=10)

if __name__ == "__main__":
    maximize_console_window()
    root = tk.Tk()
    show_welcome_page(root)
    root.mainloop()
