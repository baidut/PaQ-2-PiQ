from fastai.vision import *
import seaborn as sns

"""
from fastiqa.database.csv_proc.size import *
from fastiqa import *

sort_by_size(FLIVE_Rois0123())


# size_summary(FLIVE_XYHW0123())
size_summary(FLIVE_Patch1(), suffix='_patch_1')


"""




#
# print(f'{len(df)} in total, group them according to similar sizes')

'''
%matplotlib inline
from fastiqa import *
lbl = IqaLabel()

lbl.size_count().head(30)
lbl.size_count(decimals=-1).head(30)
lbl.jointplot_image_height_width(df=lbl.df_unique_size, decimals=-1)
lbl.show_image_size_distribution()
'''


# TODO WONTFIX for now: show image/patch size 2d hist
# def show_image_size_distribution(self):
#     # all images
#     fig, axes = plt.subplots(1, 4, sharey=True, sharex=True, figsize=(6 * 4, 5))  # True
#     axes[1].hist2d(patch1_width, patch1_height, bins=(10, 10), cmap=plt.cm.gray)
#     # pixel num distribution
#     # list all possible image sizes
#     # not histogram
#     # scatter point and histogram # joint
#     pass


def jointplot_image_height_width(self, df=None, decimals=0, kind="hex", suffix='_image', **kwargs):
    # only image
    # df = self.df.drop_duplicates(subset="name_image")
    if df is None:
        df = self.df[['name_image', 'mos_image', 'bottom_image', 'right_image']] \
            .dropna().drop_duplicates(subset="name_image")

    x = df['bottom_image'].round(decimals)  # height
    y = df['right_image'].round(decimals)  # width
    sns.set(style="white", color_codes=True)
    return sns.jointplot(x, y, kind=kind, **kwargs).set_axis_labels("height", "width")


def show_image_size_distribution(self, df=None):
    """
    lbl.show_image_size_distribution(lbl.df_unique_size)
    :param self:
    :param df:
    :return:
    """
    if df is None:
        df = self.df_image_height_width
    # compute n_pixel
    df['num_px'] = df['bottom_image'] * df['right_image']
    px_min = df['num_px'].min()
    px_max = df['num_px'].max()
    item_min = df.loc[df['num_px'].idxmin()]  # not iloc!
    item_max = df.loc[df['num_px'].idxmax()]
    print(f'Min pixel number = {px_min:.0f} ({item_min.bottom_image:.0f}x{item_min.right_image:.0f})')
    print(f'Max pixel number = {px_max:.0f} ({item_max.bottom_image:.0f}x{item_max.right_image:.0f})')
    # draw pixel number histogram
    sns.distplot(df['num_px'], kde=False, rug=True, vertical=True)
    # draw image size distribution with patch

    # count how many different sets
    df_sizes = self.df[['bottom_image', 'right_image']].dropna().drop_duplicates()
    print(f'Number of different sizes: {len(df_sizes) - 1}')

    # no need to show the height statistics, only (height, width)

    # ax = sns.countplot(y="class", hue="who", data=titanic)
    # draw the population
    # largest group


def size_count(self, df=None, decimals=0):
    from IPython.display import display
    if df is None:
        df = self.df[['name_image', 'bottom_image', 'right_image']] \
            .dropna().drop_duplicates(subset="name_image")
    print(f'{len(df)} in total, group them according to similar sizes')
    df['num_pix'] = df['bottom_image'] * df['right_image']
    df['size'] = df['bottom_image'].astype(int).round(decimals).astype(str) + 'x' + \
                 df['right_image'].astype(int).round(decimals).astype(str)

    # sns.countplot(y="size", data=df_sorted)







    return self.size_cnt




'''
from fastiqa import *
lbl = IqaLabel()
lbl.split_train_valid_test(lbl.df_image_roi_3patch_roi)

data contain duplicates
'''

# PatchDataBunch.split_train_valid_test = split_train_valid_test
# PatchDataBunch.size_count = size_count
# PatchDataBunch.show_image_size_distribution = show_image_size_distribution
# PatchDataBunch.jointplot_image_height_width = jointplot_image_height_width


# Counter(FLIVE).size_cnt(df)
"""
Merger(FLIVE).df = Counter(FLIVE).df_sorted
Merger(FLIVE).df['is_valid'] = Spliter(FLIVE).split(0.2)


Viewer(FLIVE).

Merger(FLIVE).save()
"""





            # sns.countplot(y="size", data=df_sorted)
