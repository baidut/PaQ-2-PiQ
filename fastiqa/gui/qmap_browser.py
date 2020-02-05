# from ..learner import IqaLearner
# from ..rois.learner import RoIPoolLearner
# from ..models.PaQ2PiQ import RoIPoolModel, Rois0123
# from ..iqa_exp import IqaExp
# # from fastai.vision import *  # AttributeError: type object 'Image' has no attribute 'fromarray'
# from ..labels import *
# from ..models.bunch.regression import Im2MOS
# # from ..models.raw_resnet import *

from ..all import *

# load PIL last to avoid AttributeError: type object 'Image' has no attribute 'fromarray'
from .browser import Browser
import matplotlib.pyplot as plt

import numpy as np
from PIL import Image as PIL_Image

"""
# %%
from fastiqa.gui import *
from fastiqa.gui.qmap_browser import *; QmapBrowser(CLIVE)
from fastiqa.gui.qmap_browser import *; QmapBrowser(KonIQ)
from fastiqa.gui.qmap_browser import *; QmapBrowser(TestImages)
#  Browser(FLIVE640)
from fastiqa.gui import *; Browser(TestImages)
# %%
from fastiqa.bunches.rois import *;
from fastiqa.labels import *;
# Rois0123(FLIVE640).data
# Rois0123(TestImages, batch_size=1).data  BUG
Im2MOS(TestImages, batch_size=1).data
# Rois0123(TestImages, batch_size=1).data
"""


# https://stackoverflow.com/questions/53509131/tkinter-saving-canvas-at-wrong-scale
def open_eps(ps, dpi=300.0):
    img = PIL_Image.open(BytesIO(ps.encode('utf-8')))
    original = [float(d) for d in img.size]
    scale = dpi/72.0
    if dpi is not 0:
        img.load(scale = math.ceil(scale))
    if scale != 1:
        img.thumbnail([round(scale * d) for d in original], PIL_Image.ANTIALIAS)
    return img


class QmapBrowser(Browser):
    """

    grayscale image --> jet color image
    https://stackoverflow.com/questions/43457308/is-there-any-good-color-map-to-convert-gray-scale-image-to-colorful-ones-using-p

    blend images
    https://stackoverflow.com/questions/5324647/how-to-merge-a-transparent-png-image-with-another-image-using-pil

    maybe I should have used matplotlib as backend?
    """
    # hide_scores = True
    mos_range = [40, 80]
    opt_alpha = [0.8, 1, 0]
    out_dir = Path('data/TestImages')
    opt_resample = np.array([PIL_Image.BILINEAR, PIL_Image.NEAREST, PIL_Image.BICUBIC])
    opt_blk_size = np.array([[32, 32], [16, 16], [8, 8], [4, 4]])

    # show_qmap = False  # must be false during __init__, can be updated later
    # img_proc = lambda x: x  # custom post proc?
    learner = None

    def __init__(self, label, learner: IqaLearner = None, **kwargs):
        super().__init__(label, **kwargs)
        if learner is None:
            #e = IqaExp('!exp/plcc=0.441', gpu=0)
            #e += RoIPoolLearner(Rois0123(FLIVE640, batch_size=100), RoIPoolModel())
            e = IqaExp('!exp/plcc=0.435/seed=0/CVPR2020/fit(10,bs=120)', seed=0)
            e += RoIPoolLearner(Rois0123(FLIVE), RoIPoolModel())

            e.load()
            learner = e['RoIPoolModel']

            # e += IqaLearner(FLIVE640(batch_size=100), NoRoIPoolModel())
            # e.load()
            # learner = e['NoRoIPoolModel']
            # print('NoRoIPoolModel is loaded.')
            learner.data = Im2MOS(TestImages, batch_size=1) # Im2MOS(TestImages)

        self.learner = learner
        self.__dict__.update(kwargs)

    def on_key(self, event):
        super(QmapBrowser, self).on_key(event)
        if event.char is 'm':  # map # image process
            # self.apply_img_proc = not self.apply_img_proc
            self.show_qmap = not self.show_qmap
            self.show()
        elif event.char is 'a':
            self.opt_alpha = np.roll(self.opt_alpha, 1)
            self.show()
        elif event.char is 'i':  # i
            self.opt_resample = np.roll(self.opt_resample, 1)
            self.show()
        elif event.char is 'b':  # save capture
            self.opt_blk_size = np.roll(self.opt_blk_size, 1)
            self.show()
        elif event.char is 'c':  # save capture
            self.copy_sample()


    def copy_sample(self):
        # avoid IsADirectoryError: [Errno 21] Is a directory: 'data/TestImages/5235142622.jpg'
        name = str(self.out_dir / self.abbr / (self.fn.rsplit('.', 1)[0]))
        dir = name.rsplit('/', 1)[0]
        if not os.path.exists(dir):
            os.makedirs(dir)
        # TODO remove those dirty code
        #  mos_image
        # save original files
        img = PIL_Image.open(self.path / self.folder / self.fn)
        img.save(name + '.jpg')

        self.img.save(name + '_qmap.jpg')

        # save label information
        self.canvas.postscript(colormode='color', file=name + '_labels.eps')
        ps = self.canvas.postscript(colormode='color')
        img = open_eps(ps, dpi=119.5)  #PIL_Image.open(io.BytesIO(ps.encode('utf-8')))
        img.save(name + '_labels.jpg')

        # save scores
        # mos = self.df['mos_image'][self.index]
        label_file = self.out_dir / 'labels.csv'
        df = pd.read_csv(label_file)
        df = df.append(self.df.iloc[self.index].to_dict(), ignore_index=True)  # {'name': self.fn, 'mos': mos}
        df.to_csv(label_file, index=False)


    def open_image(self, file):
        # raw_im = super().open_image(file)
        # width, height = raw_im.size
        fastai_im = vision.open_image(file)
        qmap = self.learner.predict_quality_map(fastai_im, self.opt_blk_size[0].tolist())
        self.pred = qmap.global_score
        # qmap.img = super().open_image(file) # PIL image
        return qmap.blend(self.mos_range, alpha = self.opt_alpha[0], resample=self.opt_resample[0])
