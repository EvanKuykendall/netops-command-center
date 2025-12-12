import sys
import subprocess
import os
import ctypes
import webbrowser
from urllib.parse import urlparse, unquote

# --- CONFIGURATION ---
# Base directory is where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WG_DIR = os.path.join(BASE_DIR, "WireGuard")
OVPN_DIR = os.path.join(BASE_DIR, "OpenVPN")

# Standard OpenVPN Path (Users can edit this if needed)
OVPN_EXE = r"C:\Program Files\OpenVPN\bin\openvpn-gui.exe"
# ---------------------

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def manage_vpn(url_scheme):
    try:
        parsed = urlparse(url_scheme)
        protocol = parsed.netloc.lower()
        parts = parsed.path.strip("/").split("/")
        
        if len(parts) >= 2:
            action, target = parts[0], unquote(parts[1])
        elif len(parts) == 1:
            action, target = "open", unquote(parts[0])
        else:
            return

        print(f"Action: {action} | Protocol: {protocol} | Target: {target}")

        if protocol == "wireguard":
            conf_path = os.path.join(WG_DIR, f"{target}.conf")
            if action == "connect":
                if not os.path.exists(conf_path):
                    print(f"Error: Config not found at {conf_path}")
                    input("Press Enter...")
                    return
                subprocess.run(["wireguard", "/installtunnelservice", conf_path], check=True)
            elif action == "disconnect":
                subprocess.run(["wireguard", "/uninstalltunnelservice", target], check=True)

        elif protocol == "openvpn":
            if not os.path.exists(OVPN_EXE):
                print(f"Error: OpenVPN executable not found at {OVPN_EXE}")
                print("Please edit dispatcher.py to match your installation.")
                input("Press Enter...")
                return
            ovpn_file = f"{target}.ovpn"
            if action == "connect":
                subprocess.Popen([OVPN_EXE, "--connect", ovpn_file, "--config_dir", OVPN_DIR])
            elif action == "disconnect":
                subprocess.run([OVPN_EXE, "--command", "disconnect", ovpn_file], check=True)

        elif protocol == "rdp":
            subprocess.Popen(f"mstsc /v:{target}")
        
        elif protocol == "ssh":
            subprocess.Popen(f"start cmd /k ssh {target}", shell=True)

        elif protocol in ["http", "https"]:
            webbrowser.open(f"{protocol}://{target}")

    except Exception as e:
        print(f"Critical Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    if not is_admin():
        # Re-launch as Admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(f'"{arg}"' for arg in sys.argv), None, 1)
        sys.exit()

    if len(sys.argv) > 1:
        manage_vpn(sys.argv[1])
    else:
        print("MSP VPN Dispatcher is ready.")
        print(f"Scanning for configs in: {BASE_DIR}")
        input("Press Enter to close...")