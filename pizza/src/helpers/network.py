import subprocess
import re
import requests

class Network:
    def __init__(self):
        self.ssid = None
        self.protocol = None
        self.security_type = None
        self.network_band = None
        self.network_channel = None
        self.link_speed = None
        self.mac = None
        self.ipv4_address = None
        self.signal = None
        self.ipv4_dns_servers = None
        self.manufacturer = None
        self.description = None
        self.driver_version = None
        self.public_ip = None
        self.fetch()

    def fetch(self):
        self.interface_info()
        self.ip_dns()
        self.driver()
        self.publicip()

    def interface_info(self):
        try:
            output = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], text=True) 
            # re is soo shit
            # *:\s(.+)$
            self.ssid = self.pattern(output, r"^\s*SSID\s*:\s(.+)$")
            self.protocol = self.pattern(output, r"^\s*Radio type\s*:\s(.+)$")
            self.security_type = self.pattern(output, r"^\s*Authentication\s*:\s(.+)$")
            self.network_channel = self.pattern(output, r"^\s*Channel\s*:\s(.+)$")
            self.mac = self.pattern(output, r"^\s*Physical address\s*:\s(.+)$")
            self.signal = self.pattern(output, r"^\s*Signal\s*:\s(.+)$")
            rx = self.pattern(output, r"^\s*Receive rate \(Mbps\)\s*:\s(.+)$")
            tx = self.pattern(output, r"^\s*Transmit rate \(Mbps\)\s*:\s(.+)$")
            if rx and tx:
                self.link_speed = f"{rx}/{tx} Mbps"

            proto = (self.protocol or "").lower()
            if "802.11n" in proto:
                self.network_band = "2.4 GHz or 5 GHz (depends on device)"
            elif "802.11ac" in proto:
                self.network_band = "5 GHz"
            elif "802.11ax" in proto:
                self.network_band = "2.4 GHz and/or 5 GHz (wifi 6)"
        except Exception:
            pass

    def ip_dns(self):
        try:
            output = subprocess.check_output(["ipconfig", "/all"], text=True)
            # [.\s]*:\s([0-9\.]+)
            self.ipv4_address = self.pattern(output, r"IPv4 Address[.\s]*:\s([0-9\.]+)")
            dns = re.findall(r"DNS Servers[.\s]*:\s([0-9\.]+)", output)
            self.ipv4_dns_servers = dns if dns else None
        except Exception:
            pass

    def driver(self):
        try:
            output = subprocess.check_output(["netsh", "wlan", "show", "drivers"], text=True)
            self.manufacturer = self.pattern(output, r"^\s*Vendor\s*:\s(.+)$")
            self.description = self.pattern(output, r"^\s*Name\s*:\s(.+)$")
            self.driver_version = self.pattern(output, r"^\s*Driver\s*:\s(.+)$")
        except Exception:
            pass

    def publicip(self):
      try:
          response = requests.get('https://api.ipify.org', timeout=5)
          response.raise_for_status()
          self.public_ip = response.text
      except Exception:
          pass

    def pattern(self, text, pattern):
        match = re.search(pattern, text, re.MULTILINE)
        return match.group(1).strip() if match else None
