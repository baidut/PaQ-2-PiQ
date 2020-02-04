from ._roi_pool import *

# Feed4Scores
# currently, feedback both image and patch scores to refine
# TODO: only feed back patch scores (need to separate the rois)
class FeedbackModel(RoIPoolModel):
    contain_image_roi = True
    refine_image_score = True


    # TODO support n input (quality map as input, exactly the same model)
    @staticmethod
    def split_on(m):
        return [[m.body], [m.patch_head, m.image_head]]

    def __init__(self, drop=0.5, **kwargs):
        super().__init__()
        self.image_pool = nn.Sequential(*([AdaptiveConcatPool2d(), Flatten()]))
        self.patch_pool = ROIPool((2, 2), 1 / 32)
        nf = num_features_model(self.body) * 2

        n_output = 1  # 1 image score
        self.patch_head = create_head(nf, 1)

        n_rois = 4 if self.contain_image_roi else 3  # TODO later it will change

        self.image_head = nn.Sequential(*(
                bn_drop_lin(nf + n_rois, 512, bn=True, p=drop, actn=nn.ReLU(inplace=True))
                + bn_drop_lin(512, n_output, bn=True, p=drop, actn=None))
                                        )
        self.__dict__.update(kwargs)

    def create_head(self):
        return None  # no param for old head

    #TypeError: forward() takes 2 positional arguments but 3 were given
    def forward(self, im_data: Tensor, rois_data: Tensor=None, **kwargs) -> Tensor:
        """
        if only image_roi, then rois_data [bs, 4]

        """
        # n_rois = 3  # 3 patch rois
        use_fixed_rois = rois_data is None or rois_data.size(1) == 4

        batch_size = im_data.size(0)  # may change (last batch)
        idx = get_idx(batch_size, 4)  # n_roi = 4

        # if no rois_data or only image_roi_data is provided
        if use_fixed_rois:  # Rois0123 rois_data.size(1) == 4*4

            self.input_fixed_rois(img_size=[im_data.size(-2), im_data.size(-1)], batch_size=batch_size)
            # self.input_block_rois([[1, 3]], [im_data.size(-2), im_data.size(-1)], batch_size=batch_size)
            rois_data = self.rois

        base_feat = self.body(im_data)

        # TODO, dont use FloatItemList, or use two FloatItemList

        # print(rois_data.size())
        if self.contain_image_roi:
            # the first 4 columns correspond to image_rois_data
            rois_image = rois_data.view(batch_size, -1).clone()[:, :4].reshape(-1, 4)
            image_idx = torch.arange(batch_size, dtype=torch.float).view(1, -1).t().cuda()
            rois_image = torch.cat((image_idx, rois_image), 1)
            # patch use all 4 but update one

        # print(rois_data.size(), rois_image.size(), idx.size())
        # torch.Size([80, 16]) torch.Size([80, 5]) torch.Size([80, 1])

        rois_data = rois_data.view(-1, 4)
        # print(rois_data.size(), rois_image.size(), idx.size())
        rois = torch.cat((idx.cuda(), rois_data), 1)

        patch_feat = self.patch_pool(base_feat, rois)

        if self.contain_image_roi:
            # image features are computed without padding (image_roi is required)
            pool_feat = self.patch_pool(base_feat, rois_image)
            image_feat = self.image_pool(pool_feat)
        else:
            image_feat = self.image_pool(base_feat)

        patch_pred = self.patch_head(patch_feat).view(batch_size, -1)
        # [bs 3]  [bs 1024]
        # torch.Size([192, 1]) torch.Size([64, 1024])
        # print(patch_pred.size(), image_feat.size())

        # patch_feat = patch_pred.repeat(1, 256)  # 1024/4 otherwise the model will tend to ignore them
        if not self.contain_image_roi:
            patch_pred = patch_pred[:, 1:]   # drop image scores

        concat_feat = torch.cat((image_feat, patch_pred), 1)
        image_pred = self.image_head(concat_feat)

        # it can also extract patch quality map but no better
        if use_fixed_rois:
            return image_pred
        else:
            if self.contain_image_roi:
                # update
                patch_pred[:, ::4] = image_pred
                return patch_pred
            else:
                return torch.cat((image_pred, patch_pred), 1)
        # stage 2: only output image score
