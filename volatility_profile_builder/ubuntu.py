#!/usr/bin/env python3

import logging
logger = logging.getLogger("volatility_profile_builder:Ubuntu")

import docker
import os
import tempfile
import shutil
import tarfile
import io

from .helpers import grab_profiles

from natsort import natsorted

here = os.path.dirname(os.path.realpath(__file__))

def prompt_for_kernel(tag, tmpdirname):
    print("Enumerating default kernels in the repo ... ", end='', flush=True)
    client = docker.from_env()

    base_image = 'ubuntu:' + tag
    client.images.pull(base_image)

    out = client.containers.run(base_image, '/bin/bash -c "apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y apt-file && apt-file update && echo AAAABBBBCCCCDDDD && apt-file search -x /boot/vmlinuz*"', remove=True)
    out = out.decode()

    kernels = out.split("AAAABBBBCCCCDDDD")[1].strip().split("\n")
    kernels = [x.split(":")[0] for x in kernels if "unsigned" not in x.split(":")[0]]
    kernels = ['-'.join(x.split("-")[2:]) for x in kernels]
    kernels = natsorted(kernels)

    print("OK")
    
    for kernel in kernels:
        print(" - " + kernel)

    while True:
        kernel = input("Select a kernel to build: ").strip()
        
        if kernel not in kernels:
            logger.error("Invalid selection. Example valid selection is: " + kernels[0])
        else:
            map_file = "linux-image-" + kernel
            kernel_version = kernel
            headers = "linux-headers-" + kernel_version
            return headers, map_file, kernel_version

def build_profile(tag):

    client = docker.from_env()
    img_tag = "volatility_profile_builder:ubuntu-{}".format(tag)

    # Create Dockerfile
    with open(os.path.join(here,"docker","Dockerfile_ubuntu"), "r") as f:
        dockerfile = f.read()

    dockerfile = dockerfile.replace("TAG", tag)

    with tempfile.TemporaryDirectory() as tmpdirname:

        headers, map_file, kernel_version = prompt_for_kernel(tag, tmpdirname)
        dockerfile = dockerfile.replace("INSERT_KERNEL_MAP_HERE", map_file)
        dockerfile = dockerfile.replace("INSERT_KERNEL_VERSION_HERE", kernel_version)
        dockerfile = dockerfile.replace("INSERT_KERNEL_HEADERS_HERE", headers)

        # Write the updated Dockerfile to the tmp dir
        dockerfile_name = os.path.join(tmpdirname, "Dockerfile")
        with open(dockerfile_name, "w") as f:
            f.write(dockerfile)

        print("Building image for ubuntu:" + tag + ": " + kernel_version + " ... ", end='', flush=True)
        client.images.build(path=tmpdirname, tag=img_tag, pull=True, rm=True, forcerm=True)
        print("[ DONE ]")

        print("Copying profile out ... ", end='', flush=True)
        c = client.containers.run(image=img_tag, command='/bin/bash', detach=True)

        grab_profiles(c)
        print("[ DONE ]")


    # Return the image name and the container name
    return img_tag, c


