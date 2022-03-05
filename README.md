<!--
SPDX-FileCopyrightText: 2022 Fab City Hamburg e.V.

SPDX-License-Identifier: CC0-1.0
-->

# Kibot with extras

This docker image extends [`kibot_auto`](https://github.com/INTI-CMNB/kicad_auto)
with the following tools:

* [projvar](https://github.com/hoijui/projvar) -
  A tool that tries to ensure a certain small set
  of project related environment variables are set.
* [kicad-text-injector](https://github.com/hoijui/kicad-text-injector) -
  A CLI tool that allows you to post-process your KiCad PCB files,
  by replacing variables of the type `${NAME}` in your text elements.
* [kicad-image-injector](https://github.com/hoijui/kicad-image-injector) -
  A stand-alone (python) tool to replace rectangular template areas
  drawn onto a KiCad PCB with B&W images or QR-Codes.

The aim is to make all of these more easily accessable and build workflows,
like pre-commit hooks or CI jobs with them.

## Using this image

It is published to docker hub as `fabcityhamburg/kibotwithextras`.
The current version is `beta1`.

## Building this image

```
git clone https://gitlab.fabcity.hamburg/software/wp4-os-tools/task-3-osh-project-tools/kibot-with-extras
docker build -t kibotwithextras:test .
```

## Testing

There is a pytest based test script
that ensure all the tools are available inside the image.
It depends on `docker` and `pytest` from pip.

Once you have these,
simply run `pytest` in this repo to run the tests.

# Local Usage Example

The `testing` fork of the [for-science](https://github.com/hoijui/for-science-keyboard/tree/testing)
split keyboard shows an example of how this can be used:

With a few options,
the docker image can be used on a folder in your filesystem.
The important things are the volume maps to keep the user IDs intact.

```bash
# clone the example project
git clone --branch=testing https://github.com/hoijui/for-science-keyboard

# enable docker to run the image with access to the project as the current user
export USER_ID=$(id -u)
export GROUP_ID=$(id -g)

export proj=for-science-keyboard

# start the image and run the ci-run script from the project
docker run --rm -it \
  -v $(pwd)/$proj:/home/$USER/workdir \
  --user $USER_ID:$GROUP_ID \
  --workdir="/home/$USER" \
  --volume="/etc/group:/etc/group:ro" \
  --volume="/etc/passwd:/etc/passwd:ro" \
  --volume="/etc/shadow:/etc/shadow:ro" \
  fabcityhamburg/kibotwithextras:beta1 /bin/bash -c "cd workdir; ./ci-run"
```
