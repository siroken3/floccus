# floccus

AWS の CloudFormation が VPC (Virutal Private Cloud) に対応していないので代替として動作するツールです。VPCIDを指定すると標準出力にCloudFormationのJSONファイルを出力します。

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

本体の入手
    $ export FLOCCUS_HOME=インストール先DIRECTORY
    $ git clone https://github.com/siroken3/floccus.git ${FLOCCUS_HOME}

${FLOCCUS_HOME} 以下に bin/ と lib/ ができますので binに$PATHを通してください。

## 使い方

環境変数 AWS_ACCESS_KEY, AWS_SECRET_KEY へEC2でDescribeできる権限のアクセスキー、シークレットキーを設定して実行します。
    $ export AWS_ACCESS_KEY=アクセスキー
    $ export AWS_SECRET_KEY=シークレットキー
    $ flcs VPCID
    {
        "AWSTemplateFormatVersion": "2010-09-09",
        
        "Description": "This is auto generated cloudformation file.",
        
        "Resources": {
        (略)


## TODO
* 一部のResourceにしか対応していないので拡充
* Tagへの対応
* cloudformerのようなWebアプリケーション化

## LICENCE
MITライセンスです。ライセンス条文はLICENSEファイルをご覧ください。
