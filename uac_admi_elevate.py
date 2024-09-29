import sys
import ctypes
import subprocess

if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
    else:
        subprocess.call([sys.argv[1]] + sys.argv[2:])
