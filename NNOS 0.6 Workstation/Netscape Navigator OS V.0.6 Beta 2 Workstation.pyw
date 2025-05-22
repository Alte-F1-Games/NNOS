import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog, Toplevel, Listbox, Scrollbar
from tkinter import ttk
import subprocess
import os
import time
import shutil
import json
import ctypes
from ctypes import wintypes
import sys
import time
import calendar
from datetime import datetime
import math


REGISTRY_FILE_PATH = r'C:\NNOS\system\reg.json'

class NNOSRegistry:
    def __init__(self, reg_file):
        self.reg_file = reg_file
        if not os.path.exists(self.reg_file):
            with open(self.reg_file, 'w') as f:
                json.dump({}, f, indent=4)
        self.load_registry()

    def load_registry(self):
        with open(self.reg_file, 'r') as f:
            self.registry = json.load(f)

    def save_registry(self):
        with open(self.reg_file, 'w') as f:
            json.dump(self.registry, f, indent=4)

    def set(self, key, value):
        keys = key.split("\\")
        registry_ref = self.registry
        for k in keys[:-1]:
            registry_ref = registry_ref.setdefault(k, {})
        registry_ref[keys[-1]] = value
        self.save_registry()

    def get(self, key):
        keys = key.split("\\")
        registry_ref = self.registry
        for k in keys:
            registry_ref = registry_ref.get(k, None)
            if registry_ref is None:
                return None
        return registry_ref

    def delete(self, key):
        keys = key.split("\\")
        registry_ref = self.registry
        for k in keys[:-1]:
            registry_ref = registry_ref.get(k, None)
            if registry_ref is None:
                return
        del registry_ref[keys[-1]]
        self.save_registry()

USER_REGISTRY_PATH = "NNOS_SYSTEM\\Users"

def make_fullscreen(window):
    window.attributes("-fullscreen", True)
    window.protocol("WM_DELETE_WINDOW", disable_event)  

def disable_event():
    pass

def login_screen():
    login = tk.Toplevel(root)
    login.title("Login")
    make_fullscreen(login)

    login.configure(bg='#3B5998')
    label_font = ('Helvetica', 14)

    tk.Label(login, text="Username", bg='#3B5998', fg='#61AFEF', font=label_font).pack(pady=10)
    username_entry = tk.Entry(login, font=label_font)
    username_entry.pack(pady=5)

    tk.Label(login, text="Password", bg='#3B5998', fg='#61AFEF', font=label_font).pack(pady=10)
    password_entry = tk.Entry(login, show='*', font=label_font)
    password_entry.pack(pady=5)

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        if validate_user(username, password):
            login.destroy()  
            root.deiconify()  
            startup()  
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    tk.Button(login, text="Login", command=attempt_login, font=label_font, bg='#98C379', fg='white', relief="groove").pack(pady=20)
    
    back_button = tk.Button(login, text="Back to main Logon Menu", command=login.destroy, font=label_font, bg='#E06C75', fg='white', relief="groove")
    back_button.place(relx=0.5, rely=0.98, anchor='s')

def validate_user(username, password):
    reg = NNOSRegistry(REGISTRY_FILE_PATH)
    user_data = reg.get(f"{USER_REGISTRY_PATH}\\{username}")
    if user_data:
        if user_data.get('password') == password:
            return True
    return False

def register_screen():
    register = tk.Toplevel(root)
    register.title("Register")
    make_fullscreen(register)

    register.configure(bg='#3B5998')
    label_font = ('Helvetica', 14)

    tk.Label(register, text="Choose a Username", bg='#3B5998', fg='#61AFEF', font=label_font).pack(pady=10)
    new_username_entry = tk.Entry(register, font=label_font)
    new_username_entry.pack(pady=5)

    tk.Label(register, text="Choose a Password", bg='#3B5998', fg='#61AFEF', font=label_font).pack(pady=10)
    new_password_entry = tk.Entry(register, show='*', font=label_font)
    new_password_entry.pack(pady=5)

    def register_user():
        username = new_username_entry.get()
        password = new_password_entry.get()
        reg = NNOSRegistry(REGISTRY_FILE_PATH)
        
        if not reg.get(f"{USER_REGISTRY_PATH}\\{username}"):
            user_data = {
                "username": username,
                "password": password
            }
            reg.set(f"{USER_REGISTRY_PATH}\\{username}", user_data)
            messagebox.showinfo("Registration Successful", "You can now log in.")
            register.destroy()
        else:
            messagebox.showerror("Registration Failed", "Username already exists.")

    tk.Button(register, text="Register", command=register_user, font=label_font, bg='#98C379', fg='white', relief="groove").pack(pady=20)

    back_button = tk.Button(register, text="Back to the Logon main Menu", command=register.destroy, font=label_font, bg='#E06C75', fg='white', relief="groove")
    back_button.place(relx=0.5, rely=0.98, anchor='s')

def show_login_options():
    option_screen = tk.Toplevel(root)
    option_screen.title("Logon Options")
    make_fullscreen(option_screen)

    option_screen.configure(bg='#3B5998')
    button_font = ('Helvetica', 14)

    tk.Button(option_screen, text="Login on Netscape Navigator OS-Workstation", command=login_screen, font=button_font, bg='#61AFEF', fg='darkblue', relief="groove").pack(pady=12)
    tk.Button(option_screen, text="Register on Netscape Navigator OS-Workstation", command=register_screen, font=button_font, bg='#61AFEF', fg='green', relief="groove").pack(pady=10)

def startup():
    messagebox.showinfo("System Startup", "System started successfully")
    
root = tk.Tk()
root.withdraw()
show_login_options()


NAVIGATOR_PATH = r'C:\Program Files\Netscape\Navigator 9\navigator.exe'

NAVIGATOR_OS_PATH = r'C:\NNOS'
NAVIGATOR_INSTALLER_PATH = os.path.join(NAVIGATOR_OS_PATH, 'system', 'Netscape Navigator OS.sys.pyw')

def check_and_setup():
    missing_files_or_dirs = False

    if not os.path.isdir(NAVIGATOR_OS_PATH):
        missing_files_or_dirs = True
    elif not os.path.isdir(os.path.dirname(NAVIGATOR_INSTALLER_PATH)):
        missing_files_or_dirs = True
    elif not os.path.exists(NAVIGATOR_INSTALLER_PATH):
        missing_files_or_dirs = True

    if missing_files_or_dirs:
        show_red_screen()
def set_always_on_top(window):
    window.attributes('-topmost', True)

def show_red_screen():
    rsod = tk.Toplevel(root)
    rsod.title("RSOD: SYSTEMFILE_ERROR")
    rsod.attributes('-fullscreen', True)
    rsod.config(bg="red")
    set_always_on_top(rsod)

    header = tk.Label(rsod, text=":( RSOD: System File Error", font=("Arial", 48, "bold"), bg="red", fg="white")
    header.pack(pady=50)

    error_message = tk.Label(
        rsod,
        text="Error 001 - The system file Netscape Navigator OS.sys.pyw, folder NNOS or subfolder system doesn't exist",
        font=("Arial", 18),
        bg="red",
        fg="white"
    )
    error_message.pack(expand=True)

    cursor = tk.Label(rsod, text="_", font=("Courier New", 16), bg="red", fg="white")
    cursor.pack(anchor='w', padx=50, pady=10)

    def blink():
        cursor.config(text="__" if cursor.cget("text") == " " else " ")
        rsod.after(500, blink)

    blink()

    rsod.after(10000, root.quit)

