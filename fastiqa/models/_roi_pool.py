import sys, os

########################## ROIPOOL<
# import sys, os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/faster-rcnn.pytorch/lib")
# from model.roi_layers import ROIPool, ROIAlign  # PyTorch 1.0 specific!
########################## >ROIPOOL

# from .roi_layers import ROIPool, ROIAlign  # PyTorch 1.0 specific!

# TODO: conditional import
from torchvision.ops import RoIPool, RoIAlign
# from ._ops_roi_pool import *

from .bunches._rois import Rois0123
from ._body_head import BodyHeadModel, num_features_model

# from .prroi_pool import PrRoIPool2D
from fastai.vision import *  # Tensor





def get_idx(batch_size, n_output, device=None):  # idx of rois
    idx = torch.arange(batch_size, dtype=torch.float, device=device).view(1, -1)
    # 1 scores: idx = idx.t()
    # 4 scores: idx = torch.cat((idx, idx, idx, idx), 0).t()
    idx = idx.repeat(n_output, 1, ).t()
    idx = idx.contiguous().view(-1, 1)
    return idx  # .cuda()


def bbox2xyhw(bboxes, height, width):
    # Note that fastai gives percentage, not the coord
    # also pls concern the limitation
    # [16, n_output, 4]
    # b = torch.squeeze(bboxes, 1).t()
    # first remove negative values
    b = bboxes.view(-1, 4).t()
    top, left, bottom, right = b[0], b[1], b[2], b[3]
    x, y = (left + 1) * width // 2, (top + 1) * height // 2
    h, w = (bottom - top) * height // 2, (right - left) * width // 2
    return torch.cat((x, y, h, w), 0).view(4, -1).t()


# TODO multiscale
# also image score
def get_blockwise_rois(blk_size, img_size=None):  # [height, width]
    """
    a = get_blockwise_rois([3, 4], [400, 500])
    len(a), a

    :param blk_size:
    :param img_size: [height width]
    :return: a 1d list [x1, y1, x2, y2, x1, y1, x2, y2, ... ]
    """

    if img_size is None: img_size = [1, 1]
    y = np.linspace(0, img_size[0], num=blk_size[0] + 1)
    x = np.linspace(0, img_size[1], num=blk_size[1] + 1)
    # careful about the order of m, n! x increase first, so it's in inner loop
    a = []
    for n in range(len(y) - 1):
        for m in range(len(x) - 1):
            a += [x[m], y[n], x[m + 1], y[n + 1]]
    return a


def get_rand_rois(self, img_size, batch_size, device):
    """
    # idx with rois
    # %%

    # %%
    """
    h, w = img_size
    n = self.n_crops
    patch_h, patch_w = self.crop_sz
    # https://github.com/pytorch/pytorch/issues/10655
    sz = [batch_size * n, 1]
    x1 = torch.empty(sz, dtype=torch.float, device=device).uniform_(0, w - patch_w)
    y1 = torch.empty(sz, dtype=torch.float, device=device).uniform_(0, h - patch_h)
    # RoIPool will use interger
    # output size is 32x32
    x2 = x1 + patch_w
    y2 = y1 + patch_h
    rois = torch.cat((x1, y1, x2, y2), 1)
    idx = get_idx(batch_size, n, device)
    # print(rois.size(), idx.size()) [128, 4] [128, 1]
    return torch.cat((idx, rois), 1)


class NoRoIPoolModel(BodyHeadModel):
    # also use padded image
    # bunch opt
    # label_

    @classmethod
    def get_label_opt(cls, label_cls):
        # fixed size
        if label_cls.img_raw_size is not None:
            return {}
        elif label_cls.img_pad_size is None:
            return {'val_bs': 1}
        else: # use padded data
            return {'folder': '<=640_padded',
                'csv_labels': 'labels<=640_padded.csv'}


