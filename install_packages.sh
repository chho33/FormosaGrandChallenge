pipenv install
pipenv install https://download.pytorch.org/whl/cu100/torch-1.1.0-cp36-cp36m-linux_x86_64.whl
pipenv install https://download.pytorch.org/whl/cu100/torchvision-0.3.0-cp36-cp36m-linux_x86_64.whl
pipenv install -e git+https://github.com/huggingface/pytorch-transformers.git@47a7d4ec14#egg=pytorch-transformers
