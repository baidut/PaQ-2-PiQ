

class PadedRoisLabel(RoisLabel):
    def create_csv_labels(self):


    def shift_rois(self):
        """
        shift rois according to the padding
        :return:
        """
        # df = pd.read_csv('data/FLIVE640/labels_image_3patch_pad640.csv')
        df = self.df
        top_shift = (640 - df['height_image']) // 2
        left_shift = (640 - df['width_image']) // 2

        prefix = ['top', 'left', 'bottom', 'right', 'height', 'width']
        suffix = ['_image', '_patch_1', '_patch_2', '_patch_3']
        types = {p + s: int for p in prefix for s in suffix}

        for s in suffix:
            df['top' + s] += top_shift
            df['left' + s] += left_shift
            df['bottom' + s] = df['top' + s] + df['height' + s]
            df['right' + s] = df['left' + s] + df['width' + s]
        return df
        # df.to_csv('data/FLIVE640/labels_image_3patch_pad640.csv')
        # df.astype(types).head()
