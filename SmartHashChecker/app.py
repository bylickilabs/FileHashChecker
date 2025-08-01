
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import hashlib
import os

lang = "en"

TEXTS = {
    "en": {
        "title": "File Hash Checker (GUI)",
        "file_label": "Select file:",
        "browse": "Browse",
        "algorithm": "Hash algorithm:",
        "calculate": "Calculate hash",
        "export": "Export hash",
        "result": "Result:",
        "error_file": "File not found.",
        "error_hash": "Please calculate the hash first.",
        "exported": "Hash exported to:",
        "lang_switch": "Switch to German",
        "success": "Success",
        "error": "Error"
    },
    "de": {
        "title": "Datei-Hash Prüfer (GUI)",
        "file_label": "Datei auswählen:",
        "browse": "Durchsuchen",
        "algorithm": "Hash-Algorithmus:",
        "calculate": "Hash berechnen",
        "export": "Hash exportieren",
        "result": "Ergebnis:",
        "error_file": "Datei nicht gefunden.",
        "error_hash": "Bitte zuerst den Hash berechnen.",
        "exported": "Hash gespeichert unter:",
        "lang_switch": "Wechsle zu Englisch",
        "success": "Erfolg",
        "error": "Fehler"
    }
}

def hash_file(filepath, algorithm):
    h = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def browse_file(entry):
    filepath = filedialog.askopenfilename()
    if filepath:
        entry.delete(0, tk.END)
        entry.insert(0, filepath)

def calculate_hash():
    filepath = file_entry.get()
    algorithm = hash_algo.get()
    if not filepath or not os.path.isfile(filepath):
        messagebox.showerror(TEXTS[lang]["error"], TEXTS[lang]["error_file"])
        return
    try:
        result = hash_file(filepath, algorithm)
        result_var.set(result)
    except Exception as e:
        messagebox.showerror(TEXTS[lang]["error"], str(e))

def export_hash():
    result = result_var.get()
    if not result:
        messagebox.showwarning(TEXTS[lang]["error"], TEXTS[lang]["error_hash"])
        return
    filepath = file_entry.get()
    algorithm = hash_algo.get()
    outname = f"{os.path.basename(filepath)}.{algorithm}.hash.txt"
    with open(outname, 'w') as f:
        f.write(result)
    messagebox.showinfo(TEXTS[lang]["success"], f"{TEXTS[lang]['exported']} {outname}")

def switch_language():
    global lang
    lang = "de" if lang == "en" else "en"
    update_labels()

def update_labels():
    root.title(TEXTS[lang]["title"])
    file_label.config(text=TEXTS[lang]["file_label"])
    browse_btn.config(text=TEXTS[lang]["browse"])
    algo_label.config(text=TEXTS[lang]["algorithm"])
    calc_btn.config(text=TEXTS[lang]["calculate"])
    export_btn.config(text=TEXTS[lang]["export"])
    result_label.config(text=TEXTS[lang]["result"])
    lang_btn.config(text=TEXTS[lang]["lang_switch"])

# GUI
root = tk.Tk()
root.title(TEXTS[lang]["title"])

file_label = tk.Label(root, text=TEXTS[lang]["file_label"])
file_label.grid(row=0, column=0, sticky="w")
file_entry = tk.Entry(root, width=60)
file_entry.grid(row=1, column=0, padx=5, pady=5)
browse_btn = tk.Button(root, text=TEXTS[lang]["browse"], command=lambda: browse_file(file_entry))
browse_btn.grid(row=1, column=1)

algo_label = tk.Label(root, text=TEXTS[lang]["algorithm"])
algo_label.grid(row=2, column=0, sticky="w")
hash_algo = ttk.Combobox(root, values=["md5", "sha1", "sha256", "sha512"])
hash_algo.set("sha256")
hash_algo.grid(row=3, column=0, padx=5, pady=5, sticky="w")

calc_btn = tk.Button(root, text=TEXTS[lang]["calculate"], command=calculate_hash)
calc_btn.grid(row=4, column=0, pady=5, sticky="w")
export_btn = tk.Button(root, text=TEXTS[lang]["export"], command=export_hash)
export_btn.grid(row=4, column=1, pady=5)

result_label = tk.Label(root, text=TEXTS[lang]["result"])
result_label.grid(row=5, column=0, sticky="w")
result_var = tk.StringVar()
tk.Entry(root, textvariable=result_var, width=80).grid(row=6, column=0, columnspan=2, padx=5, pady=5)

lang_btn = tk.Button(root, text=TEXTS[lang]["lang_switch"], command=switch_language)
lang_btn.grid(row=7, column=0, pady=5, sticky="w")

root.mainloop()
