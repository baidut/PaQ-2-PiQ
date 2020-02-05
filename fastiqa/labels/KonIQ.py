from ..label import IqaLabel

'''
Download the datasets
=====================

http://database.mmsp-kn.de/koniq-10k-database.html

* koniq10k_1024x768.zip --> 1024x768
* koniq10k_224x224.zip --> 224x224
* koniq10k_scores_and_distributions.zip --> labels.csv

.
├── !data/
│   ├── KonIQ/
│        ├── labels.csv
│        ├── 1024x768/
│        │    ├── 826373.jpg
│        │
│        ├── 224x224/
│        │    ├── 826373.jpg


koniq10k_scores_and_distributions
* c_total = sum c_i
* MOS = \sum c_i*i / c_total for i = 1,2,3,4,5
* min MOS = 1, max MOS = 5
'''


class KonIQ(IqaLabel):
    path = '!data/KonIQ'
    folder = '1024x768'
    img_raw_size = 768, 1024  # height width
    fn_col = 'image_name'
    label_cols = 'MOS_zscore', # or 'MOS'
    label_types = 'MOS_zscore', # 


class KonIQ_dist(KonIQ):  # KonIQ10k with distributions
    label_cols = 'p1', 'p2', 'p3', 'p4', 'p5'
