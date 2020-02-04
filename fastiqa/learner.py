from .metric import *
from .qmap import *
from fastai.callbacks import *
from fastai.callbacks.hooks import layers_info


def abbreviate(x):
    abbreviations = ["", "K", "M", "B", "T", "Qd", "Qn", "Sx", "Sp", "O", "N",
                     "De", "Ud", "DD"]
    thing = "1"
    a = 0
    while len(thing) < len(str(x)) - 3:
        thing += "000"
        a += 1
    b = int(thing)
    thing = round(x / b, 2)
    return str(thing) + " " + abbreviations[a]


def img2patches(img_t, sz):
    n_patch_h, n_patch_w = sz
    patch_h = img_t.size(1) // n_patch_h
    patch_w = img_t.size(2) // n_patch_w
    patches = img_t.data.unfold(0, 3, 3).unfold(1, patch_h, patch_h).unfold(2, patch_w, patch_w)
    return patches.reshape([-1, 3, patch_h, patch_w])  # n_patch_h*n_patch_w


class IqaLearner(Learner):

    @classmethod
    def from_cls(cls, label, arch):
        data = arch.bunch(label)
        model = arch()
        return cls(data, model)

    def __post_init__(self):
        super().__post_init__()
        if not self.metrics:
            self.metrics = [SRCC(), LCC()]

        # [Discriminative layer training](https://docs.fast.ai/basic_train.html#Discriminative-layer-training)
        if hasattr(self.model, 'split_on'):
            self.split(self.model.split_on)

        self.callback_fns += [ShowGraph, partial(CSVLogger, append=True),
                              partial(SaveModelCallback, every='improvement',
                                      monitor=self.metrics[0].name)]

    def _repr_html_(self):
        print(self.summary())
        return

    @property
    def total_params(self):
        total_params = total_trainable_params = 0
        info = layers_info(self)
        for layer, size, params, trainable in info:
            if size is None: continue
            total_params += int(params)
            total_trainable_params += int(params) * trainable
        return {'Total params': total_params,
                'Total trainable params': total_trainable_params,
                'Total non-trainable params': total_params - total_trainable_params,
                'Summary': f'{abbreviate(total_trainable_params)} / {abbreviate(total_params)}'
                }

    # predict on database (cached) and get numpy predictions
    def get_np_preds(self, on=None, cache=True):
        """
        IqaLearner assumes that the output is only a scalar number
            output = preds[0]
            target = preds[1]
        """
        if on is None:
            on = self.data

        # if we don't flatten it, then we cannot store it.
        # so we need to only get the valid output
        # rois_learner gives three output csv

        csv_file = self.path / ('valid@' + on.name + '.csv')
        if os.path.isfile(csv_file) and cache:
            df = pd.read_csv(csv_file)
            output = df['output'].tolist()
            target = df['target'].tolist()
        else:
            # TODO fuse duplicate code with rois_learner
            current_data = self.data
            self.data = on
            preds = self.get_preds()
            self.data = current_data

            output = preds[0].flatten().numpy()
            target = preds[1].flatten().numpy()
            """
            preds is a list [output_tensor, target_tensor]
            torch.Size([8073, 4])
            """
            # don't call self.data.c to avoid unnecessary data loading
            # n_output = self.data.c  # only consider image score
            # no need since metric will take care of it
            # print(np.array(output).shape, np.array(target).shape) # (233, 1) (233,)
            if cache:
                df = pd.DataFrame({'output': output, 'target': target})
                df.to_csv(csv_file, index=False)
        return output, target


    def valid(self, on=None, metrics=None, cache=True, **kwargs):
        def valid_one(data):
            output, target = self.get_np_preds(data, cache)  # TODO note here only output 1 scores
            return {metric.name: metric.of(output, target) for metric in metrics}

        if metrics is None: metrics = self.metrics

        # avoid changing self.data
        if on is None:
            on = self.data

        if not isinstance(on, list):  # tuple
            on = [on]

        on = [self.model.bunch(x, **kwargs) if isinstance(x, type) else x for x in on]
        records = [valid_one(data) for data in on]
        return pd.DataFrame(records, index=[data.abbr for data in on])


    def predict_quality_map(self, img, blk_size=None):
        if blk_size is None:
            blk_size = [4, 4]  # [32, 32]  # very poor

        batch_x = img2patches(img.data, blk_size).cuda()
        batch_y = torch.zeros(1, blk_size[0] * blk_size[1]).cuda()
        predicts = self.pred_batch(batch=[batch_x, batch_y])
        # img.shape 3 x H x W
        h = blk_size[0]  # + int(img.shape[1] % blk_size[0] != 0)
        w = blk_size[1]  # + int(img.shape[2] % blk_size[1] != 0)
        pred = predicts.reshape(h, w)
        return QualityMap(pred, img)


def iqa_cnn_learner(data: DataBunch, base_arch: Callable, cut: Union[int, Callable] = None, pretrained: bool = True,
                    lin_ftrs: Optional[Collection[int]] = None, ps: Floats = 0.5,
                    custom_head: Optional[nn.Module] = None,
                    split_on: Optional[SplitFuncOrIdxList] = None, bn_final: bool = False, init=nn.init.kaiming_normal_,
                    concat_pool: bool = True, learner=IqaLearner, **kwargs: Any):
    "Build convnet style learner."
    from fastai.vision.learner import cnn_config
    meta = cnn_config(base_arch)
    model = create_cnn_model(base_arch, data.c, cut, pretrained, lin_ftrs, ps=ps, custom_head=custom_head,
                             bn_final=bn_final, concat_pool=concat_pool)
    model.__name__ = base_arch.__name__
    learn = learner(data, model, **kwargs)
    learn.split(split_on or meta['split'])
    if pretrained: learn.freeze()
    if init: apply_init(model[1], init)
    return learn
