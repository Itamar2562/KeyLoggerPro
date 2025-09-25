# Keylogger Trojan (Self-Learning / Ethical Hacking)

> **Disclaimer:** This software is created strictly for **educational purposes**.  
> Use only on systems you own or have explicit permission to test. Unauthorized use is illegal.

---

## What is it?

This project is a **keylogger trojan** designed for **self-learning and ethical hacking**.  

- Runs in the background on the client machine.  
- Captures all keystrokes and sends them to a server.  
- On the server, data is saved in a folder named `Targets`, with each client creating its own subfolder.  
- If the connection is lost, the client will **automatically attempt to reconnect**.  

---

## How it works

### Server
- Listens for incoming client connections.  
- Saves all received keystrokes into organized folders.  

### Client
- Runs on the target machine.  
- Captures keystrokes using `pynput`.  
- Continuously attempts to connect and send data to the server.  

---

## How to use

1. **Configure IP and Port**  
   - Open `config.json`.  
   - Change the `IP` field to your server’s IP address.  
   - Ensure the `PORT` is free and matches the server.

2. **Run the Server**  
   - Start the server script on your designated machine.

3. **Run the Client**  
   - Execute `client.exe` on the target machine with the config file in the **same folder**.  

4. **View Captured Data**  
   - Keystrokes will appear in the `Targets` folder on the server, separated by client IP.  

---

## Libraries Used

### Server
- `socket`  
- `threading`  
- `os`  

### Client
- `pynput`  
- `socket`  
- `time`  
- `threading`  
- `json`  

---

## Notes / Warnings

- **Ethical Use Only:** Running this on unauthorized computers is illegal.  
- Ensure your firewall and antivirus allow connections on the chosen port during testing.  
- The client runs in the background and will automatically try to reconnect if the server is unreachable.
