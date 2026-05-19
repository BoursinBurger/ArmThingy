import os
import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
from pathlib import Path
from SaveSlot import SaveSlot


class ArmThingyUI:

    def __init__(self, root):
        # Path declarations
        self.cwd = Path(__file__).parent
        self.icon_path = self.cwd / "ArmThingyIcon.png"
        self.hash_map_path = self.cwd / "hashes.json"

        # Main Window
        self.main_window = root
        self.main_window.title("Arm Thingy - Knuckle Jet Save Viewer")
        self.main_window.geometry("600x700")
        self.icon = tk.PhotoImage(file=self.icon_path)
        self.main_window.iconphoto(True, self.icon)

        # Save Slot Selector Frame
        self.selector_frame = ttk.Frame(self.main_window, padding=10)
        self.selector_frame.pack(fill=tk.X)

        self.selector_label = ttk.Label(self.selector_frame, text="Select Save Slot:")
        self.selector_label.pack(side=tk.LEFT)

        self.selector_text = tk.StringVar()
        self.selector_combobox = ttk.Combobox(self.selector_frame,
                                              textvariable=self.selector_text,
                                              state="readonly",
                                              width=40)
        self.selector_combobox.pack(side=tk.LEFT, padx=10)
        self.selector_combobox.bind("<<ComboboxSelected>>", self.save_slot_selected)

        self.selector_refresh = ttk.Button(self.selector_frame,
                                           text="Refresh",
                                           command=self.refresh_save_slots)
        self.selector_refresh.pack(side=tk.LEFT, padx=5)

        # Text Frame
        self.text_frame = ttk.Frame(self.main_window, padding=10)
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        self.text_box = tk.Text(self.text_frame,
                                wrap=tk.NONE,
                                font=("Consolas", 12))
        self.text_scroll_x = ttk.Scrollbar(self.text_frame,
                                           orient=tk.HORIZONTAL,
                                           command=self.text_box.xview)
        self.text_scroll_y = ttk.Scrollbar(self.text_frame,
                                           orient=tk.VERTICAL,
                                           command=self.text_box.yview)

        self.text_box.configure(xscrollcommand=self.text_scroll_x.set,
                                yscrollcommand=self.text_scroll_y.set)

        self.text_box.grid(row=0, column=0, sticky="nsew")
        self.text_scroll_y.grid(row=0, column=1, sticky="ns")
        self.text_scroll_x.grid(row=1, column=0, sticky="ew")

        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)

        # Save Slot Data
        self.save_slots: list[SaveSlot] = []

        # Hash Map
        self.hash_map: dict[str, str] = {}

    def run(self):
        self.load_hash_map()
        self.load_save_data()
        self.main_window.mainloop()

    def load_save_data(self):
        save_file_path = (Path(os.getenv("APPDATA")) / "../LocalLow/Rain/Knuckle Jet/saves.kj").resolve()
        if not save_file_path.exists():
            showerror("Error", f"Knuckle Jet save file not found:\n{save_file_path}")
            return

        with save_file_path.open("r") as save_handle:
            save_json = json.load(save_handle)

        slots = save_json.get("slots")
        if slots is None:
            showerror("Error", "Save file does not contain 'slots' key")
            return

        save_slots = []
        for slot in slots:
            s = SaveSlot(slot)
            save_slots.append(s)
        self.save_slots = save_slots

        combobox_values = []
        for index, save_slot in enumerate(self.save_slots):
            combobox_values.append(f"Slot #{index}: {save_slot.date_modified}")
        self.selector_combobox["values"] = combobox_values

    def apply_hash_map(self, obj):
        match obj:
            case str():
                hashed_str = self.hash_map.get(obj, obj)
                if hashed_str.strip():
                    return hashed_str
                else:
                    return obj
            case dict():
                return {self.apply_hash_map(key): self.apply_hash_map(value) for key, value in obj.items()}
            case list():
                return [self.apply_hash_map(item) for item in obj]
            case _:
                return obj

    @staticmethod
    def snake_case_to_human_case(snake_case_str):
        return ' '.join(word.capitalize() for word in snake_case_str.split('_'))

    def display_save_slot(self, save_slot_obj):
        display_dict = {}
        for key, value in save_slot_obj.__dict__.items():
            if key.startswith("_"):
                continue
            display_dict[self.snake_case_to_human_case(key)] = self.apply_hash_map(value)
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, json.dumps(display_dict, indent=4, default=str))

    @staticmethod
    def flatten(json_dict):
        flattened_dict = {}
        for key, value in json_dict.items():
            if isinstance(value, dict):
                flattened_dict.update(ArmThingyUI.flatten(value))
            else:
                flattened_dict[key] = value
        return flattened_dict

    def load_hash_map(self):
        if not self.hash_map_path.exists():
            showerror("Error", f"Hash Map file not found:\n{self.hash_map_path}")
            return
        with self.hash_map_path.open("r") as hash_handle:
            hash_json = json.load(hash_handle)
        self.hash_map = self.flatten(hash_json)

    def save_slot_selected(self, event=None):
        slot_index = self.selector_combobox.current()
        if slot_index != -1 and slot_index < len(self.save_slots):
            save_slot = self.save_slots[slot_index]
            self.display_save_slot(save_slot)

    def refresh_save_slots(self):
        self.load_save_data()
