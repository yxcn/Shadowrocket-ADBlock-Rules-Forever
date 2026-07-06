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
    # 清理旧二维码，避免已删除配置的残留
    if os.path.exists(figure_dir):
        for old_png in glob.glob(os.path.join(figure_dir, '*.png')):
            os.remove(old_png)
    os.makedirs(figure_dir, exist_ok=True)

    conf_files = sorted(glob.glob(os.path.join(root_dir, '*.conf')))

    for conf_path in conf_files:
        conf_name = os.path.basename(conf_path)
        if conf_name in SKIP_FILES:
            continue

        png_name = conf_name.replace('.conf', '.png')
        png_path = os.path.join(figure_dir, png_name)

        url = BASE_URL + conf_name
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        img = img.resize((100, 100))
        img.save(png_path)
        print(f'Generated: figure/{png_name} -> {url}')

if __name__ == '__main__':
    main()