root = tk.Tk()
root.withdraw()

def show_startup_screen():
    startup = tk.Toplevel(root)
    startup.title("Netscape Navigator OS :)")
    startup.attributes('-fullscreen', True) 
    startup.config(bg="yellow")
    set_always_on_top(startup)

    header = tk.Label(startup, text="Netscape Navigator OS :)", font=("Arial", 48, "bold"), bg="yellow")
    header.pack(pady=50)

    welcome_text = tk.Label(startup, text="Welcome", font=("Arial", 24), bg="yellow")
    welcome_text.pack()

    version_text = tk.Label(startup, text="Version 0.6 Beta 2, Workstation Edition", font=("Arial", 20), bg="blue")
    version_text.pack()

    loading_text = tk.Label(startup, text="Loading NNOS Services...", font=("Arial", 12), bg="yellow")
    loading_text.pack(pady=20)

    loading_label = tk.Label(startup, text="|", font=("Arial", 48, "bold"), bg="yellow", fg="red")
    loading_label.pack()

    def update_loading():
        current = loading_label.cget("text")
        if current == "|":
            loading_label.config(text="/")
        elif current == "/":
            loading_label.config(text="-")
        elif current == "-":
            loading_label.config(text="\\")
        elif current == "\\":
            loading_label.config(text="|")
        startup.after(100, update_loading) 

    update_loading()

    startup.after(3000, startup.destroy)

def startup():
    print("Starting NNOS...")
    try:
        initialize_system()
        check_and_setup()
        print("NNOS is Successful started, Lets go .")
    except Exception as e:
        print(f"Error loading NNOS: {e}")
        show_red_screen()

def initialize_system():
    print("Loading NNOS System...")
    print("Loading NNOS Logon UI...")
    print("Loading NNOS Registry...")
    print("Loading NNOS Users...")
    print("Loading NNOS Desktop UI...")
    if not os.path.exists(NAVIGATOR_INSTALLER_PATH):
        raise FileNotFoundError("A Important OS File is missing reinstall NNOS.")

def show_shutdown_screen():
    shutdown_window = tk.Toplevel(root)
    shutdown_window.title("Shutdown")
    shutdown_window.attributes('-fullscreen', True)
    shutdown_window.config(bg="black")
    shutdown_window.protocol("WM_DELETE_WINDOW", disable_event)

    header = tk.Label(shutdown_window, text="Netscape Navigator OS is shutting Down...", font=("Arial", 48, "bold"), bg="black", fg="red")
    header.pack(pady=50)

    shutdown_message = tk.Label(shutdown_window, text="Stopping NNOS Services... Please wait while the system shuts down.", font=("Arial", 24), bg="black", fg="white")
    shutdown_message.pack()

    shutdown_window.after(3000, lambda: root.quit())

def show_restart_screen():
    restart_window = tk.Toplevel(root)
    restart_window.title("Restart")
    restart_window.attributes('-fullscreen', True)
    restart_window.config(bg="black")
    restart_window.protocol("WM_DELETE_WINDOW", disable_event)

    header = tk.Label(restart_window, text="Netscape Navigator OS is restarting...", font=("Arial", 48, "bold"), bg="black", fg="red")
    header.pack(pady=50)

    restart_message = tk.Label(restart_window, text="Restarting NNOS Services... Please wait while the system restarts.", font=("Arial", 24), bg="black", fg="white")
    restart_message.pack()

    def complete_restart():
        restart_window.destroy()
        root.withdraw()
        show_startup_screen()

    restart_window.after(3000, complete_restart)

def disable_event():
    pass

def open_netscape():
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
        file_name = simpledialog.askstring("Save As", "File Name:")
        if file_name:
            try:
                file_path = os.path.join(r'C:\NNOS\document', file_name)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(text_area.get(1.0, tk.END).strip())
                messagebox.showinfo("Info", "File saved.")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving ERROR 72: {str(e)}")

    def open_file():
        file_name = simpledialog.askstring("Open", "File Name:")
        if file_name:
            try:
                file_path = os.path.join(r'C:\NNOS\document', file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    text_area.delete(1.0, tk.END)  
                    text_area.insert(tk.END, file.read())  
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found. ERROR 73")
            except Exception as e:
                messagebox.showerror("Error", f"Error opening file ERROR 74: {str(e)}")

    def new_file():
        text_area.delete(1.0, tk.END)  

    notepad_menu = tk.Menu(notepad)
    file_menu = tk.Menu(notepad_menu, tearoff=0)
    file_menu.add_command(label="New", command=new_file)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=notepad.destroy)

    help_menu = tk.Menu(notepad_menu, tearoff=0)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Notepad Version 1.2 for Netscape Navigator OS V.0.6 Beta 2 "))

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

def open_clock():
    registry = NNOSRegistry(REGISTRY_FILE_PATH)
    clock = tk.Toplevel(root)
    clock.title("Clock & Calendar")
    clock.geometry("400x280")
    clock.config(bg="lightgrey")
    set_always_on_top(clock)

    mode = tk.StringVar(value="digital")

    now = datetime.now()
    current_year = now.year
    current_month = now.month

    container = tk.Frame(clock, bg="lightgrey")
    container.pack(expand=True, fill="both")

    time_label = tk.Label(container, text="", font=("Arial", 36), bg="lightgrey")
    date_label = tk.Label(container, text="", font=("Arial", 16), bg="lightgrey")
    calendar_text = tk.Text(container, width=33, height=10, font=("Courier", 10), bg="lightgrey", bd=0)
    canvas = tk.Canvas(container, width=200, height=200, bg="lightgrey", highlightthickness=0)

    selected_day = None

    def draw_analog_clock():
        canvas.delete("all")
        center = 100
        radius = 90
        canvas.create_oval(center - radius, center - radius, center + radius, center + radius, outline="black")
        now = datetime.now()
        sec = now.second
        min = now.minute
        hr = now.hour % 12
        def hand(angle_deg, length, width, color):
            angle = math.radians(angle_deg - 90)
            x = center + length * math.cos(angle)
            y = center + length * math.sin(angle)
            canvas.create_line(center, center, x, y, width=width, fill=color)
        hand(hr * 30 + min / 2, 40, 4, "black")
        hand(min * 6, 60, 3, "blue")
        hand(sec * 6, 80, 1, "red")
        if mode.get() == "analog":
            clock.after(1000, draw_analog_clock)

    def update_time():
        time_label.config(text=time.strftime("%H:%M:%S"))
        if mode.get() == "digital":
            clock.after(1000, update_time)

    def update_date():
        date_label.config(text=time.strftime("%A, %d %B %Y"))

    def show_reminders(day):
        key = f"NNOS_Calendar\\{current_year}\\{current_month}\\{day}"
        existing = registry.get(key) or ""
        reminder = simpledialog.askstring("Reminder", f"Edit reminder for {day}/{current_month}/{current_year}:", initialvalue=existing)
        if reminder is not None:
            if reminder.strip():
                registry.set(key, reminder.strip())
            else:
                registry.delete(key)
            update_calendar()

    def update_calendar():
     calendar_text.config(state='normal')
     calendar_text.delete("1.0", tk.END)
     cal = calendar.month(current_year, current_month)
     calendar_text.insert(tk.END, cal + "\nClick a day to add/view reminders.\n")

    def on_click(event):
        try:
            index = calendar_text.index(f"@{event.x},{event.y}")
            line_start = calendar_text.index(f"{index} linestart")
            line_end = calendar_text.index(f"{index} lineend")
            line = calendar_text.get(line_start, line_end)

            char_index = int(index.split(".")[1])
            
            tokens = []
            current = ""
            start_pos = None
            for i, ch in enumerate(line):
                if ch != " ":
                    if start_pos is None:
                        start_pos = i
                    current += ch
                else:
                    if current:
                        tokens.append((start_pos, current))
                        current = ""
                        start_pos = None
            if current:
                tokens.append((start_pos, current))

            for start, token in tokens:
                if token.isdigit():
                    end = start + len(token)
                    if start <= char_index < end:
                        show_reminders(token)
                        break
        except Exception as e:
            print("Error:", e)

    calendar_text.bind("<Button-1>", on_click)
    calendar_text.config(state='disabled')

    def change_month(delta):
        nonlocal current_month, current_year
        current_month += delta
        if current_month < 1:
            current_month = 12
            current_year -= 1
        elif current_month > 12:
            current_month = 1
            current_year += 1
        update_calendar()

    def update_view():
        for widget in [time_label, date_label, calendar_text, canvas]:
            widget.pack_forget()
        if mode.get() == "digital":
            time_label.pack(pady=10)
            update_time()
        elif mode.get() == "date":
            date_label.pack(pady=10)
            update_date()
        elif mode.get() == "calendar":
            calendar_text.pack(pady=10)
            update_calendar()
        elif mode.get() == "analog":
            canvas.pack(pady=10)
            draw_analog_clock()

    btn_frame = tk.Frame(clock, bg="lightgrey")
    btn_frame.pack(pady=5)

    ttk.Button(btn_frame, text="Digital", command=lambda: mode.set("digital") or update_view()).grid(row=0, column=0, padx=2)
    ttk.Button(btn_frame, text="Analog", command=lambda: mode.set("analog") or update_view()).grid(row=0, column=1, padx=2)
    ttk.Button(btn_frame, text="Date", command=lambda: mode.set("date") or update_view()).grid(row=0, column=2, padx=2)
    ttk.Button(btn_frame, text="Calendar", command=lambda: mode.set("calendar") or update_view()).grid(row=0, column=3, padx=2)

    nav_frame = tk.Frame(clock, bg="lightgrey")
    nav_frame.pack()

    ttk.Button(nav_frame, text="<<", command=lambda: change_month(-1)).grid(row=0, column=0, padx=10)
    ttk.Button(nav_frame, text=">>", command=lambda: change_month(1)).grid(row=0, column=1, padx=10)

    update_view()

