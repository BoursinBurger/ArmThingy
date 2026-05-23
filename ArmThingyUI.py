import os
import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
from pathlib import Path
from SaveSlot import SaveSlot
from ArmThingyFunctions import flatten, pretty_time_delta, snake_case_to_human_case


class ArmThingyUI:
    v12_filename = "defaultSaveFile.saveDataSlot"
    v14_filename = "saves.kj"

    def __init__(self, root):
        """
        Initialize the UI components and set up the application window
        :param root: Tkinter root window
        """
        
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
                                              command=self.event_radio_button_selection)
        self.file_radio_v14 = ttk.Radiobutton(self.file_frame,
                                              text=self.v14_filename,
                                              variable=self.file_radio_var,
                                              value=self.v14_filename,
                                              command=self.event_radio_button_selection)
        self.file_radio_v12.pack(side=tk.LEFT, padx=5)
        self.file_radio_v14.pack(side=tk.LEFT, padx=5)

        self.file_refresh = ttk.Button(self.file_frame,
                                       text="Refresh",
                                       command=self.event_refresh_button_click)
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
        self.slot_combobox.bind("<<ComboboxSelected>>", self.event_save_slot_selection)

        # Text Frame
        self.text_frame = ttk.Frame(self.main_window, padding=10)
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        self.text_box = tk.Text(self.text_frame,
                                wrap=tk.NONE,
                                font=("Consolas", 12),
                                state=tk.DISABLED)
        self.text_box.bind("<1>", lambda event: self.text_box.focus_set())

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

    def check_save_paths(self):
        """
        Check for save file existence and configure radio buttons accordingly
        :return:
        """
        if self.save_file_v12.exists() and self.save_file_v14.exists():
            self.file_radio_v12.config(state=tk.NORMAL)
            self.file_radio_v14.config(state=tk.NORMAL)
        elif self.save_file_v12.exists():
            self.save_file_path = self.save_file_v12
            self.file_radio_v12.config(state=tk.NORMAL)
            self.file_radio_v14.config(state=tk.DISABLED)
            self.file_radio_v12.invoke()
        elif self.save_file_v14.exists():
            self.save_file_path = self.save_file_v14
            self.file_radio_v12.config(state=tk.DISABLED)
            self.file_radio_v14.config(state=tk.NORMAL)
            self.file_radio_v14.invoke()
        else:
            showerror("Error", "No save files found")

    def load_save_data(self):
        """
        Load save data from the selected save file path and populate the save slots in the combobox
        :return:
        """
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
            for index, save_slot in enumerate(self.save_slots, start=1):
                combobox_values.append(f"Slot #{index} | "
                                       f"{save_slot.date_modified.strftime('%Y-%m-%d %H:%M:%S')} | "
                                       f"{pretty_time_delta(save_slot.time_spent)}")
        else:
            combobox_values.append("Default save slot")
        self.slot_combobox["values"] = combobox_values

        # If only one slot exists, select its combobox entry by default
        if len(self.save_slots) == 1:
            self.slot_combobox.current(0)
            self.slot_combobox.event_generate("<<ComboboxSelected>>")
        # Otherwise, if a valid entry has not been selected,
        # set temporary message prompting user to select a slot and clear the text box
        else:
            slot_index = self.slot_combobox.current()
            if slot_index == -1 or slot_index >= len(self.save_slots):
                self.slot_combobox.set("Select a save slot")
                self.text_box.config(state=tk.NORMAL)
                self.text_box.delete(1.0, tk.END)
                self.text_box.config(state=tk.DISABLED)

    def display_save_slot(self, save_slot_obj):
        """
        Display the contents of the selected save slot object in a human-readable format in the Text widget
        :param save_slot_obj: Save slot object to display
        :return:
        """
        display_dict = {}
        for key, value in save_slot_obj.__dict__.items():
            if key.startswith("_"):
                continue
            # Convert snake_case attributes of the object to human-readable format
            display_dict[snake_case_to_human_case(key)] = self.apply_hash_map(value)

        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, json.dumps(display_dict, indent=4, default=str))
        self.text_box.config(state=tk.DISABLED)

    def load_hash_map(self):
        """
        Load the hash map from the JSON file path and flatten it for use in the application.
        :return:
        """
        if not self.hash_map_path.exists():
            showerror("Error", f"Hash Map file not found:\n{self.hash_map_path}")
            return
        with self.hash_map_path.open("r") as hash_handle:
            hash_json = json.load(hash_handle)
        self.hash_map = flatten(hash_json)

    def apply_hash_map[T](self, obj: T) -> T:
        """
        Recursively apply the hash map to nested objects, preserving structure and replacing matching hashes with text
        :param obj: Object to apply the hash map to
        :return: Object with the hash map applied
        """

        # Function behavior is determined by the input object type and returns the same type.
        # Apply the hash map recursively to the object components until they resolve to strings.
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

    def event_radio_button_selection(self):
        """
        Handle radio button selection for save file version: set the save file path and load save data
        :return:
        """
        selected_var = self.file_radio_var.get()

        if selected_var == self.v12_filename:
            self.save_file_path = self.save_file_v12
        elif selected_var == self.v14_filename:
            self.save_file_path = self.save_file_v14
        else:
            showerror("Error", "No save slot selected")
            return
        self.load_save_data()

    def event_save_slot_selection(self, _):
        """
        Handle the selection of a save slot in the combobox and display its contents.
        :param _: Event parameter, not used
        :return:
        """
        slot_index = self.slot_combobox.current()
        if slot_index != -1 and slot_index < len(self.save_slots):
            save_slot = self.save_slots[slot_index]
            self.display_save_slot(save_slot)

    def event_refresh_button_click(self):
        """
        Handle the Refresh button's click event: reload the save data and update the UI.
        :return:
        """
        self.load_save_data()
        self.event_save_slot_selection(None)

    def run(self):
        """
        Load the hash map from JSON, check for save files, then start running the tkinter application
        :return:
        """
        self.load_hash_map()
        self.check_save_paths()
        self.main_window.mainloop()