class RoIPoolModel(NoRoIPoolModel):
    rois = None
    drop = 0.5
    pool_size = (2, 2)
    joint = False
    bbox2xyhw = False
    bunch_type = Rois0123

    def create_head(self):
        nf = num_features_model(self.body) * 2
        if self.joint:
            return create_head(nf * 4, 4)
        else:
            return create_head(nf, 1)

    def create_roi_pool(self):
        # see #64
        if self.backbone.__name__ == 'resnet18':
            return RoIPool(self.pool_size, 1 / 32)
        else:
            raise NotImplementedError

    def __init__(self):
        super().__init__()
        self.roi_pool = self.create_roi_pool()

    def input_fixed_rois(self, rois=None, img_size=None, batch_size=1, include_image=True, cuda=True):
        """

        Note: img_size = (height, width)
        rois = np.array([324, 321, 733, 594, 701, 330, 1008, 534, 63, 259, 267, 395], np.float32)
        rois[::2] /= 1024
        rois[1::2] /= 768
        rois
        """
        if img_size is None:
            img_size = [1, 1]

        if rois is None:
            rois = [0.316406, 0.417969, 0.71582, 0.773438,
                    0.68457, 0.429688, 0.984375, 0.695312,
                    0.061523, 0.33724, 0.260742, 0.514323]
        rois = np.array(rois).reshape(-1, 4)
        rois[:, 0::2] *= img_size[1]
        rois[:, 1::2] *= img_size[0]
        a = [0, 0, img_size[1], img_size[0]] if include_image else []
        a += rois.reshape(-1).tolist()  # 1 dim list
        t = tensor(a)
        if cuda:
            t = t.cuda()
        self.rois = t.unsqueeze(0).repeat(batch_size, 1, 1).view(batch_size, -1)

    def input_block_rois(self, blk_size=None, img_size=None, batch_size=1, include_image=True, cuda=True):
        # same for each item in a batch , so repeat it with batch size
        """
        blk_size = 32x32, then output  [1, (32*32+1)*4]
        [375, 500] to [12, 16] no need to bigger than 16x16
        :param blk_size:
        :param img_size:
        :param batch_size:
        :param include_image:
        :return:
        """
        if img_size is None:
            img_size = [1, 1]
        if blk_size is None:
            blk_size = [[2, 2], [4, 4], [8, 8], [16, 16]]

        a = [0, 0, img_size[1], img_size[0]] if include_image else []
        for sz in blk_size:
            a += get_blockwise_rois(sz, img_size)
        t = tensor(a)
        if cuda:
            t = t.cuda()
        self.rois = t.unsqueeze(0).repeat(batch_size, 1, 1).view(batch_size, -1)
        # self.scale_rois = (img_size == 1)
        # https://discuss.pytorch.org/t/repeat-examples-along-batch-dimension/36217/3

    def forward(self, im_data: Tensor, rois_data: Tensor = None, labels: Tensor = None, **kwargs) -> Tensor:
        base_feat = self.body(im_data)  # torch.Size([16, 512, 12, 16])
        """
        [375, 500] to [12, 16]
        16/500,  12/375
        = 0.032
        """
        # the image shrinks! the position is wrong
        # print(base_feat.size())

        # TODO note when printing learn.summary batch size == 1
        batch_size = im_data.size(0)  # 16 or less if not enough image to pack
        if self.rois is None and rois_data is not None:
            if self.bbox2xyhw:
                bboxes, labels = rois_data
                height, width = im_data.size(2), im_data.size(3)
                rois_data = bbox2xyhw(bboxes, height, width)  # torch.Size([16, 4])
            else:
                rois_data = rois_data.view(-1, 4)
            # bboxes: torch.Size([16, n_output, 4])
            # print(bboxes); print(bboxes.size())
            # print(xyhw, xyhw.size())  # [16*n_output, 4]  % torch.Size([16, 4])
            # xyhw = xyhw.view(-1,4)
        else:
            rois_data = self.rois.view(-1, 4)  # provide rois to predict patch quality map
        # print(rois)
        """
        idx: [bs*n_rois, 1]
        rois_data: [bs*n_rois, 4]
        indexed_rois: [bs*n_rois, 5]
        """
        n_output = int(rois_data.size(0) / batch_size)
        idx = get_idx(batch_size, n_output, im_data.device)  # torch.Size([16, n_output])
        # print(n_output, batch_size, idx.size(), rois_data.size())
        indexed_rois = torch.cat((idx, rois_data), 1)
        pooled_feat = self.roi_pool(base_feat, indexed_rois)

        if self.joint:
            pooled_feat = pooled_feat.view(batch_size, -1, self.roi_pool_size[0], self.roi_pool_size[1])

        # print(batch_size, pooled_feat.size()) # ([1, 2048, 2, 2])
        pred = self.head(pooled_feat)
        # print(pred.size())
        # print(base_feat.size())  # [bs, 512, 20, 20]
        # print(pooled_feat.size()) # [bs*n_rois, 512, 2, 2]
        # print(n_output)  # n_rois
        # print(pred.size())  # torch.Size([bs*n_rois, 1])

        return pred.view(batch_size, -1)  # 1 scores or 4 scores
