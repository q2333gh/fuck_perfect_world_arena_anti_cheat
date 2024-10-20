import subprocess
import win32service
import win32serviceutil
import ctypes
import sys
import os


def driver_installed_status(driver_name):
    try:
        win32serviceutil.QueryServiceStatus(driver_name)
        return True
    except:
        return False


def is_driver_running(driver_name):
    try:
        service_status = win32serviceutil.QueryServiceStatus(driver_name)
        return service_status[1] == win32service.SERVICE_RUNNING
    except:
        return False


def stop_driver(driver_name):
    try:
        win32serviceutil.StopService(driver_name)
        print(f"Successfully stopped the driver '{driver_name}'.")
        return True
    except Exception as e:
        print(f"Failed to stop the driver '{driver_name}'. Error: {str(e)}")
        return False


def request_uac_or_exit():
    username = os.getlogin()
    print(f"Script is being run by: {username}")

    if ctypes.windll.shell32.IsUserAnAdmin():
        print("INFO: UAC request successful: Already Running as administrator.")
    else:
        print("Requesting UAC permissions...")
        #  "runas" semantics: tell os to runas_admin.
        # its not clear to human read.
        result = ctypes.windll.shell32.ShellExecuteW(
            # hwnd, lpOperation, lpFile, lpParameters, lpDirectory, nShowCmd
            None,
            "runas",
            sys.executable,
            " ".join(sys.argv),
            None,
            1,
        )
        if result > 32:
            print("UAC request successful: Running as administrator.")
        else:
            print("ERROR: UAC request failed")
            input("Press Enter to exit...")


def service_auto_statart_status(service_name):
    try:
        service_manager = win32service.OpenSCManager(
            None, None, win32service.SC_MANAGER_ALL_ACCESS
        )
        service = win32service.OpenService(
            service_manager, service_name, win32service.SERVICE_QUERY_CONFIG
        )
        config = win32service.QueryServiceConfig(service)

        if config[1] == win32service.SERVICE_AUTO_START:
            print(f"The service '{service_name}' is set to start automatically.")
            return True
        else:
            print(f"The service '{service_name}' is not set to start automatically.")
            return False
    except Exception as e:
        print(f"Failed to query the service '{service_name}'. Error: {str(e)}")
        return False


def disable_auto_start(driver_name):
    try:
        print("service is auto start,try to disable it ")
        subprocess.run(
            [
                "powershell",
                "-Command",
                f"Set-Service -Name {driver_name} -StartupType Disabled",
            ],
            check=True,
        )
        print(f"Successfully disabled auto-start for the driver '{driver_name}'.")
        return True
    except subprocess.CalledProcessError as e:
        print(
            f"Failed to disable auto-start for the driver '{driver_name}'. Error: {str(e)}"
        )


# pyinstaller --onefile stop_shit_area_driver.py
if __name__ == "__main__":
    # MessagingService_5e93b  C:\Windows\system32\svchost.exe -k UnistackSvcGroup  WAHTS  -k UnistackSvcGroup
    print(
        "INFO: 完美对战反作弊有几率造成蓝屏： anticheat driver with run(trigger) everytime when login into arena.exe\n     安装驱动然后调用他自己的DLL， 扫盘， 扫内存，扫进程，干扰Kernel"
    )

    driver_name = "MessageTransfer"

    if not driver_installed_status(driver_name):
        print(f"The driver '{driver_name}' is not installed.")
    else:
        print(f"INFO: The driver '{driver_name}' is installed.")
        # print(service_auto_statart_status(driver_name))
        if is_driver_running(driver_name):
            print(f"The driver '{driver_name}' is currently running.")
            user_input = input("Do you want to stop the driver? (y/n): ")
            if user_input.lower() == "y":
                request_uac_or_exit()
                stop_driver(driver_name)
            else:
                print("WARNING: Driver stop operation aborted by user.")
        else:
            print(f"GOOD: The driver '{driver_name}.sys' is not running.")
        if service_auto_statart_status(driver_name):
            disable_auto_start(driver_name)
            print(
                f"After disable auto start: service_auto_statart_status is: "
                + str(service_auto_statart_status(driver_name))
            )

    input("Press Enter to exit...")
