import socket
from cryptography.fernet import Fernet
import threading
import tkinter as tk
from tkinter import scrolledtext, END, simpledialog, Toplevel
from tkinter import messagebox
import sys


root = tk.Tk()  # This is needed to use simpledialog before the main GUI starts
root.withdraw()  # Hide the main window until needed

#key = input("Enter the encryption key: ").encode()
key = simpledialog.askstring("Encryption Key", "Enter the encryption key:", show='*')
if not key:
    sys.exit("No key provided")
#cipher = Fernet(key)
cipher = Fernet(key.encode())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receive():
    while True:
        try:
            encrypted_message = client.recv(1024)
            if not encrypted_message:
                break
            decrypted_msg = cipher.decrypt(encrypted_message).decode()
            messages_text.insert(tk.END, decrypted_msg.split("|", 1)[1] + "\n")
        except:
            break

def send_message(event=None):  # event is passed for bindings
    msg_content = message_entry.get()
    if msg_content:
        message = f"{alias}: {msg_content}"
        messages_text.insert(tk.END, f"You: {msg_content}\n")
        encrypted_msg = cipher.encrypt(f"{room_name}|{message}".encode())
        client.send(encrypted_msg)
    message_entry.delete(0, END)


def on_closing(event=None):
    message_entry.delete(0, END)
    message_entry.insert(0, "/quit")
    send_message()


def prompt_for_room():
    global alias, room_name, full_name, email_address
    window = Toplevel(root)
    window.geometry("400x250")
    window.title("Join or Create Room")

    tk.Label(window, text="Alias").pack(pady=5)
    alias_entry = tk.Entry(window)
    alias_entry.pack(pady=5)
    
    tk.Label(window, text="Full Name").pack(pady=5)
    full_name_entry = tk.Entry(window)
    full_name_entry.pack(pady=5)

    tk.Label(window, text="Email Address").pack(pady=5)
    email_entry = tk.Entry(window)
    email_entry.pack(pady=5)

    tk.Label(window, text="Room Name").pack(pady=5)
    room_entry = tk.Entry(window)
    room_entry.pack(pady=5)

    def proceed():
        global alias, room_name, full_name, email_address
        alias = alias_entry.get()
        full_name = full_name_entry.get()
        email_address = email_entry.get()
        room_name = room_entry.get()
        
        # Check if any of the fields is empty
        if not (alias and full_name and email_address and room_name):
            tk.messagebox.showwarning("Input Error", "All fields are mandatory!")
            return

        # Add the room name to the main chat window after connecting:
        room_label = tk.Label(root, text=f"Room: {room_name}", font=("Arial", 12, "bold"))
        room_label.pack(pady=10)

	

        # Validation can be added here, e.g., checking if the fields are empty.
        
        client.connect(('127.0.0.1', 5555))
        client.send(cipher.encrypt(room_name.encode()))

        receiver_thread = threading.Thread(target=receive)
        receiver_thread.daemon = True
        receiver_thread.start()

        window.destroy()

    tk.Button(window, text="Proceed", command=proceed).pack(pady=10)

def close_session():
    message_entry.delete(0, END)
    message_entry.insert(0, "/quit")
    send_message()
    root.destroy()


def send_typing_notification(event=None):
    """Send a typing notification to the server."""
    typing_message = f"{room_name}|{alias} is typing..."
    encrypted_msg = cipher.encrypt(typing_message.encode())
    client.send(encrypted_msg)
    message_entry.bind("<KeyPress>", send_typing_notification)

# ... [other client code] ...

def send_typing_notification(event=None):
    """Send a typing notification to the server."""
    typing_message = f"{room_name}|{alias} is typing..."
    encrypted_msg = cipher.encrypt(typing_message.encode())
    client.send(encrypted_msg)

# Bind the typing notification function to the KeyPress event in the message_entry widget
    message_entry.bind("<KeyPress>", send_typing_notification)

# ... [other client code] ...


root = tk.Tk()
root.title("Chat Client")

frame = tk.Frame(root)
scrollbar = tk.Scrollbar(frame)
messages_text = scrolledtext.ScrolledText(frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
messages_text.pack(side=tk.LEFT, fill=tk.BOTH)
messages_text.pack()
frame.pack(pady=10)

message_entry = tk.Entry(root, width=38)
message_entry.bind("<Return>", send_message)
message_entry.pack(pady=10)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

# Add this button after the send_button in the GUI:

quit_button = tk.Button(root, text="Quit", command=close_session, fg="red")
quit_button.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)
prompt_for_room()
root.mainloop()
