from ..label import IqaLabel

'''
Download the datasets
=====================

https://live.ece.utexas.edu/research/ChallengeDB/

.
├── !data/
│   ├── TID2013/
│        ├── labels.csv
│        ├── tid2013/
│        │    ├── distorted_images/
│        │    ├── 

'''

class TID2013(IqaLabel):
    path = '!data/TID2013'
    img_raw_size = [384, 512]
    folder = 'tid2013/distorted_images'
