
import hashlib
import os
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.prompt import Confirm

console = Console()
lang = "en"

TEXTS = {
    "en": {
        "menu": "File Integrity Checker",
        "opt1": "[1] Check file hash",
        "opt2": "[2] Compare two files",
        "opt3": "[3] Export hash to file",
        "opt4": "[4] Change language",
        "opt0": "[0] Exit",
        "ask_path": "Enter file path",
        "ask_alg": "Choose algorithm (md5 / sha1 / sha256 / sha512)",
        "ask_compare": "Enter second file path to compare",
        "same": "[green]Files are identical.[/green]",
        "diff": "[red]Files differ.[/red]",
        "exported": "[green]Hash exported to file.[/green]",
        "langset": "[cyan]Language switched.[/cyan]",
        "exit": "[yellow]Goodbye![/yellow]"
    },
    "de": {
        "menu": "Datei-Integritätsprüfer",
        "opt1": "[1] Datei-Hash berechnen",
        "opt2": "[2] Zwei Dateien vergleichen",
        "opt3": "[3] Hash in Datei exportieren",
        "opt4": "[4] Sprache wechseln",
        "opt0": "[0] Beenden",
        "ask_path": "Dateipfad eingeben",
        "ask_alg": "Algorithmus wählen (md5 / sha1 / sha256 / sha512)",
        "ask_compare": "Zweiten Dateipfad zum Vergleichen eingeben",
        "same": "[green]Dateien sind identisch.[/green]",
        "diff": "[red]Dateien unterscheiden sich.[/red]",
        "exported": "[green]Hash erfolgreich exportiert.[/green]",
        "langset": "[cyan]Sprache umgestellt.[/cyan]",
        "exit": "[yellow]Auf Wiedersehen![/yellow]"
    }
}

def hash_file(path, algorithm):
    h = hashlib.new(algorithm)
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def check_hash():
    path = Prompt.ask(TEXTS[lang]["ask_path"])
    if not os.path.isfile(path):
        console.print("[red]File not found![/red]")
        return
    alg = Prompt.ask(TEXTS[lang]["ask_alg"], default="sha256")
    try:
        hashval = hash_file(path, alg)
        table = Table(title=f"{alg.upper()} Hash")
        table.add_column("File", justify="left")
        table.add_column("Hash", justify="left")
        table.add_row(os.path.basename(path), hashval)
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def compare_files():
    f1 = Prompt.ask(TEXTS[lang]["ask_path"])
    f2 = Prompt.ask(TEXTS[lang]["ask_compare"])
    if not all(os.path.isfile(p) for p in [f1, f2]):
        console.print("[red]One or both files not found.[/red]")
        return
    alg = Prompt.ask(TEXTS[lang]["ask_alg"], default="sha256")
    h1 = hash_file(f1, alg)
    h2 = hash_file(f2, alg)
    if h1 == h2:
        console.print(TEXTS[lang]["same"])
    else:
        console.print(TEXTS[lang]["diff"])

def export_hash():
    path = Prompt.ask(TEXTS[lang]["ask_path"])
    if not os.path.isfile(path):
        console.print("[red]File not found![/red]")
        return
    alg = Prompt.ask(TEXTS[lang]["ask_alg"], default="sha256")
    h = hash_file(path, alg)
    outname = f"{os.path.basename(path)}.{alg}.hash.txt"
    with open(outname, 'w') as f:
        f.write(h)
    console.print(TEXTS[lang]["exported"] + f" → {outname}")

def switch_language():
    global lang
    lang = "de" if lang == "en" else "en"
    console.print(TEXTS[lang]["langset"])

def show_menu():
    console.print(f"\n[bold cyan]{TEXTS[lang]['menu']}[/bold cyan]")
    console.print(TEXTS[lang]["opt1"])
    console.print(TEXTS[lang]["opt2"])
    console.print(TEXTS[lang]["opt3"])
    console.print(TEXTS[lang]["opt4"])
    console.print(TEXTS[lang]["opt0"])

def main():
    while True:
        show_menu()
        choice = Prompt.ask(">", choices=["0", "1", "2", "3", "4"], default="0")
        if choice == "1":
            check_hash()
        elif choice == "2":
            compare_files()
        elif choice == "3":
            export_hash()
        elif choice == "4":
            switch_language()
        elif choice == "0":
            console.print(TEXTS[lang]["exit"])
            break

if __name__ == "__main__":
    main()
