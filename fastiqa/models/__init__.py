import torch
import torch.nn as nn
import torch.nn.functional as F

from .utils import *


class IqaModel(nn.Module):
    __name__ = None

    def __init__(self):
        super().__init__()
        if self.__name__ is None: self.__name__ = self.__class__.__name__

    @classmethod
    def bunch(self, label, **kwargs):
        raise NotImplementedError
