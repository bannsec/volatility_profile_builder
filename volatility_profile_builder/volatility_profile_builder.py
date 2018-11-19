#!/usr/bin/env python3

import logging
from . import Colorer

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger("volatility_profile_builder")

import json
import requests
import docker
import argparse
from prettytable import PrettyTable
import shutil
import subprocess
import sys
import os
import importlib

here = os.path.dirname(os.path.realpath(__file__))

def parse_args():
    parser = argparse.ArgumentParser(description='Helper script to build Volatility Profiles for Linux.')
    parser.add_argument('distribution', choices=['centos'],
                        help='What distribution to build for.')
    args = parser.parse_args()
    return args

def list_available_tags(distro):
    distro = distro.strip("/")
    tags = json.loads(requests.get("https://registry.hub.docker.com/v1/repositories/{}/tags".format(distro)).text)
    return [tag['name'] for tag in tags]

def pre_flight():
    """Some checks to make sure your environment is ready."""

    if sys.version_info[0] <= 2:
        logger.error("Please use python3+.")
        exit(1)

    if shutil.which("docker") == None:
        logger.error("It looks like docker is not installed. Please install it.")
        exit(1)

    try:
        subprocess.check_output(["docker","ps"], stderr=subprocess.PIPE)
    except:
        logger.error("You might need to run this with sudo: sudo -E {0}".format(sys.argv[0]))
        exit(2)
    

def main():
    pre_flight()

    args = parse_args()

    client = docker.from_env()

    #
    # Select release
    #

    tags = list_available_tags(args.distribution)

    print("Select a release to build for:")
    table = PrettyTable(['Index', 'Release'])
    for i, tag in enumerate(tags):
        table.add_row([i, tag])
    print(table)
    tag = input("Which release? ").strip()

    # Normalize for int or string
    if tag not in tags:
        # Assume index
        tag = tags[int(tag,10)]

    #
    # Call builder
    #

    builder = importlib.import_module(".{}".format(args.distribution), "volatility_profile_builder")
    image, container = builder.build_profile(tag)

    # Clean-up
    container.remove()
    client.images.remove(image)
    
    print("Your profile should be under: " + os.path.join(here, "profiles"))


if __name__ == '__main__':
    main()
