Get-WmiObject Win32_PnpEntity | Select-Object Name, DriverVersion, CreationDate | Format-Table -AutoSize | Out-File -FilePath "$PSScriptRoot\DriversList.txt"

