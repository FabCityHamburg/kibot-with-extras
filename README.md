# Kibot with extras

This docker image extends [kibot_auto](https://github.com/INTI-CMNB/kicad_auto) with the following tools:

* [projvar](https://github.com/hoijui/projvar) - A tool that tries to ensure a certain small set of project related environment variables are set. 
* [kicad-text-injector](https://github.com/hoijui/kicad-text-injector) - A CLI tool that allows you to post-process your KiCad PCB files, by replacing variables of the type `${NAME}` in your text elements. 
* [kicad-image-injector](https://github.com/hoijui/kicad-image-injector) - A stand-alone (python) tool to replace rectangular template areas drawn onto a KiCad PCB with B&W images or QR-Codes. 

The aim is to make all of these more easily accessable and build workflows, like pre-commit hooks or CI jobs with them.

# Building this image

**TODO**: publish on docker hub

```
git clone https://gitlab.fabcity.hamburg/software/wp4-os-tools/task-3-osh-project-tools/kibot-with-extras
docker build -t kibotwithextras:test .
```

# Testing

there is a test pytest based test script that ensure all the tools are available inside the image. It depends on `docker` and `pytest` from pip.

Once you have these, simply run `pytest` in this repo to run the tests.

# Example

The `oseg` fork of the [for-science](https://github.com/hoijui/for-science-keyboard/tree/oseg) split keyboard shows what this enables.

```bash

# clone the example project
git clone --branch=oseg https://github.com/hoijui/for-science-keyboard

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
  kibotwithextras:test /bin/bash -c "cd workdir; ./ci-run"
```

