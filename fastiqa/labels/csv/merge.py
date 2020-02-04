import pandas as pd
from ..label import IqaData, cached_property

# check duplicates
# merge: data.create_csv_labels()
# size summary
# add is_valid, valid_pct=0.2
# call 640.create_csv_labels()


def add_height_width(df):
    df['height'] = df['bottom'] - df['top']
    df['width'] = df['right'] - df['left']
    return df


def df_labeled_images(self):
    return self.df[['name_image', 'mos_image']] \
        .dropna().drop_duplicates(subset="name_image")





# display the images
# FLIVE_2k.
# unique_size?
# show distribution of
# Viewer(FLIVE).size(self.df_unique_size)
#





class Merger(Spliter):
    path = '!data/FLIVE'
    csv_rois_image = 'rois_image.csv'
    csv_rois_patch = 'rois_patch.csv'
    csv_labels_image = 'labels_image.csv'
    csv_labels_patch = 'labels_patch.csv'
    cols = 'width', 'height', 'top', 'left', 'bottom', 'right', 'name', 'mos', 'zscores'

    def __init___(self, **kwargs):
        super().__init__(**kwargs)

    def create_csv_labels(self):
        label_file = self.path / self.csv_labels
        try: df = self.df
        except FileNotFoundError:
            self.df_image_roi = pd.read_csv(self.path / self.csv_rois_image)
            self.df_patch_roi = pd.read_csv(self.path / self.csv_rois_patch)
            self.df_image_mos = pd.read_csv(self.path / self.csv_labels_image)
            self.df_patch_mos = pd.read_csv(self.path / self.csv_labels_patch)

            if self.check_mos:
                for df in [self.df_image_mos, self.df_patch_mos]:
                    self.drop_duplicates(df)
                    # self.drop_not_found(df)

            df = pd.merge(self.df_patch, self.df_image, on='id').drop('id', axis=1)
            df.sort()
            df.split()
            df.to_csv(label_file, index=False)


    def drop_duplicates(self, df, col='name'):
        duplicates = df[df.duplicated(subset=col, keep=False)].sort_values(by=[col])
        print(f'{len(duplicates)} of {len(df)} duplicated')
        return df.dropna().drop_duplicates(subset=col, keep=False)


    @cached_property
    def df_all(self):
        """all information in one big table, may contain missing information"""
        df_image = pd.merge(self.df_image_roi, self.df_image_mos, on='name', how='outer')
        df_patch = pd.merge(self.df_patch_roi, self.df_patch_mos, on='name', how='outer')

        pos_start, pos_end = len('patches/'), -len('_patch_1.jpg')
        df_image['id'] = df_image['name'].str.rsplit(pat="/", n=1, expand=True)[1]
        df_patch['id'] = df_patch['name'].str[pos_start:pos_end]
        return pd.merge(df_image, df_patch, on='id_image', how='outer', suffixes=('_image', '_patch'))

    @cached_property
    def df_image(self):
        cols = [lbl + '_image' for lbl in self.cols] + ['id']
        return self.df_all[cols].drop_duplicates(subset="name_image")

    @cached_property
    def df_patch(self):
        cols = [lbl + '_patch' for lbl in self.cols] + ["id"]
        df = self.df_all[cols].dropna()
        # merget patch 123
        df = [df[df['name_patch'].str.contains(f'patch_{x}')] for x in [1, 2, 3]]
        df12 = pd.merge(df[0], df[1], on='id', suffixes=('_1', '_2'))
        df3 = df[2].add_suffix('_3').rename(columns={'id_3': 'id'})
        names = [f'name_patch_{x}' for x in [1, 2, 3]]
        return pd.merge(df12, df3, on='id').drop(names, axis=1)


    # other df
    @cached_property
    def df_patch_roi_to_patch_mos(self): # image + 1 patch label
        return self.df_all[['name_image', 'bottom_image', 'right_image',
                        'name_patch', 'mos_patch',
                        'top_patch', 'left_patch', 'bottom_patch', 'right_patch']].dropna()

    @cached_property
    def df_unique_size(self):
        # assume there are no duplicate images, otherwise they will be dropped
        return self.df[list(data.size_cols)].drop_duplicates(keep=False)
