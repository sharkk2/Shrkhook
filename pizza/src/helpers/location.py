import subprocess
import json

def get_location():
    try:
        ps_script = """
        Add-Type -AssemblyName System.Device
        $geoWatcher = New-Object System.Device.Location.GeoCoordinateWatcher
        $geoWatcher.Start()
        while (($geoWatcher.Status -ne 'Ready') -and ($geoWatcher.Permission -ne 'Denied')) { Start-Sleep -Milliseconds 100 }
        if ($geoWatcher.Permission -eq 'Denied') { Write-Output '{"error": "Location access denied"}'; exit }
        $location = $geoWatcher.Position.Location
        Write-Output ('{"latitude":' + $location.Latitude + ',"longitude":' + $location.Longitude + '}')
        """
        
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        result = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True, startupinfo=startupinfo)
        location_data = json.loads(result.stdout.strip())
        
        if "error" in location_data:
            return None
        
        return location_data
    except Exception as e:
       return None
