import tkinter as tk
from tkinter import messagebox
import json
import os

# Registry-Dateipfad
REGISTRY_FILE_PATH = r'C:\NNOS\system\reg.json'

# Zugriff auf die Registry
class NNOSRegistry:
    def __init__(self, reg_file):
        self.reg_file = reg_file
        if not os.path.exists(self.reg_file):
            with open(self.reg_file, 'w') as f:
                json.dump({}, f, indent=4)
        self.load_registry()

    def load_registry(self):
        """Lädt die Registry aus der JSON-Datei."""
        with open(self.reg_file, 'r') as f:
            self.registry = json.load(f)

    def save_registry(self):
        """Speichert die Registry zurück in die JSON-Datei."""
        with open(self.reg_file, 'w') as f:
            json.dump(self.registry, f, indent=4)

    def set(self, key, value):
        """Setzt einen Wert für einen bestimmten Schlüssel."""
        keys = key.split("\\")
        registry_ref = self.registry
        for k in keys[:-1]:
            registry_ref = registry_ref.setdefault(k, {})
        registry_ref[keys[-1]] = value
        self.save_registry()

    def get(self, key):
        """Holt den Wert für einen bestimmten Schlüssel."""
        keys = key.split("\\")
        registry_ref = self.registry
        for k in keys:
            registry_ref = registry_ref.get(k, None)
            if registry_ref is None:
                return None
        return registry_ref

# Hauptklasse für den Calculator mit Verlauf
class CalculatorWithHistory:
    def __init__(self, root, reg):
        self.root = root
        self.reg = reg
        self.history_key = "NNOS_Calculator\\CalculatorHistory"  # Registry-Pfad für den Verlauf
        self.create_gui()

        # Fenster immer im Vordergrund
        self.root.attributes('-topmost', True)

    def create_gui(self):
        self.root.title("Enhanced NNOS Calculator")
        self.root.geometry("500x400")
        
        # Display für die Berechnungen
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        # Display
        display = tk.Entry(self.root, textvariable=self.result_var, font=("Arial", 24), bd=10, relief="sunken", justify="right")
        display.grid(row=0, column=0, columnspan=4)
        
        # Calculator Buttons
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('Clear', 5, 0), ('History', 5, 1)
        ]

        for (text, row, col) in buttons:
            btn = tk.Button(self.root, text=text, width=10, height=2, font=("Arial", 14), command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=col)

    def on_button_click(self, button):
        if button == "Clear":
            self.result_var.set("0")
        elif button == "=":
            try:
                calculation = self.result_var.get()  # Berechnung als String speichern
                result = eval(calculation)  # Ergebnis berechnen
                result_str = f"{calculation} = {result}"
                self.result_var.set(result)
                self.save_history(result_str)  # Speichern des gesamten Ausdrucks
            except Exception as e:
                messagebox.showerror("Error", "Invalid Expression")
        elif button == "History":
            self.show_history()
        else:
            current_text = self.result_var.get()
            if current_text == "0":
                self.result_var.set(button)
            else:
                self.result_var.set(current_text + button)

    def save_history(self, calculation):
        """Speichert den Verlauf der Berechnungen in der Registry."""
        history = self.reg.get(self.history_key) or []
        if len(history) >= 10:  # Begrenzung auf die letzten 10 Berechnungen
            history.pop(0)
        history.append(calculation)
        self.reg.set(self.history_key, history)

    def show_history(self):
        """Zeigt den Berechnungsverlauf in einem neuen Fenster."""
        history = self.reg.get(self.history_key) or []
        history_window = tk.Toplevel(self.root)
        history_window.title("Calculation History")
        history_window.geometry("300x300")
        
        history_listbox = tk.Listbox(history_window, font=("Arial", 12))
        for entry in history:
            history_listbox.insert(tk.END, entry)
        history_listbox.pack(fill=tk.BOTH, expand=True)

# Anwendung starten
def start_calculator():
    root = tk.Tk()
    reg = NNOSRegistry(REGISTRY_FILE_PATH)
    calc = CalculatorWithHistory(root, reg)
    root.mainloop()

if __name__ == "__main__":
    start_calculator()