"""generate html website code"""
# python main.py pvq.ini PatchVQ


# %%
import sys
from jinja2 import Environment, BaseLoader, FileSystemLoader, Template
import pyperclip
import random
import pandas as pd
import configparser
import webbrowser
import os

def main(ini_file, target='DEFAULT'):
    c = configparser.ConfigParser()
    c.read(ini_file)
    # c.read('amt.ini')
    cfg = dict(c[target].items())

    # cfg that ends with 's' (multiple items)
    # for x in ['phases', 'include_pages', 'addons','train_vids', 'label_vids', 'sample_vids', 'gold_vids', 'backup_vids']:
    #     if cfg[x].strip() != '':
    #         cfg[x] = cfg[x].strip().split('\n')
    #     else:
    #         cfg[x] = []

    for k in cfg.keys():
        cfg[k] = cfg[k].replace('"', '&quot;')

    # with open("./template.htm") as f: template_str = f.read()
    # template = Environment(loader=FileSystemLoader("./")).from_string(template_str)
    template = Environment(loader=FileSystemLoader("./")).from_string("""
    {% for sec in sections.split(',') %}
      {% include sec.strip()+'.htm' %}
    {% endfor %}
    """)
    rendered = template.render(**cfg)

    if cfg['out_html'] == 'clipboard':
        pyperclip.copy(rendered)
    else:
        dir = 'file://' + os.path.dirname(os.path.realpath(__file__))
        html_file = cfg['out_html'] if os.path.isabs(cfg['out_html']) else dir + os.path.sep + cfg['out_html']
        with open(cfg['out_html'], "w") as f:
            f.write(rendered)


"""
# %%
!pip install pyperclip
!python main.py video debugNoBackup
!python main.py video jerry
# %%
"""
# %%
if __name__ == "__main__":
    main(ini_file= sys.argv[1], target=sys.argv[2])
