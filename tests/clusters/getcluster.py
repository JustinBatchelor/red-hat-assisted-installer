import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

import redhat_assisted_installer.assistedinstaller as assistedinstaller

installer = assistedinstaller.assistedinstaller()

clusters = installer.getClusters()

for cluster in clusters:
    installer.getClusters( with_hosts=True, owner="tessa")