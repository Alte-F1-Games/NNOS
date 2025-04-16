import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog, Toplevel, Listbox, Scrollbar
import subprocess
import os
import time
import shutil
import json
import ctypes
import sys
import socket
import threading

# Pfade zu den Benutzerprofilen
USER_DATA_DIR = r'C:\NNOS-Server\system'
USER_FILE_TEMPLATE = os.path.join(USER_DATA_DIR, '{}.json')

def make_fullscreen(window):
    """Setzt das Fenster in den Vollbildmodus und verhindert, dass es geschlossen wird."""
    window.attributes("-fullscreen", True)  # Setzt das Fenster in den Vollbildmodus
    window.protocol("WM_DELETE_WINDOW", disable_event)  # Deaktiviert das Schließen des Fensters

def disable_event():
    """Verhindert, dass das Fenster durch das Schließen-Symbol geschlossen wird."""
    pass

def login_screen():
    """Erstellt einen Login-Bildschirm und verarbeitet die Benutzerdaten."""
    login = tk.Toplevel(root)
    login.title("Login")
    make_fullscreen(login)  # Vollbildmodus aktivieren

    # Optische Anpassungen
    login.configure(bg='#282C34')  # Dunkler Hintergrund für Modernität
    label_font = ('Helvetica', 14)

    tk.Label(login, text="Username", bg='#282C34', fg='#61AFEF', font=label_font).pack(pady=10)
    username_entry = tk.Entry(login, font=label_font)
    username_entry.pack(pady=5)

    tk.Label(login, text="Password", bg='#282C34', fg='#61AFEF', font=label_font).pack(pady=10)
    password_entry = tk.Entry(login, show='*', font=label_font)
    password_entry.pack(pady=5)
    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        if validate_user(username, password):
            login.destroy()  # Schließt das Login-Fenster
            root.deiconify()  # Zeigt das Hauptfenster wieder an
            startup()  # OS-Startup, falls das Login erfolgreich ist
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    # Attraktiver Button
    tk.Button(login, text="Login", command=attempt_login, font=label_font, bg='#98C379', fg='white', relief="groove").pack(pady=20)

def validate_user(username, password):
    """Überprüft den Benutzer und das Passwort gegen die gespeicherten Daten."""
    user_file = USER_FILE_TEMPLATE.format(username)
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        if user_data.get('password') == password:
            return True
    return False

def register_screen():
    """Erstellt einen Registrierungsbildschirm."""
    register = tk.Toplevel(root)
    register.title("Register")
    make_fullscreen(register)  # Vollbildmodus aktivieren

    # Optische Anpassungen
    register.configure(bg='#282C34')
    label_font = ('Helvetica', 14)

    tk.Label(register, text="Choose a Username", bg='#282C34', fg='#61AFEF', font=label_font).pack(pady=10)
    new_username_entry = tk.Entry(register, font=label_font)
    new_username_entry.pack(pady=5)

    tk.Label(register, text="Choose a Password", bg='#282C34', fg='#61AFEF', font=label_font).pack(pady=10)
    new_password_entry = tk.Entry(register, show='*', font=label_font)
    new_password_entry.pack(pady=5)

    def register_user():
        username = new_username_entry.get()
        password = new_password_entry.get()
        user_file = USER_FILE_TEMPLATE.format(username)
        if not os.path.exists(user_file):
            user_data = {
                "username": username,
                "password": password
            }
            with open(user_file, 'w') as f:
                json.dump(user_data, f)
            messagebox.showinfo("Registration Successful", "You can now log in.")
            register.destroy()
        else:
            messagebox.showerror("Registration Failed", "Username already exists.")

    tk.Button(register, text="Register", command=register_user, font=label_font, bg='#98C379', fg='white', relief="groove").pack(pady=20)

def show_login_options():
    """Zeigt die Login- und Registrierungsoptionen an."""
    option_screen = tk.Toplevel(root)
    option_screen.title("Login Options")
    make_fullscreen(option_screen)  # Vollbildmodus aktivieren

    # Optische Anpassungen
    option_screen.configure(bg='#282C34')
    button_font = ('Helvetica', 14)

    tk.Button(option_screen, text="Login on NNOS Server", command=login_screen, font=button_font, bg='#61AFEF', fg='darkblue', relief="groove").pack(pady=12)
    tk.Button(option_screen, text="Register on NNOS Server", command=register_screen, font=button_font, bg='#61AFEF', fg='green', relief="groove").pack(pady=10)

def startup():
    """Funktion, die beim erfolgreichen Login ausgeführt wird."""
    messagebox.showinfo("System Startup", "System started successfully")
    
# Hauptfenster (root)
root = tk.Tk()
root.withdraw()  # Versteckt das Hauptfenster bis der Login erfolgreich ist
show_login_options()  # Zeige den Login-Bildschirm


