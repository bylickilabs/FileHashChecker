import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import hashlib, os, time, csv
import pandas as pd
from datetime import datetime

LANGS = {
    "en": {
        "app_title": "File Hash Checker",
        "select_file": "Select File",
        "compare_file": "Compare File",
        "expected_hash": "Expected Hash",
        "hash_algo": "Algorithm",
        "calculate": "Calculate",
        "compare": "Compare",
        "validate": "Validate Hash",
        "folder_hash": "Hash Folder",
        "export_csv": "Export CSV",
        "duration": "Duration",
        "dark_mode": "Dark Mode",
        "light_mode": "Light Mode",
        "language": "Language",
        "plugins": "Plugins",
        "result": "Result",
        "status_ready": "Ready.",
        "status_success": "Success.",
        "status_invalid": "Invalid hash.",
        "status_valid": "Hashes match.",
        "status_diff": "Hashes do not match.",
        "status_empty": "No hash entered.",
        "select_folder": "Select Folder",
        "log": "Log",
        "nothing_export": "Nothing to export.",
        "exported": "Exported to",
        "choose_plugin": "Choose plugin",
        "run_plugin": "Run Plugin",
        "plugin_no_file": "No file selected for plugin.",
        "plugin_done": "Plugin finished",
        "plugin_failed": "Plugin failed",
        "error_file": "File not found.",
        "error_folder": "Folder not found.",
    },
    "de": {
        "app_title": "Datei-Hash Prüfer",
        "select_file": "Datei wählen",
        "compare_file": "Vergleichsdatei",
        "expected_hash": "Erwarteter Hash",
        "hash_algo": "Algorithmus",
        "calculate": "Berechnen",
        "compare": "Vergleichen",
        "validate": "Hash prüfen",
        "folder_hash": "Ordner hashen",
        "export_csv": "CSV Export",
        "duration": "Dauer",
        "dark_mode": "Dark Mode",
        "light_mode": "Heller Modus",
        "language": "Sprache",
        "plugins": "Plugins",
        "result": "Ergebnis",
        "status_ready": "Bereit.",
        "status_success": "Erfolg.",
        "status_invalid": "Hash ungültig.",
        "status_valid": "Hashes stimmen überein.",
        "status_diff": "Hashes stimmen nicht überein.",
        "status_empty": "Kein Hash eingegeben.",
        "select_folder": "Ordner wählen",
        "log": "Verlauf",
        "nothing_export": "Nichts zu exportieren.",
        "exported": "Exportiert nach",
        "choose_plugin": "Plugin wählen",
        "run_plugin": "Plugin ausführen",
        "plugin_no_file": "Keine Datei für Plugin gewählt.",
        "plugin_done": "Plugin abgeschlossen",
        "plugin_failed": "Plugin fehlgeschlagen",
        "error_file": "Datei nicht gefunden.",
        "error_folder": "Ordner nicht gefunden.",
    }
}

THEMES = {
    "light": {"bg": "#fafbfc", "fg": "#24292f", "entry": "#ffffff", "button": "#eaeaea"},
    "dark":  {"bg": "#23272e", "fg": "#b8c5d1", "entry": "#2d333b", "button": "#444c56"}
}

def get_plugins():
    plugins = []
    if os.path.isdir("plugins"):
        for f in os.listdir("plugins"):
            if f.endswith(".py"):
                plugins.append(f)
    return plugins

