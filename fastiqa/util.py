# TODO: implement load_model_file .pth
# https://stackoverflow.com/questions/128478/should-import-statements-always-be-at-the-top-of-a-module

import warnings
from joblib import Parallel, delayed

# TODO if is_parallel: import
import multiprocessing
from tqdm import tqdm

# def simple_cnn_3_16_16(pretrained=False):
#     from fastai.vision import simple_cnn
#     return simple_cnn((3, 16, 16))

def parfor(items, func, in_parallel=False, total=None):
    def processInput(f):
        sys.stdout = open(os.devnull, 'w')
        warnings.filterwarnings("ignore")
        return func(f)

    pbar = tqdm(items, total=len(items) if total is None else total)

    if in_parallel:
        num_cores = multiprocessing.cpu_count()
        return Parallel(n_jobs=num_cores)(delayed(processInput)(i) for i in pbar)
    else:
        return [func(f) for f in pbar]