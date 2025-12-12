# netops-command-center
A geolocation-based Network Operations dashboard designed mainly for MSPs. Visualizes remote networks on an interactive map and bridges the browser to the local system to instantly launch VPNs, RDP sessions, and SSH terminals.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)

## Features

* **Visual Command:** Interactive map (Leaflet.js) showing all client sites geographically.
* **One-Click Tunnels:** Custom `mspvpn://` protocol launches local VPN clients instantly.
* **Asset Tools:** Integrated launch buttons for RDP, SSH, and HTTP connections to client gateways.
* **Smart Geocoding:** Auto-resolves physical addresses to GPS coordinates.
* **Auto-Backup:** Automatic JSON database backups on every modification.

## Prerequisites

* **Python 3.14+** (Ensure **"Add Python to PATH"** is checked during installation).
* **OpenVPN Client:** [Version 2.6.17-I001-amd64](https://swupdate.openvpn.org/community/releases/OpenVPN-2.6.17-I001-amd64.msi) (Required for OpenVPN support).
* **WireGuard:** Official Windows Client installed. (App version 0.5.3 was used here).

## Installation

### 1. The Server (The Dashboard Host)
This machine hosts the map and database. It does **not** need VPN clients installed.
1.  **Install Python:** Download Python 3.14+ and install it (Check "Add to PATH").
2.  **Get the Code:** Download this repository and extract it to `C:\MSPVPN` (or your preferred location).
3.  **Install Dependencies:** Open Command Prompt as Admin and run:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Start the Server:**
    * Navigate to the `src` folder.
    * Run `start_server.vbs` (runs silently in the background) or `python server.py` (visible console).
5.  **Firewall:** Ensure Inbound Port **5000** (TCP) is open on the Windows Firewall.

### 2. The Client (Technician Laptop)
This machine executes the VPN connections.
1.  **Install Python:** Install Python 3.14+ (Check "Add to PATH").
2.  **Install VPNs:** Ensure WireGuard and OpenVPN are installed.
3.  **Run the Installer:**
    * Open Command Prompt as Administrator.
    * Run `python installers/install_protocol.py`
    * *This script registers the custom protocol and automatically creates the empty `WireGuard` and `OpenVPN` config folders in `src/`.*
4.  **Add Configs:** Place your `.conf` or `.ovpn` files into the newly created folders.

## Usage
1.  Open a browser on any computer in the network.
2.  Navigate to `http://[SERVER_IP_ADDRESS]:5000`.
3.  **Add Client:** Enter the Name, Address, and the **exact filename** of the VPN config (excluding `.conf`).
4.  **Connect:** Click the map pin -> Click "Connect". The VPN will launch on your local machine.

## Configuration Notes
* **WireGuard:** Config filenames must match the "Config Name" entered in the dashboard exactly.
* **OpenVPN:** Ensure `openvpn-gui.exe` is located at the default path (`C:\Program Files\OpenVPN\bin\`) or update `src/dispatcher.py` to match your path.
* **Security:** This tool is designed for internal LAN use. Do not expose Port 5000 to the public internet without a reverse proxy or VPN.

## License
Distributed under the MIT License. See `LICENSE` for more information.