def open_trash():
    trash = tk.Toplevel(root)
    trash.title("Trash")
    trash.geometry("300x400")
    trash.config(bg="lightgrey")
    set_always_on_top(trash)

    trash_listbox = tk.Listbox(trash, selectmode=tk.MULTIPLE)
    trash_listbox.pack(expand=True, fill='both')

    trash_data_file = r'C:\NNOS\Trash\trash_data.json'

    def list_trash():
        trash_listbox.delete(0, tk.END)
        trash_folder = r'C:\NNOS\Trash'
        if os.path.exists(trash_folder):
            files = os.listdir(trash_folder)
            for item in files:
                trash_listbox.insert(tk.END, item)
        else:
            os.makedirs(trash_folder)

    def delete_selected():
        selected_files = [trash_listbox.get(i) for i in trash_listbox.curselection()]
        trash_folder = r'C:\NNOS\Trash'
        for file in selected_files:
            file_path = os.path.join(trash_folder, file)
            if file == 'Netscape Navigator OS.sys.pyw':
                messagebox.showerror("Error", f"The file {file} cannot be deleted!")
                continue  
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting {file}: {e}")
        list_trash() 

    def restore_selected():
        selected_files = [trash_listbox.get(i) for i in trash_listbox.curselection()]
        trash_folder = r'C:\NNOS\Trash'
        if os.path.exists(trash_data_file):
            with open(trash_data_file, 'r') as f:
                trash_data = json.load(f)
        else:
            trash_data = {}

        for file in selected_files:
            file_path = os.path.join(trash_folder, file)
            if file in trash_data:  
                restore_path = trash_data[file]  
                try:
                    shutil.move(file_path, restore_path)  
                    messagebox.showinfo("Success", f"File {file} has been restored.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error restoring {file}: {e} Error 103")
            else:
                messagebox.showwarning("Warning", f"No original path found for {file} Error 104.")
        list_trash()  

    def custom_open_file():
        file_path = simpledialog.askstring("Add File", "Please enter the file path:")
        if file_path and os.path.isfile(file_path):
            add_file_to_trash(file_path)

    def add_file_to_trash(file_path):
        trash_folder = r'C:\NNOS\Trash'
        if not os.path.exists(trash_folder):
            os.makedirs(trash_folder)
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(trash_folder, file_name)

        if os.path.exists(trash_data_file):
            with open(trash_data_file, 'r') as f:
                trash_data = json.load(f)
        else:
            trash_data = {}

        trash_data[file_name] = file_path

        try:
            if os.path.exists(dest_path):
                messagebox.showwarning("Warning", "File already exists in the trash.")
            else:
                shutil.move(file_path, trash_folder)  
                with open(trash_data_file, 'w') as f:
                    json.dump(trash_data, f)  
                list_trash()
                messagebox.showinfo("Info", f"File '{file_name}' added to the trash.")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding the file: {e}")

    add_button = tk.Button(trash, text="Add File", command=custom_open_file)
    add_button.pack(pady=10)

    delete_button = tk.Button(trash, text="Delete Selected File", command=delete_selected)
    delete_button.pack(pady=10)

    restore_button = tk.Button(trash, text="Restore Selected File", command=restore_selected)
    restore_button.pack(pady=10)

    list_trash()