# Pfad zu Netscape Navigator
NAVIGATOR_PATH = r'C:\Program Files\Netscape\Navigator 9\navigator.exe'

# Pfade zu den notwendigen Dateien und Ordnern
NAVIGATOR_OS_PATH = r'C:\NNOS-Server'
NAVIGATOR_INSTALLER_PATH = os.path.join(NAVIGATOR_OS_PATH, 'system', 'Netscape Navigator OS.sys.pyw')

def check_and_setup():
    """Überprüft und richtet die notwendigen Dateien und Ordner ein."""
    missing_files_or_dirs = False

    if not os.path.isdir(NAVIGATOR_OS_PATH):
        missing_files_or_dirs = True
    elif not os.path.isdir(os.path.dirname(NAVIGATOR_INSTALLER_PATH)):
        missing_files_or_dirs = True
    elif not os.path.exists(NAVIGATOR_INSTALLER_PATH):
        missing_files_or_dirs = True

    if missing_files_or_dirs:
        show_red_screen()

def show_red_screen():
    rsod = tk.Toplevel(root)
    rsod.title("RSOD: SYSTEM FAILURE")
    rsod.attributes('-fullscreen', True)
    rsod.config(bg="red")
    set_always_on_top(rsod)

    header = tk.Label(rsod, text=":( RSOD: System File Error", font=("Arial", 48, "bold"), bg="red", fg="white")
    header.pack(pady=50)

    debug_dump = tk.Label(
        rsod,
        text="""
*** STOP: 0x000001E (0x00000000, 0x00000000, 0x00000000)
A problem has been detected and NNOS has been shut down to prevent damage
to your Netscape Navigator Operating System.

If this is the first time you’ve seen this RSOD screen,
restart your computer. If this screen appears again, please check:

Have you made a NNOS System Update and interrupt that, when yes, NNOS have not copied the Netscape Navigator OS.sys.pyw in C:\\NNOS-Server\\system

System file: Netscape Navigator OS.sys.pyw not found
Folder: C:\\NNOS-Server\\system is missing or corrupt.
""",
        font=("Courier New", 10),
        bg="red",
        fg="white",
        justify="left"
    )
    debug_dump.pack(pady=20)

# Simulierter blinkender Cursor
    cursor = tk.Label(rsod, text="_", font=("Courier New", 16), bg="red", fg="white")
    cursor.pack(anchor='w', padx=50, pady=10)

    def blink():
        cursor.config(text="_" if cursor.cget("text") == " " else " ")
        rsod.after(500, blink)

    blink()

    # Optional: nach 10 Sekunden automatisch beenden
    rsod.after(15000, root.quit)

def set_always_on_top(window):
    window.attributes('-topmost', True)

def show_startup_screen():
    """Zeigt den Startbildschirm mit gelbem Hintergrund und Begrüßungstext an."""
    startup = tk.Toplevel(root)
    startup.title("Netscape Navigator OS :)")
    startup.attributes('-fullscreen', True)  # Vollbildmodus aktivieren
    startup.config(bg="yellow")
    set_always_on_top(startup)
    
    header = tk.Label(startup, text="Netscape Navigator OS :)", font=("Arial", 48, "bold"), bg="yellow")
    header.pack(pady=50)

    welcome_text = tk.Label(startup, text="Willkommen", font=("Arial", 24), bg="yellow")
    welcome_text.pack()

    version_text = tk.Label(startup, text="Version 0.5 Beta 1, Server Edition", font=("Arial", 20), bg="blue")
    version_text.pack()

    # Timer setzen, um das Startup-Fenster nach 3 Sekunden zu schließen
    startup.after(3000, startup.destroy)  # Nach 3 Sekunden das Fenster schließen

def startup():
    """Funktion, die beim Systemstart aufgerufen wird."""
    print("Starte das System...")
    try:
        initialize_system()
        check_and_setup()
        print("System erfolgreich gestartet.")
    except Exception as e:
        print(f"Fehler beim Starten des Systems: {e}")
        show_red_screen()

def initialize_system():
    """Systeminitialisierung bei Startup."""
    print("Systeminitialisierung...")
    if not os.path.exists(NAVIGATOR_INSTALLER_PATH):
        raise FileNotFoundError("Notwendige Datei fehlt.")

