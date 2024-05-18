# Import required modules
import socket
import threading

hostServer = "localhost" 
portEntry = 9999
LISTENER_LIMIT = 5
active_clients = []  # List of all currently connected users

# Function to listen for upcoming messages from a client
def listen_for_messages(client, username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + ' : ' + message
            send_messages_to_all(final_msg)

        else:
            print(f"The message send from client {username} is empty")


# Function to send message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())

# Function to send any new message to all the clients that
# are currently connected to this server
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client):
    # Server will listen for client message that will
    # Contain the username
    run = True
    while run:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "[SERVER UPDATE] " + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            run = False
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username,)).start()

# Main function
def main():
    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block
    try:
        # Provide the server with an address in the form of
        # host IP and port

        server.bind((hostServer, portEntry))
        print(f"Running the server on {hostServer} {portEntry}")
    except:
        print(f"Unable to bind to host {hostServer} and port {portEntry}")

    # Set server limit
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        #Starts server update threading
        #this will send server updates to all users showing who joined the server via display Name
        threading.Thread(target=client_handler, args=(client,)).start()


if __name__ == '__main__':
    main()