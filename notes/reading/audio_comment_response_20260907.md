# 音声コメント監査と対応状況

対象音声: `/Users/m/Downloads/東神田1丁目1-7 35.m4a`（約37分54秒）

時刻は自動文字起こしに基づく概算である。意味のない無音・数字列は指摘として数えていない。

## 1. 音声による指摘点と対応

| No. | 時刻 | 指摘点 | 対応 | 状態 |
|---:|:---:|---|---|:---:|
| 1 | 0:10--1:19 | latent measurement modelでは、まず潜在変数、観測項目、潜在分布、測定核を基礎から説明する。 | Slide 4で$F,Y,Q_F,Q_j$とlocal independenceを定義した。 | 完了 |
| 2 | 1:23--4:13 | 旧p5の「full lawを回復しても$Q_F,Q_Y$は分離されない」は早すぎる。先にcomplete-dataのthree-view tensorを示し、非分離の問題は関連研究後へ移す。 | Slide 4をAllman型complete-data identificationで閉じ、非分離の式と問題はSlide 7へ移した。 | 完了 |
| 3 | 4:13--6:02 | 関連研究をscalar Missing IVとmultivariate MNARに分け、self-censoring / non-self-censoring系も含める。 | Slide 5を三分類にし、multivariate MNARとしてTang、Sadinle--Reiter、Li、Ni--Shaoを列挙した。 | 完了 |
| 4 | 6:02--7:36 | latent structure側を曖昧にせず、Allmanのtensor uniquenessと本文で扱うlatent-MNAR文献を明示する。 | Slide 5にAllman、Muthen、Holman--Glas、Lee--Tang、Harel--Schafer、Jung、Kano--Takai、Kuha、Xieを明示した。 | 完了 |
| 5 | 7:36--8:17 | latent shifter $W$とMissing IV $Z_S$を混同しない。$F$を積分すると$W$は一般にMissing IVにならない。 | 「Model and assumptions」の扉に続くSlide 8で、周辺化式、$Z_S$と$W$の役割分担、残る分解問題を示した。 | 完了 |
| 6 | 8:22--9:51 | Stage 1 / Stage 2だけの章区切りは唐突。model and assumptionsの章を置く。 | Slide 7をsection title「Model and assumptions」にし、後半を「Finite latent-class identification」とした。 | 完了 |
| 7 | 10:15--13:09 | technical slidesの前に、本稿の方法全体を概観するスライドが必要。 | Slide 6にtwo-stage identificationの全体図と新規性を置いた。 | 完了 |
| 8 | 13:42--14:00 | simple multivariate extensionはsupported blocksの直前へ移し、global complete caseの限界から接続する。 | Slide 9へ移動し、Slide 10のsupported-block定義へ接続した。 | 完了 |
| 9 | 14:08--15:47 | $D_j,O,R_S,Y_S,U_S,\pi_S$を数式だけでなく言葉で定義し、$R_S=0$なら$Y_S$が欠測であることを説明する。 | Slide 10とWord原稿で各記号と$R_S=0$の意味を明記した。 | 完了 |
| 10 | 15:52--16:30 | single-block DAGで$Z_S,U_S,F,Y_S,R_S$の役割を説明する。 | Slide 11にDAGと三つの短い説明を配置した。 | 完了 |
| 11 | 16:30--17:53 | overlapping supported blocks、anchor pair、extension pair、共通項目の役割を先に説明する。 | Slide 12に複数block図とanchor / extension / shared itemを示した。 | 完了 |
| 12 | 17:57--18:35 | 仮定を経て、新命題が既存scalar Missing-IV identificationのblockwise版であることを明瞭にする。 | Slides 13--14で仮定6--7とNew Proposition 1を分離して提示した。 | 完了 |
| 13 | 18:39--21:01 | proof sketchは、moment成立、complete-case uniqueness、positivity extension、IPW recoveryの順と使用仮定を示す。 | Slide 15をproof mapにし、仮定番号と四段階を図示した。 | 完了 |
| 14 | 21:18--23:33 | latent decompositionへ入る前に$p_f,G,M_j$を定義し、なぜ分解の一意性が未解決か説明する。 | Slide 17で三つの対象とobservational equivalenceを定義した。 | 完了 |
| 15 | 23:35--24:48 | identification strategy図を早い段階で一度見せ、分解段階で再掲する。 | Slides 6と18で同じtwo-stage flowを目的に応じて提示した。 | 完了 |
| 16 | 24:50--27:28 | Assumption 3.1をLemma 3.1より先に置き、three-view rank条件がAllmanと同じであることを明記する。 | Slides 19--20の順に変更し、Slide 19冒頭でAllman Theorem 1との対応を記した。 | 完了 |
| 17 | 25:19--27:43 | 既知のclass数$r$、anchor ordering、extension-pair support、rank条件の役割を理解できるようにする。 | Slide 19のassumption boxで四点を明記した。 | 完了 |
| 18 | 29:07--30:04 | Theorem 1は、pair lawsの回復と一つのanchor tensor分解から$Q_F,Q_Y$、未同時観測item lawまで得ることを端的に示す。 | Slide 21にNew Theorem 1と平易な一文要約を置いた。 | 完了 |
| 19 | 30:10--30:54 | proof mapをProposition 1、Allman uniqueness、Bayes rule、Lemma 3.1からTheorem 1へ明示的につなぐ。 | Slide 22の最終nodeと矢印をNew Theorem 1へ接続した。 | 完了 |
| 20 | 30:54--31:56 | 推定もrecover、decomposeの識別順に置き、Zhao--Shaoはplug-in順序の先例として正確に位置づける。 | Slide 23でbridge-weighted composite estimatorと依拠関係を整理した。 | 完了 |
| 21 | 31:56--33:03 | 計算はbridge、tensor decomposition、constrained refinementの順を示す。 | Slide 24に三段階の計算図を置いた。 | 完了 |
| 22 | 33:03--35:01 | DGPと五推定量を明確に定義する。 | Slide 25でAllman型DGPとoracle、MAR、正指定selection、誤指定selection、proposed bridgeを定義した。 | 完了 |
| 23 | 35:01--37:08 | $M_j,p_f$だけでは不十分。欠測前の全体のoutcome $Y$ distributionを推定・比較する。 | 8-cell $P(Y_1,Y_2,Y_3)$、total variation、周辺平均、outcome varianceを追加し、本文・Slides 26/28・Wordを更新した。 | 完了 |

