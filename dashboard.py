import psutil
import tkinter as tk
from tkinter import ttk
import threading
import os
import signal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ProcessMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Process Monitoring Dashboard")
        self.root.geometry("1000x600")
        self.root.configure(bg="#2E2E2E")
        
        # Title Label
        title_label = tk.Label(root, text="Real-Time Process Monitoring Dashboard", font=("Arial", 16, "bold"), fg="white", bg="#2E2E2E")
        title_label.pack(pady=10)

        # Search Bar
        search_frame = tk.Frame(root, bg="#2E2E2E")
        search_frame.pack(pady=5)

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_button = ttk.Button(search_frame, text="Search", command=self.search_process)
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Setting up the treeview
        self.tree = ttk.Treeview(root, columns=("PID", "Name", "CPU", "Memory"), show="headings")
        self.tree.heading("PID", text="PID",command=lambda: self.sort_column("PID"))
        self.tree.heading("Name", text="Name",command=lambda: self.sort_column("Name"))
        self.tree.heading("CPU", text="CPU (%)",command=lambda: self.sort_column("CPU"))
        self.tree.heading("Memory", text="Memory (MB)",command=lambda: self.sort_column("Memory"))
        self.tree.pack(fill=tk.BOTH, expand=True,padx=10,pady=5)

        
        # Kill Process Button
        self.kill_button = ttk.Button(root, text="Kill Process", command=self.kill_selected_process)
        self.kill_button.pack(pady=5)

        # Matplotlib Graphs for CPU & Memory Usage
        self.figure, self.axs = plt.subplots(2, 1, figsize=(5, 2))
        self.axs[0].set_title("CPU Usage (%)")
        self.axs[1].set_title("Memory Usage (%)")

        self.cpu_data, self.memory_data = [], []
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().pack(pady=5)


        # Refresh data every second
        self.update_processes()
        self.update_graphs()

    def update_processes(self):
        # updates process list in the table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch and display process data
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                cpu = proc.info['cpu_percent']
                #Check if memory_info is None before accessing rss
                memory_info = proc.info.get('memory_info')
                memory = round(memory_info.rss / (1024 * 1024), 2) if memory_info else 0.0

                self.tree.insert("", "end", values=(pid, name, cpu, memory))
            except (psutil.NoSuchProcess, psutil.AccessDenied,psutil.ZombieProcess):
                continue

        # Schedule next update
        self.root.after(1000, self.update_processes)


if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessMonitor(root)
    root.mainloop()
