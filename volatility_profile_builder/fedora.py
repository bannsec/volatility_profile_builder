#!/usr/bin/env python3

import logging
logger = logging.getLogger("volatility_profile_builder:Fedora")

import docker
import os
import tempfile
import shutil
import tarfile
import io

from .helpers import grab_profiles

here = os.path.dirname(os.path.realpath(__file__))

def build_profile(tag):

    client = docker.from_env()
    img_tag = "volatility_profile_builder:fedora-{}".format(tag)

    # Create Dockerfile
    with open(os.path.join(here,"docker","Dockerfile_fedora"), "r") as f:
        dockerfile = f.read()

    dockerfile = dockerfile.replace("TAG", tag)

    with tempfile.TemporaryDirectory() as tmpdirname:

        # Write the updated Dockerfile to the tmp dir
        dockerfile_name = os.path.join(tmpdirname, "Dockerfile")
        with open(dockerfile_name, "w") as f:
            f.write(dockerfile)

        # Copy libdwarf over
        #shutil.copy(os.path.join(here, "libdwarf-20180809.tar.gz"), tmpdirname)
        
        print("Building image for fedora:" + tag + " ... ", end='', flush=True)
        client.images.build(path=tmpdirname, tag=img_tag, pull=True, rm=True, forcerm=True)
        print("[ DONE ]")

        print("Copying profile out ... ", end='', flush=True)
        c = client.containers.run(image=img_tag, command='/bin/bash', detach=True)

        grab_profiles(c)
        print("[ DONE ]")


    # Return the image name and the container name
    return img_tag, c


