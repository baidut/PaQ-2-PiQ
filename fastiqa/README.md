# Why FastIQA?

* easy to get started for [FastAI](https://github.com/fastai/fastai) users.
* training and validating an IQA model in a few lines of code

```python
%matplotlib inline
from fastiqa.basics import *

label = CLIVE                                      # LIVE Challenge Database
data = Im2MOS(label, valid_pct=0.3)
model = BodyHeadModel(backbone=resnet18) 
learn = IqaLearner(data, model)
learn.fit(10)                                      # training for 10 epochs
learn.valid(on=[CLIVE, All(KonIQ), All(FLIVE)])    # valid on other databases 
```



```python
from fastqia.vis import *

learn.jointplot(on=KonIQ)
```

## Ablation Study

## Experiment

```python
from fastiqa.basics import *

e = IqaExp('different_backbone')
data = Im2MOS(CLIVE)

for backbone in [alexnet, resnet18, resnet34]:
	model = BodyHeadModel(backbone=backbone) 
    e[backbone.__name__] = IqaLearner(data, model)

e.fit(10)
e.valid(on=[CLIVE, All(KonIQ), All(FLIVE)])
```

