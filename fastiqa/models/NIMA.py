import torch.nn as nn
from torchvision.models.mobilenet import mobilenet_v2
from fastai.vision.learner import num_features_model, models
from ._body_head import BodyHeadModel
from .bunches.crop import RandCrop2MOS

# https://github.com/baidut/FBIQA/wiki/NIMA


class NIMA(BodyHeadModel):
    n_output = 10
    backbone = models.vgg16_bn

    @classmethod
    def bunch(cls, label, **kwargs):
        return RandCrop2MOS(label,
                            img_crop_size=224,
                            folder='rescale-256',
                            **kwargs
                            )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))

    def create_head(self):
        # num_features_model is 512 for resnet18, is 1280 for mobilenet
        modules = [nn.ReLU(inplace=True),
                   nn.Dropout(p=0.75),
                   nn.Linear(num_features_model(self.body), self.n_output)]

        if self.n_output != 1:
            modules.append(nn.Softmax(dim=1))

        return nn.Sequential(*modules)  # 1280 for mobilenet: 224x224 --> 7x7

    # 1280
    def forward(self, x):
        # [50, 1280, 1, 1]
        # 256 × 256,
        x = self.body(x)  # torch.Size([50, 1280, 20, 20]) for [640x640
        # pool
        # print(x.size())  # torch.Size([50, 1280, 7, 7]) for [640x640
        x = self.avgpool(x)  # torch.Size([50, 1280, 1, 1])
        x = x.view(x.size(0), -1)  # torch.Size([50, 1280])
        # print(x.size())
        x = self.head(x)
        return x


class NIMA_o1(NIMA):
    n_output = 1
    backbone = mobilenet_v2


class NIMA_o1_resnet18(NIMA_o1):
    backbone = models.resnet18
