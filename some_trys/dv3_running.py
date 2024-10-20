import wmi
import os

# Initialize the WMI client
c = wmi.WMI()

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Open the output file
with open(os.path.join(script_dir, "DriversList2.txt"), "w") as file:
    # Write the header
    file.write(
        f"{'DisplayName':<90} {'PathName':<120} {'State':<15} {'StartMode':<15} {'InstallDate':<25}\n"
    )
    file.write("=" * 155 + "\n")

    # Query the Win32_SystemDriver class
    for driver in c.Win32_SystemDriver():
        if (
            driver.State == "Running"
            and "Microsoft" not in driver.DisplayName
            and "Windows" not in driver.DisplayName
            and "Intel" not in driver.DisplayName
            and "Disk" not in driver.DisplayName
            and "USB" not in driver.DisplayName
            and "VMware" not in driver.DisplayName
            and "Mouse" not in driver.DisplayName
            and "Bluetooth" not in driver.DisplayName
        ):
            display_name = driver.DisplayName or "N/A"
            path_name = driver.PathName or "N/A"
            state = driver.State or "N/A"
            start_mode = driver.StartMode or "N/A"
            install_date = driver.InstallDate or "N/A"

            # Write the driver information to the file
            file.write(
                f"{display_name:<90} {path_name:<120} {state:<15} {start_mode:<15} {install_date:<25}\n"
            )

print("Filtered running driver information has been saved to DriversList.txt")
