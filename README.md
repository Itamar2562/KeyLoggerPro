# Keylogger Trojan (Self-Learning / Ethical Hacking)

> **Disclaimer:** This software is created strictly for **educational purposes**.  
> Use only on systems you own or have explicit permission to test. Unauthorized use is illegal.

---

## What is it?

This project is a **keylogger trojan** designed for **self-learning and ethical hacking**.  

- Runs in the background on the client machine.  
- Captures **all keystrokes** and sends them to a server.  
- Takes **screenshots every minute** and sends them to the server.  
- On the server, all data is saved in a folder named `Targets`. Each client has its **own subfolder**, which contains:
  - `Keylog.txt` (keystrokes)  
  - `Screenshots/` (all screenshots captured from the client)  
- If the connection is lost, the client will **automatically attempt to reconnect**.

---

## How it works

### Server
- Listens for incoming client connections.  
- Stores all received keystrokes in `Keylog.txt`.  
- Saves received screenshots into `Screenshots/` inside each client’s folder.  

### Client
- Runs on the target machine.  
- Captures keystrokes using `pynput`.  
- Captures the screen using `PIL.ImageGrab` and sends screenshots every minute.  
- Continuously attempts to reconnect if the server is unavailable.  

---

## How to Use

1. **Configure IP and Port**  
   - Open `Client/config.json`.  
   - Change `IP` to your server’s IP address and ensure the port matches the server.  

2. **Run the Server**  
   - Execute `Server/server.py` on the server machine.  

3. **Run the Client**  
   - Run `Client/client.exe` on the target machine with `config.json` in the **same folder** .  

4. **Monitor Captured Data**  
   - Keystrokes are saved in `Targets/data of <client_ip>/Keylog.txt`.  
   - Screenshots are saved in `Targets/data of <client_ip>/Screenshots/`.  

---

## Libraries Used

### Server
- `socket`  
- `threading`  
- `os`  
- `io`  
- `PIL.Image`  
- `datetime`  

### Client
- `pynput`  
- `socket`  
- `time`  
- `threading`  
- `json`  
- `PIL.ImageGrab`  
- `io`  
