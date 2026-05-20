import os
import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
from pathlib import Path
from SaveSlot import SaveSlot


class ArmThingyUI:

    v12_filename = "defaultSaveFile.saveDataSlot"
    v14_filename = "saves.kj"

    def __init__(self, root):
        # Path declarations
        self.cwd = Path(__file__).parent
        self.icon_path = self.cwd / "ArmThingyIcon.png"
        self.hash_map_path = self.cwd / "hashes.json"
        appdata = os.getenv("APPDATA")
        if not appdata:
            showerror("Error", "APPDATA environment variable not found. Is this not a Windows machine?")
            return
        self.save_directory = (Path(appdata) / "../LocalLow/Rain/Knuckle Jet").resolve()
        self.save_file_v12 = self.save_directory / self.v12_filename
        self.save_file_v14 = self.save_directory / self.v14_filename
        self.save_file_path = None

        # Main Window
        self.main_window = root
        self.main_window.title("Arm Thingy - Knuckle Jet Save Viewer")
        self.main_window.geometry("600x700")
        self.icon = tk.PhotoImage(file=self.icon_path)
        self.main_window.iconphoto(True, self.icon)

        # Save File Selector Frame
        self.file_frame = ttk.Frame(self.main_window, padding=5)
        self.file_frame.pack(fill=tk.X)

        self.file_radio_label = ttk.Label(self.file_frame, text="Select Save File:")
        self.file_radio_label.pack(side=tk.LEFT)

        self.file_radio_var = tk.StringVar()
        self.file_radio_v12 = ttk.Radiobutton(self.file_frame,
                                              text=self.v12_filename,
                                              variable=self.file_radio_var,
                                              value=self.v12_filename,
                                              command=self.radio_button_selection)
        self.file_radio_v14 = ttk.Radiobutton(self.file_frame,
                                              text=self.v14_filename,
                                              variable=self.file_radio_var,
                                              value=self.v14_filename,
                                              command=self.radio_button_selection)
        self.file_radio_v12.pack(side=tk.LEFT, padx=5)
        self.file_radio_v14.pack(side=tk.LEFT, padx=5)

        self.file_refresh = ttk.Button(self.file_frame,
                                       text="Refresh",
                                       command=self.refresh_save_slots)
        self.file_refresh.pack(side=tk.LEFT, padx=5)

        # Save Slot Selector Frame
        self.slot_frame = ttk.Frame(self.main_window, padding=5)
        self.slot_frame.pack(fill=tk.X)



        self.slot_combobox_label = ttk.Label(self.slot_frame, text="Select Save Slot:")
        self.slot_combobox_label.pack(side=tk.LEFT)

        self.slot_var = tk.StringVar()
        self.slot_combobox = ttk.Combobox(self.slot_frame,
                                          textvariable=self.slot_var,
                                          state="readonly",
                                          width=40)
        self.slot_combobox.pack(side=tk.LEFT, padx=10)
        self.slot_combobox.bind("<<ComboboxSelected>>", self.save_slot_selected)



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
        self.check_save_paths()
        self.main_window.mainloop()

    def radio_button_selection(self):
        selected_var = self.file_radio_var.get()

        if selected_var == self.v12_filename:
            self.save_file_path = self.save_file_v12
        elif selected_var == self.v14_filename:
            self.save_file_path = self.save_file_v14
        else:
            showerror("Error", "No save slot selected")
            return
        self.load_save_data()

    def check_save_paths(self):
        if self.save_file_v12.exists() and self.save_file_v14.exists():
            self.file_radio_v12.config(state='normal')
            self.file_radio_v14.config(state='normal')
        elif self.save_file_v12.exists():
            self.save_file_path = self.save_file_v12
            self.file_radio_v12.config(state='normal')
            self.file_radio_v14.config(state='disabled')
            self.file_radio_v12.invoke()
        elif self.save_file_v14.exists():
            self.save_file_path = self.save_file_v14
            self.file_radio_v12.config(state='disabled')
            self.file_radio_v14.config(state='normal')
            self.file_radio_v14.invoke()
        else:
            showerror("Error", "No save files found")

    def load_save_data(self):
        if not self.save_file_path.exists():
            showerror("Error", f"Knuckle Jet save file not found:\n{self.save_file_path}")
            return

        with self.save_file_path.open("r") as save_handle:
            save_json = json.load(save_handle)

        # Determine save file format:
        # v12 save file format consists of a single save slot
        # v14 save file format consists of multiple save slots
        if "slots" in save_json:
            slots = save_json.get("slots")
            save_format = "v14"
        else:
            slots = [save_json]
            save_format = "v12"

        save_slots = []
        for slot in slots:
            s = SaveSlot(slot)
            save_slots.append(s)
        self.save_slots = save_slots

        combobox_values = []
        # For v14 save file format, create combobox values with slot index and date modified
        # For v12 save file format, create a single default combobox value
        if save_format == "v14":
            for index, save_slot in enumerate(self.save_slots):
                combobox_values.append(f"Slot #{index}: {save_slot.date_modified}")
        else:
            combobox_values.append("Default")
        self.slot_combobox["values"] = combobox_values

        # If only one slot exists, select its combobox entry by default
        if len(self.save_slots) == 1:
            self.slot_combobox.current(0)
            self.slot_combobox.event_generate("<<ComboboxSelected>>")

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

    def save_slot_selected(self, _):
        slot_index = self.slot_combobox.current()
        if slot_index != -1 and slot_index < len(self.save_slots):
            save_slot = self.save_slots[slot_index]
            self.display_save_slot(save_slot)

    def refresh_save_slots(self):
        self.load_save_data()
        self.save_slot_selected(None)
