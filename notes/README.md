# notes

作業メモ、ブリーフィング、音声メモなどを置きます。DOCXや音声ファイルはGit追跡対象外です。

## Legacy TeX notes

少し前の論文メモや差し込み候補のTeX断片を保存しています。主論文ファイルは `../manuscript/main.tex` ですが、以下は検討履歴として残します。

- `missing_iv_latent_dhaultfoeuille_style_fullcontent.tex`: `main.tex` 化する前の旧稿
- `missing_iv_latent_vector_IV_revised.tex`: ベクトルIV版の改訂メモ
- `missing_iv_latent_with_dags_background_extended.tex`: DAGと背景説明を拡張したメモ
- `shadow_variable_section_insert.tex`: shadow variable 節の差し込み候補

## Reading notes

- `reading/dhaultfoeuille2010_annotated_ja.tex`: d'Haultfoeuille (2010) の注釈付き日本語読解ノート
- `reading/zhao_shao2015_annotated_ja.tex`: Zhao and Shao (2015) の注釈付き日本語読解ノート
- `reading/kano_takai2011_nmar_latent_annotated_ja.tex`: Kano and Takai (2011) の注釈付き日本語読解ノート

コンパイル:

```sh
make reading-dhaultfoeuille2010
make reading-zhao-shao2015
make reading-kano-takai2011
```
