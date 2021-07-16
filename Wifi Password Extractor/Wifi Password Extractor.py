import subprocess

FORMAT = "utf-8"

data = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode(FORMAT).split("\n")
# wifis = [line.split(":")[1][1:-1] for line in data if "All User Profile" in line] # Fails if : in name
wifis = [line[27:-1] for line in data if "All User Profile" in line]

def num_space(word, longest, allowance = 5):
    return f"{word:<{longest + allowance}}"

longest = len(max(wifis, key = len))
output = []
for wifi_name in wifis:
    results = subprocess.check_output(["netsh", "wlan", "show", "profile", wifi_name, "key=clear"]).decode(FORMAT).split("\n")
    results = [line.split(":")[1][1:-1] for line in results if "Key Content" in line]

    line = f"Name: {num_space(wifi_name, longest)}"
    try:
        line += f"Password: {results[0]}"
    except IndexError:
        line += f"Password: NONE - as in none, signed - Owner"

    print (line)
    output.append(line + "\n")

with open("Extract.txt", "w") as f:
    f.writelines(output)
