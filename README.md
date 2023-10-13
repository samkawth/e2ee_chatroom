# Encrypted Chatroom

A secure chatroom application with support for text messages,

## Features

- **End-to-End Encryption**: All communication between server and client is encrypted using a shared encryption key.
- **Voice Messaging**: Record and send voice messages seamlessly. *** Feature will be available in the next version. ***
- **File Transfer**: Share files directly through the chatroom. *** Feature will be available in the next version. ***
- **Multi-room Support**: Different chatrooms can be set up, and users can join any room of their choice.

## Installation

### Prerequisites

1. **Python**: Ensure you have Python 3.x installed. You can download it from [python.org](https://www.python.org/downloads/).

2. **Dependencies**: Install the required Python libraries:

   ```bash
   pip3 install cryptography pyaudio tkinter (this is for Voice feature)
   ```

### Setting up the Server

1. Clone this repository:
   ```bash
   git clone https://github.com/samkawth/e2ee_chatroom
   ```

2. Navigate to the directory:
   ```bash
   cd path-to-directory
   ```

3. Run the server:
   ```bash
   python3 server.py
   ```

### Setting up the Client

1. On a client machine, ensure you have cloned the repository and installed the prerequisites.

2. Navigate to the directory:
   ```bash
   cd path-to-directory
   ```

3. Run the client:
   ```bash
   python3 client.py
   ```

4. When prompted, enter the encryption key provided by the server.

5. Choose or join a room and start chatting!

## Usage

- **Send Text**: Type your message and press `Enter` or click `Send`.

## Troubleshooting

- **Connection Issues**: Ensure both the server and client are running and are on the same network. Make sure to enter the correct encryption key on the client side.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---
