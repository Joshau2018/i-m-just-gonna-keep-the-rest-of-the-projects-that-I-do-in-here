import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
from datetime import datetime


class HistoryApp:
    def __init__(self, root):
        self.WINDOW_WIDTH = 1150
        self.WINDOW_HEIGHT = 475
        self.root = root
        self.root.title("On This Date in History")
        self.root.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}')
        self.data = ""

        # Create Widgets
        self.setup_widgets()

    def setup_widgets(self):
        self.top_frame = tk.Frame(self.root)
        self.top_frame.grid(row=0, column=0)
        self.side_frame = tk.Frame(self.root)
        self.side_frame.grid(row=1, column=5)

        # Month and Day selection
        self.month_var = tk.StringVar()
        self.day_var = tk.IntVar(value=datetime.now().day)

        self.month_label = tk.Label(self.top_frame, text="Month")
        self.month_label.grid(row=0, column=0, padx=5, pady=10)
        months = [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)]
        self.month_combo = ttk.Combobox(self.top_frame, values=months, textvariable=self.month_var)
        self.month_combo.bind("<<ComboboxSelected>>", self.combobox_changed)
        self.month_combo.grid(column=1, row=0, padx=10, pady=10)
        self.month_combo.current(0)

        self.day_label = tk.Label(self.top_frame, text="Day")
        self.day_label.grid(column=2, row=0, padx=5, pady=10)
        self.day_spin = tk.Spinbox(self.top_frame, from_=1, to=31, textvariable=self.day_var, command=self.clear_data)
        self.day_spin.grid(column=3, row=0, padx=10, pady=10)

        # Event type selection
        self.event_type_var = tk.StringVar(value="Births")
        self.rb_births = ttk.Radiobutton(self.side_frame, text="Births", variable=self.event_type_var, value="Births", command=self.populate_text_area)
        self.rb_births.grid(column=0, row=0, sticky=tk.W, padx=10)
        self.rb_deaths = ttk.Radiobutton(self.side_frame, text="Deaths", variable=self.event_type_var, value="Deaths", command=self.populate_text_area)
        self.rb_deaths.grid(column=0, row=1, sticky=tk.W, padx=10)
        self.rb_events = ttk.Radiobutton(self.side_frame, text="Events", variable=self.event_type_var, value="Events", command=self.populate_text_area)
        self.rb_events.grid(column=0, row=2, sticky=tk.W, padx=10)

        # Text area for output with no wrap
        self.text_area = tk.Text(self.root, wrap=tk.NONE, width=120, height=20)
        self.text_area.grid(column=0, row=1, columnspan=4, sticky='nsew', padx=10, pady=15)

        # Horizontal Scrollbar
        self.h_scroll = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.text_area.xview)
        self.h_scroll.grid(column=0, row=3, columnspan=4, sticky='ew')
        self.text_area['xscrollcommand'] = self.h_scroll.set

        # Vertical Scrollbar
        self.v_scroll = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.text_area.yview)
        self.v_scroll.grid(column=4, row=1, sticky='ns')
        self.text_area['yscrollcommand'] = self.v_scroll.set


        # Button to fetch history
        self.fetch_btn = ttk.Button(self.root, text="What Happened?", command=self.fetch_history)
        self.fetch_btn.grid(column=0, row=4, columnspan=4, pady=10)

    def fetch_history(self):
        pass

    def combobox_changed(self, event):
        pass

    def clear_data(self):
        pass

    def populate_text_area(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = HistoryApp(root)
    root.mainloop()