def open_paint():
    paint = tk.Toplevel(root)
    paint.title("SuperPaint")
    paint.geometry("900x700")
    paint.config(bg="white")

    def start_draw(event):
        global last_x, last_y
        last_x, last_y = event.x, event.y

    def draw_line(event):
        global last_x, last_y
        x, y = event.x, event.y
        color = color_var.get()
        brush_size = brush_size_var.get()
        canvas.create_line(last_x, last_y, x, y, fill=color, width=brush_size)
        draw_commands.append(f"line {last_x} {last_y} {x} {y} {color} {brush_size}")
        last_x, last_y = x, y

    def save_drawing():
        filename = filename_entry.get().strip()
        if not filename:
            messagebox.showwarning("Warning", "Please enter a file name.")
            return
        file_path = f"C:/NNOS/pictures/{filename}.txt"
        os.makedirs("C:/NNOS/pictures", exist_ok=True)
        try:
            with open(file_path, 'w') as file:
                for command in draw_commands:
                    file.write(command + "\n")
            messagebox.showinfo("Success", f"Drawing saved at: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving the file: {e}")

    def open_drawing():
        filename = filename_entry.get().strip()
        if not filename:
            messagebox.showwarning("Warning", "Please enter a file name.")
            return
        file_path = f"C:/NNOS/pictures/{filename}.txt"
        try:
            with open(file_path, 'r') as file:
                canvas.delete("all")
                draw_commands.clear()
                for line in file:
                    command = line.strip()
                    draw_commands.append(command)
                    parts = command.split()
                    if parts[0] == "line":
                        x1, y1, x2, y2, color, width = int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), parts[5], int(parts[6])
                        canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
            messagebox.showinfo("Success", "Drawing loaded successfully.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Drawing file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading the file: {e}")

    canvas = tk.Canvas(paint, bg="white")
    canvas.pack(fill="both", expand=True)
    canvas.bind("<Button-1>", start_draw)
    canvas.bind("<B1-Motion>", draw_line)

    color_var = tk.StringVar(value="black")
    brush_size_var = tk.IntVar(value=5)
    draw_commands = []
    last_x, last_y = None, None  

    color_palette = tk.Frame(paint)
    color_palette.pack(side="left", fill="y")

    for color in ["black", "red", "blue", "green", "yellow", "purple", "orange"]:
        color_button = tk.Button(color_palette, bg=color, command=lambda c=color: color_var.set(c))
        color_button.pack(fill="x")

    brush_size_frame = tk.Frame(paint)
    brush_size_frame.pack(side="right", fill="y")

    brush_size_label = tk.Label(brush_size_frame, text="Brush Size")
    brush_size_label.pack()

    for size in [3, 5, 10, 15, 20]:
        size_button = tk.Button(brush_size_frame, text=str(size), command=lambda s=size: brush_size_var.set(s))
        size_button.pack(fill="x")

    filename_frame = tk.Frame(paint)
    filename_frame.pack(side="bottom", fill="x", padx=5, pady=5)

    filename_label = tk.Label(filename_frame, text="File Name:")
    filename_label.pack(side="left")

    filename_entry = tk.Entry(filename_frame)
    filename_entry.pack(side="left", fill="x", expand=True)

    button_frame = tk.Frame(paint)
    button_frame.pack(side="bottom", fill="x")

    save_button = tk.Button(button_frame, text="Save", command=save_drawing)
    save_button.pack(side="left", padx=5, pady=5)

    open_button = tk.Button(button_frame, text="Open", command=open_drawing)
    open_button.pack(side="left", padx=5, pady=5)

def open_my_computer():
    my_computer = tk.Toplevel(root)
    my_computer.title("My Computer")
    my_computer.geometry("460x300")
    my_computer.config(bg="lightgrey")
    set_always_on_top(my_computer)

    TRASH_DIR = r"C:\NNOS\Trash"
    TRASH_LOG_FILE = os.path.join(TRASH_DIR, "trash_data.json")

    def list_directory(path):
        contents_listbox.delete(0, tk.END)
        try:
            if path == "C:/":
                if os.path.isdir("C:/NNOS"):
                    contents_listbox.insert(tk.END, "NNOS")
            else:
                for item in os.listdir(path):
                    contents_listbox.insert(tk.END, item)
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    def open_item(event):
        selected_item = contents_listbox.get(tk.ACTIVE)
        if selected_item:
            current_path = os.path.join(current_directory.get(), selected_item)
            if os.path.isdir(current_path):
                list_directory(current_path)
                current_directory.set(current_path)
            elif selected_item.endswith(".txt"):
                choice = messagebox.askquestion("Öffnen mit", "Do you want open this txt File in Notepad (yes) or in Superpaint (no)?", 
                                                icon='question', type='yesnocancel', default='yes')
                if choice == 'yes':
                    open_notepad_with_file(current_path)
                elif choice == 'no':
                    open_superpaint_with_file(current_path)
            elif selected_item.endswith(".py") or selected_item.endswith(".pyw"):
                run_python_script(current_path)
            else:
                messagebox.showinfo("Info", f"{selected_item} is no directory, .txt or .py or .pyw File.")

    def go_up():
        parent_directory = os.path.dirname(current_directory.get())
        list_directory(parent_directory)
        current_directory.set(parent_directory)

    def delete_file():
        selected_item = contents_listbox.get(tk.ACTIVE)
        if selected_item:
            file_path = os.path.join(current_directory.get(), selected_item)

            if selected_item.endswith(".sys.pyw"):
                messagebox.showerror("Error", f"The File {selected_item} is a OS File and cannot deleted!")
                return

            try:
                os.makedirs(TRASH_DIR, exist_ok=True)
                trash_path = os.path.join(TRASH_DIR, selected_item)

                counter = 1
                base, ext = os.path.splitext(selected_item)
                while os.path.exists(trash_path):
                    selected_item = f"{base} ({counter}){ext}"
                    trash_path = os.path.join(TRASH_DIR, selected_item)
                    counter += 1

                shutil.move(file_path, trash_path)

                if os.path.exists(TRASH_LOG_FILE):
                    with open(TRASH_LOG_FILE, "r") as f:
                        trash_log = json.load(f)
                else:
                    trash_log = {}

                trash_log[selected_item] = file_path

                with open(TRASH_LOG_FILE, "w") as f:
                    json.dump(trash_log, f, indent=4)

                list_directory(current_directory.get())
                messagebox.showinfo("Trash", f"{selected_item} was deleted.")
            except Exception as e:
                messagebox.showerror("Error", f"Cannot delete File: {str(e)}")

    def copy_file():
      selected_item = contents_listbox.get(tk.ACTIVE)
      if selected_item:
        src_path = os.path.join(current_directory.get(), selected_item)
        if not os.path.exists(src_path):
            messagebox.showerror("Error", "The source file does not exist.")
            return

        target_path = simpledialog.askstring("Enter Destination", f"Enter the path to copy '{selected_item}' to:")
        if target_path:
            if os.path.isdir(target_path):
                try:
                    shutil.copy2(src_path, target_path)
                    messagebox.showinfo("Copied", f"'{selected_item}' was successfully copied to:\n{target_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while copying:\n{e}")
            else:
                messagebox.showerror("Error", "The target path is not a valid directory.")

    def rename_file():
        selected_item = contents_listbox.get(tk.ACTIVE)
        if selected_item:
            old_path = os.path.join(current_directory.get(), selected_item)
            new_name = simpledialog.askstring("Rename File", f"New Name for {selected_item}:")

            if new_name:
                new_path = os.path.join(current_directory.get(), new_name)
                try:
                    os.rename(old_path, new_path)
                    list_directory(current_directory.get())
                    messagebox.showinfo("Renamed", f"{selected_item} was renamed to {new_name}")
                except Exception as e:
                    messagebox.showerror("Error", f"Cannot rename File: {e}")

    current_directory = tk.StringVar(value="C:/") 

    contents_listbox = tk.Listbox(my_computer)
    contents_listbox.pack(expand=True, fill='both')

    button_frame = tk.Frame(my_computer)
    button_frame.pack(fill='x', pady=5)

    tk.Button(button_frame, text="⬆️ Up", command=go_up).pack(side='left', padx=5)
    tk.Button(button_frame, text="🗑️ Delete File/Folder", command=delete_file).pack(side='left', padx=5)
    tk.Button(button_frame, text="📄 Copy File/Folder", command=copy_file).pack(side='left', padx=5)
    tk.Button(button_frame, text="✏️ Rename File/Folder", command=rename_file).pack(side='left', padx=5)

    list_directory(current_directory.get())
    contents_listbox.bind("<Double-1>", open_item)

def run_python_script(file_path):
    try:
        if file_path.endswith(".pyw"):
            subprocess.Popen(["pythonw", file_path])
        else:
            subprocess.Popen(["python", file_path])
    except Exception as e:
        messagebox.showerror("Error", f"Error by running the Program: {str(e)}")