def show_shutdown_screen():
    """Zeigt den Shutdown-Bildschirm im Vollbildmodus an."""
    shutdown_window = tk.Toplevel(root)
    shutdown_window.title("Shutdown")
    shutdown_window.attributes('-fullscreen', True)
    shutdown_window.config(bg="black")
    shutdown_window.protocol("WM_DELETE_WINDOW", disable_event)

    header = tk.Label(shutdown_window, text="Netscape Navigator OS is shutting Down...", font=("Arial", 48, "bold"), bg="black", fg="red")
    header.pack(pady=50)

    shutdown_message = tk.Label(shutdown_window, text="Stopping NNOS Services... Please wait while the system shuts down.", font=("Arial", 24), bg="black", fg="white")
    shutdown_message.pack()

    # Nach einer kurzen Verzögerung schließen wir die Anwendung
    shutdown_window.after(3000, lambda: root.quit())  # Warte 3 Sekunden, dann beende das Hauptfenster


def show_restart_screen():
    """Zeigt den Restart-Bildschirm im Vollbildmodus an und startet das Programm nach einer Verzögerung neu."""
    restart_window = tk.Toplevel(root)
    restart_window.title("Restart")
    restart_window.attributes('-fullscreen', True)
    restart_window.config(bg="black")
    restart_window.protocol("WM_DELETE_WINDOW", disable_event)

    header = tk.Label(restart_window, text="Netscape Navigator OS is restarting...", font=("Arial", 48, "bold"), bg="black", fg="red")
    header.pack(pady=50)

    restart_message = tk.Label(restart_window, text="Restarting NNOS Services... Please wait while the system restarts", font=("Arial", 24), bg="black", fg="white")
    restart_message.pack()

    # Nach einer kurzen Verzögerung das Programm neu starten
    restart_window.after(3000, lambda: restart_program())

def restart_program():
    """Startet das Programm neu."""
    python = sys.executable
    try:
        # Starte das Programm mit subprocess.Popen
        subprocess.Popen([python] + sys.argv)  # Startet das Skript neu
        root.quit()  # Beendet das alte Programmfenster
    except Exception as e:
        print(f"Fehler beim Neustart: {e}")

def disable_event():
    """Verhindert das Schließen des Restart-Fensters."""
    pass

def open_netscape():
    """Öffnet den Netscape Navigator."""
    try:
        if os.path.exists(NAVIGATOR_PATH):
            subprocess.Popen([NAVIGATOR_PATH], shell=True)
        else:
            messagebox.showwarning("Warnung", "Netscape Navigator nicht gefunden!")
    except Exception as e:
        messagebox.showerror("Fehler", str(e))
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog

def open_notepad():
    notepad = tk.Toplevel(root)
    notepad.title("Notepad")
    notepad.geometry("400x300")
    notepad.config(bg="lightgrey")
    set_always_on_top(notepad)

    text_area = scrolledtext.ScrolledText(notepad, wrap=tk.WORD, bg="lightgrey", fg="black")
    text_area.pack(expand=True, fill='both')

    def save_file():
        file_name = simpledialog.askstring("Speichern unter", "Dateiname:")
        if file_name:
            try:
                # Verwende den vollständigen Pfad
                file_path = os.path.join(r'C:\NNOS-Server\document', file_name)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(text_area.get(1.0, tk.END).strip())
                messagebox.showinfo("Info", "Datei gespeichert.")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Speichern ERROR 72: {str(e)}")

    def open_file():
        file_name = simpledialog.askstring("Öffnen", "Dateiname:")
        if file_name:
            try:
                # Verwende den vollständigen Pfad
                file_path = os.path.join(r'C:\NNOS-Server\document', file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    text_area.delete(1.0, tk.END)  # Textbereich leeren
                    text_area.insert(tk.END, file.read())  # Inhalt der Datei einfügen
            except FileNotFoundError:
                messagebox.showerror("Fehler", "Datei nicht gefunden. ERROR 73")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Öffnen ERROR 74: {str(e)}")

    def new_file():
        text_area.delete(1.0, tk.END)  # Textbereich leeren

    # Menü erstellen
    notepad_menu = tk.Menu(notepad)
    file_menu = tk.Menu(notepad_menu, tearoff=0)
    file_menu.add_command(label="New", command=new_file)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=notepad.destroy)

    help_menu = tk.Menu(notepad_menu, tearoff=0)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Notepad Version 1.2 for Netscape Navigator OS V.0.5 Beta 1 "))

    notepad_menu.add_cascade(label="File", menu=file_menu)
    notepad_menu.add_cascade(label="Help", menu=help_menu)
    notepad.config(menu=notepad_menu)

