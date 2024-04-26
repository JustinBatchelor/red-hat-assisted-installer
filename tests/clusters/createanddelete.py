import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

import redhat_assisted_installer.assistedinstaller as assistedinstaller

installer = assistedinstaller.assistedinstaller()

installer.postCluster(f"ocp-testing", "4.15")

for cluster in installer.getClusters():
    installer.deleteCluster(cluster['id'])