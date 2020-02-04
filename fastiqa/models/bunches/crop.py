from .regression import *
from fastai.vision import *  # ImageList

"""
# %%
%matplotlib inline
from fastiqa.bunches.crop import *
from fastiqa.labels import *
data = MultiCropIm2MOS(CLIVE, n_crops=2)
data
# %%
MultiCropIm2MOS(KonIQ, n_crops=3, crop_sz=100)
"""

# fixed top left crop: crop(size=self.img_crop_size, row_pct=0, col_pct=0)
# random crop: crop(size=self.img_crop_size, row_pct=(0., 1.), col_pct=(0., 1.))


class RandCrop2MOS(Im2MOS):
    img_crop_size = 227

    def get_augment(self, data):
        tfms = [crop(size=self.img_crop_size, row_pct=(0., 1.), col_pct=(0., 1.))]
        return data.transform([tfms, tfms], resize_method=ResizeMethod.NO)


"""
When putting into batches,
we make a multi-channel image with #channel = #crops * 3
since it's easy to reshape to [#batch, #crops, #channel, height, width]
on the model side, see models.MultiCropModel
and therefore no need to change the collate function

When displaying,
we arrange patches vertically
"""


class MultiCropImageList(ImageList):
    n_crops = 32
    crop_sz = 32

    # data is normalized from [0,1] to [-1, 1]: -1+2*self.img2.data
    # check CLIVE().train_ds[0][0].data, it's ranged [0, 1]
    def open(self, fn: PathOrStr) -> Image:
        img = super().open(fn)
        tfms = crop(size=self.crop_sz, row_pct=(0., 1.), col_pct=(0., 1.))
        patches = [img.apply_tfms(tfms).data for _ in range(self.n_crops)]
        # # 3, H, W
        # # 0, 1, 2
        # return vision.Image(px=torch.cat(patches, 1))

        # multi-channel images
        return vision.Image(px=torch.cat(patches, 0))

    def reconstruct(self, t: Tensor):
        """for viewing only"""
        # [n*3, H, W] --> [n, 3, H, W] --> [3, n, H, W] --> [3, n*H, W]
        "Reconstruct one of the underlying item for its data `t`."
        t = t.reshape(-1, 3, t.size(-2), t.size(-1)).transpose(0, 1)
        t = t.reshape(3, -1, t.size(-1))
        return Image(t.float().clamp(min=0, max=1))


class MultiCropIm2MOS(Im2MOS):
    n_crops = 32
    crop_sz = 32

    # build a class dynamically: self.cls ==
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        name = f'Patch{self.crop_sz}_{self.n_crops}Crops'
        self.data_cls = type(name, (MultiCropImageList,),
                             {"n_crops": self.n_crops,
                              "crop_sz": self.crop_sz,
                              })
