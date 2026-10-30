"""Desktop launcher retained under the original filename."""

import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

from shop import PROFILES, generate_inventory


def main():
    root = tk.Tk()
    root.title("D&D shop inventory")
    root.geometry("760x650")
    frame = ttk.Frame(root, padding=16)
    frame.pack(fill="both", expand=True)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(3, weight=1)
    store = tk.StringVar(value="village")
    seed = tk.StringVar()
    status = tk.StringVar(
        value="Choose a settlement. An optional seed repeats an inventory."
    )
    result = None
    ttk.Label(frame, text="Shop profile").grid(row=0, column=0, sticky="w")
    ttk.Combobox(
        frame, textvariable=store, values=list(PROFILES), state="readonly"
    ).grid(row=0, column=1, sticky="ew")
    ttk.Label(frame, text="Seed (optional)").grid(row=1, column=0, sticky="w", pady=8)
    ttk.Entry(frame, textvariable=seed).grid(row=1, column=1, sticky="ew")
    output = tk.Text(frame, wrap="word", state="disabled")
    output.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10)
    scrollbar = ttk.Scrollbar(frame, command=output.yview)
    scrollbar.grid(row=3, column=2, sticky="ns")
    output.configure(yscrollcommand=scrollbar.set)
    ttk.Label(frame, textvariable=status, wraplength=650).grid(
        row=4, column=0, columnspan=2
    )

    def generate():
        nonlocal result
        result = None
        output.configure(state="normal")
        output.delete("1.0", "end")
        try:
            result = generate_inventory(
                store.get(), int(seed.get()) if seed.get().strip() else None
            )
            seed.set(str(result["seed"]))
            for rarity, items in result["categories"].items():
                if items:
                    output.insert("end", f"{rarity.replace('_', ' ').title()}\n")
                    output.insert(
                        "end", "\n".join(f"• {item}" for item in items) + "\n\n"
                    )
            status.set(
                " ".join(result["warnings"])
                or f"Generated {sum(map(len, result['categories'].values()))} items."
            )
        except (ValueError, OSError) as error:
            status.set(f"Cannot generate inventory: {error}")
        finally:
            output.configure(state="disabled")

    def export():
        if result is None:
            status.set("Generate an inventory first.")
            return
        path = filedialog.asksaveasfilename(
            parent=root, defaultextension=".json", filetypes=[("JSON", "*.json")]
        )
        if path:
            try:
                Path(path).write_text(
                    json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
                status.set("Inventory saved.")
            except OSError as error:
                status.set(f"Cannot save: {error}")

    ttk.Button(frame, text="Generate", command=generate).grid(
        row=2, column=0, sticky="ew"
    )
    ttk.Button(frame, text="Export JSON…", command=export).grid(
        row=2, column=1, sticky="ew"
    )
    root.mainloop()


if __name__ == "__main__":
    main()
