import matplotlib.pyplot as plt
import numpy as np
from PIL import Image as PIL_Image
from fastai.vision import image2np

class QualityMap:
    """Note here the image is fastai image"""
    def __init__(self, mat, img, global_score=0):
        self.mat, self.img = mat, img
        self.global_score = global_score

    @property
    def pil_image(self):
        return PIL_Image.fromarray((255 * image2np(self.img.px)).astype(np.uint8))

    def plot(self, vmin=0, vmax=100):
        fig, axes = plt.subplots(1, 3, figsize=(12, 8 * 3))

        # fastai image
        self.img.show(axes[0], title='Input image')  # title mos
        self.img.show(axes[1], title=f'Predicted: {self.global_score:.2f}')  # title prediction

        _, H, W = self.img.shape
        h, w = self.mat.shape  # self.mat.size()
        extent = (0, W // w * w, H // h * h, 0)

        axes[1].imshow(self.mat, alpha=0.8, cmap='magma',
                       extent=extent, interpolation='bilinear')
        axes[2].imshow(self.mat, cmap='gray', extent=extent,
                       vmin=vmin, vmax=vmax)
        axes[2].set_title(f'Quality map {h}x{w}')

    def _repr_html_(self):
        self.plot()
        return ''

    def savefig(self, filename):
        plt.savefig(filename, bbox_inches='tight')

    def blend(self, mos_range=(0, 100), alpha=0.8, resample=PIL_Image.BILINEAR):
        """qmap.blend().save('qmap.jpg')"""

        def stretch(image, minimum, maximum):
            if maximum is None:
                maximum = image.max()
            if minimum is None:
                minimum = image.min()
            image = (image - minimum) / (maximum - minimum)
            image[image < 0] = 0
            image[image > 1] = 1
            return image

        cm = plt.get_cmap('magma')
        # min-max normalize the image, you can skip this step
        qmap_matrix = self.mat
        if mos_range is not None:
            qmap_matrix = 100*stretch(np.array(qmap_matrix), mos_range[0], mos_range[1])
        qmap_matrix = (np.array(qmap_matrix) * 255 / 100).astype(np.uint8)
        colored_map = cm(qmap_matrix)
        # Obtain a 4-channel image (R,G,B,A) in float [0, 1]
        # But we want to convert to RGB in uint8 and save it:
        heatmap = PIL_Image.fromarray((colored_map[:, :, :3] * 255).astype(np.uint8))
        sz = self.img.shape[-1], self.img.shape[-2]
        heatmap = heatmap.resize(sz, resample=resample)

        return PIL_Image.blend(self.pil_image, heatmap, alpha=alpha)
