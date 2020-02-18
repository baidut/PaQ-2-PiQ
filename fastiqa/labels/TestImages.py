from ..label import *
from tqdm import tqdm
from fastai.vision import open_image
import os
from PIL import Image as PIL_Image

"""
# %%
from fastiqa.all import *
learn = RoIPoolLearner.from_cls(FLIVE, RoIPoolModel)
learn.path = Path('.')
learn.load('RoIPoolModel-fit(10,bs=120)')
learn.export('trained_model.pkl')

from fastiqa.all import *; # Im2MOS(TestImages(path='/var/www/yourapplication'))
data.df
# %%
"""

class TestImages(IqaLabel): # Rois0123Label
    path = '.'
    img_tfm_size = None
    valid_pct = 1
    batch_size = 1
    csv_labels = 'scores.csv'

    @classmethod
    def from_learner(cls, learn, path=None, dir_qmap=None, sz=None, **kwargs):
        def proc_file(f):
            im = open_image(os.path.join(path, f))
            if dir_qmap is not None:
                qmap = learn.predict_quality_map(im, [32, 32])

                name = os.path.basename(f).split('.')[0]

                qmap.plot()
                qmap.savefig(os.path.join(dir_qmap, name + '.jpg'))
                score = qmap.global_score

                if sz is not None:
                    height, width = qmap.img.size
                    new_width  = sz # 500
                    new_height = new_width * height // width
                    qmap.pil_image.resize((new_width, new_height), PIL_Image.ANTIALIAS).save(os.path.join(dir_qmap, name + '_raw.jpg'))
                    qmap.blend(mos_range=(None, None)).resize((new_width, new_height), PIL_Image.ANTIALIAS).save(os.path.join(dir_qmap, name + '_map.jpg'))
            else:
                score = learn.predict(im)[0].obj[0]
            del im
            del qmap
            return score


        if dir_qmap is not None:
            os.makedirs(dir_qmap, exist_ok=True)

        valid_images = (".jpg",".jpeg",".png",".bmp",".tif")
        files = os.listdir(path if path is not None else cls.path)
        files = [f for f in files if f.lower().endswith(valid_images)]
        scores = [proc_file(f) for f in tqdm(files)]
        df = pd.DataFrame({'mos': scores, 'name': files})
        df.to_csv('scores.csv', index=False)

        return cls(path=path)
    pass