def open_calculator():
    calculator = tk.Toplevel(root)
    calculator.title("Calculator")
    calculator.geometry("250x300")
    calculator.config(bg="lightgrey")
    set_always_on_top(calculator)

    result_area = tk.Label(calculator, text="", bg="white", anchor='e', font=("Arial", 18), relief=tk.SUNKEN)
    result_area.grid(row=0, column=0, columnspan=4, sticky='nsew')

    def append_operation(operation):
        result_area['text'] += str(operation)

    def calculate_result():
        try:
            result_area['text'] = str(eval(result_area['text']))
        except Exception as e:
            result_area['text'] = "Error"

    def delete_last():
        result_area['text'] = result_area['text'][:-1]

    buttons = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
        ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
        ('DEL', 5, 0)
    ]

    for (text, row, col) in buttons:
        if text == '=':
            btn = tk.Button(calculator, text=text, command=calculate_result, bg="lightgrey", font=("Arial", 14))
        elif text == 'DEL':
            btn = tk.Button(calculator, text=text, command=delete_last, bg="lightgrey", font=("Arial", 14))
        else:
            btn = tk.Button(calculator, text=text, command=lambda t=text: append_operation(t), bg="lightgrey", font=("Arial", 14))
        btn.grid(row=row, column=col, sticky='nsew')

    for i in range(6):
        calculator.grid_rowconfigure(i, weight=1)
    for i in range(4):
        calculator.grid_columnconfigure(i, weight=1)

def open_file_explorer(mode="open"):
    explorer = tk.Toplevel(root)
    explorer.title("Datei Auswahl")
    explorer.geometry("500x150")
    set_always_on_top(explorer)

    def browse_file():
        if mode == "open":
            file_path = filedialog.askopenfilename()
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            path_var.set(file_path)

    def confirm_selection():
        path = path_var.get()
        if mode == "save" or os.path.exists(path):
            explorer.destroy()
            return path
        else:
            messagebox.showerror("Fehler", "Der angegebene Pfad ist nicht gültig.")
            return None

    path_var = tk.StringVar()
    path_entry = tk.Entry(explorer, textvariable=path_var, width=60)
    path_entry.pack(pady=10)

    browse_button = tk.Button(explorer, text="Durchsuchen", command=browse_file)
    browse_button.pack(pady=5)

    confirm_button = tk.Button(explorer, text="Bestätigen", command=confirm_selection)
    confirm_button.pack(pady=10)

    explorer.wait_window()  # Warten, bis das Fenster geschlossen wird

    return path_var.get()

def open_clock():
    clock = tk.Toplevel(root)
    clock.title("Clock")
    clock.geometry("250x150")
    clock.config(bg="lightgrey")
    set_always_on_top(clock)

    time_label = tk.Label(clock, text="", font=("Arial", 48), bg="lightgrey")
    time_label.pack(expand=True)

    def update_time():
        current_time = time.strftime("%H:%M:%S")
        time_label.config(text=current_time)
        clock.after(1000, update_time)  # Aktualisiert jede Sekunde

    update_time()

