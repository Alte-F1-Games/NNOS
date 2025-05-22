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

def create_html_file(path, title="Welcome to Netscape Navigator OS Store", message="Thank you for using our NNOS Store, this is our place to install external software to our NNOS, please note this is a Beta Implemation!"):
    """Erstellt eine HTML-Datei im angegebenen Verzeichnis mit dynamischen Inhalten."""
    
    # HTML-Inhalt mit Platzhaltern
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            color: #333;
            text-align: center;
            padding: 20px;
        }}
        header {{
            background-color: #333;
            color: white;
            padding: 10px 0;
            font-size: 24px;
        }}
        .content {{
            margin: 20px;
        }}
        .button {{
            background-color: #4CAF50;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            cursor: pointer;
            border: none;
        }}
        .button:hover {{
            background-color: #45a049;
        }}
    </style>
</head>
<body>
    <header>
        {title}
    </header>
    <div class="content">
        <p>{message}</p>
        <a href="willbeeditlater" class="button">Download External Program</a>
        <p>Or explore more programs:</p>
        <a href="willbeeditlaterl-program" class="button">Explore More</a>
    </div>
</body>
</html>"""

    # Dateipfad für die HTML-Datei
    html_file_path = os.path.join(path, "index.html")
    
    # Versuchen, die Datei zu erstellen
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

def validate_product_key(key):
    """Überprüft, ob der Produktkey im richtigen Format ist und nicht generisch oder ungültig."""
    
    # Regulärer Ausdruck für das Format des Produktkeys (5 Gruppen von 5 Zeichen, getrennt durch '-')
    key_pattern = r'^[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}$'
    
    # Überprüfe, ob der Key dem Muster entspricht
    if not re.match(key_pattern, key):
        return False
    
    # Blockiere generische Keys, die aus exakt gleichen Zeichen bestehen (z.B. '11111-11111-11111-11111-11111')
    if re.match(r"^([A-Z0-9])\1{4}-\1{4}-\1{4}-\1{4}-\1{4}$", key):
        return False
    
    # Prüfe auf fortlaufende Ziffern oder Buchstaben (z.B. '12345-12345-12345-12345-12345' oder 'ABCDE-ABCDE-ABCDE-ABCDE-ABCDE')
    if re.match(r"(\d)\1{4}-(\d)\2{4}-(\d)\3{4}-(\d)\4{4}-(\d)\5{4}", key):
        return False
    if re.match(r"([A-Z])\1{4}-([A-Z])\2{4}-([A-Z])\3{4}-([A-Z])\4{4}-([A-Z])\5{4}", key):
        return False

    # Blockiere Keys, die aus aufeinanderfolgenden Ziffern oder Buchstaben bestehen (z.B. 'ABCDE-ABCDE-ABCDE-ABCDE-ABCDE')
    if re.match(r"([A-Z]{5})-\1-\1-\1-\1", key):
        return False
    if re.match(r"(\d{5})-\1-\1-\1-\1", key):
        return False

    # Überprüfe Kombinationen aus zufälligen Buchstaben/Ziffern mit wiederholten Ziffern
    # Beispiel: 'wnhj1-11111-11111-11111-11111' oder ähnliche Muster
    if re.match(r"^[A-Z0-9]{5}-\d{5}-\d{5}-\d{5}-\d{5}$", key):
        return False
    if re.match(r"^[A-Z0-9]{5}-[A-Z0-9]{5}-\d{5}-\d{5}-\d{5}$", key):
        return False
    if re.match(r"^[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-\d{5}-\d{5}$", key):
        return False

    # Eine Liste häufiger generischer oder ungültiger Keys (z.B. Test-Keys)
    invalid_keys = [
        "PRODUCT-KEY-XXXXX",  # Beispiel für einen Testkey
        "AAAAA-AAAAA-AAAAA-AAAAA-AAAAA",  # Ein generischer Key
        "11111-11111-11111-11111-11111",  # Wiederholte Ziffern
        "22222-22222-22222-22222-22222",  # Wiederholte Ziffern
        "12345-12345-12345-12345-12345",  # Eine häufige ungültige Zahlenkombination
        "ABCDE-ABCDE-ABCDE-ABCDE-ABCDE",  # Eine häufige ungültige Buchstabenkombination
    ]
    
    # Blockiere Keys, die in der Liste der ungültigen Keys sind
    if key in invalid_keys:
        return False
    
    # Zusätzliche Überprüfung für "schwache" Keys
    if re.match(r"^[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}$", key):
        # Überprüfe, ob der Key schwach ist (z.B. wenn der erste Teil des Keys aus sehr einfachen Zeichen besteht)
        if key.startswith("11111") or key.startswith("12345") or key.startswith("ABCDE"):
            return False

    return True

def show_welcome_page(root):
    """Zeigt die Willkommensseite im Hauptfenster an."""
    root.attributes('-fullscreen', True)
    root.title("Netscape Navigator OS V.0.6 DEV Release, Workstation Edition Setup")

    welcome_frame = tk.Frame(root, bg="darkblue")
    welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)

    welcome_label = tk.Label(welcome_frame, text="Willkommen zum Netscape Navigator OS V.0.6 Beta 2, Workstation Edition Setup", bg="darkblue", fg="yellow", font=("Arial", 22, "bold"))
    welcome_label.pack(pady=20)

    license_label = tk.Label(welcome_frame, text="Lizenzvereinbarung:", bg="darkblue", fg="yellow", font=("Arial", 18, "bold"))
    license_label.pack(pady=10)

    license_text = tk.Text(welcome_frame, wrap="word", bg="white", fg="black", font=("Arial", 12), height=20, width=90)
    license_text.insert("1.0", "EULA für Netscape Navigator OS 0.6 Beta 2 Workstation: Dies ist ein Produkt von Alte F1 Games, Sie sind nur zur Nutzung berechtigt. Jede Weiterverbreitung ist strafbar, das Copyright liegt ausschließlich bei AF1G/ New Netscape! Sie als Beta Tester dürfen Verbesserungsvorschläge senden, aber nicht selbst den Code verändern. Sie haben die Erlaubnis das OS zu installieren oder neu zu installieren! Da dies eine Beta ist, tragen Sie die Verantwortung für die Wartung Ihres eigenen Systems. Die NNOS Registry ist ein kritischer Teil von NNOS und darf nicht molifiziert werden, niemand ohne Kenntnis über die NNOS Registry sollte sie verwenden.")
    license_text.config(state="disabled")  # Nur-Lese-Modus
    license_text.pack(pady=10)

    button_frame = tk.Frame(welcome_frame, bg="darkblue")
    button_frame.pack(pady=10)

    accept_button = tk.Button(button_frame, text="Akzeptieren", command=lambda: show_key_input_page(root), bg="green", fg="black", font=("Arial", 14, "bold"))
    accept_button.pack(side="left", padx=10)

    cancel_button = tk.Button(button_frame, text="Abbrechen", command=root.quit, bg="red", fg="white", font=("Arial", 14, "bold"))
    cancel_button.pack(side="right", padx=10)

def show_key_input_page(root):
    """Zeigt die Seite zur Eingabe des Produktschlüssels."""
    clear_window(root)

    key_input_frame = tk.Frame(root, bg="darkblue")
    key_input_frame.pack(fill="both", expand=True, padx=20, pady=20)

    key_label = tk.Label(key_input_frame, text="Bitte geben Sie Ihren Produktkey ein, wir brauchen dies um die Echtheit der NNOS Kopie zu bestätigen.", bg="darkblue", fg="yellow", font=("Arial", 16))
    key_label.pack(pady=20)

    key_entry = tk.Entry(key_input_frame, width=40, font=("Arial", 14))
    key_entry.pack(pady=10)

    next_button = tk.Button(key_input_frame, text="Weiter", command=lambda: check_product_key(root, key_entry.get()), bg="green", fg="black", font=("Arial", 14, "bold"))
    next_button.pack(pady=10)

    cancel_button = tk.Button(key_input_frame, text="Abbrechen", command=root.quit, bg="red", fg="white", font=("Arial", 14, "bold"))
    cancel_button.pack(pady=10)

def check_product_key(root, key):
    """Überprüft den Produktschlüssel."""
    # Entferne führende und nachfolgende Leerzeichen und setze den Key in Großbuchstaben
    key = key.strip().upper()
    
    # Überprüfe den Produktschlüssel mit der erweiterten Validierungsfunktion
    if validate_product_key(key):
        messagebox.showinfo("Erfolg", "Produktkey ist gültig!")
        show_install_options(root)  # Zeigt die Installationsoptionen an
    else:
        messagebox.showerror("Fehler", "Ungültiger Produktschlüssel. Bitte versuchen Sie es erneut.")

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
    programms_dir = os.path.join(base_dir, "programms")

    create_directory(base_dir)
    create_directory(system_dir)
    create_directory(programms_dir)
    create_directory(document_dir)

    create_html_file(programms_dir)  # HTML-Datei im neuen Ordner erstellen

    show_progress(root, "Erstelle Verzeichnisse", 160)

    desktop_path = r"C:/Users/User/Desktop/Netscape Navigator OS V.0.6 Beta 2-Workstation.pyw"
    onedrive_path = r"C:/Users/User/OneDrive/Desktop/Netscape Navigator OS V.0.6 Beta 2-Workstation.pyw"
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

    # Kopiere die Datei in den Autostart
    copy_to_startup(destination_file)

    # Zeige die OOBE-Seite an
    show_oobe(root)

def show_oobe(root):
    """Zeigt die Out-Of-Box Experience (OOBE) an."""
    clear_window(root)

    oobe_frame = tk.Frame(root, bg="darkblue")
    oobe_frame.pack(fill="both", expand=True, padx=20, pady=20)

    oobe_label = tk.Label(oobe_frame, text="Erste Schritte", bg="darkblue", fg="yellow", font=("Arial", 24, "bold"))
    oobe_label.pack(pady=20)

    instructions = """Willkommen zu Ihrem neuen Netscape Navigator OS!\n
Hier sind einige Schritte, um Ihnen den Einstieg zu erleichtern:\n
1. Starten sie ihr Windows neu.\n
2. Registieren sie sich im Netscape Navigator OS.\n
3. Melden sie sich Anschießend in ihrer Workstation an..\n
4. Nutzen sie das Benutzerfreundliche NNOS.\n"""
    instructions_label = tk.Label(oobe_frame, text=instructions, bg="darkblue", fg="white", font=("Arial", 14))
    instructions_label.pack(pady=20)

    close_button = tk.Button(oobe_frame, text="Fertig", command=root.destroy, bg="green", fg="white", font=("Arial", 14, "bold"))
    close_button.pack(pady=10)

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
    """Öffnet einen Dateiauswahl-Dialog und gibt den Pfad der ausgewählten Datei zurück."""
    file_path = filedialog.askopenfilename(title="Wählen Sie eine Datei aus", filetypes=[("Python-Dateien", "*.pyw")])
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
