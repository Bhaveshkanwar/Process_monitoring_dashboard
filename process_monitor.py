import psutil
import time
import os
from prettytable import PrettyTable

def clear_console():
    """Clear the console output."""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_memory(mem_bytes):
    """Format memory size to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if mem_bytes < 1024:
            return f"{mem_bytes:.2f} {unit}"
        mem_bytes /= 1024
    return f"{mem_bytes:.2f} PB"

def display_process_info():
    """Display real-time process information."""
    while True:
        clear_console()
        table = PrettyTable(['PID', 'Name', 'CPU %', 'Memory Usage', 'Status', 'Threads'])
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status', 'num_threads']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                cpu = proc.info['cpu_percent']
                memory = format_memory(proc.info['memory_info'].rss)
                status = proc.info['status']
                threads = proc.info['num_threads']

                table.add_row([pid, name, cpu, memory, status, threads])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        print("Real-Time Process Monitoring Dashboard")
        print(table)
        print("Press Ctrl+C to exit.")
        time.sleep(1)

if __name__ == "__main__":
    display_process_info()
