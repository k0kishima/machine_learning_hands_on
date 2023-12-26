## 概要

機械学習の自習用リポジトリ
<br>
テーマを競馬予想としてロジスティック回帰を行う

## 動作環境

- Python 3.10

## セットアップ

### Rye をインストール

- https://rye-up.com/guide/installation/

※ 他のツールを使いたい場合はそれで代用も可能

### リポジトリを clone

```bash
git clone git@github.com:k0kishima/machine_learning_hands_on.git
```

### パッケージインストール

```bash
rye sync
```

## 運用

### データの入手

引数は対象の年

```bash
python scripts/netkeiba/download_race_pages.py 2019
```

結構時間かかるので注意

```
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 8400/8400 [2:50:47<00:00,  1.22s/it]
```

### スクレイピング

DataFrame を pickle で保存（素振りなので移植性や再利用性は特に気にしない）

```bash
python scripts/netkeiba/create_race_result_data_frame.py
```

### 予想の実施

`jupyter lab` を起動しておく

```bash
python -m jupyter lab
```

[http://localhost:8888/](http://localhost:8888/) へアクセスし、以下の NoteBook を実行する

[logistic_regression_exam.ipynb](./logistic_regression_exam.ipynb)

## その他

### 参考資料

- [競馬予想で始める機械学習〜完全版〜](https://zenn.dev/dijzpeb/books/848d4d8e47001193f3fb)
- [【競馬予想 AI】Python で正規表現を使って競馬データを加工する【機械学習】 - YouTube](https://www.youtube.com/watch?v=FPnzEgKBy8w)
