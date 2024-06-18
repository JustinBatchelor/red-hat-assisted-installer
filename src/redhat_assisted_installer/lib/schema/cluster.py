import os

from ..utils import *
"""
{
  "additional_ntp_source": {
    "type": "string",
    "description": "A comma-separated list of NTP sources (name or IP) going to be added to all the hosts."
  },
  "api_vips": [
    {
      "description": "The virtual IPs used to reach the OpenShift cluster's API. Enter one IP address for single-stack clusters, or up to two for dual-stack clusters (at most one IP address per IP stack used). The order of stacks should be the same as order of subnets in Cluster Networks, Service Networks, and Machine Networks.",
      "api_vip": {
        "description": "The virtual IP used to reach the OpenShift cluster's API.",
        "cluster_id": {
          "type": "string",
          "format": "uuid",
          "description": "The cluster that this VIP is associated with."
        },
        "ip": {
          "type": "string",
          "pattern": "^(?:(?:(?:[0-9]{1,3}\\.){3}[0-9]{1,3})|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,}))?$"
        },
        "verification": {
          "type": "string",
          "default": "unverified",
          "description": "VIP verification result.",
          "enum": ["unverified", "failed", "succeeded"]
        }
      }
    }
  ],
  "base_dns_domain": {
    "type": "string",
    "description": "Base domain of the cluster. All DNS records must be sub-domains of this base and include the cluster name."
  },
  "cluster_network_cidr": {
    "type": "string",
    "default": "10.128.0.0/14",
    "pattern": "^(?:(?:(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\/((?:[0-9])|(?:[1-2][0-9])|(?:3[0-2])))|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,})\\/((?:[0-9])|(?:[1-9][0-9])|(?:1[0-1][0-9])|(?:12[0-8])))$",
    "description": "IP address block from which Pod IPs are allocated. This block must not overlap with existing physical networks. These IP addresses are used for the Pod network, and if you need to access the Pods from an external network, configure load balancers and routers to manage the traffic."
  },
  "cluster_network_host_prefix": {
    "type": "integer",
    "default": 23,
    "maximum": 128,
    "minimum": 1,
    "description": "The subnet prefix length to assign to each individual node. For example, if clusterNetworkHostPrefix is set to 23, then each node is assigned a /23 subnet out of the given CIDR (clusterNetworkCIDR), which allows for 510 (2^(32 - 23) - 2) pod IP addresses. If you are required to provide access to nodes from an external network, configure load balancers and routers to manage the traffic."
  },
  "cluster_networks": [
    {
      "x-nullable": true,
      "description": "Cluster networks that are associated with this cluster.",
      "cluster_network": {
        "description": "A network from which Pod IPs are allocated. This block must not overlap with existing physical networks. These IP addresses are used for the Pod network, and if you need to access the Pods from an external network, configure load balancers and routers to manage the traffic.",
        "cidr": {
          "type": "string",
          "pattern": "^(?:(?:(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\/((?:[0-9])|(?:[1-2][0-9])|(?:3[0-2])))|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,})\\/((?:[0-9])|(?:[1-9][0-9])|(?:1[0-1][0-9])|(?:12[0-8])))$"
        },
        "cluster_id": {
          "type": "string",
          "format": "uuid",
          "description": "The cluster that this network is associated with."
        },
        "host_prefix": {
          "type": "integer",
          "maximum": 128,
          "minimum": 1,
          "description": "The subnet prefix length to assign to each individual node. For example, if is set to 23, then each node is assigned a /23 subnet out of the given CIDR, which allows for 510 (2^(32 - 23) - 2) pod IP addresses."
        }
      }
    }
  ],
  "cpu_architecture": {
    "type": "string",
    "default": "x86_64",
    "description": "The CPU architecture of the image (x86_64/arm64/etc).",
    "enum": ["x86_64", "aarch64", "arm64", "ppc64le", "s390x", "multi"]
  },
  "disk_encryption": {
    "type": "object",
    "properties": {
      "enable_on": {
        "type": "string",
        "default": "none",
        "description": "Enable/disable disk encryption on master nodes, worker nodes, or all nodes.",
        "enum": ["none", "all", "masters", "workers"]
      },
      "mode": {
        "type": "string",
        "default": "tpmv2",
        "description": "The disk encryption mode to use.",
        "enum": ["tpmv2", "tang"]
      },
      "tang_servers": {
        "type": "string",
        "example": "[{\"url\":\"http://tang.example.com:7500\",\"thumbprint\":\"PLjNyRdGw03zlRoGjQYMahSZGu9\"}, {\"url\":\"http://tang.example.com:7501\",\"thumbprint\":\"PLjNyRdGw03zlRoGjQYMahSZGu8\"}]",
        "description": "JSON-formatted string containing additional information regarding tang's configuration"
      }
    }
  },
  "high_availability_mode": {
    "type": "string",
    "default": "Full",
    "description": "Guaranteed availability of the installed cluster. 'Full' installs a Highly-Available cluster over multiple master nodes whereas 'None' installs a full cluster over one node.",
    "enum": ["Full", "None"]
  },
  "http_proxy": {
    "type": "string",
    "description": "A proxy URL to use for creating HTTP connections outside the cluster. http://<username>:<pswd>@<ip>:<port>"
  },
  "https_proxy": {
    "type": "string",
    "description": "A proxy URL to use for creating HTTPS connections outside the cluster. http://<username>:<pswd>@<ip>:<port>"
  },
  "hyperthreading": {
    "type": "string",
    "default": "all",
    "description": "Enable/disable hyperthreading on master nodes, worker nodes, or all nodes.",
    "enum": ["masters", "workers", "none", "all"]
  },
  "ignition_endpoint": {
    "type": "object",
    "properties": {
      "description": {
        "type": "string",
        "description": "Explicit ignition endpoint overrides the default ignition endpoint."
      },
      "ca_certificate": {
        "type": "string",
        "description": "Base64 encoded CA certificate to be used when contacting the URL via https."
      },
      "url": {
        "type": "string",
        "description": "The URL for the ignition endpoint."
      }
    }
  },
  "ingress_vips": [
    {
      "description": "The virtual IPs used for cluster ingress traffic. Enter one IP address for single-stack clusters, or up to two for dual-stack clusters (at most one IP address per IP stack used). The order of stacks should be the same as order of subnets in Cluster Networks, Service Networks, and Machine Networks.",
      "ingress_vip": {
        "description": "The virtual IP used for cluster ingress traffic.",
        "cluster_id": {
          "type": "string",
          "format": "uuid",
          "description": "The cluster that this VIP is associated with."
        },
        "ip": {
          "type": "string",
          "pattern": "^(?:(?:(?:[0-9]{1,3}\\.){3}[0-9]{1,3})|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,}))?$"
        },
        "verification": {
          "type": "string",
          "default": "unverified",
          "description": "VIP verification result.",
          "enum": ["unverified", "failed", "succeeded"]
        }
      }
    }
  ],
  "machine_networks": [
    {
      "x-nullable": true,
      "description": "Machine networks that are associated with this cluster.",
      "machine_network": {
        "description": "A network that all hosts belonging to the cluster should have an interface with IP address in. The VIPs (if exist) belong to this network.",
        "cidr": {
          "type": "string",
          "pattern": "^(?:(?:(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\/((?:[0-9])|(?:[1-2][0-9])|(?:3[0-2])))|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,})\\/((?:[0-9])|(?:[1-9][0-9])|(?:1[0-1][0-9])|(?:12[0-8])))$"
        },
        "cluster_id": {
          "type": "string",
          "format": "uuid",
          "description": "The cluster that this network is associated with."
        }
      }
    }
  ],
  "name": {
    "type": "string",
    "maxLength": 54,
    "minLength": 1,
    "description": "Name of the OpenShift cluster."
  },
  "network_type": {
    "type": "string",
    "description": "The desired network type used.",
    "enum": ["OpenShiftSDN", "OVNKubernetes"]
  },
  "no_proxy": {
    "type": "string",
    "description": "An \"*\" or a comma-separated list of destination domain names, domains, IP addresses, or other network CIDRs to exclude from proxying."
  },
  "ocp_release_image": {
    "type": "string",
    "description": "OpenShift release image URI."
  },
  "olm_operators": [
    {
      "name": {
        "type": "string",
        "description": "List of OLM operators to be installed."
      },
      "properties": {
        "type": "string",
        "description": "Blob of operator-dependent parameters that are required for installation."
      }
    }
  ],
  "openshift_version": {
    "type": "string",
    "description": "Version of the OpenShift cluster."
  },
  "platform": {
    "type": "object",
    "description": "The configuration for the specific platform upon which to perform the installation.",
    "properties": {
      "external": {
        "type": "object",
        "description": "Configuration used when installing with an external platform type.",
        "properties": {
          "cloud_controller_manager": {
            "type": "string",
            "description": "When set to external, this property will enable an external cloud provider.",
            "enum": ["", "External"]
          },
          "platform_name": {
            "type": "string",
            "minLength": 1,
            "description": "Holds the arbitrary string representing the infrastructure provider name."
          }
        }
      },
      "type": {
        "type": "string",
        "enum": ["baremetal", "nutanix", "vsphere", "none", "external"],
        "description": "Type of platform."
      }
    }
  },
  "pull_secret": {
    "type": "string",
    "description": "The pull secret obtained from Red Hat OpenShift Cluster Manager at console.redhat.com/openshift/install/pull-secret."
  },
  "schedulable_masters": {
    "type": "boolean",
    "default": false,
    "description": "Schedule workloads on masters"
  },
  "service_network_cidr": {
    "type": "string",
    "default": "172.30.0.0/16",
    "pattern": "^(?:(?:(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\/((?:[0-9])|(?:[1-2][0-9])|(?:3[0-2])))|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,})\\/((?:[0-9])|(?:[1-9][0-9])|(?:1[0-1][0-9])|(?:12[0-8])))$",
    "description": "The IP address pool to use for service IP addresses. You can enter only one IP address pool. If you need to access the services from an external network, configure load balancers and routers to manage the traffic."
  },
  "service_networks": [
    {
      "x-nullable": true,
      "description": "Service networks that are associated with this cluster.",
      "service_network": {
        "description": "IP address block for service IP blocks.",
        "cidr": {
          "type": "string",
          "pattern": "^(?:(?:(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\/((?:[0-9])|(?:[1-2][0-9])|(?:3[0-2])))|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,})\\/((?:[0-9])|(?:[1-9][0-9])|(?:1[0-1][0-9])|(?:12[0-8])))$"
        },
        "cluster_id": {
          "type": "string",
          "format": "uuid",
          "description": "A network to use for service IP addresses. If you need to access the services from an external network, configure load balancers and routers to manage the traffic."
        }
      }
    }
  ],
  "ssh_public_key": {
    "type": "string",
    "description": "SSH public key for debugging OpenShift nodes."
  },
  "tags": {
    "type": "string",
    "description": "A comma-separated list of tags that are associated to the cluster."
  },
  "user_managed_networking": {
    "type": "boolean",
    "default": false,
    "description": "(DEPRECATED) Indicate if the networking is managed by the user."
  },
  "vip_dhcp_allocation": {
    "type": "boolean",
    "default": false,
    "description": "Indicate if virtual IP DHCP allocation mode is enabled."
  }
}

"""
class ClusterParams:
    def __init__(self, 
                 name: str = None, 
                 openshift_version: str = None,
                 cluster_id: str = None, 
                 pull_secret: str = os.environ.get("REDHAT_PULL_SECRET"),
                 additional_ntp_source: str = None,
                 api_vip: str = None,
                 base_dns_domain: str = None,
                 cluster_network_cidr: str = None,
                 cluster_network_host_prefix: int = None,
                 cpu_architecture: str = None,
                 high_availability_mode: str = None,
                 http_proxy: str = None,
                 https_proxy: str = None,
                 hyperthreading: str = None,
                 ingress_vip: str = None,
                 network_type: str = None,
                 service_network_cidr: str = None,
                 user_managed_networking: bool = None,
                 ssh_authorized_key: str = None,
                 vip_dhcp_allocation: bool = None,
                ):
        self.params = {}

        if name is not None:
            self.params['name'] = name

        if openshift_version is not None and is_valid_openshift_version(openshift_version):
            self.params['openshift_version'] = openshift_version

        if cluster_id is not None:
            self.params['cluster_id'] = cluster_id

        if pull_secret is not None:
            self.params['pull_secret'] = pull_secret

        if additional_ntp_source is not None and is_valid_ip(additional_ntp_source):
            self.params['additional_ntp_source'] = additional_ntp_source

        if api_vip is not None and is_valid_ip(api_vip):
            self.params['api_vip'] = api_vip

        if base_dns_domain is not None and is_valid_base_domain(base_dns_domain):
            self.params['base_dns_domain'] = base_dns_domain

        if cluster_network_cidr is not None and is_valid_cidr(cluster_network_cidr):
            self.params['cluster_network_cidr'] = cluster_network_cidr

        if cluster_network_host_prefix is not None and isinstance(cluster_network_host_prefix, int) and cluster_network_host_prefix > 0 and cluster_network_host_prefix < 128:
            self.params['cluster_network_host_prefix'] = cluster_network_host_prefix

        if cpu_architecture is not None and is_valid_cpu_architecture(cpu_architecture):
            self.params['cpu_architecture'] = cpu_architecture

        if high_availability_mode is not None and is_valid_ha_mode(high_availability_mode):
            self.params['high_availability_mode'] = high_availability_mode

        if http_proxy is not None and is_valid_ip(http_proxy):
            self.params['http_proxy'] = http_proxy

        if https_proxy is not None and is_valid_ip(https_proxy):
            self.params['https_proxy'] = https_proxy

        if hyperthreading is not None and is_valid_hyperthread(hyperthreading):
            self.params['hyperthreading'] = hyperthreading

        if ingress_vip is not None and is_valid_ip(ingress_vip):
            self.params['ingress_vip'] = ingress_vip

        if network_type is not None and is_valid_network_type(network_type):
            self.params['network_type'] = network_type

        if service_network_cidr is not None and is_valid_cidr(service_network_cidr):
            self.params['service_network_cidr'] = service_network_cidr

        if ssh_authorized_key is not None:
            self.params['ssh_authorized_key'] = ssh_authorized_key

        if user_managed_networking is not None:
            self.params['user_managed_networking'] = user_managed_networking

        if vip_dhcp_allocation is not None:
            self.params['vip_dhcp_allocation'] = vip_dhcp_allocation

    def create_params(self):
        return {key: value for key, value in self.params.items() if value is not None}
    


