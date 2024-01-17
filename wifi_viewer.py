import subprocess
import re
import time

__author__ = "Munseer-am"
leading_spaces=0

text = f"Wifi Password Viewer Created by {__author__}"
text_chars = list(text)
current, mutated = "", ""
for i in range(len(text)):
    original = text_chars[i]
    current += original
    mutated += f"\033[1;38;5;82m{text_chars[i].upper()}\033[0m"
    print(f'\r{" " * leading_spaces}{mutated}', end="")
    time.sleep(0.05)
    print(f'\r{" " * leading_spaces}{current}', end="")
    mutated = current

print(f'\r{" " * leading_spaces}{text}\n')

command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

wifi_list = []

if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = {}
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            if password == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]
            wifi_list.append(wifi_profile)

for x in range(len(wifi_list)):
    print(wifi_list[x])