## 2. 追加検証との対応

| 検証 | 識別上の役割 | 比較対象 | 主な出力 |
|---|---|---|---|
| supported-pair lawの直接回復 | Stage 1のbridgeがselection biasを除くかを分解前に確認 | population truth、full-data empirical、respondent-only、direct bridge | `allman_y_pair_distribution.csv`、旧pair-law figure（notebook内の補助診断） |
| 全体の$Y$ joint law | Stage 1で回復したoverlapping lawsをStage 2が一つの分布へ接続できるかを確認 | oracle/truth、MAR、正指定selection、誤指定selection、proposed bridge | `allman_y_joint_distribution.csv`、8-cell comparison figure |
| total variation distance | 8 cells全体の分布誤差を一つの尺度で比較 | 実際にfitした五推定量 | `allman_y_joint_tv_summary.csv` |
| 周辺平均とoutcome variance | 欠測補正が$P(Y_j=1)$と$\operatorname{Var}(Y_j)$を回復するかを確認 | 五推定量 | `allman_y_marginal_summary.csv` |
| $M_j$と$p_f$ | 本稿固有のlatent decomposition対象を確認 | 五推定量 | `allman_summary.csv`、latent-parameter figure |

確率整合性として、全method・全replicationで8-cell probabilitiesの和が1になること、8-cell lawから周辺化した$P(Y_j=1)$が各fitの保存済み値と$10^{-10}$以内で一致することをnotebook実行時に確認する。

## 3. 対応漏れと今回の修正

前回までにNo. 1--22はスライド構成・本文・Word原稿へ反映済みであった。残っていたのはNo. 23であり、前回追加したsupported-pair comparisonはStage 1だけの診断で、五手法による全体の$Y$分布比較にはなっていなかった。

今回、これを次のように修正した。

1. 五手法の$\widehat p_f$と$\widehat M_{jf}$から8-cell $\widehat P(Y_1,Y_2,Y_3)$を構成した。
2. 主図を五手法のjoint-law comparisonへ置き換えた。図中のoracleはpopulation truthとした。
3. 実際にfitしたoracleを含む各replicationのtotal variation distanceを別途集計した。
4. $P(Y_j=1)$のbias、outcome varianceのbias、推定量のMonte Carlo varianceを区別した。
5. 旧supported-pair figureはnotebook内のStage-1補助診断として残した。

Mean total variation distanceは、complete-data oracle 0.0406、MAR 0.1171、正指定selection likelihood 0.0696、誤指定selection likelihood 0.1006、proposed saturated bridge 0.0651であった。提案法はMARより約44%、誤指定selection likelihoodより約35%低い。一方、これは提案法の一般的な効率優位を意味せず、正指定selection likelihoodとの優劣はDGPと有限標本varianceに依存する。
