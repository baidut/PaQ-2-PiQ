
import math
# from PIL import Image
import torch
from torchvision import transforms
import matplotlib.pyplot as plt
import numpy as np





# show a batch
# can be used to show patches
def show_batch(patches, fig_sz=None):
    """Imshow for Tensor."""
    """
     [32, 3, 32, 32] [n_patch, 3, patch_h, patch_w]
    """
    if fig_sz is None:
        h = int(math.sqrt(patches.size(0)))
        w = math.ceil(patches.size(0) / h)
        fig_sz = (h, w)

    patches = patches.cpu()
    transp = transforms.ToPILImage()
    fig_h, fig_w = fig_sz
    fig, axes = plt.subplots(fig_h, fig_w)  # , figsize=(4, 4)
    for n in range(patches.size(0)):
        inp = transp(patches[n])
        inp = np.array(inp)
        axes[n // fig_w, n % fig_w].imshow(inp)


def key_transformation(old_key):
    # print(old_key)
    if '.' in old_key:
        a, b = old_key.split('.', 1)
        if a == "cnn":
            return f"body.{b}"
    return old_key
    # body.0.weight", "cnn.1.weight


# https://gist.github.com/the-bass/0bf8aaa302f9ba0d26798b11e4dd73e3
# rename_state_dict_keys(e['Feed4Scores'].path/'models'/'bestmodel.pth', key_transformation)
def rename_state_dict_keys(source, key_transformation, target=None):
    from collections import OrderedDict
    """
    source             -> Path to the saved state dict.
    key_transformation -> Function that accepts the old key names of the state
                          dict as the only argument and returns the new key name.
    target (optional)  -> Path at which the new state dict should be saved
                          (defaults to `source`)
    Example:
    Rename the key `layer.0.weight` `layer.1.weight` and keep the names of all
    other keys.
    ```py
    def key_transformation(old_key):
        if old_key == "layer.0.weight":
            return "layer.1.weight"
        return old_key
    rename_state_dict_keys(state_dict_path, key_transformation)
    ```
    """
    if target is None:
        target = source

    state_dict = torch.load(source)
    new_state_dict = OrderedDict()

    for key, value in state_dict['model'].items():
        new_key = key_transformation(key)
        new_state_dict[new_key] = value

    torch.save(new_state_dict, target)
