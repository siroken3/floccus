# floccus

AWS の CloudFormation が VPC (Virutal Private Cloud) に対応していないので代替として動作するツールです。VPCIDを指定すると標準出力にCloudFormationのJSONファイルを出力します。

## 動作環境
Linux/MacOS 10以降で動作します。また必要なライブラリは以下のとおりです。

* python>=2.6
* boto==2.6.0
* Jinja2==2.6
* argparse>=1.2.1 (python 2.7以降は不要です)

## インストール

まず必要なライブラリをインストールするためのdistribute(easy_install) と pipをインストールします。distributeでもインストール可能なはずですが pip を気に入っているのでここではpipによる方法で説明します。

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

${FLOCCUS_HOME} 以下に bin/ と lib/ ができますので ${FLOCCUS_HOME}/bin に$PATHを通してください。なおFLOCCUS_HOME環境変数は説明のために入れていますので必須ではありません。

## 使い方

環境変数 AWS_ACCESS_KEY, AWS_SECRET_KEY へEC2でDescribeできる権限のアクセスキー、シークレットキーを設定してCloudFormationのJSONを出力したいVPCのIDを指定します。

    $ export AWS_ACCESS_KEY=アクセスキー
    $ export AWS_SECRET_KEY=シークレットキー
    $ flcs VPCID
    {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "This is auto generated cloudformation file.",
        "Resources": {
        (略)

アクセスキー、シークレットキーは引数で指定することもできます。

    $ flcs --aws-access-key アクセスキー --aws-secret-key シークレットキー VPCID

対象のVPCが us-east-1 以外のリージョンに存在する場合は --region 引数で指定する必要があります。

    $ flcs --region 'ap-northeast-1' VPCID

--help で簡単なヘルプを見ることができます。

    bin/flcs --help
    usage: flcs [-h] [-O AWS_ACCESS_KEY] [-W AWS_SECRET_KEY] [--region REGION]
                vpcid
    
    positional arguments:
      vpcid
    
    optional arguments:
      -h, --help            show this help message and exit
      -O AWS_ACCESS_KEY, --aws-access-key AWS_ACCESS_KEY
      -W AWS_SECRET_KEY, --aws-secret-key AWS_SECRET_KEY
      --region REGION

## TODO
* 一部のResourceにしか対応していないので拡充
* Tagへの対応
* cloudformerのようなWebアプリケーション化

## LICENCE
MITライセンスです。ライセンス条文はLICENSEファイルをご覧ください。
