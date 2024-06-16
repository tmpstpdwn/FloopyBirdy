### IMPORTS ###
import importlib

### Check if pygame is installed ###
try:
    importlib.import_module('pygame')
    print("pygame is already installed.")
except ImportError:
    print("pygame is not installed. Installing...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'pygame'])
    print("pygame has been successfully installed.")

### Import FloopyBirdy after pygame installation ###
from floopybirdy import FloopyBirdy

### MAIN ###
if __name__ == "__main__":
    floopyInstance = FloopyBirdy()
    floopyInstance.run()

### END ###
