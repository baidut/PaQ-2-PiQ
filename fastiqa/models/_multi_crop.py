
import torch
from . import IqaModel
from .bunches.crop import MultiCropIm2MOS

"""
patch based models

# %% Test forward patch
%matplotlib inline
from fastiqa.basics import *

class TestMultiCropModel(MultiCropModel):
    n_crops=4
    crop_sz=200
    def forward(self, t):
        print(t.size())
        p = tensor2patches(t)
        show_batch(p[0])
        return 1

IqaLearner.from_cls(CLIVE, TestMultiCropModel).pred_batch()
Im2MOS(CLIVE).show_batch(1, DatasetType.Valid)

# %%
IqaLearner.from_cls(FLIVE, TestMultiCropModel).pred_batch()
Im2MOS(FLIVE).show_batch(1, DatasetType.Valid)
# %%
data = MultiCropIm2MOS(CLIVE, n_crops=9, crop_sz=100)
model = TestMultiCropModel()
IqaLearner(data, model).pred_batch()
# %%
"""


def tensor2patches(t):
    "for grayscale image, t = [bs, n_crops, 1, H, W]"
    "[bs, n_crops*C, H, W] --> [bs, n_crops, C, H, W]"

    n_dim = len(t.size())
    if n_dim is 5: return t
    assert(n_dim is 4 and t.size(1) % 3 == 0)
    return t.reshape(t.size(0), -1, 3, t.size(-2), t.size(-1))


class MultiCropModel(IqaModel):
    crop_sz = (32, 32)
    n_crops = 32

    @classmethod
    def bunch(cls, label, **kwargs):
        return MultiCropIm2MOS(label, n_crops=cls.n_crops, crop_sz=cls.crop_sz, **kwargs)

    def forward(self, t):
        """
        :param t: [bs, n_crops*C, H, W] or [bs, n_crops, C, H, W]
        :return:  [n_image, n_labels] or [n_image] when n_labels == 1
        """
        if self.n_crops == 1: return self.forward_patch(t)
        patches = tensor2patches(t)
        bs = patches.size(0)
        x = [self.forward_crops(patches[n]) for n in range(bs)]
        return torch.stack(x, 0).squeeze()

    def forward_crops(self, x):
        "return [n_labels] for N crops from 1 image [N, 3, H, W]"
        raise NotImplementedError


"""
References:
https://discuss.pytorch.org/t/how-to-extract-smaller-image-patches-3d/16837/9
"""
