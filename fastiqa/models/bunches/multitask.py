from . import Im2MOS
from ._multi_task import *
from ._rois import *

"""
# %%
%matplotlib inline
# %%
from fastiqa.all import *; MultiTask(FLIVE640, tasks = [Im2MOS, Im2Tags])
# %%
from fastiqa.all import *
data = MultiTask(FLIVE640, tasks = [Im2MOS, Im2Tags])
data.mt_classes

data.mt_lengths # [1, 5]
# %%

acc_02 = partial(accuracy_thresh, thresh=0.2)
acc_02.__name__ = 'acc_02'
metrics = data.get_metrics([acc_02, SRCC])
metrics
# %%
data.c = sum(data.mt_lengths)
learn = IqaLearner(data, BodyHeadModel(n_output=data.c), metrics=metrics)
learn.fit_one_cycle(1)
# %%
"""

class MultiTask(Im2MOS):
    #data_cls = ImageList
    #data_cls = MultitaskLabelLists
    tasks = None

    def get_metrics(self, metric_funcs):
        return mt_metrics_generator(metric_funcs, self)

    @property
    def c(self):
        return sum(self.mt_lengths)

    def get_label(self, data):
        assert self.tasks is not None
        mt_labels = []
        for task in self.tasks:
            t = task(self.label)
            lbl = t.get_list()
            lbl = t.get_split(lbl)
            lbl = t.get_label(lbl)
            mt_labels.append(lbl)

        mt_names = [task.__name__ for task in self.tasks]

        mt_train_list = MultitaskItemList(
            [data.train.y for data in mt_labels],
            mt_names=mt_names
        )
        mt_valid_list = MultitaskItemList(
            [data.valid.y for data in mt_labels],
            mt_names=mt_names
        )
        data.train = data.train._label_list(x=data.train, y=mt_train_list)
        data.valid = data.valid._label_list(x=data.valid, y=mt_valid_list)
        data.__class__ = MultitaskLabelLists # TODO: Class morphing should be avoided, to be improved.
        data.train.__class__ = MultitaskLabelList
        data.valid.__class__ = MultitaskLabelList
        return data


class RoisMultiTask(MultiTask, Rois0123):
    pass 
