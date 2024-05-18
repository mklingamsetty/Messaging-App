import socket
import threading
import tkinter as tk
from tkinter import scrolledtext #This allows a scroll feature in the case of too many messages
from tkinter import messagebox #This will display a windows TextBox Error


hostServer = "localhost"
portEntry = 9999

isThereMessage = False
isServerConnected = False

#customize initalization
DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
ORANGE = '#FF4500'
FONT = ("Comic Sans MS", 16)
BUTTON_FONT = ("Comic Sans MS", 15)
SMALL_FONT = ("Comic Sans MS", 13)

# Creating a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#windows display box error message function
def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

#connection function
def connect():
    try:
        client.connect((hostServer, portEntry))
        print("Successfully connected to server")
        isServerConnected = True

    except:
        messagebox.showerror("Unable to connect to server",
                             f"Unable to connect to server {hostServer} {portEntry}")

    username = username_textbox.get()
    if username == '':
        messagebox.showerror("Invalid username", "Username cannot be empty")
    else:
        client.sendall(username.encode())

    #starts the threading to the host server
    #This allows for messages to appear real time for all users
    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

#send message function
def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
        isThereMessage = True
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

def listen_for_messages_from_server(client):
    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            add_message(message)
        else:
            messagebox.showerror("Error", "Message received from client is empty")


# Initialize Tkinter root window
root = tk.Tk()
root.geometry("600x600")
root.title("MessengerApp")
root.resizable(False, False)

#Make TKINTER screen
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter Display Name:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=ORANGE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=8)


message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)


message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=ORANGE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

# Create a canvas and place the image on it
canvas = tk.Canvas(middle_frame, width=600, height=400)
canvas.pack(fill="both", expand=True)

# Place the ScrolledText on top of the canvas
message_box = scrolledtext.ScrolledText(canvas, font=SMALL_FONT, width=67, height=26.5, bg=OCEAN_BLUE, fg ="white", wrap=tk.WORD)
message_box.config(state=tk.DISABLED, highlightthickness=0, bd=0)

# Create a window on the canvas for the ScrolledText widget
canvas.create_window((0, 0), window=message_box, anchor="nw")


def main():
    root.mainloop()

if __name__ == '__main__':
    main()
