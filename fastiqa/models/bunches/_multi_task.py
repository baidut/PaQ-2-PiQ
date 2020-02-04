from .import *

__all__ = ['MultitaskItem',
           'MultitaskItemList',
           'MultitaskLabelList',
           'MultitaskLabelLists',
           'multitask_loss',
           'mt_metrics_generator'
          ]

def multitask_loss(data, inputs_concat, *targets, weights=None, **kwargs):
    mt_lengths, mt_types = data.mt_lengths, data.mt_types # TODO: avoid global variable
    start = 0

    loss_size = targets[0].shape[0] if kwargs.get('reduction') == 'none' else 1
    losses = torch.zeros([loss_size]).cuda()

    for i, length in enumerate(data.mt_lengths):

        input = inputs_concat[:,start: start + length]
        target = targets[i]

        # input, target = _remove_nan_values(input, target, data.mt_types[i], data.mt_classes[i])

        if data.mt_types[i] == CategoryList:
            loss = CrossEntropyFlat(**kwargs)(input, target).cuda()
        elif data.mt_types[i] == MultiCategoryList:
            loss = BCEWithLogitsFlat(**kwargs)(input, target).cuda()
        elif issubclass(data.mt_types[i], FloatList):
            loss = MSELossFlat(**kwargs)(input, target).cuda()

        weight = weights[i] if weights is not None else 1
        losses += weight * loss
        start += length

    if kwargs.get('reduction') == 'none':
        return losses
    return losses.sum()

# # Monkey patch FloatItem with a better default string formatting.
# def float_str(self):
#     return "{:.4g}".format(self.obj)
# FloatItem.__str__ = float_str

class MultitaskItem(MixedItem):
    def __init__(self, *args, mt_names=None, **kwargs):
        super().__init__(*args,**kwargs)
        self.mt_names = mt_names

    def __repr__(self):
        return '|'.join([f'{self.mt_names[i]}:{item}' for i, item in enumerate(self.obj)])

class MultitaskItemList(MixedItemList):

    def __init__(self, *args, mt_names=None, **kwargs):
        super().__init__(*args,**kwargs)
        self.mt_classes = [getattr(il, 'classes', None) for il in self.item_lists]
        self.mt_types = [type(il) for il in self.item_lists]
        self.mt_lengths = [len(i) if i else 1 for i in self.mt_classes]
        self.mt_names = mt_names
        self.loss_func = partial(multitask_loss, self)

    def get(self, i):
        return MultitaskItem([il.get(i) for il in self.item_lists], mt_names=self.mt_names)

    def reconstruct(self, t_list):
        items = []
        t_list = self.unprocess_one(t_list)
        for i,t in enumerate(t_list):
            if self.mt_types[i] == CategoryList:
                items.append(Category(t, self.mt_classes[i][t]))
            elif self.mt_types[i] == MultiCategoryList:
                o = [i for i in range(self.mt_lengths[i]) if t[i] == 1.]
                items.append(MultiCategory(t, [self.mt_classes[i][p] for p in o], o))
            elif issubclass(self.mt_types[i], FloatList):
                items.append(FloatItem(t))
        return MultitaskItem(items, mt_names=self.mt_names)

    def analyze_pred(self, pred, thresh:float=0.5):
        predictions = []
        start = 0
        for length, mt_type in zip(self.mt_lengths, self.mt_types):
            if mt_type == CategoryList:
                predictions.append(pred[start: start + length].argmax())
            elif issubclass(mt_type, FloatList):
                predictions.append(pred[start: start + length][0])
            start += length
        return predictions

    def unprocess_one(self, item, processor=None):
        if processor is not None: self.processor = processor
        self.processor = listify(self.processor)
        for p in self.processor:
            item = _processor_unprocess_one(p, item)
        return item

