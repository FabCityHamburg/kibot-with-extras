import sys
import pytest
import docker

IMAGE="kibotpp:test"
client = docker.from_env()

def test_has_image():
    out = run_image("echo hello world")
    assert out == b"hello world\n"

def test_has_projvar():
    want = b"projvar 0.8.0"
    out = run_image("projvar -V")
    assert out.startswith(want)

def test_has_txtinjector():
    want = b"kicad-text-injector 0.2.4"
    out = run_image("kicad-text-injector -V")
    assert out.startswith(want)

def test_has_img_injector():
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


def run_image(cmd):
    return client.containers.run(IMAGE, cmd, remove=True, detach=False)
