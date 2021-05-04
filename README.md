## 概要

機械学習の自習用リポジトリ
<br>
テーマを競馬予想として代表的な教師あり学習である分類と回帰を試す

## セットアップ

### リポジトリを clone

```bash
git clone git@github.com:k0kishima/machine_learning_hands_on.git
```

### 仮想環境構築

```bash
cd /path/to/project
python3 -m venv venv
```

### パッケージインストール

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## 運用

- 事前に `venv` を有効化しておくこと
- パスを通しておくこと

```bash
source venv/bin/activate
export PYTHONPATH=".:$PYTHONPATH"
```

### データの入手

引数は対象の年

```bash
python scripts/netkeiba/download_race_pages.py 2019
```

DataFrame を pickle で保存（目的は分類と回帰を各々試すことなので移植性や再利用性は特に気にしない）

```bash
python scripts/netkeiba/create_race_result_data_frame.py
```
