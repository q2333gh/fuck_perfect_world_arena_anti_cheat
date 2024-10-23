import subprocess
import glob
import shutil
import os
import sys

# TODO still not work as ps1 did. buggy.
# Run PyInstaller with realtime output
process = subprocess.Popen(
    ["pyinstaller", "--onefile", "./stop_shit_area_driver.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
    bufsize=1,
)

# Print output in realtime, TODO some lib must can do this, cause other people also need this feature
while True:
    output = process.stdout.readline()
    error = process.stderr.readline()

    if output:
        print(output.strip())
    if error:
        print(error.strip(), file=sys.stderr)

    # Break if process is finished
    if output == "" and error == "" and process.poll() is not None:
        break

# Get the path of the generated executable
exe_path = glob.glob(os.path.join("dist", "*.exe"))[0]

# Copy the executable to the current directory, overwriting if it exists
# !safety: just cp dist build exe file, so its ok.
shutil.copy2(exe_path, ".", follow_symlinks=True)
