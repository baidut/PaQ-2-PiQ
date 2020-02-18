from .basics import *
from fastai.callbacks import *

import random
import torch  # pytorch RNGs
import numpy as np  # numpy RNG


class IqaExp(dict):
    path = '!exp'
    seed = None

    def __init__(self, path=None, gpu=None, seed=None):
        super().__init__()
        self.path = Path(path) if path else Path(self.path)
        if gpu is not None:
            torch.cuda.set_device(gpu)

        self.seed = seed
        self.set_seed()

        # self.testdb = testdb
        # self.metrics = metrics

    def set_seed(self):
        if self.seed is not None:
            x = self.seed
            random.seed(x)
            np.random.seed(x)
            torch.manual_seed(x)
            torch.backends.cudnn.deterministic = True
            if torch.cuda.is_available(): torch.cuda.manual_seed_all(x)

    def __iadd__(self, other):
        self[other.model.__name__] = other
        return self

    def __setitem__(self, key, learn):
        """ NOTE this will change the learn.path """
        if hasattr(learn.data, 'name'):
            data_name = learn.data.name
        else:
            data_name = learn.data.path.split('/')[-1]

        config = 'default' if learn.model.__name__ == key else key
        exp_path = self.path / learn.model.__name__ / ('train@' + data_name) / config  # exp/resnet18/CLIVE
        learn.path = exp_path
        super().__setitem__(key, learn)

    @property
    def one_item(self):
        return next(iter(self.values()))


    # TODO self[key] = self[key].to_fp16()
    # func=fine_tune
    def run(self, func, destroy=False, append=False):
        # TODO option load best or load latest

        for key, learn in self.items():
            exp_path = learn.path  # exp/resnet18/CLIVE
            if append is False:
                try:
                    os.makedirs(exp_path)
                except FileExistsError:
                    print(f'Skip cuz FileExists {exp_path}')
                    continue

            self.set_seed()
            func(learn)
            # learn.save(key)
            if destroy:
                learn.destroy()
            self[key] = learn  # call __setitem__
        return self

    def load(self, name=None):
        if name is None: name = 'bestmodel'
        return self.run(lambda x: x.load(name), append=True)

    def fit(self, n, append=False, **kwargs):
        return self.run(lambda x: x.fit(n, **kwargs), append=append)

    def fit_one_cycle(self, n, append=False, **kwargs):
        return self.run(lambda x: x.fit_one_cycle(n, **kwargs), append=append)

    def _repr_html_(self, clear=True):
        for key, learn in self.items():
            if not hasattr(learn, 'csv_logger'):
                learn.csv_logger = CSVLogger(learn, append=True)

        self.show_losses()
        self.show_metrics()
        return ''

    def __getattr__(self, k: str):  # total_params
        # %% when returning a single value
        # d = {key: getattr(learn, k) for key, learn in self.items()}
        # return pd.DataFrame([d], index=[k]).T

        # %% when return a dict
        return pd.DataFrame([getattr(learn, k)
                             for learn in self.values()], self.keys())

    def valid(self, data, metrics=None, cache=True, **kwargs):

        def valid_one(l):
            df = l.valid(data, metrics, cache, **kwargs).T
            return df[df.columns].apply(lambda row: ','.join(row.map('{:.3f}'.format)))

        # %%
        # frames = [learn.valid(data).add_prefix(key+'_') for key, learn in self.items()]
        # return pd.concat(frames)
        d = [valid_one(learn) for learn in self.values()]
        # pd.options.display.float_format = '{:,.3f}'.format
        return pd.DataFrame(d, index=self.keys())


    def show_losses(self):
        # Train error and Test error
        # from ast import literal_eval

        fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(8, 3))
        # fig.set_size_inches(18.5, 10.5, forward=True)
        ax1.set_title("Train error")
        ax2.set_title("Test error")
        for key, learner in self.items():
            # TODO AttributeError: 'Learner' object has no attribute 'csv_logger'
            df = learner.csv_logger.read_logged_file()
            # a = [literal_eval(x) for x in learner.records['train loss'].tolist()]
            # train_losses = np.array(a).flatten()
            # valid_losses = learner.records['valid loss'].to_list()
            df = df[df.epoch != 'epoch']
            train_losses = df['train_loss'].astype(float).to_list()
            valid_losses = df['valid_loss'].astype(float).to_list()
            ax1.plot(log(train_losses), label=key)
            ax2.plot(log(valid_losses), label=key)

        ax1.set_ylabel('Log Loss')
        ax1.set_xlabel('Batches processed')
        ax1.legend()

        ax2.set_ylabel('Log Loss')
        ax2.set_xlabel('Batches processed')
        # ax2.legend()

    def show_metrics(self, sharey=True):  # metrics
        metrics = self.one_item.metrics
        if not metrics:
            return  # no metrics
        if sharey:
            fig, axes = plt.subplots(1, len(metrics), sharey=True, figsize=(8, 3))
        else:
            fig, axes = plt.subplots(len(metrics), 1, figsize=(6, 5 * len(metrics)))

        if len(metrics) == 1:
            axes = [axes]

        for idx, metric in enumerate(metrics):
            name = metric.name
            axes[idx].set_title(name)
            axes[idx].set_ylabel('score')
            axes[idx].set_xlabel('Batches processed')
            for key, learner in self.items():
                # score = learner.records[name].to_list()
                df = learner.csv_logger.read_logged_file()
                df = df[df.epoch != 'epoch']
                score = df[name].astype(float).to_list()
                # print(score)
                axes[idx].plot(score, label=key)

        axes[0].legend()