def open_trash():
    trash = tk.Toplevel(root)
    trash.title("Trash")
    trash.geometry("300x400")
    trash.config(bg="lightgrey")
    set_always_on_top(trash)

    trash_listbox = tk.Listbox(trash, selectmode=tk.MULTIPLE)
    trash_listbox.pack(expand=True, fill='both')

    # Pfad-Daten speichern, um die ursprünglichen Speicherorte der Dateien zu verwalten
    trash_data_file = r'C:\NNOS-Server\Trash\trash_data.json'

    def list_trash():
        """Füllt die Listbox mit den Dateien im Papierkorb."""
        trash_listbox.delete(0, tk.END)
        trash_folder = r'C:\NNOS\Trash'
        if os.path.exists(trash_folder):
            files = os.listdir(trash_folder)
            for item in files:
                trash_listbox.insert(tk.END, item)
        else:
            os.makedirs(trash_folder)

    def delete_selected():
        """Löscht die ausgewählten Dateien im Papierkorb."""
        selected_files = [trash_listbox.get(i) for i in trash_listbox.curselection()]
        trash_folder = r'C:\NNOS-Server\Trash'
        for file in selected_files:
            file_path = os.path.join(trash_folder, file)
            # Verhindern, dass die kritische Datei gelöscht wird
            if file == 'Netscape Navigator OS.sys.pyw':
                messagebox.showerror("Fehler", f"Die Datei {file} kann nicht gelöscht werden!")
                continue  # Überspringen, wenn es die geschützte Datei ist
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  # Datei löschen
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Verzeichnis löschen
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Löschen von {file}: {e}")
        list_trash()  # Aktualisiert die Liste nach dem Löschen

    def restore_selected():
        """Stellt die ausgewählten Dateien aus dem Papierkorb wieder her."""
        selected_files = [trash_listbox.get(i) for i in trash_listbox.curselection()]
        trash_folder = r'C:\NNOS-Server\Trash'
        # Lade die ursprünglichen Speicherorte aus der JSON-Datei
        if os.path.exists(trash_data_file):
            with open(trash_data_file, 'r') as f:
                trash_data = json.load(f)
        else:
            trash_data = {}

        for file in selected_files:
            file_path = os.path.join(trash_folder, file)
            if file in trash_data:  # Wenn der ursprüngliche Pfad bekannt ist
                restore_path = trash_data[file]  # Pfad zum ursprünglichen Speicherort
                try:
                    shutil.move(file_path, restore_path)  # Datei wiederherstellen
                    messagebox.showinfo("Erfolg", f"Datei {file} wurde wiederhergestellt.")
                except Exception as e:
                    messagebox.showerror("Fehler", f"Fehler beim Wiederherstellen von {file}: {e}")
            else:
                messagebox.showwarning("Warnung", f"Kein ursprünglicher Pfad für {file} gefunden.")
        list_trash()  # Aktualisiert die Liste nach der Wiederherstellung

    def custom_open_file():
        """Öffnet ein benutzerdefiniertes Eingabefeld zur Dateiauswahl."""
        file_path = simpledialog.askstring("Datei hinzufügen", "Bitte den Pfad zur Datei eingeben:")
        if file_path and os.path.isfile(file_path):
            add_file_to_trash(file_path)

    def add_file_to_trash(file_path):
        """Fügt eine Datei zum Papierkorb hinzu und speichert den ursprünglichen Pfad."""
        trash_folder = r'C:\NNOS-Server\Trash'
        if not os.path.exists(trash_folder):
            os.makedirs(trash_folder)
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(trash_folder, file_name)

        # Lade die bestehenden Trash-Daten
        if os.path.exists(trash_data_file):
            with open(trash_data_file, 'r') as f:
                trash_data = json.load(f)
        else:
            trash_data = {}

        # Den ursprünglichen Pfad speichern
        trash_data[file_name] = file_path

        try:
            if os.path.exists(dest_path):
                messagebox.showwarning("Warnung", "Datei existiert bereits im Papierkorb.")
            else:
                shutil.move(file_path, trash_folder)  # Datei verschieben
                with open(trash_data_file, 'w') as f:
                    json.dump(trash_data, f)  # Pfaddaten speichern
                list_trash()  # Aktualisiert die Liste
                messagebox.showinfo("Info", f"Datei '{file_name}' zum Papierkorb hinzugefügt.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Hinzufügen der Datei: {e}")

    # Buttons für den Papierkorb
    add_button = tk.Button(trash, text="Datei hinzufügen", command=custom_open_file)
    add_button.pack(pady=10)

    delete_button = tk.Button(trash, text="Ausgewählte löschen", command=delete_selected)
    delete_button.pack(pady=10)

    restore_button = tk.Button(trash, text="Ausgewählte wiederherstellen", command=restore_selected)
    restore_button.pack(pady=10)

    # Initiales Auffüllen der Listbox
    list_trash()


def open_my_computer():
    """Öffnet das Fenster 'Mein Computer' und zeigt Laufwerke als durchsuchbare Ordner an."""
    my_computer = tk.Toplevel(root)
    my_computer.title("My Computer")
    my_computer.geometry("600x400")
    my_computer.config(bg="lightgrey")
    set_always_on_top(my_computer)

    def list_directory(path):
        """Zeigt den Inhalt eines Verzeichnisses in einer Listbox an."""
        contents_listbox.delete(0, tk.END)
        try:
            for item in os.listdir(path):
                contents_listbox.insert(tk.END, item)
        except PermissionError:
            messagebox.showerror("Fehler", "Zugriff verweigert.")
        except FileNotFoundError:
            messagebox.showerror("Fehler", "Verzeichnis nicht gefunden.")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    def open_item(event):
        """Öffnet das ausgewählte Verzeichnis oder Datei."""
        selected_item = contents_listbox.get(tk.ACTIVE)
        if selected_item:
            current_path = os.path.join(current_directory.get(), selected_item)
            if os.path.isdir(current_path):
                list_directory(current_path)
                current_directory.set(current_path)
            elif selected_item.endswith(".txt"):
                open_notepad_with_file(current_path)
            elif selected_item.endswith(".py") or selected_item.endswith(".pyw"):
                # Python Skripte ausführen
                run_python_script(current_path)
            else:
                messagebox.showinfo("Info", f"{selected_item} ist keine Verzeichnis oder .txt Datei.")

    def go_up():
        """Geht eine Ebene nach oben im Verzeichnisbaum."""
        parent_directory = os.path.dirname(current_directory.get())
        list_directory(parent_directory)
        current_directory.set(parent_directory)

    current_directory = tk.StringVar(value="C:/")  # Startverzeichnis

    contents_listbox = tk.Listbox(my_computer)
    contents_listbox.pack(expand=True, fill='both')

    up_button = tk.Button(my_computer, text="Up", command=go_up)
    up_button.pack(side=tk.TOP, anchor='w', padx=10, pady=10)

    list_directory(current_directory.get())
    contents_listbox.bind("<Double-1>", open_item)