def open_notepad_with_file(file_path):
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
        messagebox.showerror("Error", "File not found.")

    def save_file():
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text_area.get(1.0, tk.END).strip())
            messagebox.showinfo("Succsess", "File Saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Error by saveing file: {str(e)}")

    notepad_menu = tk.Menu(notepad)
    file_menu = tk.Menu(notepad_menu, tearoff=0)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_command(label="Exit", command=notepad.destroy)
    notepad_menu.add_cascade(label="File", menu=file_menu)
    notepad.config(menu=notepad_menu)


def open_superpaint_with_file(file_path):
    paint = tk.Toplevel(root)
    paint.title("SuperPaint")
    paint.geometry("800x600")
    paint.config(bg="white")

    canvas = tk.Canvas(paint, bg="white")
    canvas.pack(fill="both", expand=True)

    draw_commands = []
    current_line = None

    def save_drawing():
        with open(file_path, 'w') as file:
            for command in draw_commands:
                file.write(command + "\n")
        messagebox.showinfo("Success", "Drawing saved.")

    def load_drawing():
        try:
            with open(file_path, 'r') as file:
                canvas.delete("all")
                draw_commands.clear()
                for line in file:
                    command = line.strip()
                    draw_commands.append(command)
                    parts = command.split()
                    if parts[0] == "line":
                        x1, y1, x2, y2, color, width = int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), parts[5], int(parts[6])
                        canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
        except FileNotFoundError:
            messagebox.showerror("Error", "Superpaint File not found.")

    def start_draw(event):
        global current_line
        current_line = (event.x, event.y)

    def draw(event):
        global current_line
        if current_line:
            x1, y1 = current_line
            x2, y2 = event.x, event.y
            color = "black" 
            width = 2       
            canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
            draw_commands.append(f"line {x1} {y1} {x2} {y2} {color} {width}")
            current_line = (x2, y2)

    def stop_draw(event):
        global current_line
        current_line = None

    load_drawing()  

    canvas.bind("<Button-1>", start_draw)
    canvas.bind("<B1-Motion>", draw)     
    canvas.bind("<ButtonRelease-1>", stop_draw)

    save_button = tk.Button(paint, text="Save File", command=save_drawing)
    save_button.pack(side="bottom", pady=10)

def manage_users():
    reg = NNOSRegistry(REGISTRY_FILE_PATH)
    users_keys = list(reg.registry.get("NNOS_SYSTEM", {}).get("Users", {}).keys())

    user_window = tk.Toplevel(root)
    user_window.title("User Control")
    user_window.geometry('400x450')
    user_window.configure(bg='#f0f0f0')

    tk.Label(user_window, text="User Control", font=('Helvetica', 12), bg='#f0f0f0').pack(pady=10)

    user_listbox = tk.Listbox(user_window, height=10, width=40, font=('Helvetica', 10))
    for user in users_keys:
        user_listbox.insert(tk.END, user)
    user_listbox.pack(pady=10)

    def delete_user():
        selected_user = user_listbox.curselection()
        if not selected_user:
            messagebox.showwarning("Warning", "Choose a User to delete!")
            return

        user_to_delete = users_keys[selected_user[0]]
        confirm = messagebox.askyesno("Question", f"Do you want delete the User {user_to_delete}")
        if confirm:
            try:
                reg.delete(f"NNOS_SYSTEM\\Users\\{user_to_delete}")
                messagebox.showinfo("Success", f"The User {user_to_delete} was deleted!")
                user_listbox.delete(selected_user)
                users_keys.remove(user_to_delete)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while deleting user: {str(e)}")

    def add_user():
        user_name = user_name_entry.get()
        password = password_entry.get()
        if user_name and password:
            try:
                reg.set(f"NNOS_SYSTEM\\Users\\{user_name}\\username", user_name)
                reg.set(f"NNOS_SYSTEM\\Users\\{user_name}\\password", password)
                messagebox.showinfo("Success", f"The User {user_name} was added!")
                user_listbox.insert(tk.END, user_name)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while adding user: {str(e)}")
        else:
            messagebox.showwarning("Input", "Please enter a username and password.")

    user_name_label = tk.Label(user_window, text="Enter username:", font=('Helvetica', 10), bg='#f0f0f0')
    user_name_label.pack(pady=5)
    user_name_entry = tk.Entry(user_window, font=('Helvetica', 10), width=30)
    user_name_entry.pack(pady=5)

    password_label = tk.Label(user_window, text="Enter password:", font=('Helvetica', 10), bg='#f0f0f0')
    password_label.pack(pady=5)
    password_entry = tk.Entry(user_window, font=('Helvetica', 10), width=30, show="*")
    password_entry.pack(pady=5)

    add_user_button = tk.Button(user_window, text="Add User", command=add_user, font=('Helvetica', 10), bg='#4CAF50', fg='white')
    add_user_button.pack(pady=5)

    delete_user_button = tk.Button(user_window, text="Delete User", command=delete_user, font=('Helvetica', 10), bg='#FF5722', fg='white')
    delete_user_button.pack(pady=5)

def open_settings():
    messagebox.showinfo("Settings", "Will be added later.")

def show_system_info():
    messagebox.showinfo("System Info", "Operating System: Netscape Navigator OS\nVersion: 0.6 Beta 2")

def manage_programs():
    program_folder = r'C:\NNOS\programms'
    if not os.path.exists(program_folder):
        os.makedirs(program_folder) 

    programs = [f for f in os.listdir(program_folder) if f.endswith('.py') or f.endswith('.pyw')]
    
    program_window = tk.Toplevel(root)
    program_window.title("Manage Programs")
    program_window.geometry('400x350')
    program_window.configure(bg='#f0f0f0')

    tk.Label(program_window, text="Program Management", font=('Helvetica', 12), bg='#f0f0f0').pack(pady=10)

    program_listbox = tk.Listbox(program_window, height=10, width=40, font=('Helvetica', 10))
    for program in programs:
        program_listbox.insert(tk.END, program)
    program_listbox.pack(pady=10)

    def delete_program():
        selected_program = program_listbox.curselection()
        if not selected_program:
            messagebox.showwarning("Warning", "Choose a program to delete!")
            return

        program_to_delete = programs[selected_program[0]]
        confirm = messagebox.askyesno("Question", f"Do you want to delete the program {program_to_delete}?")
        if confirm:
            try:
                os.remove(os.path.join(program_folder, program_to_delete))
                messagebox.showinfo("Success", f"The program {program_to_delete} was deleted!")
                program_listbox.delete(selected_program)
                programs.remove(program_to_delete)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while deleting the program: {str(e)}")

    delete_program_button = tk.Button(program_window, text="Delete Program", command=delete_program, font=('Helvetica', 10), bg='#FF5722', fg='white')
    delete_program_button.pack(pady=5)

def open_control_panel():
    panel_window = tk.Toplevel(root)
    panel_window.title("Control Panel")
    panel_window.geometry('400x300')
    panel_window.configure(bg='#f0f0f0')

    label_font = ('Helvetica', 12)
    tk.Label(panel_window, text="Netscape Navigator OS 0.6 Beta 2 Control Panel", font=label_font, bg='#f0f0f0').pack(pady=10)

    tk.Button(panel_window, text="Settings", command=open_settings, font=label_font, bg='#4CAF50', fg='white').pack(pady=10)
    tk.Button(panel_window, text="Manage Programs", command=manage_programs, font=label_font, bg='#FF9800', fg='white').pack(pady=10)
    tk.Button(panel_window, text="User Control", command=manage_users, font=label_font, bg='#FF5722', fg='white').pack(pady=10)

