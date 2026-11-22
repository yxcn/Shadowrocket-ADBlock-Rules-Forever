# -*- coding: utf-8 -*-

import os
import qrcode

from publications import CONFIG_NAMES

# GitHub Pages base URL
BASE_URL = 'https://yxcn.github.io/Shadowrocket-ADBlock-Rules-Forever/'

def main():
    root_dir = os.path.join(os.path.dirname(__file__), '..')
    figure_dir = os.path.join(root_dir, 'figure')
    os.makedirs(figure_dir, exist_ok=True)

    for name in CONFIG_NAMES:
        conf_name = name + '.conf'
        png_name = name + '.png'
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
