## 概要

機械学習の自習用リポジトリ
<br>
テーマを競馬予想としてロジスティック回帰を行う

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

DataFrame を pickle で保存（素振りなので移植性や再利用性は特に気にしない）

```bash
python scripts/netkeiba/create_race_result_data_frame.py
```

### 予想の実施

`jupyter lab` を起動しておく

```bash
jupyter lab
```

[http://localhost:8888/](http://localhost:8888/) へアクセスし、以下のNoteBookを実行する

[logistic_regression_exam.ipynb](./logistic_regression_exam.ipynb)

## その他

### 参考資料

* [競馬予想で始める機械学習〜完全版〜](https://zenn.dev/dijzpeb/books/848d4d8e47001193f3fb)
* [【競馬予想AI】Pythonで正規表現を使って競馬データを加工する【機械学習】 - YouTube](https://www.youtube.com/watch?v=FPnzEgKBy8w)
