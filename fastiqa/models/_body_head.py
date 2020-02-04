from . import IqaModel
from .bunches.regression import Im2MOS
from fastai.vision import *
from fastai.vision.learner import num_features_model

"""
# %%
from fastiqa.models._body_head import *; BodyHeadModel()

# %%
from fastiqa.models._body_head import *
from fastiqa.basics import *
learn = IqaLearner(Im2MOS(FLIVE_8k), BodyHeadModel())
learn.summary()

# %%
"""


class BodyHeadModel(IqaModel):
    backbone = models.resnet18
    n_output = 1
    bunch_type = Im2MOS

    @classmethod
    def get_label_opt(cls, label):
        return {}

    @classmethod
    def bunch(cls, label_cls, bs=64, **kwargs):
        opt = cls.get_label_opt(label_cls)
        return cls.bunch_type(label_cls(**opt), batch_size=bs, **kwargs)

    @staticmethod
    def cut(m):
        return nn.Sequential(*list(m.children())[:-1])

    @staticmethod
    def split_on(m):
        return [[m.body], [m.head]]

    def create_body(self):
        try:
            return create_body(self.backbone)
        except StopIteration:
            return create_body(self.backbone, cut=self.cut)

    def create_head(self):
        nf = num_features_model(self.body) * 2
        return create_head(nf, self.n_output)

    def __init__(self, backbone=None, n_output=None):
        super().__init__()
        if backbone is not None:
            self.__name__ += f' ({backbone.__name__})'
            self.backbone = backbone
        if n_output is not None:
            self.n_output = n_output
        self.body = self.create_body()
        self.head = self.create_head()

    def forward(self, im_data: Tensor, *args, **kwargs) -> Tensor:
        base_feat = self.body(im_data)
        pred = self.head(base_feat)
        return pred.view(-1, self.n_output)