def run_python_script(file_path):
    """Führt ein Python-Skript aus (für .py oder .pyw Dateien)."""
    try:
        if file_path.endswith(".pyw"):
            # .pyw Dateien im Hintergrund ohne Konsole ausführen
            subprocess.Popen(["pythonw", file_path])
        else:
            # .py Dateien im Konsolenmodus ausführen
            subprocess.Popen(["python", file_path])
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Ausführen des Skripts: {str(e)}")

def open_notepad_with_file(file_path):
    """Öffnet eine .txt Datei im Notepad."""
    notepad = tk.Toplevel(root)
    notepad.title(f"Notepad - {file_path}")
    notepad.geometry("400x300")
    notepad.config(bg="lightgrey")
    set_always_on_top(notepad)

    text_area = scrolledtext.ScrolledText(notepad, wrap=tk.WORD, bg="lightgrey", fg="black")
    text_area.pack(expand=True, fill='both')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text_area.insert(tk.END, file.read())
    except FileNotFoundError:
        messagebox.showerror("Fehler", "Datei nicht gefunden.")

    def save_file():
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text_area.get(1.0, tk.END).strip())
            messagebox.showinfo("Info", "Datei gespeichert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {str(e)}")

    notepad_menu = tk.Menu(notepad)
    file_menu = tk.Menu(notepad_menu, tearoff=0)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_command(label="Exit", command=notepad.destroy)
    notepad_menu.add_cascade(label="File", menu=file_menu)
    notepad.config(menu=notepad_menu)

# Funktion für die Benutzerverwaltung
def manage_users():
    # Verzeichnis mit den Benutzerdateien
    user_dir = r'C:\NNOS-Server\system'
    
    # Überprüfen, ob das Verzeichnis existiert
    if not os.path.exists(user_dir):
        messagebox.showerror("Fehler", f"Benutzerverzeichnis {user_dir} nicht gefunden!")
        return
    
    # Alle .json-Dateien im Verzeichnis auflisten (jede Datei stellt einen Benutzer dar)
    users = [f for f in os.listdir(user_dir) if f.endswith('.json')]

    # Fenster zur Benutzerverwaltung öffnen
    user_window = tk.Toplevel(root)
    user_window.title("User Control")
    user_window.geometry('400x300')
    user_window.configure(bg='#f0f0f0')

    # Panel-Überschrift
    tk.Label(user_window, text="User Control", font=('Helvetica', 12), bg='#f0f0f0').pack(pady=10)

    # Benutzer anzeigen
    user_listbox = tk.Listbox(user_window, height=10, width=40, font=('Helvetica', 10))
    for user in users:
        user_listbox.insert(tk.END, user)  # Zeige nur die Dateinamen (Benutzernamen)
    user_listbox.pack(pady=10)

    # Benutzer löschen
    def delete_user():
        selected_user = user_listbox.curselection()
        if not selected_user:
            messagebox.showwarning("Warnung", "Bitte wählen Sie einen Benutzer aus!")
            return

        user_to_delete = users[selected_user[0]]
        user_path = os.path.join(user_dir, user_to_delete)
        
        # Löschen des Benutzers
        try:
            os.remove(user_path)  # Löscht die JSON-Datei
            users.remove(user_to_delete)  # Entfernt den Benutzer aus der Liste
            user_listbox.delete(selected_user)  # Entfernt den Benutzer aus der Anzeige
            messagebox.showinfo("Erfolg", f"Benutzer {user_to_delete} wurde gelöscht!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Löschen des Benutzers: {str(e)}")

    # Button zum Löschen eines Benutzers
    tk.Button(user_window, text="User delete", command=delete_user, font=('Helvetica', 10), bg='#FF5722', fg='white').pack(pady=10)

# Beispielaktionen für verschiedene Funktionen
def open_settings():
    messagebox.showinfo("Einstellungen", "Einstellungen wurden geöffnet!")

def show_system_info():
    messagebox.showinfo("Systeminfo", "Betriebssystem: Netscape Navigator OS\nVersion: 0.5 Beta 1")

def manage_programs():
    messagebox.showinfo("Programme", "Programmverwaltung: Programme starten oder beenden")

# Control Panel-Fenster erstellen
def open_control_panel():
    panel_window = tk.Toplevel(root)
    panel_window.title("Control Panel")
    panel_window.geometry('400x300')
    panel_window.configure(bg='#f0f0f0')

    # Panel-Überschrift
    label_font = ('Helvetica', 12)
    tk.Label(panel_window, text="Netscape Navigator OS 0.5 Beta 1 Control Panel", font=label_font, bg='#f0f0f0').pack(pady=10)

    # Buttons für verschiedene Funktionen
    tk.Button(panel_window, text="Einstellungen", command=open_settings, font=label_font, bg='#4CAF50', fg='white').pack(pady=10)
    tk.Button(panel_window, text="Programme verwalten", command=manage_programs, font=label_font, bg='#FF9800', fg='white').pack(pady=10)
    tk.Button(panel_window, text="User Control", command=manage_users, font=label_font, bg='#FF5722', fg='white').pack(pady=10)


