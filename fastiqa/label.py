from pathlib import Path
import pandas as pd

try:
    from cached_property import cached_property
except ImportError:
    class cached_property(object):
        '''Computes attribute value and caches it in the instance.
        Python Cookbook (Denis Otkidach) https://stackoverflow.com/users/168352/denis-otkidach
        This decorator allows you to create a property which can be computed once and
        accessed many times. Sort of like memoization.
        '''

        def __init__(self, method, name=None):
            # record the unbound-method and the name
            self.method = method
            self.name = name or method.__name__
            self.__doc__ = method.__doc__

        def __get__(self, inst, cls):
            # self: <__main__.cache object at 0xb781340c>
            # inst: <__main__.Foo object at 0xb781348c>
            # cls: <class '__main__.Foo'>
            if inst is None:
                # instance attribute accessed on class, return self
                # You get here if you write `Foo.bar`
                return self
            # compute, cache and return the instance's attribute value
            result = self.method(inst)
            # setattr redefines the instance's attribute so this doesn't get called again
            setattr(inst, self.name, result)
            return result


class IqaLabel:
    path = None
    folder = 'images'

    name = None
    abbr = None  # will be used by IqaExp.valid

    img_raw_size = None  # None if the database only different sizes
    img_tfm_size = None  # 500  # if not none, apply tfm with this size
    img_pad_size = None  # None if padded images are not available
    img_size = None  # only use image with this size

    csv_labels = 'labels.csv'

    fn_col = 'name'  # 'im_names'
    fn_suffix = ''  # '.jpg'

    valid_pct = None  # use is_valid col by default
    val_bs = None  # valid batch size

    label_cols = 'mos',
    label_types = 'mos',
    size_cols = 'height', 'width'  # 'bottom', 'right'
    label_idx = 0  # 0 for image, 1 for patch 1
    label_suffixes = '',

    rois_cols = ['zero', 'zero', 'width', 'height']  # for RoIPool models

    # browser
    # opt_bbox_class = '',

    def __init__(self, **kwargs):
        if self.name is None: self.name = self.__class__.__name__
        if self.abbr is None: self.abbr = self.name

        # load user setting
        self.__dict__.update(kwargs)  # must put this after, overwrite everything

        # format user setting, TODO use properties.setter is safer
        self.path = Path(self.path)

        # check label file
        # file = self.path / self.csv_labels
        # if not os.path.isfile(file):
        #     print(f'label not founded: {file}, self.create_csv_labels() is called.')
        #     self.create_csv_labels()

        # double check class types
        if not isinstance(self.label_cols, (list, tuple)):
            raise TypeError("label_cols must be a list or a tuple.")

    # def create_csv_labels(self):
    #     raise NotImplementedError

    # TODO img_size cannot be set after initing
    @cached_property
    def df(self):
        df = pd.read_csv(self.path / self.csv_labels)

        # be compatitble with Rois0123
        if 'zero' in self.rois_cols:
            df['zero'] = df['left'] = df['top'] = 0
        if self.img_raw_size is not None:
            if self.size_cols[0] not in df.columns:
                df['bottom'] = df[self.size_cols[0]] = self.img_raw_size[0]
            if self.size_cols[1] not in df.columns:
                df['right'] = df[self.size_cols[1]] = self.img_raw_size[1]

        if self.img_size is not None:
            df = df[(df[self.size_cols[0]] == self.img_size[0]) &
                    (df[self.size_cols[1]] == self.img_size[1])].reset_index()
        return df


class Rois0123Label(IqaLabel):
    csv_labels = 'labels_image_3patch.csv'
    size_cols = 'height_image', 'width_image'
    fn_col = 'name_image'
    label_suffixes = '_image', '_patch_1', '_patch_2', '_patch_3'
    label_cols = 'mos_image', 'mos_patch_1', 'mos_patch_2', 'mos_patch_3'

    rois_cols = ['left_image', 'top_image', 'right_image', 'bottom_image',
                 'left_patch_1', 'top_patch_1', 'right_patch_1', 'bottom_patch_1',
                 'left_patch_2', 'top_patch_2', 'right_patch_2', 'bottom_patch_2',
                 'left_patch_3', 'top_patch_3', 'right_patch_3', 'bottom_patch_3']


class IqaData:
    label = IqaLabel

    def __init__(self, label, filter=None, **kwargs):
        self.label = label() if isinstance(label, type) else label
        self.name = f'{self.label.name}_{self.__class__.__name__}'

        # lazy loading, only load when we have to, see #76
        self.c = len(self.label.label_cols)
        # define self.device at IqaDataBunch
        # define self.loss at Im2MOS

        self.__dict__.update(kwargs)
        if filter is not None:
            self.df = self.df[filter(self.df)]

    def __getattr__(self, k: str):
        return getattr(self.label, k)

    def to_csv(self, path_or_buf=None):
        if path_or_buf is None:
            path_or_buf = self.path / self.csv_labels
        self.df.to_csv(path_or_buf, index=False)
