# SPDX-FileCopyrightText: 2022 Fab City Hamburg e.V.
#
# SPDX-License-Identifier: MIT

import os
import pytest
import docker

# check if we have CI variables or fall back to defaults
IMAGE_NAME="fabcityhamburg/kibotwithextras"
IMAGE_NAME = os.environ.get("IMAGE_NAME", IMAGE_NAME)
IMAGE_VERSION = os.environ.get("CI_COMMIT_SHORT_SHA", "test")

IMAGE = IMAGE_NAME + ':' + IMAGE_VERSION

# start docker client connection
client = docker.from_env()

@pytest.mark.parametrize(
        "tool,version",
        [
            ("echo hello world", b"hello world\n"), # has image
            ("projvar -V", b"projvar 0.9.0\n"),
            ("kicad-text-injector -V", b"kicad-text-injector 0.2.4\n"),
            ("kibot -V", b"KiBot 0.11.0 - Copyright 2018-2021, Salvador E. Tropea/INTI/John Beard - License: GPL v3+\n"),
            ("pcbdraw --version", b"PcbDraw 0.6.0\n"),
        ])
def test_has_tools(tool, version):
    out = run_image(tool)
    assert out == version

def test_image_injector():
    want =b"""11111111111111111111111111111111
1                              1
1                              1
1                              1
1                              1
1                              1
1    111111         111111     1
1   11    11       11    11    1
1  111     11     111     11   1
1 111      111   111      111  1
1 111       11   111       11  1
1 11        11   11        11  1
1 111       111  111       111 1
1 111       111  111       111 1
1 111       111  111       111 1
1  11       111   11       111 1
1   1111 111111    1111 111111 1
1    11111  11      11111  11  1
1           111            111 1
1           11             11  1
1          111            111  1
1          111            111  1
1  1       11     1       11   1
1  1      111     1      111   1
1  11   111       11   111     1
1  111111         111111       1
1                              1
1                              1
11111111111111111111111111111111
"""
    out = run_image("python3 /usr/src/kicad-image-injector/string_pixels_source.py")
    assert out == want


# utils
def run_image(cmd):
    return client.containers.run(IMAGE, cmd, remove=True, detach=False)
