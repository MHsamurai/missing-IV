# 観測カテゴリ候補モデルの再検証

2026-09-07。元の原稿・スライド・シミュレーションは変更しない。
候補ノートは `notes/reading/latent_mnar_observed_category_identification_candidate.md`。

## 結果

`observed_category_validation.ipynb` は実行済み。MCAR/MAR/MNARそれぞれ100反復、n=500とn=5,000を実行した。
機構間で同じ完全データ・応答乱数を用いる。測定核、n=500、100反復、平均item観測率80%は以前の設定を維持。
Zの生成は変更し、V=(W,Z)を先に生成してFを生成する。全手法に同じV情報を与える。

MNAR、n=500のbias（全100反復）:

| 対象 | Ignorable FIML | 候補法 |
|---|---:|---:|
| M2(1,class 2) | -0.1570 | -0.0151 |
| M3(1,class 2) | -0.1329 | -0.0138 |
| p(class 2) | -0.0150 | -0.0011 |
| E(Y2) | -0.0926 | -0.0118 |
| E(Y3) | -0.0798 | -0.0024 |

MNARでは候補法の測定核6成分の平均絶対biasは0.0094（FIML: 0.0690）、
成分別RMSEの平均は0.0545（FIML: 0.0870、oracle: 0.0351）。
一方、MCAR/MARではFIMLの成分別RMSE平均は0.0426/0.0423、候補法は0.0660/0.0671であり、補正の分散コストがある。

ただし、候補法はn=500のMNARで41/100が計算上の境界付近となり、Wald CIを無効と判定した。
MCAR/MARでも30/29件が境界付近。coverageをCIの得られた反復のみで評価して95%達成と主張してはいけない。
n=5,000では候補法の境界解・CI作成失敗は全機構で0/100。MNARの測定核coverageは0.93〜0.98、
outcome平均Y2/Y3は0.95/0.96、クラス比率は0.99。100反復のMonte Carlo誤差は残る。
誤指定selectionはMNARで両nとも全反復が境界付近であり、そのWald SE/coverageは報告しない。

## DAGとrank

`figures/candidate_dag.png` の通り W,Z -> F -> Yj、Y1,Yj -> Dj。
測定核へのZの直接効果、FからW/Zへの逆向き生成は入れない。Xは固定。
Y1は常時観測、D2とD3はYを条件として独立、応答確率にF/Vの直接効果はない。
これらは元の一般的なMissing-IVモデルより強い追加制約。

母集団の観測テンソルだけを使ったmatrix-pencil分解と正規化・逆算により、M2,M3,pi,G,pf,M1を絶対誤差1e-9未満で回復した。
K2,K3,Gのcolumn Kruskal rankはすべて2で、2+2+2=2r+2=6。
MNARの最小特異値はK2: 0.4106/0.3489、K3: 0.5428/0.4604（Y1=0/1）、G: 0.3838。
選択確率を分離する2x2行列式も非零。標本でrankを保証したという意味ではない。

旧4セルblockの任意関数に対するcompletenessは依然として不成立（rank 2、必要rank 4）。
今回の結果は旧stage 1の証明を復活させるものではない。
global complete caseが存在しない設定も対象外。今回はcomplete-case率が約49〜52%ある。

## 推定法と比較の意味

欠測も含むO=(Y1,V,T2,T3)の全観測パターンを用い、共通測定核とクラス比率、各selectionセルを同時尤度で推定する。
旧bridge-weighted estimatorは使用しない。

- oracle: 全Yを用いるがFは推定する。
- Ignorable FIML: MCAR/MARで正指定、MNARで誤指定。
- Restricted selection (Yj only): MCARでは正指定。MAR/MNARではY1効果を除いた誤指定。
- Candidate saturated: 各pi_j(Y1,Yj)を4セル自由にする。

二値のY1,Yjについて切片・両主効果・交互作用を含むlogisticは飽和4セルと一対一対応する。
したがって「正指定parametric selection」と「候補法」は同じモデルであり、4本の異なる曲線にまとめた。
候補法が正指定parametric likelihoodより優れているという実験ではない。
selection linkの形は制限しないが、応答の条件付き独立、直接効果exclusion、クラス数、測定族は指定している。

## 推論・検証

6個の乱数初期値を使用し、真値初期化なし。最小目的関数を選択するが大域解の保証はしない。
logit範囲[-10,10]の絶対値9.9以上を境界付近と記録する。
推定SEはVの経験分布も含むsandwich + delta法。
非収束・大きな勾配・境界付近・非正定値HessianではCIを無効化する。

- bias/RMSE/SD: 全反復。境界解も除外しない。
- estimated_SE/coverage_valid/SD_valid: CIが有効な同一部分標本内。
- valid_CI/CI_failure_rate: 利用可能な区間数と作成失敗率。
- covered_and_available: 区間作成成功かつ真値を含む割合。通常のcoverageとは区別する。
- 独立レビュー: 尤度・勾配・sandwich・DGP整合性を検算。勾配差分誤差5.7e-11未満、SE差8.0e-10未満。

## 再実行

リポジトリ直下から:

```sh
uv pip install --python simulation/.venv/bin/python -r simulation/observed_category/requirements.txt
simulation/.venv/bin/python -m unittest discover -s simulation/observed_category -p 'test_*.py' -v
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 simulation/.venv/bin/python simulation/observed_category/experiment.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 simulation/.venv/bin/python simulation/observed_category/experiment.py --sample-size 5000 --output results_n5000
simulation/.venv/bin/python simulation/observed_category/build_notebook.py
simulation/.venv/bin/python -m jupyter nbconvert --execute --to notebook --inplace simulation/observed_category/observed_category_validation.ipynb
```

結果CSVは `results/` と `results_n5000/`、集計は `comparison_summary.csv`。
設定はJSON互換YAMLの `config.yml`、実行設定・Python/library versions・ソースSHA256を各結果ディレクトリに保存。
notebookの既定動作は保存済みMonte Carlo結果の読込と再集計・描画・母集団検算。RUN_MC=Trueで標本生成から再実行する。