REGISTRY_FILE_PATH = r'C:\NNOS\system\reg.json'

class NNOSRegistry:
    def __init__(self, reg_file):
        self.reg_file = reg_file
        if not os.path.exists(self.reg_file):
            with open(self.reg_file, 'w') as f:
                json.dump({}, f, indent=4)
        self.load_registry()

    def load_registry(self):
        with open(self.reg_file, 'r') as f:
            self.registry = json.load(f)

    def save_registry(self):
        with open(self.reg_file, 'w') as f:
            json.dump(self.registry, f, indent=4)

    def set(self, key, value):
        keys = key.split("\\")
        registry_ref = self.registry
        for k in keys[:-1]:
            registry_ref = registry_ref.setdefault(k, {})
        registry_ref[keys[-1]] = value
        self.save_registry()

    def get(self, key):
        keys = key.split("\\")
        registry_ref = self.registry
        for k in keys:
            registry_ref = registry_ref.get(k, None)
            if registry_ref is None:
                return None
        return registry_ref

    def delete(self, key):
        keys = key.split("\\")
        registry_ref = self.registry
        for k in keys[:-1]:
            registry_ref = registry_ref.get(k, None)
            if registry_ref is None:
                print(f"Key {key} not found.")
                return
        del registry_ref[keys[-1]]
        self.save_registry()

class RegistryEditor:
    def __init__(self, root, reg_path):
        self.root = root
        self.registry = NNOSRegistry(reg_path)
        self.create_gui()

    def create_gui(self):
        self.root.title("NNOS Registry Editor")
        self.root.geometry("600x400")

        self.key_listbox = tk.Listbox(self.root, width=80, height=20)
        self.key_listbox.pack(padx=10, pady=10)

        self.add_button = tk.Button(self.root, text="Add Key", command=self.add_key)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.edit_button = tk.Button(self.root, text="Edit Key", command=self.edit_key)
        self.edit_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Key", command=self.delete_key)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.save_button = tk.Button(self.root, text="Save Changes", command=self.save_changes)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.update_key_list()

    def update_key_list(self):
        self.key_listbox.delete(0, tk.END)
        self._populate_key_list(self.registry.registry, '')

    def _populate_key_list(self, registry, parent_key):
        for key, value in registry.items():
            full_key = f"{parent_key}\\{key}" if parent_key else key
            self.key_listbox.insert(tk.END, full_key)
            if isinstance(value, dict):  
                self._populate_key_list(value, full_key)

    def add_key(self):
        new_key = simpledialog.askstring("Add Key", "Enter the registry key (e.g. NNOS_SYSTEM\\NewKey):")
        if new_key:
            new_value = simpledialog.askstring("Add Value", f"Enter the value for key {new_key}:")
            if new_value:
                self.registry.set(new_key, new_value)
                self.update_key_list()

    def edit_key(self):
        selected_key = self.key_listbox.get(tk.ACTIVE)
        if selected_key:
            new_value = simpledialog.askstring("Edit Key", f"Enter new value for key {selected_key}:")
            if new_value is not None:
                self.registry.set(selected_key, new_value)
                self.update_key_list()

    def delete_key(self):
        selected_key = self.key_listbox.get(tk.ACTIVE)
        if selected_key:
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the key {selected_key}?")
            if confirm:
                self.registry.delete(selected_key)
                self.update_key_list()

    def save_changes(self):
        self.registry.save_registry()
        messagebox.showinfo("Save Changes", "Changes have been saved successfully!")

def start_registry_editor():
    root = tk.Tk()
    editor = RegistryEditor(root, REGISTRY_FILE_PATH)

def nnos_command_prompt():
    root = tk.Tk()
    root.title("NNOS Workstation Command Prompt")
    root.geometry("600x400")

    version_info = "0.6 Beta 2 Build 530_MAIN"
    root_directory = "C:\\NNOS"
    current_dir = [root_directory]

    output_text = scrolledtext.ScrolledText(root, height=20, width=70, wrap=tk.WORD, state=tk.DISABLED)
    output_text.pack(padx=10, pady=10)

    input_entry = tk.Entry(root, width=70)
    input_entry.pack(padx=10, pady=10)

    def process_command(event):
        command = input_entry.get().strip()
        if command == "":
            return

        prompt = f"{current_dir[0]}> {command}\n"
        add_output(prompt)
        input_entry.delete(0, tk.END)

        if command == "ver":
            show_version()
        elif command == "list":
            list_files()
        elif command == "help":
            show_help()
        elif command == "clear":
            clear_output()
        elif command.startswith("copy "):
            copy_file(command)
        elif command.startswith("rename "):
            rename_file(command)
        elif command.startswith("del "):
            delete_file(command)
        elif command.startswith("cd "):
            change_directory(command)
        elif command == "notepad":
            open_notepad()
        elif command == "calculator":
            open_calculator()
        elif command == "netscape":
            open_netscape()
        elif command == "clock":
            open_clock()
        elif command == "trash":
            open_trash()
        elif command == "mycomputer":
            open_my_computer()
        elif command == "paint":
            open_paint()
        elif command == "taskmanager":
            open_taskmanager()
        elif command == "regedit":
            start_registry_editor()
        elif command == "control":
            open_control_panel()
        elif command == "usercontrol":
            manage_users()
        elif command == "lockdown":
            show_login_options()
        else:
            add_output(f"Unknown command: {command}\n")

    def show_version():
        add_output(f"NNOS Workstation [Version {version_info}]\n")

    def list_files():
        try:
            files = os.listdir(current_dir[0])
            add_output(f"Files in {current_dir[0]}:\n" + "\n".join(files) + "\n")
        except Exception as e:
            add_output(f"Error listing files: {str(e)}\n")

    def clear_output():
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.config(state=tk.DISABLED)

    def show_help():
        help_text = (
            "Available commands:\n"
            "  ver                 - Show NNOS version\n"
            "  list                - List files in current directory\n"
            "  help                - Display help\n"
            "  clear               - Clear screen\n"
            "  copy <src> <dst>    - Copy file\n"
            "  rename <old> <new>  - Rename file\n"
            "  del <file>          - Delete file\n"
            "  mkdir <dir>         - Create directory\n"
            "  cd <dir>            - Change directory\n"
	    "  notepad             - Open Notepad\n"
            "  calculator          - Open Calculator\n"
            "  netscape            - Open Netscape\n"
            "  clock               - Open Clock\n"
            "  trash               - Open Trash\n"
            "  mycomputer          - Open My Computer\n"
            "  paint               - Open SuperPaint\n"
            "  control             - Open NNOS Control Panel\n"
            "  taskmanager         - Open NNOS Taskmanager\n"
            "  regedit             - Open NNOS Registry Editor\n"
            "  lockdown            - Lock the NNOS Workstation and go to Logonui\n"
        )
        add_output(help_text)

    def make_directory(command):
        parts = command.split(" ", 1)
        if len(parts) < 2:
            add_output("Usage: mkdir <Directory>\n")
            return
        dir_name = os.path.join(current_dir[0], parts[1])
        try:
            os.makedirs(dir_name)
            add_output(f"Directory created: {dir_name}\n")
        except Exception as e:
            add_output(f"Error creating directory: {str(e)}\n")

    def copy_file(command):
        parts = command.split(" ", 2)
        if len(parts) < 3:
            add_output("Usage: copy <SourcePath> <DestinationPath>\n")
            return
        source = os.path.join(current_dir[0], parts[1])
        destination = os.path.join(current_dir[0], parts[2])
        if not os.path.isfile(source):
            add_output(f"Source file does not exist: {source}\n")
            return
        try:
            shutil.copy(source, destination)
            add_output(f"Copied: {source} -> {destination}\n")
        except Exception as e:
            add_output(f"Copy error: {str(e)}\n")

    def rename_file(command):
        parts = command.split(" ", 2)
        if len(parts) < 3:
            add_output("Usage: rename <OldName> <NewName>\n")
            return
        old_path = os.path.join(current_dir[0], parts[1])
        new_path = os.path.join(current_dir[0], parts[2])
        if not os.path.exists(old_path):
            add_output(f"File does not exist: {old_path}\n")
            return
        try:
            os.rename(old_path, new_path)
            add_output(f"Renamed: {old_path} -> {new_path}\n")
        except Exception as e:
            add_output(f"Rename error: {str(e)}\n")

    def delete_file(command):
        parts = command.split(" ", 1)
        if len(parts) < 2:
            add_output("Usage: del <Filename>\n")
            return
        file_path = os.path.join(current_dir[0], parts[1])
        if not os.path.exists(file_path):
            add_output(f"File does not exist: {file_path}\n")
            return
        try:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
            add_output(f"Deleted: {file_path}\n")
        except Exception as e:
            add_output(f"Delete error: {str(e)}\n")

    def change_directory(command):
        parts = command.split(" ", 1)
        if len(parts) < 2:
            add_output("Usage: cd <Directory>\n")
            return
        path = parts[1]
        new_dir = os.path.abspath(os.path.join(current_dir[0], path))
        if os.path.isdir(new_dir):
            current_dir[0] = new_dir
            add_output(f"Changed directory to {new_dir}\n")
        else:
            add_output(f"Directory does not exist: {path}\n")

    def add_output(text):
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, text)
        output_text.config(state=tk.DISABLED)
        output_text.yview(tk.END)

    input_entry.bind("<Return>", process_command)
    add_output(f"NNOS Workstation [Version {version_info}]\nType 'help' to see a list of commands.\n")

