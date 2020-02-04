from ._bunch import *
from .regression import *
# from .crop import *
# from .rois import *

IQA_URL = 'https://s3.amazonaws.com/fbiqa/public_data/'


class IQA_URLs(URLs):
    CLIVE = f'{IQA_URL}CLIVE'


_checks = {
    IQA_URLs.CLIVE: (325977489, 'ea9fe8aa0f5631aa472aaa4212e9fc8e'),
}


def _check_file(fname):
    size = os.path.getsize(fname)
    with open(fname, "rb") as f:
        hash_nb = hashlib.md5(f.read(2 ** 20)).hexdigest()
    return size, hash_nb


def _url2tgz(url, data=True, ext: str = '.tgz'):
    return datapath4file(f'{url2name(url)}{ext}', ext=ext) if data else modelpath4file(f'{url2name(url)}{ext}', ext=ext)


def untar_iqa_data(url: str, fname: PathOrStr = None, dest: PathOrStr = None, data=True, force_download=False) -> Path:
    "Download `url` to `fname` if `dest` doesn't exist, and un-tgz to folder `dest`."
    dest = url2path(url, data) if dest is None else Path(dest) / url2name(url)
    fname = Path(ifnone(fname, _url2tgz(url, data)))
    if force_download or (fname.exists() and url in _checks and _check_file(fname) != _checks[url]):
        print(f"A new version of the {'dataset' if data else 'model'} is available.")
        if fname.exists(): os.remove(fname)
        if dest.exists(): shutil.rmtree(dest)
    if not dest.exists():
        fname = download_data(url, fname=fname, data=data)
        if url in _checks:
            assert _check_file(fname) == _checks[
                url], f"Downloaded file {fname} does not match checksum expected! Remove that file from {Config().data_archive_path()} and try your code again."
        tarfile.open(fname, 'r:gz').extractall(dest.parent)
    return dest


"""

transform
=========


def transform(self, tfms:Optional[Tuple[TfmList,TfmList]]=(None,None), **kwargs):
        "Set `tfms` to be applied to the xs of the train and validation set."
        if not tfms: tfms=(None,None)
        assert is_listy(tfms) and len(tfms) == 2, "Please pass a list of two lists of transforms (train and valid)."

tfms = ([crop_pad()], [])
tfms = ([], [])
data.transform(size=500)

rand_crop()
https://docs.fast.ai/vision.transform.html#rand_pad didn’t find the difference
rand_pad()


* https://docs.fast.ai/vision.transform.html#get_transforms
* get_transforms() return (res + listify(xtra_tfms), [crop_pad()])
* get_transforms(do_flip=True, flip_vert=False, max_zoom=1, max_warp=False, max_rotate=False, max_lighting=False) # only do flip
* data.transform


"""
