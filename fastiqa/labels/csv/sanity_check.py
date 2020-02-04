from fastai.vision import *
from ..label import IqaLabel
from ..util import parfor
"""
csv validation

https://github.com/baidut/FBIQA/issues/11

df[ (df['bottom_image'].isnull()) ]
df.iloc[df['num_px'].idxmax()]

"""

'''
from fastiqa.database.csv_proc.sanity_check import *
data = IqaLabel(path='data/FLIVE', csv_labels='haoran/all_patches_scores.csv')
check_duplicates(data)
'''


from ..label import Rois0123Label

class Checker(Rois0123Label):
    # check (self.df_patch_roi)
    # add size if not exist
    def check_size(self, df=None, fix=True, in_parallel=False):
        def get_size(f):
            im = PIL.Image.open(os.path.join(self.path, self.folder, f))
            width, height = im.size
            if im.mode is not 'RGB':
                print(f'{f}: {im.mode}')
            return height, width

        if df is None:
            df = self.df
        results = parfor(df[self.fn_col], get_size, in_parallel)
        df_ = pd.DataFrame.from_records(results, columns=['height', 'width'])

        if fix:
            self.df[self.size_col[0]] = df['height']
            self.df[self.size_col[1]] = df['width']
            self.df.to_csv(self.path / self.csv_labels, index=False)

        wrong_height = self.df[self.size_col[0]] != df_['height']
        wrong_width = self.df[self.size_col[1]] != df_['width']
        return df_[wrong_height | wrong_width]


def check_file_exist(self, fix=True, in_parallel=False):
    '''

    :param self:
    :param fix:
    :param in_parallel:
    :return: the filename of not existed files
    '''

    def is_exist(f):
        return os.path.isfile(os.path.join(self.path, f))

    existed = parfor(self.df[self.fn_col], is_exist, in_parallel)

    if fix:
        self.df[existed].to_csv(self.csv_labels, index=False)

    return self.df[~pd.Series(existed)][self.fn_col]


'''
data = IqaLabel(path='data/FLIVE', csv_labels='rois_image.csv', size_col=['bottom', 'right'])
check_size(data)


data = IqaLabel(path='data/KonIQ', csv_labels='labels.csv', size_col=['height', 'width'])
check_size(data)

from fastiqa import *
from fastiqa.database.csv_proc.sanity_check import *
data = IqaLabel(path='data/CLIVE', folder='Images', csv_labels='labels.csv', size_col=['height', 'width'])
check_size(data)
'''





# TODO default use self.csv_rois_patch? don't have image locations
'''
from fastiqa.database.csv_proc.sanity_check import *
from fastiqa.database import *
data = Patch0(path='data/FLIVE')
# check_patch_rois(data, 394)
not_matched = check_patch_rois(data)
not_matched.to_csv(data.path/'wrong_location.csv', header=True)

# use Patch0 to fix rois
# then use Patch0123
'''




def check_patch_rois(self, n=False, fix=True, in_parallel=True):
    """
    check if patch locations are correct
    show a patch by loading the patch file
    and load the subimage with the given coord
    and check if they are consistent

    :param self:
    :param n:
    :param fix:
    :param in_parallel:
    :return:
    """
    from PIL import ImageChops

    def check_if_mismatched(t, visualize=False):
        def show_sample():
            if visualize:
                # img.show()
                # patch.show()
                # patch_from_loc.show()
                _, axs = plt.subplots(1, 3, figsize=(12, 4))
                axs[0].imshow(np.asarray(im))
                axs[1].imshow(np.asarray(patch))
                axs[2].imshow(np.asarray(patch_from_loc))

        # df = pd.read_csv('data/FLIVE/labels_image_3patch.csv')
        # df = df = pd.read_csv('data/FLIVE/labels_old/3k/labels_image_3patch.csv')
        # row = df.iloc[-18]
        idx = t[0]
        row = t[1]
        img = PIL.Image.open(os.path.join('data/FLIVE', row['name_image']))
        patch = PIL.Image.open(os.path.join('data/FLIVE', row['name_patch']))  # + '_patch_1.jpg'
        patch_from_loc = img.crop((row['left_patch'], row['top_patch'], row['right_patch'], row['bottom_patch']))

        try:
            # images do not match for gray images like 394 2042 4576
            diff = ImageChops.difference(patch.convert('L'), patch_crop.convert('L'))
        except ValueError:  # ValueError: images do not match
            print(f'{idx} {row.name_image}: images do not match')
            show_sample()
            print(patch.size, patch_crop.size)
            return False
        mean_diff = np.asarray(diff).mean()
        if mean_diff > 4:
            print(f'{idx} {row.name_image}: {mean_diff}')

        show_sample()
        print(f'{idx} {row.name_image}: {mean_diff}')
        return mean_diff > 4

    df = self.df_all[['name_image', 'top_image', 'left_image', 'bottom_image', 'right_image',
                      'name_patch', 'top_patch', 'left_patch', 'bottom_patch', 'right_patch']].dropna()
    for col in ['top_image', 'left_image', 'bottom_image', 'right_image',
                'top_patch', 'left_patch', 'bottom_patch', 'right_patch']:
        df[col] = df[col].astype('int')

    if n:
        return check_if_mismatched((n, df.iloc[n]), visualize=True)
    else:
        not_matched = parfor(df.iterrows(), check_if_mismatched, in_parallel, total=len(df))
        df_matched = df[~pd.Series(not_matched)]
        if fix:
            df_rois_patch = pd.read_csv(self.path/self.csv_rois_patch)
            df_rois_patch = df_rois_patch[df_rois_patch.name.isin(df_matched.name_patch)]
            df_rois_patch.to_csv(self.path/self.csv_rois_patch, index=False)
            # self.df[~pd.Series(not_matched)].to_csv(self.path / self.csv_labels, index=False)
        return df[not_matched]['name_patch']

# def remove_wrong_locations(self, n=False, fix=True, in_parallel=True):