user32 = ctypes.WinDLL('user32', use_last_error=True)

EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
GetWindowText = user32.GetWindowTextW
GetWindowTextLength = user32.GetWindowTextLengthW
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
IsWindowVisible = user32.IsWindowVisible
PostMessage = user32.PostMessageW

def open_taskmanager():
    win = tk.Toplevel()
    win.title("NNOS Task Manager")
    win.geometry("650x500")
    win.config(bg="white")
    win.attributes("-topmost", 1)

    output_box = tk.Text(win, bg="black", fg="lime", font=("Consolas", 9))
    output_box.pack(fill="both", expand=True, padx=10, pady=5)

    window_list = {}

    def enum_windows():
        def callback(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    GetWindowText(hwnd, buff, length + 1)
                    title = buff.value
                    pid = ctypes.c_ulong()
                    GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                    if is_python_process(pid.value):
                        window_list[title] = hwnd  
            return True
        window_list.clear()
        EnumWindows(EnumWindowsProc(callback), 0)

    def is_python_process(pid):
        try:
            output = subprocess.check_output(
                f'tasklist /FI "PID eq {pid}" /FO LIST',
                shell=True, text=True
            )
            return "python" in output.lower()
        except:
            return False

    def refresh_tasklist():
        output_box.delete(1.0, tk.END)
        enum_windows()
        if not window_list:
            output_box.insert(tk.END, "No NNOS processes found.\n")
        else:
            output_box.insert(tk.END, f"{'Window Title':<50}{'HWND'}\n")
            output_box.insert(tk.END, "-"*70 + "\n")
            for title, hwnd in window_list.items():
                output_box.insert(tk.END, f"{title:<50}{hwnd}\n")

    def kill_process():
        title = simpledialog.askstring("Kill Process", "Enter window title to kill:")
        if title and title in window_list:
            hwnd = window_list[title]
            try:
                PostMessage(hwnd, 0x0010, 0, 0)  
                messagebox.showinfo("Killed", f"Window '{title}' closed.")
                refresh_tasklist()
            except Exception as e:
                messagebox.showerror("Error", f"Could not close window: {str(e)}")
        else:
            messagebox.showwarning("Not Found", "Window title not found.")

    btn_frame = tk.Frame(win, bg="white")
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Refresh", command=refresh_tasklist).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Kill Process by Title", command=kill_process).pack(side="left", padx=5)

    threading.Thread(target=update_system_stats, daemon=True).start()
    refresh_tasklist()

gadgets = {}

def create_clock_gadget():
    if "clock" in gadgets:
        return  

    gadget = tk.Toplevel(root)
    gadget.overrideredirect(True)
    gadget.attributes("-topmost", True)
    gadget.geometry("150x50+100+200")  

    label = tk.Label(gadget, text="", font=("Arial", 18), bg="black", fg="lime")
    label.pack(fill=tk.BOTH, expand=True)

    def update_time():
        label.config(text=time.strftime("%H:%M:%S"))
        gadget.after(1000, update_time)

    def start_drag(event):
        gadget._drag_start_x = event.x
        gadget._drag_start_y = event.y

    def do_drag(event):
        x = gadget.winfo_x() + event.x - gadget._drag_start_x
        y = gadget.winfo_y() + event.y - gadget._drag_start_y
        gadget.geometry(f"+{x}+{y}")

    gadget.bind("<Button-1>", start_drag)
    gadget.bind("<B1-Motion>", do_drag)

    update_time()
    gadgets["clock"] = gadget

def remove_gadget(name):
    if name in gadgets:
        gadgets[name].destroy()
        del gadgets[name]

def toggle_gadget(name, create_func):
    if name in gadgets:
        remove_gadget(name)
    else:
        create_func()

def create_note_gadget():
    if "note" in gadgets:
        return

    save_path = r"C:\NNOS\document\note.txt"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    gadget = tk.Toplevel(root)
    gadget.overrideredirect(True)
    gadget.attributes("-topmost", True)
    gadget.geometry("250x200+200+200")
    gadget.configure(bg="lightyellow")

    text_area = tk.Text(gadget, wrap="word", font=("Arial", 10), bg="lightyellow", fg="black", undo=True)
    text_area.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

    def save_note():
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(text_area.get("1.0", tk.END).strip())
        except Exception as e:
            print("Error by Saving:", e)

    def load_note():
        if os.path.exists(save_path):
            try:
                with open(save_path, "r", encoding="utf-8") as f:
                    text_area.insert("1.0", f.read())
            except Exception as e:
                print("Error by Loading:", e)

    def autosave_loop():
        save_note()
        gadget.after(60000, autosave_loop)  

    def start_drag(event):
        gadget._drag_start_x = event.x
        gadget._drag_start_y = event.y

    def do_drag(event):
        x = gadget.winfo_x() + event.x - gadget._drag_start_x
        y = gadget.winfo_y() + event.y - gadget._drag_start_y
        gadget.geometry(f"+{x}+{y}")

    def show_note_menu(event):
        menu = tk.Menu(gadget, tearoff=0)
        menu.add_command(label="Save", command=save_note)
        menu.add_command(label="Close", command=lambda: remove_gadget("note"))
        menu.post(event.x_root, event.y_root)

    gadget.bind("<Button-1>", start_drag)
    gadget.bind("<B1-Motion>", do_drag)
    gadget.bind("<Button-3>", show_note_menu)
    text_area.bind("<Control-s>", lambda e: save_note())

    load_note()
    autosave_loop()
    gadgets["note"] = gadget

