import sys
import os
import winreg
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def register_protocol():
    # 1. Determine paths dynamically
    installer_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(os.path.dirname(installer_dir), "src")
    dispatcher_path = os.path.join(src_dir, "dispatcher.py")
    python_exe = sys.executable

    # 2. Define the command to run
    # Format: "C:\Path\To\python.exe" "C:\Path\To\dispatcher.py" "%1"
    command = f'"{python_exe}" "{dispatcher_path}" "%1"'

    print(f"Registering mspvpn:// protocol...")
    print(f"Target Script: {dispatcher_path}")

    try:
        # 3. Create Registry Keys
        # HKEY_CLASSES_ROOT\mspvpn
        key_path = r"mspvpn"
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "URL:MSP VPN Protocol")
            winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
        
        # HKEY_CLASSES_ROOT\mspvpn\shell\open\command
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{key_path}\\shell\\open\\command") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command)

        print("\nSUCCESS! Protocol registered.")
        print("You can now click 'mspvpn://' links in your browser.")
        
        # 4. Create VPN folders if missing
        for folder in ["WireGuard", "OpenVPN"]:
            path = os.path.join(src_dir, folder)
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"Created directory: {path}")

    except Exception as e:
        print(f"\nERROR: Could not write to registry. {e}")

if __name__ == "__main__":
    if not is_admin():
        print("Requesting Admin privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(f'"{arg}"' for arg in sys.argv), None, 1)
    else:
        register_protocol()
        input("\nPress Enter to exit...")