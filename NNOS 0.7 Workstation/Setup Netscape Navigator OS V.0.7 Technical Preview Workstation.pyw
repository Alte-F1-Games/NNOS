import os
import shutil
import tkinter as tk
from tkinter import ttk
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
    """Displays the modern welcome screen with license agreement."""
    root.attributes('-fullscreen', True)
    root.title("Netscape Navigator OS v0.7 Technical Preview Workstation Setup")

    style = ttk.Style()
    style.theme_use('default')
    style.configure("TFrame", background="#1e1e1e")
    style.configure("TLabel", background="#1e1e1e", foreground="#dddddd", font=("Segoe UI", 14))
    style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground="#00ffff")
    style.configure("TButton", font=("Segoe UI", 12), padding=6)
    style.map("TButton",
              background=[('active', '#007acc')],
              foreground=[('active', 'white')])

    welcome_frame = ttk.Frame(root)
    welcome_frame.pack(fill="both", expand=True, padx=40, pady=40)

    welcome_label = ttk.Label(welcome_frame, text="Welcome to the Netscape Navigator OS v0.7 Technical Preview Workstation Setup", style="Header.TLabel")
    welcome_label.pack(pady=(0, 30))

    license_label = ttk.Label(welcome_frame, text="End User License Agreement:")
    license_label.pack()

    license_text = tk.Text(welcome_frame, wrap="word", bg="#2b2b2b", fg="#f0f0f0", font=("Consolas", 10), height=18, width=90, relief="flat")
    license_text.insert("1.0", (
        "END USER LICENSE AGREEMENT (EULA)\n"
        "Netscape Navigator OS v0.7 Technical Preview Workstation\n\n"
        "IMPORTANT: Please read this agreement carefully before using this software.\n\n"
        "This software is provided by Alte F1 Games (AF1G) for evaluation and testing purposes only. "
        "By clicking 'Accept', you agree to the following terms:\n\n"
        "1. License Grant: You are granted a non-exclusive, non-transferable license to use this software solely for personal, "
        "non-commercial purposes. You may not redistribute, sublicense, or resell this software.\n\n"
        "2. Beta/Technical Preview Disclaimer: This is a Technical Preview release and may contain bugs, unfinished features, or performance issues. "
        "You acknowledge and accept that this version is not intended for production use.\n\n"
        "3. Modification: You may not modify, reverse-engineer, or decompile any part of the system, including but not limited to "
        "its registry and internal system components.\n\n"
        "4. Feedback: As a beta tester, you may provide feedback to AF1G. Feedback may be used to improve future versions.\n\n"
        "5. Termination: This license will terminate automatically if you fail to comply with its terms. Upon termination, "
        "you must delete all copies of the software.\n\n"
        "6. No Warranty: This software is provided 'AS IS', without warranty of any kind, either express or implied.\n\n"
        "By accepting this agreement, you confirm that you understand and agree to the above terms."
    ))
    license_text.config(state="disabled")
    license_text.pack(pady=20)

    button_frame = ttk.Frame(welcome_frame)
    button_frame.pack(pady=10)

    accept_button = ttk.Button(button_frame, text="Accept", command=lambda: show_key_input_page(root))
    accept_button.pack(side="left", padx=10)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=root.quit)
    cancel_button.pack(side="right", padx=10)

def show_key_input_page(root):
    """Displays the product key entry screen."""
    clear_window(root)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("TFrame", background="#1e1e1e")
    style.configure("TLabel", background="#1e1e1e", foreground="#dddddd", font=("Segoe UI", 14))
    style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#00ffff")
    style.configure("TButton", font=("Segoe UI", 12), padding=6)
    style.map("TButton",
              background=[('active', '#007acc')],
              foreground=[('active', 'white')])

    key_input_frame = ttk.Frame(root)
    key_input_frame.pack(fill="both", expand=True, padx=40, pady=40)

    key_label = ttk.Label(
        key_input_frame,
        text="Please enter your product key. This is required to verify the authenticity of your NNOS installation.",
        style="Header.TLabel",
        wraplength=700,
        justify="center"
    )
    key_label.pack(pady=(0, 30))

    key_var = tk.StringVar()
    key_entry = ttk.Entry(key_input_frame, textvariable=key_var, font=("Consolas", 14), width=35)
    key_entry.pack(pady=10)
    key_entry.focus()

    button_frame = ttk.Frame(key_input_frame)
    button_frame.pack(pady=20)

    next_button = ttk.Button(button_frame, text="Next", command=lambda: check_product_key(root, key_var.get()))
    next_button.pack(side="left", padx=10)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=root.quit)
    cancel_button.pack(side="right", padx=10)

def check_product_key(root, key):
    """Überprüft den Produktschlüssel."""
    # Entferne führende und nachfolgende Leerzeichen und setze den Key in Großbuchstaben
    key = key.strip().upper()
    
    # Überprüfe den Produktschlüssel mit der erweiterten Validierungsfunktion
    if validate_product_key(key):
        messagebox.showinfo("Success", "Productkey is authentic!")
        show_install_options(root) 
    else:
        messagebox.showerror("Error", "Productkey does not match to Install this Veraion of NNOS, try again.")

