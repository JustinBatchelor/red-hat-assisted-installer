import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/tests/"))

from utils import *

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))
from redhat_assisted_installer import assisted_installer
from redhat_assisted_installer.lib.schema.infra_env import *

import pprint


try:
    infra = InfraEnv(
        name="networked-infra-env",
        image_type="minimal-iso",
        proxy=Proxy(
            http_proxy="http://proxy.example.com:8080",
            https_proxy="http://proxy.example.com:8443",
            no_proxy="localhost,127.0.0.1,.example.com",
        ),
        static_network_config=[StaticNetworkConfig(
            mac_interface_map=[MacInterfaceMap(
                logical_nic_name="eth0",
                mac_address="00:1A:2B:3C:4D:5E",
            )],
            network_yaml='interfaces:\\n  - name: eth0\\n    type: ethernet\\n    state: up\\n    mac-address: 00:1A:2B:3C:4D:5E\\n    ipv4:\\n      enabled: true\\n      address:\\n        - ip: 192.168.1.100\\n          prefix-length: 24\\n      gateway: 192.168.1.1\\n      dns:\\n        - 8.8.8.8\\n        - 8.8.4.4\\n',
        )],
    )
    create_api_response = assisted_installer.post_infrastructure_environment(infra_env=infra)
    create_api_response.raise_for_status()
    pprint.pprint(create_api_response.json(), compact=True)

    if assisted_installer.delete_infrastructure_environment(infra_env_id=create_api_response.json()['id']):
        print(f"Successfully delete infra_env: {create_api_response.json()['id']}")
        infra_envs = assisted_installer.get_infrastructure_environements()
        pprint.pprint(infra_envs.json(), compact=True)
        print(len([infra_envs.json()]))
    else:
        print(create_api_response.json())
        print(f"Failed to delete infra_env: {create_api_response.json()['id']}")

except Exception as e:
    print(f"Failed to create infra_env: {create_api_response.json()}")
