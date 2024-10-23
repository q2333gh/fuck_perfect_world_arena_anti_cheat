import subprocess
import glob
import shutil
import os

# Run PyInstaller and print output in shell
result = subprocess.run(
    ["pyinstaller", "--onefile", "./stop_shit_area_driver.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

# Get the path of the generated executable
exe_path = glob.glob(os.path.join("dist", "*.exe"))[0]

# Copy the executable to the current directory, overwriting if it exists
# !safety: just cp  dist build exe  file, so its ok.
shutil.copy2(exe_path, ".", follow_symlinks=True)
