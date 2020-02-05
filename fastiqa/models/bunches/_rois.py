from .regression import *
from fastai.vision import *



"""


# %%
%matplotlib inline
from fastiqa.labels import *
from fastiqa.bunches.rois import *
# %%
Rois0123(FLIVE640)
df = Rois0123(FLIVE).show('blur_dataset/motion0001.jpg')
Rois0123(FLIVE).show('voc_emotic_ava/EMOTIC__0yp3ixisn6pvw3uoph.jpg')
Rois0123(FLIVE640).show('voc_emotic_ava/AVA__376479.jpg')

# %% for debugging
from fastiqa.labels import *
from fastiqa.bunches.rois import *
Rois0123(FLIVE).get_data()
# %%


"""


"""
ImageXYHWList renamed to ImageRoisList


The COCO bounding box format is [top left x position, top left y position, width, height]
// For each ROI R = [batch_index x1 y1 x2 y2]: max pool over R
h_start, w_start, h_end, w_end
:param rois: (1, N, 4) N refers to bbox num, 4 represent (ltx, lty, w, h)
"""


def xyhw2bboxes(xyhw):
    """
    xyhw = [[1, 2, 3, 4], [5, 6, 7, 8]]
    xyhw2bboxes(xyhw)
    [[1, 2, 5, 5], [5, 6, 13, 13]]
    :param xyhw:
    :return:
    """
    t = np.array(xyhw).T
    x, y, h, w = t[0], t[1], t[2], t[3]
    left, top = x, y
    right, bottom = x + w, y + h
    return np.array([top, left, bottom, right]).T.tolist()


def rois2bboxes(rois):
    """
    https://medium.com/@andrewjong/how-to-use-roi-pool-and-roi-align-in-your-neural-networks-pytorch-1-0-b43e3d22d073
    image_id, upper_left_x, upper_left_y, lower_right_x, lower_right_y
    # left, top, right, bottom
    LTRB
    :param xyhw:
    :return:
    """
    t = np.array(rois).T
    left, top, right, bottom = t[0], t[1], t[2], t[3]
    return np.array([top, left, bottom, right]).T.tolist()


class ImageRoisList(MixedItemList):  # ImageXYHWList
    classes = ['image', 'patch1', 'patch2', 'patch3']

    def reconstruct(self, t: Tensor):
        "Reconstruct one of the underlying item for its data `t`."

        """
        torch.Size([3, 500, 500]) torch.Size([4])
        """
        image = Image(t[0].float().clamp(min=0, max=1))
        bboxes = rois2bboxes(t[1].view(-1, 4).tolist())
        if len(bboxes) <= len(self.classes):
            labels = list(range(len(bboxes)))  # [n for n in range(len(bboxes))]
        else:
            labels = [1]*len(bboxes)
        imageBBox = ImageBBox.create(t[0].size()[1], t[0].size()[2], bboxes, labels, classes=self.classes)
        return image, imageBBox

    # TODO directly call method of other class
    def show_xys(self, xs, ys, imgsize: int = 4, figsize: Optional[Tuple[int, int]] = None, **kwargs):
        "Show the `xs` and `ys` on a figure of `figsize`. `kwargs` are passed to the show method."
        rows = int(np.ceil(math.sqrt(len(xs))))
        axs = subplots(rows, rows, imgsize=imgsize, figsize=figsize)
        for x, y, ax in zip(xs, ys, axs.flatten()): x[0].show(ax=ax, y=x[1], title=f'{str(y)}', **kwargs)
        for ax in axs.flatten()[len(xs):]: ax.axis('off')
        plt.tight_layout()


class Rois0123(Im2MOS):
    label_col_idx = slice(None)  # all cols
    data_cls = ImageRoisList
    def get_list(self):
        # cont_names = ['zero', 'zero', *self.size_cols]  # 'top', 'left', 'left', 'right'
        img_list = ImageList.from_df(self.df, path=self.path, cols=self.fn_col, folder=self.folder)
        roi_list = FloatList.from_df(self.df, path=self.path, cols=self.rois_cols)
        return self.data_cls([img_list, roi_list], self.path, inner_df=img_list.inner_df)

    def get_augment(self, data):
        """
        tfms = get_transforms(max_zoom=1.05, max_rotate=5.0, p_affine=0, p_lighting=0)
        if self.do_augment:
            mixed_tfms = [[tfms[1], tfms[1]], [tfms[1], tfms[1]]]
        else:
            mixed_tfms = [[tfms[0], tfms[0]], [tfms[1], tfms[1]]]  # if self.valid_pct > 0 else [[tfms[0], tfms[0]], None]
        return data if self.no_tfms else data.transform(mixed_tfms, size=ifnone(self.img_size, 500))
        """
        if self.img_tfm_size is None:
            return data
        else:
            #  ([], [])
            # tfms = get_transforms(max_zoom=1.05, max_rotate=5.0, p_affine=0, p_lighting=0)
            # mixed_tfms = [[tfms[1], tfms[1]], [tfms[1], tfms[1]]]
            mixed_tfms = [[[], []], [[], []]]
            return data.transform(mixed_tfms, size=self.img_tfm_size)

class Rois2MOS(Rois0123):
    pass # make sure old API still works
