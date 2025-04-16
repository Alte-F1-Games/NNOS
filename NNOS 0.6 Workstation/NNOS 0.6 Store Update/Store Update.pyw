import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import time
import re

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
    root.title("Netscape Navigator OS V.0.6 DEV Release, Workstation Edition Setup")

    welcome_frame = tk.Frame(root, bg="darkblue")
    welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)

    welcome_label = tk.Label(welcome_frame, text="Willkommen zum NNOS V.0.6 DEV Release, NNOS Store Update Setup", bg="darkblue", fg="yellow", font=("Arial", 22, "bold"))
    welcome_label.pack(pady=20)

    license_label = tk.Label(welcome_frame, text="Lizenzvereinbarung:", bg="darkblue", fg="yellow", font=("Arial", 18, "bold"))
    license_label.pack(pady=10)

    license_text = tk.Text(welcome_frame, wrap="word", bg="white", fg="black", font=("Arial", 12), height=20, width=90)
    license_text.insert("1.0", "EULA")
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
    fixed_dir = "C:\\NNOS"
    dir_entry = tk.Entry(options_frame, width=40, font=("Arial", 14))
    dir_entry.insert(0, fixed_dir)
    dir_entry.config(state='disabled')  # Deaktiviert das Bearbeiten des Pfads
    dir_entry.pack(pady=5)

    install_button = tk.Button(options_frame, text="Installieren", command=lambda: start_installation(root, fixed_dir), bg="green", fg="white", font=("Arial", 14, "bold"))
    install_button.pack(pady=10)

    repair_button = tk.Button(options_frame, text="Reparieren", command=lambda: repair_installation(root, fixed_dir), bg="blue", fg="white", font=("Arial", 14, "bold"))
    repair_button.pack(pady=10)

    cancel_button = tk.Button(options_frame, text="Abbrechen", command=root.quit, bg="red", fg="white", font=("Arial", 14, "bold"))
    cancel_button.pack(pady=10)

def clear_window(root):
    """Leert das Hauptfenster."""
    for widget in root.winfo_children():
        widget.destroy()

def start_installation(root, base_dir):
    """Startet die Installation, erstellt Verzeichnisse und kopiert die Dateien."""
    system_dir = os.path.join(base_dir, "system")
    document_dir = os.path.join(base_dir, "document")
    programms_dir = os.path.join(base_dir, "programms")

    create_directory(base_dir)
    create_directory(system_dir)
    create_directory(programms_dir)
    create_directory(document_dir)

    show_progress(root, "Erstelle Verzeichnisse", 160)

    desktop_path = r"C:/Users/User/Desktop/Store Update.pyw"
    onedrive_path = r"C:/Users/User/OneDrive/Desktop/Store Update"
    destination_file = os.path.join(programms_dir, "index.html")

    source_file = None
    if os.path.isfile(desktop_path):
        source_file = desktop_path
    elif os.path.isfile(onedrive_path):
        source_file = onedrive_path

    if not source_file:
        source_file = select_file(root)
        if not source_file:
            messagebox.showerror("Fehler", "Keine Datei ausgewählt. Beende Installation.")
            root.quit()  # Beendet die Anwendung, wenn keine Datei ausgewählt wurde
            return

    copy_file(source_file, destination_file)
    show_progress(root, "Kopiere Dateien", 160)

    messagebox.showinfo("Installation abgeschlossen", "Die Installation wurde erfolgreich abgeschlossen.")
    root.quit()  # Beendet die Anwendung nach Abschluss der Installation

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

    # Nach dem Fortschritt, schließe das Fenster
    root.quit()  # Beendet die Anwendung, wenn der Fortschritt abgeschlossen ist

def select_file(root):
    """Öffnet einen Dateiauswahl-Dialog und gibt den Pfad der ausgewählten Datei zurück."""
    file_path = filedialog.askopenfilename(title="Wählen Sie eine Datei aus", filetypes=[("NNOS Store new HTML", "*.html")])
    return file_path

def repair_installation(root, base_dir):
    """Repariert eine bestehende Installation (hier einfach eine Platzhalterfunktion)."""
    messagebox.showinfo("Reparieren", "Reparatur nicht implementiert. Funktion wird später hinzugefügt.")

if __name__ == "__main__":
    maximize_console_window()
    root = tk.Tk()
    root.configure(bg="darkblue")
    show_welcome_page(root)
    root.mainloop()
