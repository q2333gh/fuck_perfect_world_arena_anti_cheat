import wmi
from datetime import datetime


def get_driver_info():
    c = wmi.WMI()
    drivers = []

    for driver in c.Win32_PnPSignedDriver():
        if driver.DeviceName and driver.DriverDate:
            # Convert the WMI datetime string to a readable format
            driver_date = datetime.strptime(
                driver.DriverDate.split(".")[0], "%Y%m%d%H%M%S"
            )
            formatted_date = driver_date.strftime("%Y-%m-%d %H:%M:%S")
            drivers.append((driver.DeviceName, formatted_date, driver_date))

    # Sort drivers by driver date (latest first)
    drivers.sort(key=lambda x: x[2], reverse=True)

    with open("driver_info.txt", "w") as file:
        file.write(f"{'Driver Name':<50} | {'Driver Date':<20}\n")
        file.write(f"{'-'*50} | {'-'*20}\n")

        for driver in drivers:
            file.write(f"{driver[0]:<50} | {driver[1]:<20}\n")


if __name__ == "__main__":
    get_driver_info()
