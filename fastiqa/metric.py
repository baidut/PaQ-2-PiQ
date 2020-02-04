from fastai.vision import *
from scipy import stats
from fastai.metrics import RegMetrics


class IqaMetric(RegMetrics):
    fn: Lambda = None
    name: str = None  # need this
    distribution: bool = False
    col: int = 0  # compute based on image scores only
    proc_targs = lambda s, x: x
    proc_preds = lambda s, x: x

    def __init__(self, **kwargs):
        self.name = self.__class__.__name__
        self.__dict__.update(kwargs)

    @classmethod
    def of(cls, preds, targs):
        return cls.fn(np.asarray(preds), np.asarray(targs))[0]

    def on_batch_end(self, last_output: Tensor, last_target: Tensor, **kwargs):
        super().on_batch_end(self.proc_preds(last_output),
                             self.proc_targs(last_target), **kwargs)

    def on_epoch_end(self, last_metrics, **kwargs):
        def get_column(x, idx_col):
            return x if x.dim() == 1 \
                else x[:, idx_col].view(1, -1)[0]

        if self.targs.size(0) < 10:
            print('Return nan since the len of validation set is too small to compute a reliable result')
            metric = np.nan
        else:
            output = get_column(self.preds, self.col)
            target = get_column(self.targs, self.col)
            metric = self.of(output, target)
        return add_metrics(last_metrics, metric)


class SRCC(IqaMetric):
    fn: Lambda = stats.spearmanr


class LCC(IqaMetric):
    fn: Lambda = stats.pearsonr


class KROCC(IqaMetric):
    fn: Lambda = stats.kendalltau
