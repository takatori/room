Room
===
リアルタイムマイニングシステム
宅内に配置されたセンサや家電の状態をリアルタイムに解析して家電操作のレコメンドを行う

- Contents
  - [Features](#features)
  - [Architecture](#architecture)
  - [Modules](#modules)
  - [Requirement](#requirement)
  - [Install](#install)
  - [Setting](#setings)
  - [Usage](#usage)

  
## Features
- リアルタイムストリーム処理
- モジュールを細かく分割することにより様々なデータフォーマット・マイニングアルゴリズムを柔軟に追加できる
- pub/subアーキテクチャにより自由にモジュールを構成できる
- pythonで簡単な記述を行うだけでマイニングを実行できる
- supervisorによりシステムを動かしながらモジュールの追加や更新を行うことができる
  - 後からパーサーやマイニング手法の追加をシステムを止めずに実行できる

## Architecture
![architecture](img/room-architecture.jpeg)

## Modules
### router
- httpサーバ
- ルーティングを行う
  - /dataにデータをpostすると対応するparserに渡す

#### Input data format

```json
{
    "data-type": "sensor",
    "data": {
        temperature: ...
    }
}
```

- postデータ
  - data-type: parserの選択、unique制約(他のデータソースと名前がかぶらないようにする必要がある)
  - data: データ本体、以下のフォーマットの**jsonデータ**


### parser
- routerから受け取ったjsonデータを以下のフォーマットに変換してbufferに渡す
- フォーマットがバラバラなのでデータソース毎にparserを用意する必要がある
    - pythonで簡単に実装できる

#### Output data format

```json
{
    "key": "value"
}
```

- key: マイニングを行う際の変数名(列名)になる
- value: 文字か数値のみ、入れ子構造にはできない

例

```json
{
    "sparkcore-core00-temperature": 22
}
```


### buffer
- センサと家電の状態を保持し一定時間毎にoutput

- parserからデータを受け取る
  - sensor(説明変数)とappliance(目的変数)の二つの口がある
- parserで処理されたデータを保持するディクショナリを持つ
- 一定時間毎にディクショナリのすべてのアイテムをjsonにダンプしてcoreモジュールとdatabaseモジュールに渡す

#### Output data format

```json
{
    "timestamp": "2015-11-11 17:33:02.958697+09:00",
    "sensor": {
        "sparkcore-core00-temperature": 22,
        "sparkcore-core00-humidity": 40.0,
        ...
    },
    "appliance": {
        "viera": 0,
        "tv": 1,
        "fan": 1
    }

}

```

### core
- マイニングを行うモジュール
- bufferから渡されたjsonデータおよびdatabaseのデータを駆使してマイニングを行う

#### Output data format

```json
{
    "appliance": "viera",
    "method": "on"
}

```

### database
- bufferから吐き出されたデータをDBに保存する


### output
- マイニング結果を現実世界にフィードバックする
- mikuに結果を喋らせたり家電を操作する



## Requirement
- Python 3.4

## Install
- Pythonインストール
- pipインストール
- packageインストール
- git clone

## Setting
- supervisor.conf
- config.ini


## Usage
- 実行

```bash
./run.sh
```

