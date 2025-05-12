FROM sulfurheron/nvidia-cuda:10.0-cudnn7-devel-ubuntu16.04-2019-07-29
# FROM pytorch/pytorch:1.2-cuda10.0-cudnn7-devel

#Set of all dependencies needed for pyenv to work on Ubuntu
RUN apt-get update \ 
        && apt-get install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget ca-certificates curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev mecab-ipadic-utf8 git

# # Set-up necessary Env vars for PyEnv
ENV PYTHON_VERSION=3.6.9
ENV PYENV_ROOT=/root/.pyenv
ENV PATH=$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
# # ENV TF_FORCE_GPU_ALLOW_GROWTH=true
# # ENV CUDA_VISIBLE_DEVICES=1

# Install pyenv
RUN set -ex \
    && curl https://pyenv.run | bash \
    && pyenv update \
    && pyenv install $PYTHON_VERSION \
    && pyenv global $PYTHON_VERSION \
    && pyenv rehash

RUN git clone https://github.com/TIoJIuHa/pytorch-superpoint.git /app

WORKDIR /app

RUN pip install --trusted-host pypi.python.org pytest-xdist
RUN pip install --trusted-host pypi.python.org --upgrade pip

RUN pip install -r requirements.txt
RUN pip install -r requirements_torch.txt

RUN pip3 install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

RUN echo "DATA_PATH = './datasets'" >> ./settings.py
RUN echo "EXPER_PATH = './experiment'" >> ./settings.py


RUN python -V