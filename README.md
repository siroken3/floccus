# floccus

## 動作環境
Linux/MacOS 10以降で動作します。また必要なライブラリは以下のとおりです。

python>=2.6
boto==2.6.0
Jinja2==2.6
argparse>=1.2.1 (python 2.7以降は不要です)

## インストール

必要なライブラリをインストールするためのdistributeとpipのインストールします。

    $ curl -O http://python-distribute.org/distribute_setup.py
    $ python distribute_setup.py
    $ easy_install pip

必要なライブラリのインストール

    $ pip install boto
    $ pip install jinja2
    $ pip install argparse # python 2.7以降の場合は不要


## LICENCE
Please see LICENSE file
