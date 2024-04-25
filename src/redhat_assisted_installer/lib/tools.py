import tempfile
import requests
import re

def validateName(name):
    # Regular expression pattern to match the name criteria
    pattern = r'^[a-z0-9]([-a-z0-9]*[a-z0-9])?$'
    # return Matching the name with the pattern
    return re.match(pattern, name)

def validateVersion(version):
    # Regular expression pattern to match the version criteria
    pattern = r'^[0-9]+\.[0-9]+$'
    # return Matching the name with the pattern
    return re.match(pattern, version)

def validateCPUArchitecture(self, cpu):
    validArchitecture = ['x86_64', 'aarch64', 'arm64', 'ppc64le', 's390x']
    return cpu in validArchitecture