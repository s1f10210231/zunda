#!/usr/bin/env bash
# exit on error
set -o errexit

wget https://github.com/VOICEVOX/voicevox_core/releases/download/0.14.3/voicevox_core-0.14.3+cpu-cp38-abi3-linux_x86_64.whl
wget https://github.com/microsoft/onnxruntime/releases/download/v1.13.1/onnxruntime-linux-x64-1.13.1.tgz
tar xvzf onnxruntime-linux-x64-1.13.1.tgz
mv onnxruntime-linux-x64-1.13.1/lib/libonnxruntime.so.1.13.1 ./
wget http://downloads.sourceforge.net/open-jtalk/open_jtalk_dic_utf_8-1.11.tar.gz
tar xvzf open_jtalk_dic_utf_8-1.11.tar.gz

pip3 install -r requestment.txt

python3 manage.py collectstatic --no-input
python3 manage.py migrate
python3 manage.py newsuperuser