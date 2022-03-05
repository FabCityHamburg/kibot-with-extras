# SPDX-FileCopyrightText: 2022 Fab City Hamburg e.V.
# SPDX-FileCopyrightText: 2022 Robin Vobruba <hoijui.quaero@gmail.com>
#
# SPDX-License-Identifier: MIT

FROM rust:latest AS rusttools

WORKDIR /apps

RUN cd /apps && \
  git config --global user.email "buildbot@fabcity.hamburg" && \
  git config --global user.name "the fab city hamburg build bot" && \
  git config --global advice.detachedHead false && \
  git clone --branch=0.9.0 https://github.com/hoijui/projvar.git && \
  git clone https://github.com/hoijui/kicad-text-injector.git

# build projvar
RUN cd /apps/projvar && \
  cargo build --release

# build text injector
RUN cd /apps/kicad-text-injector && \
  cargo build --release

# begin from final base image with kibot etc
FROM setsoft/kicad_auto:10.4-5.1.9

ENV TOOL_PROJVAR /usr/local/bin/projvar
COPY --from=rusttools \
  /apps/projvar/target/release/projvar \
  "$TOOL_PROJVAR"
ENV TOOL_TXT_INJ /usr/local/bin/kicad-text-injector
COPY --from=rusttools \
  /apps/kicad-text-injector/target/release/kicad-text-injector \
  "$TOOL_TXT_INJ"

# update debian
RUN apt-get update && apt-get -y upgrade && apt-get install -y build-essential wget git python3-pip libffi-dev qrencode fonts-liberation2
# install image-injector
RUN mkdir -p /usr/src/ && cd /usr/src && \
  git clone "https://github.com/hoijui/kicad-image-injector.git" && \
  cd kicad-image-injector && \
  git checkout latest_compat_pcbnew_5 \
  pip3 install -r ./requirements.txt
ENV TOOL_IMG_INJ /usr/src/kicad-image-injector/placeholder2image.py

# HACK For "shell not found" error when starting the resulting image.
#      See details here:
#      <https://gitlab.com/gitlab-org/gitlab-runner/-/issues/27614#note_517446691>
#ENTRYPOINT ["/bin/bash", "-c", "ln -snf /bin/bash /bin/sh && /bin/bash -c $0" ]

LABEL maintainer="Robin Vobruba <hoijui.quaero@gmail.com>"
LABEL description="A CI base image for generating output for a KiCad based project - \
https://github.com/FabCityHamburg/kibot-with-extras"
