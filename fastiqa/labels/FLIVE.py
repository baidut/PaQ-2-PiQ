from ..label import *

# FLIVE640 and FLIVE don't share labels and images, so we put them separately
__all__ = ['FLIVE',
           'FLIVE_P1',
           'FLIVE_P2',
           'FLIVE_P3',
           'FLIVE_2k',
           'FLIVE_2k_P1',
           'FLIVE_2k_P2',
           'FLIVE_2k_P3',
           'FLIVE_8k',
           'FLIVE640',
           'FLIVE_100',
           'FLIVE640_100',
           'FLIVE640_varsz',
           'FLIVE_256']

# FLIVE640 renamed to FLIVE_padded

# default databunch type is IqaData
class FLIVE(Rois0123Label):
    img_pad_size = 640, 640
    path = '!data/FLIVE'
    folder = 'images'
    csv_labels = 'labels<=640.csv'
    # browser
    # opt_bbox_class = '_image', '_patch_1', '_patch_2', '_patch_3'

    def create_csv_labels(self):
        df = pd.read_csv(self.path / 'labels_image_3patch.csv')
        valid = (df.width_image <= 640) & (df.height_image <= 640)
        df[valid].to_csv(self.path / self.csv_labels, index=False)


class FLIVE_8k(FLIVE):
    img_size = [375, 500]


class FLIVE640(FLIVE):
    # remove those too big
    img_raw_size = 640, 640
    img_tfm_size = None  # no tfms
    folder = '<=640_padded'  # '640x640'
    csv_labels = 'labels<=640_padded.csv'

"""
# FLIVE 100
from fastiqa.basics import *
from fastiqa.csv.group_by_size import *
df = create_csv_labels(label=FLIVE)
df.to_csv('/media/zq/Seagate/IQA/FBIQA/!data/FLIVE/labels_sample100for27sizes.csv', index=False)

# FLIVE640 100
from fastiqa.basics import *
from fastiqa.csv.group_by_size import *
df = create_csv_labels(label=FLIVE640)
df.to_csv('/media/zq/Seagate/IQA/FBIQA/!data/FLIVE/labels_sample100for27sizes_padded.csv', index=False)


"""


class FLIVE_100(FLIVE):
    csv_labels = 'labels_sample100for27sizes.csv'

class FLIVE640_100(FLIVE_100):
    folder = '<=640_padded'
    csv_labels = 'labels_sample100for27sizes_padded.csv'


class FLIVE640_varsz(FLIVE):
    folder = '<=640_padded'
    csv_labels = 'labels<=640_padded_varsz.csv'
    # all for training
    # valid_pct = 1 # not useful, might be overwritten

class FLIVE_P1(FLIVE):
    # batch_size = 1  # otherwise can't collate (model might crop)
    label_cols = 'mos_patch_1',
    fn_col = 'name_patch'
    fn_suffix = '_patch_1.jpg'

class FLIVE_P2(FLIVE):
    # batch_size = 1  # otherwise can't collate (model might crop)
    label_cols = 'mos_patch_2',
    fn_col = 'name_patch'
    fn_suffix = '_patch_2.jpg'

class FLIVE_P3(FLIVE):
    # batch_size = 1  # otherwise can't collate (model might crop)
    label_cols = 'mos_patch_3',
    fn_col = 'name_patch'
    fn_suffix = '_patch_3.jpg'

# class FLIVE_375x500(FLIVE):
#     img_size = [375, 500]

class FLIVE_2k(FLIVE):
    img_pad_size = None
    # csv_labels = 'labels_image_3patch_pad640_testing.csv'
    csv_labels = 'labels>640.csv'
    valid_pct = 1
    # batch_size = 1 # no use, will be overwritten by Im2MOS
    # abbr = 'FLIVE>640'

    def create_csv_labels(self):
        df = pd.read_csv(self.path / super().csv_labels)
        valid = (df.width_image <= 640) & (df.height_image <= 640)
        df[~valid].to_csv(self.path / self.csv_labels, index=False)


class FLIVE_2k_P1(FLIVE_2k):
    # batch_size = 1  # otherwise can't collate (model might crop)
    label_cols = 'mos_patch_1',
    fn_col = 'name_patch'
    fn_suffix = '_patch_1.jpg'

class FLIVE_2k_P2(FLIVE_2k):
    # batch_size = 1  # otherwise can't collate (model might crop)
    label_cols = 'mos_patch_2',
    fn_col = 'name_patch'
    fn_suffix = '_patch_2.jpg'

class FLIVE_2k_P3(FLIVE_2k):
    # batch_size = 1  # otherwise can't collate (model might crop)
    label_cols = 'mos_patch_3',
    fn_col = 'name_patch'
    fn_suffix = '_patch_3.jpg'


class FLIVE_256(FLIVE):
    folder = 'rescale-256'