def _processor_unprocess_one(self, item:Any): # TODO: global function to avoid subclassing MixedProcessor. To be cleaned.
    res = []
    for procs, i in zip(self.procs, item):
        for p in procs:
            if hasattr(p, 'unprocess_one'):
                i = p.unprocess_one(i)
        res.append(i)
    return res



class MultitaskLabelList(LabelList):
    def get_state(self, **kwargs):
        kwargs.update({
            'mt_classes': self.mt_classes,
            'mt_types': self.mt_types,
            'mt_lengths': self.mt_lengths,
            'mt_names': self.mt_names
        })
        return super().get_state(**kwargs)

    @classmethod
    def load_state(cls, path:PathOrStr, state:dict) -> 'LabelList':
        res = super().load_state(path, state)
        res.mt_classes = state['mt_classes']
        res.mt_types = state['mt_types']
        res.mt_lengths = state['mt_lengths']
        res.mt_names = state['mt_names']
        return res

class MultitaskLabelLists(LabelLists):
    @classmethod
    def load_state(cls, path:PathOrStr, state:dict):
        path = Path(path)
        train_ds = MultitaskLabelList.load_state(path, state)
        valid_ds = MultitaskLabelList.load_state(path, state)
        self.loss_func = partial(multitask_loss, self)
        return MultitaskLabelLists(path, train=train_ds, valid=valid_ds)


# def _clean_nan_values(input, target, mt_type, mt_classes):
#     if mt_type == CategoryList and 'NA' in mt_classes:
#         index = mt_classes.index('NA')
#         nan_mask = target == index
#
#         input[nan_mask] = 0.
#         input[nan_mask][:, index] = 1e5
#
#     elif mt_type == MultiCategoryList and 'nan' in mt_classes:
#         index = mt_classes.index('nan')
#         nan_mask = target == index
#
#         input[nan_mask] = 0.
#         # input[nan_mask][:, index] = 1e5
#
#     elif issubclass(mt_type, FloatList):
#         nan_mask = (torch.isnan(target)) | (target < 0)
#         input[nan_mask] = 0.
#         target[nan_mask] = 0.
#     return input, target



def _remove_nan_values(input, target, mt_type, mt_classes):
    if mt_type == CategoryList and 'NA' in mt_classes:
        index = mt_classes.index('NA')
        nan_mask = target == index
    elif mt_type == MultiCategoryList and 'nan' in mt_classes:
        index = mt_classes.index('nan')
        nan_mask = target == index
    elif issubclass(mt_type, FloatList):
        nan_mask = (torch.isnan(target)) | (target < 0)
    return input[nan_mask], target[nan_mask]

class MultitaskAverageMetric(AverageMetric):
    def __init__(self, func, name=None):
        super().__init__(func)
        self.name = name # subclass uses this attribute in the __repr__ method.

def _mt_parametrable_metric(inputs, *targets, data, func, start=0, length=1, i=0):
    input = inputs[:,start: start + length]
    target = targets[i]

    _remove_nan_values(input, target, data.mt_types[i], data.mt_classes[i]) # TODO: Avoid data global reference.

    if func.__name__ == 'root_mean_squared_error':
        processor = listify(learn.data.y.processor)
        input = processor[0].procs[i][0].unprocess_one(input) # TODO: support multi-processors
        target = processor[0].procs[i][0].unprocess_one(target.float())
    return func(input, target)

def _format_metric_name(field_name, metric_func):
    return f"{field_name} {metric_func.__name__.replace('root_mean_squared_error', 'RMSE')}"

def mt_metrics_generator(metric_funcs, data):
    mt_lengths = data.mt_lengths
    metrics = []
    start = 0
    for i, (task, metric_func, length) in enumerate(zip(data.tasks, metric_funcs, mt_lengths)):
        name = task.__name__
        if metric_func:
            partial_metric = partial(_mt_parametrable_metric, start=start, length=length, i=i, func=metric_func, data=data)
            metrics.append(MultitaskAverageMetric(partial_metric, _format_metric_name(name,metric_func)))
        start += length
    return metrics
