import psutil
import time
import os
from prettytable import PrettyTable

def clear_console():
    #Clear the console output.
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
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status', 'num_threads']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                status = proc.info['status']
                threads = proc.info['num_threads']
                cpu=proc.cpu_percent(interval=0.1)
                
                memory_info=proc.info.get('memory_info')
                memory = format_memory(proc.info['memory_info'].rss) if memory_info else "N/A"
                
               
                    
                processes.append([pid, name, cpu, memory, status, threads])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        #Sort processes by CPU usage (highest first)
        processes.sort(key=lambda x: x[2], reverse=True)

        #Add to table
        for proc in processes:
            table.add_row(proc)
            
        print("Real-Time Process Monitoring Dashboard\n")
        print(table)
        print("\n Press Ctrl+C to exit.")
        time.sleep(1)

if __name__ == "__main__":
    display_process_info()
