# Run PyInstaller to create a one-file executable
pyinstaller --onefile stop_shit_area_driver.py

# Get the path of the generated executable
$exePath = Get-ChildItem ./dist/*.exe | Select-Object -ExpandProperty FullName

# Copy the executable to the current folder, overwriting any existing file,
# -Force safety: just dist build exe  file, so its ok.

Copy-Item $exePath -Destination . -Force