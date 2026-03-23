# -*- coding: utf-8 -*-

import glob
import os
import qrcode

# GitHub Pages base URL (custom domain)
BASE_URL = 'https://shadowrules.teches.top/'

# Skip these files (not Shadowrocket configs)
SKIP_FILES = set()

def main():
    root_dir = os.path.join(os.path.dirname(__file__), '..')
    figure_dir = os.path.join(root_dir, 'figure')
    os.makedirs(figure_dir, exist_ok=True)

    conf_files = sorted(glob.glob(os.path.join(root_dir, '*.conf')))

    for conf_path in conf_files:
        conf_name = os.path.basename(conf_path)
        if conf_name in SKIP_FILES:
            continue

        png_name = conf_name.replace('.conf', '.png')
        png_path = os.path.join(figure_dir, png_name)

        url = BASE_URL + conf_name
        img = qrcode.make(url)
        img.save(png_path)
        print(f'Generated: figure/{png_name} -> {url}')

if __name__ == '__main__':
    main()
