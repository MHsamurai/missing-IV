# 欠測IV 研究プロジェクト

欠測IVに関する論文執筆・論文読解のための作業ディレクトリです。

主に以下を参照します。

- `manuscript/`: 論文本文
- `notes/`: 読解・検討メモ
- `resources/`: 文献・発表資料・旧版などの補助資料
- `docs/`: プロジェクトの前提と作業方針

## 現在の主要メモ

- `manuscript/main.tex`
- `manuscript/vector_missing_iv_identification_proof.tex`
- `manuscript/vector_missing_iv_identification_beamer.tex`
- `notes/onepage/vector_missing_iv_identification_onepage.tex`
- `manuscript/欠測IV (1).pdf`（ローカル資料。Git追跡対象外）

## コンパイル

主論文ファイルは `manuscript/main.tex` です。

```sh
make pdf
make proof
make beamer
```

出力PDFは `build/formal/main/main.pdf` に生成されます。LaTeXの設定は `.latexmkrc` にまとめています。

## ビルド成果物

- `build/formal/main/`: 主論文 `main.tex` と関連生成物
- `build/formal/vector_missing_iv_identification_onepage/`: 正式なアブストラクトとプレビュー
- `build/formal/vector_missing_iv_identification_proof/`: onepage版に続く正式なベクトル識別証明
- `build/formal/vector_missing_iv_identification_beamer/`: ベクトル識別証明の発表用Beamer
- `build/supplementary_reading/`: 著者・年別の副読資料
- `build/templates/`: レイアウトテンプレート

## ディレクトリ構成

- `manuscript/`: 論文本文・現在の執筆メモ
- `docs/`: プロジェクトの前提・作業方針
- `notes/`: ブリーフィング、音声メモなどの作業メモ
- `resources/`: 文献、講義ノート、発表資料、レイアウト参考、旧版
- `build/`: PDFなどの生成物・一時出力

## Git管理方針

- atomic commitを維持する。
- TeX、README、軽量な管理ファイルを中心に追跡する。
- PDF、ZIP、PPTX、DOCX、音声・動画、データ、生成物は原則としてGit追跡対象外にする。
- 削除が必要な場合は、作業目的を確認してから行う。