def create_icon(name, command, x, y):
    icon = tk.Button(root, text=name, command=command, bg="lightgrey", font=("Arial", 12), width=20, height=2)
    icon.place(x=x, y=y)
    
    def on_drag_start(event):
        icon._drag_data = {'x': event.x, 'y': event.y}

    def on_drag_end(event):
        context_menu.post(event.x_root, event.y_root)
    
    def on_drag_motion(event):
        x = icon.winfo_x() - icon._drag_data['x'] + event.x
        y = icon.winfo_y() - icon._drag_data['y'] + event.y
        icon.place(x=x, y=y)
    
    def show_start_option():
        result = messagebox.askyesno("Starten?", f"Willst du '{name}' starten?")
        if result:
            command()

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 12345
SERVER_FILES_PATH = r'C:\NNOS-Server\Files'

def start_nnos_server():
    if not os.path.exists(SERVER_FILES_PATH):
        os.makedirs(SERVER_FILES_PATH)

    class ServerApp:
        def __init__(self, root):
            self.root = root
            self.root.title("NNOS File Server Manager")
            self.root.geometry("500x400")

            self.log = tk.Text(root, state="disabled", bg="black", fg="lime")
            self.log.pack(expand=True, fill="both")

            threading.Thread(target=self.start_server, daemon=True).start()

        def log_msg(self, msg):
            self.log.config(state="normal")
            self.log.insert("end", msg + "\n")
            self.log.see("end")
            self.log.config(state="disabled")

        def start_server(self):
            try:
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.bind((SERVER_HOST, SERVER_PORT))
                server_socket.listen(5)
                self.log_msg(f"📡 Server gestartet auf Port {SERVER_PORT}")

                while True:
                    conn, addr = server_socket.accept()
                    self.log_msg(f"📥 Verbindung von {addr}")
                    conn.send("Welcome to NNOS Server!".encode())
                    threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
            except Exception as e:
                self.log_msg(f"❌ Fehler beim Start des Servers: {e}")

        def handle_client(self, conn, addr):
            try:
                while True:
                    command = conn.recv(1024).decode()
                    if command == "send":
                        self.receive_file(conn)
                    elif command == "receive":
                        self.send_file(conn)
                    elif command == "list_files":
                        files = os.listdir(SERVER_FILES_PATH)
                        conn.send("\n".join(files).encode())
                    elif command == "exit":
                        self.log_msg(f"❌ Verbindung zu {addr} geschlossen.")
                        break
                    else:
                        conn.send("Invalid command".encode())
            finally:
                conn.close()

        def receive_file(self, conn):
            filename = conn.recv(1024).decode()
            filepath = os.path.join(SERVER_FILES_PATH, filename)
            conn.send("ACK".encode())
            filesize = int(conn.recv(1024).decode())
            conn.send("ACK".encode())

            with open(filepath, 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    if f.tell() >= filesize:
                        break

            self.log_msg(f"📁 Datei empfangen: {filename}")

        def send_file(self, conn):
            filename = conn.recv(1024).decode()
            filepath = os.path.join(SERVER_FILES_PATH, filename)

            if not os.path.exists(filepath):
                conn.send("File not found".encode())
                return

            conn.send("ACK".encode())
            filesize = os.path.getsize(filepath)
            conn.send(str(filesize).encode())
            conn.recv(1024)

            with open(filepath, 'rb') as f:
                while chunk := f.read(1024):
                    conn.send(chunk)

            self.log_msg(f"📤 Datei gesendet: {filename}")

    # Wir starten das Serverfenster in einem neuen Thread!
    def launch_server_window():
        server_root = tk.Tk()
        app = ServerApp(server_root)
        server_root.mainloop()

    threading.Thread(target=launch_server_window, daemon=True).start()

    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Starten", command=show_start_option)
    context_menu.add_command(label="Entfernen", command=icon.destroy)

    icon.bind("<Button-1>", on_drag_start)
    icon.bind("<B1-Motion>", on_drag_motion)
    icon.bind("<ButtonRelease-1>", on_drag_end)

def add_desktop_icons():
    x_start = 50
    y_start = 50
    x_offset = 200

    create_icon("Notepad", open_notepad, x_start, y_start)
    create_icon("Calculator", open_calculator, x_start + x_offset, y_start)
    create_icon("Netscape", open_netscape, x_start + 2 * x_offset, y_start)
    create_icon("My Computer", open_my_computer, x_start , y_start + 100)
    create_icon("Control Panel", open_control_panel, x_start + x_offset, y_start + 100)
    
def change_background_color(color):
    root.config(bg=color)

def create_desktop_context_menu():
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Blau", command=lambda: change_background_color("darkblue"))
    context_menu.add_command(label="Rot", command=lambda: change_background_color("red"))



    def show_context_menu(event):
        context_menu.post(event.x_root, event.y_root)

    root.bind("<Button-3>", show_context_menu)

def create_start_button():
    # Taskbar ist die Hauptleiste unten, Startbutton wird hinzugefügt
    start_button = tk.Button(taskbar, text="Start", command=open_start_menu, bg="lightgrey", font=("Arial", 14))
    start_button.pack(side=tk.LEFT, padx=5, pady=2)

# Startmenü erstellen
def open_start_menu():
    start_menu = tk.Menu(root, tearoff=0, bg="lightgrey", font=("Arial", 12))

    # "Programme" Untermenü hinzufügen
    programmes_menu = tk.Menu(start_menu, tearoff=0, font=("Arial", 12))
    programmes_menu.add_command(label="Notepad", command=open_notepad)
    programmes_menu.add_command(label="Calculator", command=open_calculator)
    programmes_menu.add_command(label="Netscape", command=open_netscape)
    programmes_menu.add_command(label="Control Panel", command=open_control_panel)
    programmes_menu.add_command(label="Clock", command=open_clock)
    programmes_menu.add_command(label="Trash", command=open_trash)
    programmes_menu.add_command(label="My Computer", command=open_my_computer)
    programmes_menu.add_command(label="NNOS Server", command=start_nnos_server)
    start_menu.add_cascade(label="Programme", menu=programmes_menu)

    # Menü anzeigen
    start_menu.post(root.winfo_pointerx(), root.winfo_pointery())

# Taskleiste erweitern, um den Startbutton hinzuzufügen
def create_taskbar():
    global taskbar  # Taskbar muss global sein, um Startbutton hinzuzufügen
    taskbar = tk.Frame(root, bg="grey", height=30)
    taskbar.pack(side=tk.BOTTOM, fill=tk.X)

    date_label = tk.Label(taskbar, text="", bg="grey", fg="white")
    date_label.pack(side=tk.RIGHT, padx=10)

    time_label = tk.Label(taskbar, text="", bg="grey", fg="white")
    time_label.pack(side=tk.RIGHT, padx=10)

    def update_clock_and_date():
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%d.%m.%Y")
        time_label.config(text=current_time)
        date_label.config(text=current_date)
        root.after(1000, update_clock_and_date)

    update_clock_and_date()

    create_start_button()  # Startbutton hinzufügen

# Hauptfenster erstellen
root = tk.Tk()
root.title("Netscape Navigator OS")
root.attributes('-fullscreen', True)  # Vollbildmodus aktivieren
root.config(bg="darkblue")

# Zeige den Startbildschirm
show_startup_screen()

# Überprüfen und Einrichten der erforderlichen Dateien und Ordner
startup()

# Menü hinzufügen
main_menu = tk.Menu(root)
file_menu = tk.Menu(main_menu, tearoff=0)

# Shutdown-Option
file_menu.add_command(label="Shutdown", command=show_shutdown_screen)

# Restart-Option
file_menu.add_command(label="Restart", command=show_restart_screen)

# Logout-Option
file_menu.add_command(label="Log Server", command=lambda: [root.withdraw(), show_login_options()])

# Menüleiste anzeigen
main_menu.add_cascade(label="Shutdown Options", menu=file_menu)
root.config(menu=main_menu)

help_menu = tk.Menu(main_menu, tearoff=0)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Netscape Navigator OS\nVersion 0.5 Beta 1, Server Codename Louisa-Server\nCopyright Alte F1 Games 2024, 2025-New Netscape"))
help_menu.add_command(label="How works Netscape Navigator OS?", command=lambda: messagebox.showinfo("How works Netscape Navigator OS?", "Netscape Navigator OS 0.5 Beta 1 Server, Windows Version, based on Python 3.13. For Windows 7 Users work Python 3.8.10 but Windows 8.1 with 3.13 is more stabil!"))
help_menu.add_command(label="Whats new?", command=lambda: messagebox.showinfo("Whats new?", "Netscape Navigator OS 0.5 Beta 1 had a now a Startmenü with all Programms, not all of it are on the Desktop, a Control Panel, User Control, Support extern Apps in py and pyw Format and a Funktion to restart Netscape Navigator OS"))
main_menu.add_cascade(label="Information about Netscape Navigator OS", menu=help_menu)

root.config(menu=main_menu)

# Desktop-Icons hinzufügen
add_desktop_icons()

# Taskleiste erstellen
create_taskbar()

# Desktop Kontextmenü hinzufügen
create_desktop_context_menu()

root.mainloop()