def create_diashow_gadget():
    gadget_window = tk.Toplevel(root)
    gadget_window.geometry("800x600")
    gadget_window.config(bg="white", bd=0)  
    gadget_window.overrideredirect(True)  
  

    canvas = tk.Canvas(gadget_window, bg="white")
    canvas.pack(fill="both", expand=True)

    draw_commands = []

    def load_and_draw(file_path):
        canvas.delete("all")
        draw_commands.clear()
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    command = line.strip()
                    draw_commands.append(command)
                    parts = command.split()
                    if parts[0] == "line":
                        x1, y1, x2, y2, color, width = int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), parts[5], int(parts[6])
                        canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
        except Exception as e:
            messagebox.showerror("Error Gadget Diashow (1)", f"Error loading File {file_path}: {e}")

    def start_diashow():
        files = [f for f in os.listdir("C:/NNOS/pictures") if f.endswith(".txt")]
        if not files:
            messagebox.showerror("Error Gadget Diashow (2)", "No pictures for Diashow found.")
            return

        current_index = 0

        def display_next_image():
            nonlocal current_index
            if current_index < len(files):
                file_path = os.path.join("C:/NNOS/pictures", files[current_index])
                load_and_draw(file_path)
                current_index += 1
            else:
                current_index = 0  
            gadget_window.after(3000, display_next_image)  

        display_next_image()  

    start_button = tk.Button(gadget_window, text="Start Diashow", command=start_diashow)
    start_button.pack(side="bottom", padx=5, pady=5)

    def start_move(event):
        gadget_window.x = event.x
        gadget_window.y = event.y

    def move_window(event):
        deltax = event.x - gadget_window.x
        deltay = event.y - gadget_window.y
        new_x = gadget_window.winfo_x() + deltax
        new_y = gadget_window.winfo_y() + deltay
        gadget_window.geometry(f"+{new_x}+{new_y}")

    gadget_window.bind("<Button-1>", start_move)
    gadget_window.bind("<B1-Motion>", move_window)

    return gadget_window

def show_gadget(event):
    global gadget_window
    if gadget_window.winfo_exists():  
        gadget_window.lift()  
    else:
        gadget_window = create_diashow_gadget()


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
        result = messagebox.askyesno("Start?", f"Do you what start '{name}'?")
        if result:
            command()

    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Start", command=show_start_option)
    context_menu.add_command(label="Delete form Desktop this item", command=icon.destroy)

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
    create_icon("Superpaint", open_paint, x_start + x_offset, y_start + 100)
    create_icon("Control Panel", open_control_panel, x_start + 2 * x_offset, y_start + 100)
    
def change_background_color(color):
    root.config(bg=color)

def create_desktop_context_menu():
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Blue Desktop Color", command=lambda: change_background_color("darkblue"))
    context_menu.add_command(label="Yellow Desktop Color", command=lambda: change_background_color("yellow"))
    context_menu.add_command(label="Green Desktop Color", command=lambda: change_background_color("green"))
    context_menu.add_command(label="Red Desktop Color", command=lambda: change_background_color("red"))
    gadgets_menu = tk.Menu(context_menu, tearoff=0)
    gadgets_menu.add_command(label="Toggle Clock", command=lambda: toggle_gadget("clock", create_clock_gadget))
    gadgets_menu.add_command(label="Toggle Scratchpad", command=lambda: toggle_gadget("note", create_note_gadget))
    gadgets_menu.add_command(label="Diashow", command=create_diashow_gadget)

    context_menu.add_cascade(label="Gadgets", menu=gadgets_menu)



    def show_context_menu(event):
        context_menu.post(event.x_root, event.y_root)

    root.bind("<Button-3>", show_context_menu)

def create_start_button():
    global start_button
    start_button = tk.Button(taskbar, text="Start", command=open_start_menu, bg="lightgrey", font=("Arial", 14))
    start_button.pack(side=tk.LEFT, padx=5, pady=2)

def open_start_menu():
    start_menu = tk.Menu(root, tearoff=0, bg="lightgrey", font=("Arial", 12))

    programmes_menu = tk.Menu(start_menu, tearoff=0, font=("Arial", 12))
    programmes_menu.add_command(label="Notepad", command=open_notepad)
    programmes_menu.add_command(label="Calculator", command=open_calculator)
    programmes_menu.add_command(label="Netscape", command=open_netscape)
    programmes_menu.add_command(label="Clock", command=open_clock)
    programmes_menu.add_command(label="Trash", command=open_trash)
    programmes_menu.add_command(label="My Computer", command=open_my_computer)
    programmes_menu.add_command(label="SuperPaint", command=open_paint)
    start_menu.add_cascade(label="Programms", menu=programmes_menu)
    system_control_tools = tk.Menu(start_menu, tearoff=0, font=("Arial", 12))
    system_control_tools.add_command(label="Registry Editor", command=start_registry_editor)
    system_control_tools.add_command(label="Control Panel", command=open_control_panel)
    system_control_tools.add_command(label="Command Prompt", command=nnos_command_prompt)
    system_control_tools.add_command(label="Taskmanager", command=open_taskmanager)
    start_menu.add_cascade(label="System Control Tools", menu=system_control_tools)

    start_button_x = start_button.winfo_rootx()
    start_button_y = start_button.winfo_rooty()

    start_menu.post(start_button_x, start_button_y - start_menu.winfo_reqheight())

def create_taskbar():
    global taskbar 
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

    create_start_button() 

root = tk.Tk()
root.title("Netscape Navigator OS")
root.attributes('-fullscreen', True)
root.config(bg="darkblue")

show_startup_screen()

startup()

main_menu = tk.Menu(root)
file_menu = tk.Menu(main_menu, tearoff=0)

file_menu.add_command(label="Shutdown", command=show_shutdown_screen)

file_menu.add_command(label="Restart", command=show_restart_screen)

file_menu.add_command(label="Log Workstation", command=lambda: [root.withdraw(), show_login_options()])

main_menu.add_cascade(label="Shutdown Options", menu=file_menu)
root.config(menu=main_menu)

help_menu = tk.Menu(main_menu, tearoff=0)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Netscape Navigator OS\nVersion 0.6 Beta 2, Workstation Codename Louisa\nCopyright Alte F1 Games 2024, 2025-New Netscape"))
help_menu.add_command(label="How works Netscape Navigator OS?", command=lambda: messagebox.showinfo("How works Netscape Navigator OS?", "Netscape Navigator OS 0.6 Beta 2 Workstation, Windows Version, based on Python 3.13. For Windows 7 Users work Python 3.8.10 but Windows 8.1 with 3.13 is more stabil!"))
help_menu.add_command(label="Whats new?", command=lambda: messagebox.showinfo("Whats new?", "Netscape Navigator OS 0.6 Beta 2 had a Update on the NNOS Startmenu that is now fixed on his postion, additional NNOS 0.6 Beta 2 had new Programms (NNOS Workstation Command Prompt, NNOS Taskmanager), a Updated Control Panel and NNOS Gadgets like Windows 7 or Vista "))
main_menu.add_cascade(label="Information about Netscape Navigator OS", menu=help_menu)

root.config(menu=main_menu)

add_desktop_icons()

create_taskbar()

create_desktop_context_menu()

root.mainloop()


