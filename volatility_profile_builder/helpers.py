#!/usr/bin/env python3

import io
import tarfile

def grab_profiles(container):
    b = io.BytesIO(b''.join(container.get_archive("/profiles/", chunk_size=None)[0]))
    tar = tarfile.open(fileobj=b)
    tar.extractall(".")