class HashCheckerApp:
    def __init__(self, root):
        self.root = root
        self.lang = "en"
        self.theme = "light"
        self.hashes = []
        self.plugins = get_plugins()
        self.log_entries = []
        self.widgets = {}
        self.build_gui()
        self.set_theme()
        self.set_lang()

    def build_gui(self):
        l = LANGS[self.lang]
        self.root.title(l["app_title"])
        self.root.geometry("760x620")
        self.root.resizable(False, False)

        # ---- FILE SELECTION ----
        file_frame = tk.LabelFrame(self.root, text=l["select_file"])
        file_frame.pack(fill="x", padx=15, pady=5)
        self.widgets['file_entry'] = tk.Entry(file_frame, width=60)
        self.widgets['file_entry'].pack(side="left", padx=6, pady=6)
        tk.Button(file_frame, text=l["select_file"], width=13, command=self.select_file).pack(side="left", padx=5)

        # ---- HASHING ----
        hash_frame = tk.LabelFrame(self.root, text=l["result"])
        hash_frame.pack(fill="x", padx=15, pady=5)
        hash_algo_label = tk.Label(hash_frame, text=l["hash_algo"])
        hash_algo_label.grid(row=0, column=0, padx=6, sticky="e")
        self.widgets['algo_box'] = ttk.Combobox(hash_frame, values=["md5", "sha1", "sha256", "sha512"], width=10)
        self.widgets['algo_box'].set("sha256")
        self.widgets['algo_box'].grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(hash_frame, text=l["calculate"], command=self.calculate_hash).grid(row=0, column=2, padx=5, sticky="w")
        self.result_var = tk.StringVar()
        self.widgets['result_entry'] = tk.Entry(hash_frame, textvariable=self.result_var, width=70)
        self.widgets['result_entry'].grid(row=1, column=0, columnspan=3, padx=6, pady=3, sticky="w")
        tk.Label(hash_frame, text=l["duration"]).grid(row=2, column=0, sticky="e")
        self.duration_var = tk.StringVar()
        self.widgets['duration_entry'] = tk.Entry(hash_frame, textvariable=self.duration_var, width=18, state="readonly")
        self.widgets['duration_entry'].grid(row=2, column=1, sticky="w", padx=2)

        # ---- EXPECTED HASH ----
        validate_frame = tk.LabelFrame(self.root, text=l["expected_hash"])
        validate_frame.pack(fill="x", padx=15, pady=5)
        self.widgets['expected_entry'] = tk.Entry(validate_frame, width=70)
        self.widgets['expected_entry'].grid(row=0, column=0, padx=6, pady=5)
        self.widgets['validate_label'] = tk.Label(validate_frame, text="")
        self.widgets['validate_label'].grid(row=1, column=0, padx=6, sticky="w")
        tk.Button(validate_frame, text=l["validate"], command=self.validate_hash).grid(row=0, column=1, padx=5)

        # ---- COMPARE FILES ----
        compare_frame = tk.LabelFrame(self.root, text=l["compare_file"])
        compare_frame.pack(fill="x", padx=15, pady=5)
        self.widgets['compare_entry'] = tk.Entry(compare_frame, width=60)
        self.widgets['compare_entry'].pack(side="left", padx=6, pady=6)
        tk.Button(compare_frame, text=l["select_file"], width=13, command=self.select_compare_file).pack(side="left", padx=5)
        tk.Button(compare_frame, text=l["compare"], command=self.compare_files).pack(side="left", padx=5)
        self.widgets['compare_label'] = tk.Label(compare_frame, text="")
        self.widgets['compare_label'].pack(anchor="w", padx=10, pady=2)

        # ---- FOLDER / EXPORT / MODE / LANG / PLUGINS ----
        ops_frame = tk.Frame(self.root)
        ops_frame.pack(fill="x", padx=15, pady=5)
        tk.Button(ops_frame, text=l["folder_hash"], command=self.hash_folder).pack(side="left", padx=3)
        tk.Button(ops_frame, text=l["export_csv"], command=self.export_csv).pack(side="left", padx=3)
        tk.Button(ops_frame, text=l["dark_mode"], command=self.toggle_theme).pack(side="left", padx=3)
        tk.Button(ops_frame, text=l["language"], command=self.switch_language).pack(side="left", padx=3)
        tk.Button(ops_frame, text=l["plugins"], command=self.plugin_menu).pack(side="left", padx=3)
        tk.Button(ops_frame, text=l["log"], command=self.save_log).pack(side="left", padx=3)

        # ---- LOG ----
        log_frame = tk.LabelFrame(self.root, text=l["log"])
        log_frame.pack(fill="both", expand=True, padx=15, pady=7)
        self.widgets['log_text'] = tk.Text(log_frame, width=90, height=8, state="normal")
        self.widgets['log_text'].pack(fill="both", expand=True)

        # ---- STATUS ----
        self.status_var = tk.StringVar(value=l["status_ready"])
        status_bar = tk.Label(self.root, textvariable=self.status_var, anchor="w", relief="groove")
        status_bar.pack(fill="x", padx=0, pady=(0, 4))

    def set_theme(self):
        t = THEMES[self.theme]
        self.root.configure(bg=t["bg"])
        style = ttk.Style()
        style.theme_use('clam' if self.theme == 'dark' else 'default')
        style.configure('TCombobox', fieldbackground=t["entry"], background=t["button"], foreground=t["fg"])
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.LabelFrame, tk.Frame)):
                widget.configure(bg=t["bg"])
                for child in widget.winfo_children():
                    if isinstance(child, (tk.Label, tk.Button)):
                        try:
                            child.configure(bg=t["bg"], fg=t["fg"])
                        except tk.TclError:
                            pass
                    elif isinstance(child, tk.Entry):
                        try:
                            child.configure(bg=t["entry"], fg=t["fg"])
                        except tk.TclError:
                            pass
                    elif isinstance(child, tk.Text):
                        try:
                            child.configure(bg=t["entry"], fg=t["fg"])
                        except tk.TclError:
                            pass
            elif isinstance(widget, (tk.Label, tk.Button)):
                try:
                    widget.configure(bg=t["bg"], fg=t["fg"])
                except tk.TclError:
                    pass
            elif isinstance(widget, tk.Entry):
                try:
                    widget.configure(bg=t["entry"], fg=t["fg"])
                except tk.TclError:
                    pass
            elif isinstance(widget, tk.Text):
                try:
                    widget.configure(bg=t["entry"], fg=t["fg"])
                except tk.TclError:
                    pass

    def set_lang(self):
        l = LANGS[self.lang]
        self.root.title(l["app_title"])
        # Update aller Texte/Labels/Buttons/Frames
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.LabelFrame):
                old = widget.cget("text")
                for key in ["select_file", "result", "expected_hash", "compare_file", "log"]:
                    if LANGS["en"][key] in old or LANGS["de"][key] in old:
                        widget.config(text=l[key])
            elif isinstance(widget, tk.Frame):
                for idx, btn in enumerate(widget.winfo_children()):
                    txt_map = ["folder_hash", "export_csv", "dark_mode", "language", "plugins", "log"]
                    if idx < len(txt_map):
                        btn.config(text=l[txt_map[idx]])
        self.widgets['validate_label'].config(text="")
        self.widgets['compare_label'].config(text="")

    def select_file(self):
        fname = filedialog.askopenfilename()
        if fname:
            self.widgets['file_entry'].delete(0, tk.END)
            self.widgets['file_entry'].insert(0, fname)

    def select_compare_file(self):
        fname = filedialog.askopenfilename()
        if fname:
            self.widgets['compare_entry'].delete(0, tk.END)
            self.widgets['compare_entry'].insert(0, fname)

    def calculate_hash(self):
        path = self.widgets['file_entry'].get().strip()
        algo = self.widgets['algo_box'].get()
        if not os.path.isfile(path):
            self._status("error_file")
            return
        start = time.time()
        h = self._hash_file(path, algo)
        duration = time.time() - start
        self.result_var.set(h)
        self.duration_var.set(f"{duration:.2f} s")
        self._log(f"{os.path.basename(path)} [{algo}]: {h}")
        self.hashes.append({"file": path, "algo": algo, "hash": h, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")})
        self._status("status_success")

    def _hash_file(self, path, algo):
        h = hashlib.new(algo)
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    def compare_files(self):
        f1 = self.widgets['file_entry'].get().strip()
        f2 = self.widgets['compare_entry'].get().strip()
        algo = self.widgets['algo_box'].get()
        if not (os.path.isfile(f1) and os.path.isfile(f2)):
            self._status("error_file")
            self.widgets['compare_label'].config(text=LANGS[self.lang]["error_file"], fg="red")
            return
        h1 = self._hash_file(f1, algo)
        h2 = self._hash_file(f2, algo)
        if h1 == h2:
            self.widgets['compare_label'].config(text=LANGS[self.lang]["status_valid"], fg="green")
            self._log(f"COMPARE: Match {os.path.basename(f1)} = {os.path.basename(f2)}")
        else:
            self.widgets['compare_label'].config(text=LANGS[self.lang]["status_diff"], fg="red")
            self._log(f"COMPARE: Difference {os.path.basename(f1)} ≠ {os.path.basename(f2)}")

    def validate_hash(self):
        actual = self.result_var.get().strip().lower()
        expected = self.widgets['expected_entry'].get().strip().lower()
        if not actual or not expected:
            self.widgets['validate_label'].config(text=LANGS[self.lang]["status_empty"], fg="orange")
            self._status("status_empty")
            return
        actual, expected = actual.replace(" ", ""), expected.replace(" ", "")
        if len(actual) != len(expected):
            self.widgets['validate_label'].config(text=LANGS[self.lang]["status_invalid"], fg="red")
            self._status("status_invalid")
        elif actual == expected:
            self.widgets['validate_label'].config(text=LANGS[self.lang]["status_valid"], fg="green")
            self._status("status_valid")
            self._log(f"VALIDATE: {actual} = {expected}")
        else:
            self.widgets['validate_label'].config(text=LANGS[self.lang]["status_diff"], fg="red")
            self._status("status_diff")
            self._log(f"VALIDATE: {actual} ≠ {expected}")

    def hash_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            self._status("error_folder")
            return
        algo = self.widgets['algo_box'].get()
        results = []
        start = time.time()
        file_count = 0
        error_count = 0
        for rootdir, dirs, files in os.walk(folder):
            for name in files:
                path = os.path.join(rootdir, name)
                try:
                    h = self._hash_file(path, algo)
                    results.append({"file": path, "algo": algo, "hash": h, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")})
                    self._log(f"[{algo}] {path}: {h}")
                    file_count += 1
                except Exception as e:
                    self._log(f"{name}: error ({str(e)})")
                    error_count += 1
        duration = time.time() - start
        self.duration_var.set(f"{duration:.2f} s (folder)")
        outname = f"folder_hash_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            pd.DataFrame(results).to_csv(outname, index=False)
            self._log(f"{LANGS[self.lang]['exported']} {outname} ({file_count} files, {error_count} errors)")
        except Exception as e:
            self._log(f"Folder export failed: {e}")
            messagebox.showerror("Export Error", f"Could not save folder export:\n{e}")

    def export_csv(self):
        if not self.hashes:
            self._log(LANGS[self.lang]["nothing_export"])
            return
        outname = f"hash_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            df = pd.DataFrame(self.hashes)
            df.to_csv(outname, index=False)
            self._log(f"{LANGS[self.lang]['exported']} {outname}")
        except Exception as e:
            self._log(f"CSV export failed: {e}")
            messagebox.showerror("Export Error", f"Could not save CSV export:\n{e}")

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.set_theme()

    def switch_language(self):
        self.lang = "de" if self.lang == "en" else "en"
        self.set_lang()

    def plugin_menu(self):
        if not self.plugins:
            self._log("No plugins found.")
            return
        win = tk.Toplevel(self.root)
        win.title(LANGS[self.lang]["plugins"])
        tk.Label(win, text=LANGS[self.lang]["choose_plugin"]).pack()
        plugin_var = tk.StringVar(value=self.plugins[0])
        plugin_menu = ttk.Combobox(win, textvariable=plugin_var, values=self.plugins)
        plugin_menu.pack()

        def run_plugin():
            plugin_file = plugin_var.get()
            file_path = self.widgets['file_entry'].get().strip()
            if not file_path:
                messagebox.showinfo(LANGS[self.lang]["plugins"], LANGS[self.lang]["plugin_no_file"])
                return
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("plugin", os.path.join("plugins", plugin_file))
                plugin = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(plugin)
                result = plugin.check(file_path)
                msg = LANGS[self.lang]["plugin_done"] if result else LANGS[self.lang]["plugin_failed"]
                self._log(f"{plugin_file}: {msg}")
                win.destroy()
            except Exception as e:
                self._log(f"{LANGS[self.lang]['plugin_failed']}: {str(e)}")
                win.destroy()

        tk.Button(win, text=LANGS[self.lang]["run_plugin"], command=run_plugin).pack(pady=8)

    def save_log(self):
        out = f"hash_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(out, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for line in self.log_entries:
                    writer.writerow([line])
            self._log(f"{LANGS[self.lang]['exported']} {out}")
        except Exception as e:
            self._log(f"Log export failed: {e}")
            messagebox.showerror("Log Export", f"Failed to save log:\n{e}")

    def _log(self, msg):
        t = time.strftime("%H:%M:%S")
        self.widgets['log_text'].insert(tk.END, f"[{t}] {msg}\n")
        self.widgets['log_text'].see(tk.END)
        self.log_entries.append(f"[{t}] {msg}")

    def _status(self, key):
        self.status_var.set(LANGS[self.lang].get(key, key))

if __name__ == "__main__":
    root = tk.Tk()
    app = HashCheckerApp(root)
    root.mainloop()
