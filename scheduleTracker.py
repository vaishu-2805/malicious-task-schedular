import os
import subprocess

def CheckValidTask(creator, task):
    allowlist = ["Microsoft", "Mozilla", "Adobe Systems Incorporated"]
    extensions = [".exe", ".py", ".dll"]

    # Check if the creator is trusted
    trusted = any(creator.startswith(x) for x in allowlist)

    # Check if the task has a trusted extension
    executable = any(task.endswith(ext) for ext in extensions)

    if executable:
        exe = task.split(" ")[0]  # Extract the main executable
        p = os.path.expandvars(exe).lower()
        # Check if the executable is in a safe directory
        if p.startswith(r"c:\\windows\\system32") or p.startswith(r"c:\\windows\\syswow64"):
            return True
        else:
            return trusted
    else:
        return trusted

# Get the list of scheduled tasks
output = subprocess.check_output("schtasks /query /v /fo csv /nh", shell=True, text=True)
results = [line.split('","') for line in output.splitlines()]

# Process the results
for res in results:
    if len(res) > 8:
        name = res[1].strip('"')
        creator = res[7].strip('"')
        task = res[8].strip('"')
        if not CheckValidTask(creator, task):
            print(f"{name}, {creator}, {task}")
