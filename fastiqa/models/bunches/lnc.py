from torchvision import transforms
from fastai.vision import *
from scipy.signal import convolve2d
import PIL.Image as PIL_Image
from .regression import *


def test_patch_collate():
    """
    fastai will supress the collate_fn error if it fails.
    so here we build a test
    ====
    from fastiqa.data.FLIVE640 import test_patch_collate
    test_patch_collate()
    """

    # from .CLIVE import CLIVE
    # ds = CLIVE().valid_ds

    # ds = FLIVE().train_ds # will pop out a warning, don't worry
    # samples = [ds[0], ds[1], ds[2], ds[4]]

    self = FLIVE()
    idx = next(iter(self.train_dl.batch_sampler))
    samples, fails = [], []
    for i in idx:
        samples.append(self.train_dl.dataset[i])

    im_b, mos_b = Collator().collate(samples)
    print(im_b.size(), mos_b.size())
    # torch.Size([4, 32, 3, 32, 32]) torch.Size([4, 1])


def apply_lcn(patch, P=3, Q=3, C=1):
    """
    Local contrast normalization (LCN)

    both input output are numpy
    :param patch:
    :param P:
    :param Q:
    :param C:
    :return:
    """
    # patch = patch.numpy()
    kernel = np.ones((P, Q)) / (P * Q)
    patch_mean = convolve2d(patch, kernel, boundary='symm', mode='same')
    patch_sm = convolve2d(np.square(patch), kernel, boundary='symm', mode='same')
    patch_std = np.sqrt(np.maximum(patch_sm - np.square(patch_mean), 0)) + C
    return (patch - patch_mean) / patch_std
    # patch_ln = torch.from_numpy((patch - patch_mean) / patch_std).float().unsqueeze(0)


# create a new object is more efficient
# don't use ImageList, use PatchList
# TODO now we are PIL-->tensor-->PIL-->tensor, very inefficient
#  Use RoIPool is a solution

@dataclass
class Collator:
    crop_sz: Optional[Union[int, TensorImageSize]] = 32  # (32, 32)
    n_patches: int = 32

    def collate(self, samples):
        '''
        :param samples: a list sized bs of (Image, MOS)
        :param pad_idx:
        :return: [bs, 32, 3, 32, 32], [bs 1]
        '''
        # print('Warning: custom collate fn is called')

        # print(len(samples), samples[0],  samples[1])
        # 16 (Image (3, 375, 500), FloatItem 68.29045) (Image (3, 353, 640), FloatItem 78.1787)
        ls = []
        tfm = rand_crop()
        for s in samples:
            img = s[0]
            # [3, 32, 32]
            # img = self.proc_pil_image(transp(img))
            patches = [img.apply_tfms(tfm, size=self.crop_sz).data for _ in range(self.n_patches)]
            patches = torch.stack(patches, dim=0)  # [32, 3, 32, 32]
            ls.append(patches)

        scores = [tensor(s[1].data[None]) for s in samples]
        return torch.stack(ls), torch.stack(scores)
        # grayscale torch.Size([16, 32, 32, 32]) torch.Size([16, 1]) if remove LocalNormalization unsqueeze
        # torch.Size([16, 32, 1, 32, 32]) torch.Size([16, 1])

# TODO make LNC model side, here use fastai to convert to grayscale
class LCNCollator(Collator):
    def proc_pil_image(self, img):
        """
        input and output are pil images
        :param img:
        :return:
        """
        img = img.convert('L')  # grayscale PIL image
        img = np.array(img)
        return PIL_Image.fromarray(img)

    def proc_pil_patch(self, img):
        """
        input and output are pil images
        :param img:
        :return:
        """
        img = np.array(img)
        img = apply_lcn(img)  # numpy image
        return PIL_Image.fromarray(img)

    def collate(self, samples):
        '''
        :param samples: a list sized bs of (Image, MOS)
        :param pad_idx:
        :return: [bs, 32, 3, 32, 32], [bs 1]
        '''
        # def patch_collate(samples, pad_idx=0):
        "Function that collect samples and adds padding."

        # print('Warning: custom collate fn is called')
        # transp = transforms.ToPILImage()
        # size=self.im_crop_size

        transt = transforms.ToTensor()
        transp = transforms.ToPILImage()
        img2patch = transforms.RandomCrop(size=(32, 32) ) # self.crop_sz
        # print(len(samples), samples[0],  samples[1])
        # 16 (Image (3, 375, 500), FloatItem 68.29045) (Image (3, 353, 640), FloatItem 78.1787)
        ls = []
        for s in samples:
            img = s[0].data
            # [3, 32, 32]
            img = self.proc_pil_image(transp(img))
            patches = []
            for _ in range(self.n_patches):
                p = img2patch(img)
                # torch.Size([1, 32, 32])
                # .float().unsqueeze(0)
                p = self.proc_pil_patch(p)
                patches.append(transt(p))
            patches = torch.stack(patches, dim=0)  # [32, 3, 32, 32]
            ls.append(patches)

        scores = [tensor(s[1].data[None]) for s in samples]
        return torch.stack(ls), torch.stack(scores)
        # grayscale torch.Size([16, 32, 32, 32]) torch.Size([16, 1]) if remove LocalNormalization unsqueeze
        # torch.Size([16, 32, 1, 32, 32]) torch.Size([16, 1])


class CropData(Im2MOS):
    collator = Collator()

    def get_bunch(self, data, **kwargs):
        return data.databunch(bs=self.batch_size,
                              collate_fn=lambda x: self.collator.collate(x), **kwargs)


"""
aka Divisive normalization
Local contrast normalization (LCN) is a method used to normalize the contrast of an image in a non-linear way.
Instead of performing a global normalization based on the range of values of the entire image,
LCN operates on local patches of the image on a per pixel basis. This can be done by removing
the mean of a neighborhood from a particular pixel and dividing by the variation of the pixel values.
(This should sound familiar to generating a zero mean and unit variance Gaussian)

This method can be associated with the concept of local receptive fields in mammalian vision.
Think of a brain neuron which is only connected to a spatially local amount of visual receptor neurons.
So insofar as local patches go, distant patches don't have as much (if any) contribution
to a given patch of the visual field.
https://www.quora.com/What-is-local-contrast-normalization-in-computer-vision
"""


class LCNCropData(CropData):
    collator = LCNCollator()
