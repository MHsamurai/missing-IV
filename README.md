# 欠測IV 研究プロジェクト

欠測IVに関する論文執筆・論文読解のための作業ディレクトリです。

主に以下を参照します。

- `manuscript/`: 論文本文
- `notes/`: 読解・検討メモ
- `references/`: 関連文献とレイアウト参考資料
- `docs/`: プロジェクトの前提と作業方針

## 現在の主要メモ

- `manuscript/main.tex`
- `manuscript/欠測IV (1).pdf`（ローカル資料。Git追跡対象外）

## コンパイル

主論文ファイルは `manuscript/main.tex` です。

```sh
make pdf
```

出力PDFは `build/main.pdf` に生成されます。LaTeXの設定は `.latexmkrc` にまとめています。

## ディレクトリ構成

- `manuscript/`: 論文本文・現在の執筆メモ
- `docs/`: プロジェクトの前提・作業方針
- `references/missing_iv/`: 欠測IVに直接関係する文献
- `references/data_fusion/`: data fusion / data combination 関連文献
- `references/course_notes/`: 講義ノート等
- `references/conference/`: 学会資料
- `references/layout/`: レイアウト参考資料
- `notes/`: ブリーフィング、音声メモなどの作業メモ
- `presentations/`: 発表資料
- `data/`: データ置き場。原則としてGitには載せない
- `figures/`: 図表素材
- `tables/`: 表素材
- `archive/`: 旧版・圧縮ファイル等
- `build/`: PDFなどの生成物・一時出力

## Git管理方針

- atomic commitを維持する。
- TeX、README、軽量な管理ファイルを中心に追跡する。
- PDF、ZIP、PPTX、DOCX、音声・動画、データ、生成物は原則としてGit追跡対象外にする。
- 削除が必要な場合は、作業目的を確認してから行う。
