"""Export n=1000 results for the manuscript and separate candidate slide deck."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import nbformat
from nbclient import NotebookClient
import experiment as e

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'report_n1000'
METHODS = e.METHODS
LABELS = dict(zip(METHODS, ['Oracle', 'Ignorable', 'Restricted', 'Saturated']))
COLORS = dict(zip(METHODS, ['#525252', '#2369bd', '#cf6819', '#18815c']))


def load():
    path = ROOT/'results_n1000'
    c = json.loads((path/'run_config.json').read_text())
    expected = e.config()
    expected['sample_size'] = 1000
    assert c == expected
    assert json.loads((path/'provenance.json').read_text())['source_sha256'] == hashlib.sha256((ROOT/'experiment.py').read_bytes()).hexdigest()
    s = pd.read_csv(path/'summary.csv')
    d = pd.read_csv(path/'diagnostics.csv')
    raw = pd.read_csv(path/'estimates.csv')
    assert len(raw) == 3*100*4*len(e.NAMES)
    assert d.stationary.all()
    return s, d, raw


def save(fig, name):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    frame = fig.bbox
    unused_ticks = set()
    for ax in fig.axes:
        for axis, limits in [(ax.xaxis, ax.get_xlim()), (ax.yaxis, ax.get_ylim())]:
            low, high = sorted(limits)
            for tick in axis.get_major_ticks():
                if not low <= tick.get_loc() <= high:
                    unused_ticks.update([tick.label1, tick.label2])
    for text in fig.findobj(matplotlib.text.Text):
        if text not in unused_ticks and text.get_visible() and text.get_text():
            box = text.get_window_extent(renderer)
            if box.x0 < frame.x0-1 or box.y0 < frame.y0-1 or box.x1 > frame.x1+1 or box.y1 > frame.y1+1:
                raise ValueError(f'Clipped text in {name}: {text.get_text()}')
    fig.savefig(OUT/(name+'.pdf'))
    fig.savefig(OUT/(name+'.png'), dpi=180)
    plt.close(fig)


def criteria(s, size, targets, labels, metrics, name):
    slide = size == 'slide'
    width, height, font = (14, 5.3, 11) if slide else (8.2, 8.0, 9)
    plt.rcParams.update({'font.size': font, 'axes.titlesize': font})
    fig, axs = plt.subplots(1 if slide else 2, 2 if slide else 1,
                            figsize=(width/2.54, height/2.54), squeeze=False)
    for ax, (metric, title) in zip(axs.ravel(), metrics):
        for method in METHODS:
            g = s[(s.mechanism=='MNAR')&(s.method==method)].set_index('parameter').loc[targets]
            ax.plot(range(len(targets)), g[metric], color=COLORS[method], marker='o', ms=3,
                    lw=1.2, label=LABELS[method])
        ax.set_xticks(range(len(targets)), labels, rotation=35 if len(labels)>3 else 0, ha='right' if len(labels)>3 else 'center')
        ax.set_title(title)
        ax.grid(axis='y',alpha=.2)
        if metric == 'coverage_valid':
            ax.set_ylim(0,1.08)
            ax.axhline(.95,color='black',lw=.8,ls=':')
        elif metric == 'bias':
            ax.axhline(0,color='black',lw=.8,ls=':')
        else:
            ax.set_ylim(bottom=0)
    handles, labels = axs.ravel()[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='lower center',ncol=4 if slide else 2,frameon=False,
               handlelength=1.1,columnspacing=.8,bbox_to_anchor=(.5,0))
    fig.tight_layout(pad=.5,rect=(0,.15 if slide else .13,1,1))
    save(fig, f'{size}_{name}')


def make_report():
    OUT.mkdir(exist_ok=True)
    s,d,raw = load()
    for size in ['slide','paper']:
        criteria(s,size,['mean_Y1','mean_Y2','mean_Y3'],['Y1','Y2','Y3'],
                 [('bias','Bias'),('SD','SD')], 'outcome_point')
        criteria(s,size,['mean_Y1','mean_Y2','mean_Y3'],['Y1','Y2','Y3'],
                 [('estimated_SE','Mean SE (valid)'),('coverage_valid','Coverage (valid)')], 'outcome_inference')
        criteria(s,size,e.NAMES[:7],['1:1','1:2','2:1','2:2','3:1','3:2','p2'],
                 [('bias','Bias'),('RMSE','RMSE')], 'latent_point')
        width,height,font = (14,5.3,11) if size=='slide' else (8.2,6.0,9)
        plt.rcParams.update({'font.size':font})
        fig,ax=plt.subplots(figsize=(width/2.54,height/2.54))
        joint=raw[(raw.mechanism=='MNAR')&raw.parameter.str.startswith('P')]
        names=e.NAMES[-8:]
        ax.plot(range(8),joint.groupby('parameter').truth.first().reindex(names),
                color='black',ls='--',lw=1.2,label='Truth')
        for method in METHODS:
            ax.plot(range(8),joint[joint.method==method].groupby('parameter').estimate.mean().reindex(names),
                    color=COLORS[method],marker='o',ms=3,lw=1.2,label=LABELS[method])
        ax.set_xticks(range(8),[p[1:] for p in names])
        ax.set(ylabel='Cell probability',xlabel='Y1 Y2 Y3',ylim=(0,.36))
        ax.grid(axis='y',alpha=.2)
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center',bbox_to_anchor=(.5,0),ncol=5 if size=='slide' else 3,
                   frameon=False,handlelength=1.0,columnspacing=.6)
        fig.subplots_adjust(left=.16,bottom=.32 if size=='slide' else .36,right=.98,top=.98)
        save(fig,f'{size}_joint')
    compact=[]
    for (mechanism,method),g in s.groupby(['mechanism','method']):
        m=g[g.parameter.str.startswith('M')]
        pf=g[g.parameter=='p_class2'].iloc[0]
        compact.append(dict(mechanism=mechanism,method=method,M_abs_bias=m.bias.abs().mean(),
                            M_RMSE=m.RMSE.mean(),p_bias=pf.bias,p_RMSE=pf.RMSE,
                            valid_CI=int(pf.valid_CI)))
    compact=pd.DataFrame(compact)
    compact.to_csv(OUT/'compact.csv',index=False)
    table=[r'\begin{tabular}{@{}llrrrr@{}}',r'\hline',
           r'機構 & 方法 & $|\mathrm{Bias}|_M$ & RMSE$_M$ & Bias$_p$ & RMSE$_p$\\',r'\hline']
    for mechanism in ['MCAR','MAR','MNAR']:
        for method in METHODS:
            row=compact[(compact.mechanism==mechanism)&(compact.method==method)].iloc[0]
            short=dict(zip(METHODS,['O','I','R','C']))[method]
            table.append(f'{mechanism} & {short} & {row.M_abs_bias:.4f} & {row.M_RMSE:.4f} & {row.p_bias:.4f} & {row.p_RMSE:.4f}'+r'\\')
    table.extend([r'\hline',r'\end{tabular}'])
    (OUT/'paper_summary.tex').write_text('\n'.join(table)+'\n')
    table=[r'\begin{tabular}{@{}lrrrrr@{}}',r'\hline',r'対象 & Bias & SD & SE & Cov. & $B_{\rm CI}$\\',r'\hline']
    targets={'M2_class2':r'$M_2(1,2)$','M3_class2':r'$M_3(1,2)$','p_class2':r'$p_2$',
             'mean_Y2':r'$\mu_2$','mean_Y3':r'$\mu_3$'}
    for p,label in targets.items():
        row=s[(s.mechanism=='MNAR')&(s.method=='candidate_saturated')&(s.parameter==p)].iloc[0]
        table.append(f'{label} & {row.bias:.4f} & {row.SD:.4f} & {row.estimated_SE:.4f} & {row.coverage_valid:.3f} & {int(row.valid_CI)}'+r'\\')
    table.extend([r'\hline',r'\end{tabular}'])
    (OUT/'paper_inference.tex').write_text('\n'.join(table)+'\n')
    table=[r'\begin{tabular}{@{}lrrrr@{}}',r'\toprule',r'Method & $\mu_2$ bias & $\mu_3$ bias & $M$ RMSE & Valid CI\\',r'\midrule']
    for method in METHODS:
        g=s[(s.mechanism=='MNAR')&(s.method==method)].set_index('parameter')
        m=compact[(compact.mechanism=='MNAR')&(compact.method==method)].iloc[0]
        table.append(f'{LABELS[method]} & {g.loc["mean_Y2","bias"]:.4f} & {g.loc["mean_Y3","bias"]:.4f} & {m.M_RMSE:.4f} & {m.valid_CI}/100'+r'\\')
    table.extend([r'\bottomrule',r'\end{tabular}'])
    (OUT/'slide_summary.tex').write_text('\n'.join(table)+'\n')
    return compact


def notebook():
    nb=nbformat.v4.new_notebook()
    nb.metadata.kernelspec={'display_name':'Python 3','language':'python','name':'python3'}
    nb.cells=[
      nbformat.v4.new_markdown_cell('''# 観測カテゴリMNARモデル n=1,000
## 結論
MCAR/MAR/MNAR各100反復。MNARのoutcome平均biasは候補法で小さい一方、境界解19/100で通常のWald推論は未解決。
保存済みMonte Carlo結果を検証・再集計する実行済みnotebook。新スライドと本文図表は同じCSVから生成する。
## 方法
V=(W,Z) -> F -> Yj、(Y1,Yj) -> Dj。X固定、Y1常時観測、2クラス、条件付き独立な応答。
piは各Y1,Yjセルで自由。旧block bridgeではなく共通測定核を課した観測尤度を用いる。
飽和selectionと正指定の全交互作用logisticは同じモデルなので4手法を比較する。
母集団の三方向rankは2+2+2。旧4セルblock completenessは不成立。
## 再実行
リポジトリ直下から `simulation/.venv/bin/python simulation/observed_category/experiment.py --sample-size 1000 --output results_n1000`。
生成・推定のコードと設定は同ディレクトリに保存されている。'''),
      nbformat.v4.new_code_cell('''from pathlib import Path
import sys
from IPython.display import display, Image
root=Path.cwd()
if not (root/'experiment.py').exists(): root=root/'simulation'/'observed_category'
sys.path.insert(0,str(root))
import build_n1000_report as report
import experiment as e
import pandas as pd
summary, diagnostics, raw=report.load()
checks=pd.DataFrame([r for m in e.config()['mechanisms'] for r in e.population_checks(e.config(),m)])
display(checks)
display(report.make_report().round(4))'''),
      nbformat.v4.new_markdown_cell('''## 推論と診断
bias・SD・RMSEは全100反復。SEとcoverage_validはCIが有効な反復のみ。
境界解・非収束・非正定値HessianにWald CIを付与しない。CI成功率も必ず併記する。
制約されたselection (Yjのみ) はMCARで正指定、今回のMAR/MNARで誤指定。'''),
      nbformat.v4.new_code_cell('''display(diagnostics.groupby(['mechanism','method'])[['boundary','valid_se','stationary','item_rate','complete_rate']].mean())
display(summary[(summary.mechanism=='MNAR') & summary.parameter.isin(['M2_class2','M3_class2','p_class2','mean_Y2','mean_Y3'])].round(4))
for name in ['slide_outcome_point','slide_outcome_inference','slide_latent_point','slide_joint']:
    display(Image(filename=str(report.OUT/(name+'.png'))))'''),
      nbformat.v4.new_markdown_cell('''## 限界
候補法のMNARのCIは81/100でのみ計算可能で、coverage_validを全反復のcoverageと呼べない。
MCAR/MARではFIMLに比べ追加推定の分散コストがある。正指定飽和logisticに対する優位性を示す実験ではない。
応答独立性・測定exclusion・既知クラス数の誤指定は許容しない。
このシミュレーションは旧bridge推定量の定理やglobal complete case不存在の場合を検証していない。''')]
    nbformat.validate(nb)
    NotebookClient(nb,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute()
    nbformat.write(nb,ROOT/'observed_category_n1000.ipynb')


if __name__=='__main__':
    make_report()
    notebook()
