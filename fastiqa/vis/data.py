from . import IqaData
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

"""
# %%
%matplotlib inline
from fastiqa.all import *
from fastiqa.vis import *

# %% size distribution
Vis(FLIVE).scatter('width_image', 'height_image')
# %%
Vis(CLIVE).hist()
Vis(FLIVE).hist()

Vis(CLIVE).distplot_image_mos()
Vis(FLIVE).distplot_image_mos()

Vis(FLIVE, filter=lambda x: x.is_valid).distplot_image_mos()
Im2MOS(FLIVE)

Vis.mos_dist([CLIVE, KonIQ, FLIVE])
Vis.mos_dist([CLIVE, KonIQ, FLIVE], figsize=[4, 2.5], rug=False)

Vis(FLIVE).jointplot('mos_image', 'mos_patch_1', kind='hex')

# %%
f = lambda x: x.size_image_cnt>100) & ~x.is_valid
Vis(FLIVE, filter=f).jointplot('mos_image', 'mos_patch_1', kind='hex')


# %%
Vis(FLIVE).corr_image_patch_mos()
Vis(FLIVE640).corr_image_patch_mos()

Vis(FLIVE640).distplot_patch_mos()

# %% High-res figure
grid = Vis(FLIVE640).jointplot(data, 'mos_image', 'mos_patch_1', edgecolor='w', s=80, kind='scatter')
grid.set_axis_labels('Image MOS', 'Patch 1 MOS')
grid.fig.set_figwidth(8)
grid.fig.set_figheight(8)

%% TODO
sizes = data.df[data.df.size_image_cnt>100].drop_duplicates(subset='size_image').size_image.tolist()

%% add_width_height
df['height'] = df['bottom'] - df['top']
df['width'] = df['right'] - df['left']
"""

def show_scatter(x, y):
    "In Praful's honor"
    from matplotlib.lines import Line2D
    from collections import Counter
    import numpy as np
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    c = Counter(zip(x, y))
    s = [c[(xx, yy)] for xx, yy in zip(x, y)]
    fig, ax = plt.subplots()
    im = ax.scatter(x, y, s=np.log(np.array(s) + 1) ** 3, edgecolor='k', alpha=0.2)
    # divider = make_axes_locatable(ax)
    plt.xlabel('Width', fontsize=16)
    plt.ylabel('Height', fontsize=16)
    # cax = divider.append_axes('right', size='5%', pad=0.05)
    # fig.colorbar(im, cax=cax, orientation='vertical')
    # plt.legend(*im.legend_elements("sizes", num=6))
    # plt.savefig('pic_dim.png', dpi = 100, bbox_inches='tight')

    legend_elements = [
        Line2D([0], [0], marker='o', label='~8k', markeredgecolor='k', markersize=25, linestyle='none'),
        Line2D([0], [0], marker='o', label='~1k', markeredgecolor='k', markersize=17, linestyle='none'),
        Line2D([0], [0], marker='o', label='~500', markeredgecolor='k', markersize=10, linestyle='none'),
        Line2D([0], [0], marker='o', label='~100', markeredgecolor='k', markersize=5, linestyle='none'),
        Line2D([0], [0], marker='o', label='<10', markeredgecolor='k', markersize=1, linestyle='none')]
    ax.legend(handles=legend_elements, frameon=False, labelspacing=1, fontsize=12,
              handletextpad=0.7) # ncol=len(legend_elements)//2, loc='lower left',
              # put legend outside: bbox_to_anchor=(1,1),
    # plt.savefig('pic_dim.png', dpi = 300, bbox_inches='tight')
    plt.gca().set_aspect('equal', adjustable='box') # The scales of x-axis and y-axis should be the same.
    plt.show()

# .set_axis_labels("output", "target").annotate(stats.pearsonr)
# xlim=(0, 100), ylim=(0, 100)
# sns.set(style="white", color_codes=True)
# from IPython.display import display
# df.sample(n=500) # subsample unstable problem?
# sets = [1, 2, 3]
# fig, axes = plt.subplots(1, len(sets), sharey=True, sharex=True, figsize=(3 * len(sets), 2))

class Vis(IqaData):
    def scatter(self, x, y):
        show_scatter(self.df[x], self.df[y])

    def scatter_size(self):
        col_h, col_w = self.size_cols
        self.scatter(col_w, col_h) # x - width, y - height

    def jointplot(self, x, y, **kwargs):
        return sns.jointplot(x, y, self.df, stat_func=stats.pearsonr, **kwargs) \
            .set_axis_labels(x, y)

    def jointplot_image_patch_score(self, prefix='mos_', **kwargs):
        for n in [1, 2, 3]:
            self.jointplot(prefix + 'image', prefix + f'patch_{n}',
                           edgecolor="w",
                           kind='hex',
                           **kwargs)

    def corr(self, x, y):
        x_data, y_data = self.df[x], self.df[y]
        return {'SRCC': stats.spearmanr(x_data, y_data)[0],
                'LCC': stats.pearsonr(x_data, y_data)[0]}

    def corr_image_patch_mos(self, prefix='mos_'):
        items = [self.corr(prefix + 'image', f'{prefix}patch_{n}') for n in (1, 2, 3)]
        return pd.DataFrame(items)

    def hist(self, x=None, **kwargs):
        """by default, show label distributions"""
        if x is None: x = list(self.label_cols)
        return self.df.hist(x, **kwargs)

    def distplot(self, x, **kwargs):
        return sns.distplot(self.df[x], **kwargs)

    def distplot_patch_mos(self, kde=True, rug=True, hist_kws=None):
        fig, axes = plt.subplots(len(self.label_cols), 1, sharey=True, sharex=True,
                                 figsize=(3, 2 * len(self.label_cols)))
        for n, col in enumerate(self.label_cols):
            self.distplot(col, hist_kws=hist_kws, ax=axes[n], kde=kde, rug=rug)

    def distplot_image_mos(self, idx=0, kde=True, rug=True, hist_kws=None, **kwargs):
        if hist_kws is None:
            hist_kws = {"range": [0, 100]}

        col = self.label_cols[idx]
        ax = self.distplot(col, hist_kws=hist_kws, kde=kde, rug=rug, **kwargs)
        ax.set_title(self.abbr)
        # fit=stats.gamma,

    @staticmethod
    def mos_dist(databases, figsize=None, vert=False, **kwargs):
        if figsize is None:
            figsize = [3, 2]

        if vert:
            fig, axes = plt.subplots(len(databases), 1, sharey=True, sharex=True,
                                     figsize=(figsize[1], figsize[0] * len(databases)))
        else:
            fig, axes = plt.subplots(1, len(databases), sharey=True, sharex=True,
                                     figsize=(figsize[0] * len(databases), figsize[1]))
        if len(databases) == 1: axes = [axes]
        for n, data in enumerate(databases):
            Vis(data).distplot_image_mos(ax=axes[n], **kwargs)



"""
import matplotlib.lines as lines
division correlation- random
scores2 = pd.read_csv('/home/zq/Downloads/half_image_scores_2.csv')
scores1 = pd.read_csv('/home/zq/Downloads/half_image_scores_1.csv')
sns.scatterplot(scores1.scores_1, scores2.scores_2) # , hist_kws={"range": [0, 100]}, rug=True
"""
