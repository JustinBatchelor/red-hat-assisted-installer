

class infraEnvCreateParams:
    def __init__(self, name, pullsecret, cpuarchitecture="x86_64", version=None, clusterid=None):
        self.params = {}
        self.params['name'] = name + "-infra-env"
        self.params['pull_secret'] = pullsecret
        self.params['cpu_architecture'] = cpuarchitecture
        if version is not None:
            self.params['openshift_version'] = version
        if clusterid is not None:
            self.params['cluster_id'] = clusterid

    def getParams(self):
        return self.params
    
    

class clusterCreateParams:
    def __init__(self, name, pullsecret, version, basedomain, hamode="None", cpuarchitecture='x86_64'):
        self.params = {}
        self.params['name'] = name
        self.params['pull_secret'] = pullsecret
        self.params['openshift_version'] = version
        self.params['high_availability_mode'] = hamode
        self.params['base_dns_domain'] = basedomain
        self.params['cpu_architecture'] = cpuarchitecture

    def getParams(self):
        return self.params