def show_install_options(root):
    """Displays the installation options page."""
    clear_window(root)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("TFrame", background="#1e1e1e")
    style.configure("TLabel", background="#1e1e1e", foreground="#dddddd", font=("Segoe UI", 14))
    style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#00ffff")
    style.configure("TButton", font=("Segoe UI", 12), padding=6)
    style.map("TButton",
              background=[('active', '#007acc')],
              foreground=[('active', 'white')])

    options_frame = ttk.Frame(root)
    options_frame.pack(fill="both", expand=True, padx=40, pady=40)

    instruction_label = ttk.Label(options_frame, text="Installation Directory:", style="Header.TLabel")
    instruction_label.pack(pady=(0, 10))

    fixed_dir = "C:\\NNOS"
    dir_var = tk.StringVar(value=fixed_dir)
    dir_entry = ttk.Entry(options_frame, textvariable=dir_var, font=("Consolas", 13), width=40, state="disabled")
    dir_entry.pack(pady=10)

    button_frame = ttk.Frame(options_frame)
    button_frame.pack(pady=30)

    install_button = ttk.Button(button_frame, text="Install", command=lambda: start_installation(root, fixed_dir))
    install_button.pack(side="left", padx=10)

    repair_button = ttk.Button(button_frame, text="Repair", command=lambda: repair_installation(root, fixed_dir))
    repair_button.pack(side="left", padx=10)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=root.quit)
    cancel_button.pack(side="left", padx=10)

def clear_window(root):
    """Leert das Hauptfenster."""
    for widget in root.winfo_children():
        widget.destroy()

def show_progress(root, message, total_steps):
    """Displays installation progress screen."""
    clear_window(root)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("TFrame", background="#1e1e1e")
    style.configure("TLabel", background="#1e1e1e", foreground="#dddddd", font=("Segoe UI", 14))
    style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#00ffff")

    progress_frame = ttk.Frame(root)
    progress_frame.pack(fill="both", expand=True, padx=40, pady=40)

    progress_label = ttk.Label(progress_frame, text=message, style="Header.TLabel", wraplength=600, justify="center")
    progress_label.pack(pady=20)

    progress_bar = ttk.Progressbar(progress_frame, length=500, mode="determinate")
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

    show_progress(root, "Create Directorys", 160)

    desktop_path = r"C:/Users/User/Desktop/Netscape Navigator OS V.0.7 Technical Preview Workstation.pyw"
    onedrive_path = r"C:/Users/User/OneDrive/Desktop/Netscape Navigator OS V.0.7 Technical Preview Workstation.pyw"
    destination_file = os.path.join(system_dir, "Netscape Navigator OS.sys.pyw")

    source_file = None
    if os.path.isfile(desktop_path):
        source_file = desktop_path
    elif os.path.isfile(onedrive_path):
        source_file = onedrive_path

    if not source_file:
        source_file = select_file(root)
        if not source_file:
            messagebox.showerror("Error", "No file for Installtion selceted, abort Installtion.")
            root.destroy()
            return

    copy_file(source_file, destination_file)
    show_progress(root, "Copy files", 160)

    # Kopiere die Datei in den Autostart
    copy_to_startup(destination_file)

    
    show_oobe(root)

def show_oobe(root):
    clear_window(root)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("TFrame", background="#1e1e1e")
    style.configure("Feature.TLabel", font=("Segoe UI", 16, "bold"), foreground="#00ffff", background="#1e1e1e")
    style.configure("Desc.TLabel", font=("Segoe UI", 12), foreground="white", background="#1e1e1e")

    oobe_frame = ttk.Frame(root)
    oobe_frame.pack(fill="both", expand=True, padx=20, pady=20)

    canvas = tk.Canvas(oobe_frame, bg="#1e1e1e", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    features = [
        ("Modern User Interface", "Netscape Navigator OS V.0.7 Technical Preview have a new modern UI for the Logon Menu (includeing Login and Register a New User), in the Control Panel, My Computer and Notepad."),
        ("More Powerfull User Control", "User Control can now change the Passowrd of Users and Search Users by his Name."),
        ("Legacy App Support", "Runs all previews NNOS Software nativly."),
        ("A better My Computer", "My Computer can now create new .txt Files and Folder move Copx, Rename, Delete with Create a txt File and folder in a rightclick Menu for more Productiv Work."),
        ("Optimized Performance", "NNOS 0.7 Technical Preview run with the New UI and Functions so fast as NNOS 0.6 Beta 2, so you can have a better looking OS with no performace Lost.")
    ]

    slide_frames = []
    for title, desc in features:
        frame = tk.Frame(canvas, bg="#1e1e1e", width=600, height=200)
        ttk.Label(frame, text=title, style="Feature.TLabel").pack(pady=(10, 5))
        ttk.Label(frame, text=desc, style="Desc.TLabel", wraplength=500, justify="center").pack()
        slide_frames.append(frame)

    current_slide = [0]  
    slide_widgets = []

    def animate_slide_in(index):
        canvas.delete("all")
        slide = slide_frames[index]
        slide.update_idletasks()

        widget_window = canvas.create_window(800, 100, window=slide, anchor="nw")  

        def move_left(x=800):
            if x > 100:
                canvas.move(widget_window, -20, 0)
                root.after(10, lambda: move_left(x - 20))
            else:
                root.after(3000, show_next_slide)

        move_left()

    def show_next_slide():
        current_slide[0] = (current_slide[0] + 1) % len(slide_frames)
        animate_slide_in(current_slide[0])

    animate_slide_in(0)

    finish_button = ttk.Button(oobe_frame, text="Start Using NNOS after a Windows reboot", command=root.destroy)
    finish_button.pack(pady=20)

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
