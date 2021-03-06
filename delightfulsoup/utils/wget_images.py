"""
utils.wget_images
===========

"""
import urllib as _urllib
import os as _os
import shutil as _shutil

import delightfulsoup as _ds
import shortcuts as _shc

# -------------------------------------------------------------------------------


def wget_images(imgs,
                dir_root=_os.system('pwd'),
                dir_download='wget-images',
                dir_publish=False,
                img_src_map=dict(),
                custom_img_name=False,
                translate_src=False,
                img_alt=False):
    """
    """

    # A few constants
    png_raw = 'data:image/png;base64'
    http = ('https://', 'http://')

    img_i = 0  # init image counter

    # Make download, if needed
    if not _os.path.exists(dir_download):
        _os.makedirs(dir_download)

    # If not dir_publish given, set it to dir_download
    if not dir_publish:
        dir_publish = dir_download

    for img in imgs:  # loop through imgs

        if img.name != 'img':
            raise Exception("'imgs' argument contains "
                            "bs4.Tags other than <img>")
        if not img['src']:
            continue

        img_src = img['src']

        # Skip if raw png, or already in map dict
        if (not img_src.startswith(png_raw)
                and img_src not in img_src_map.keys()):

            img_i += 1

            # Name image
            if custom_img_name:
                if hasattr(custom_img_name, '__call__'):
                    img_name = custom_img_name(img_src, img_i)
                else:
                    raise Exception('')
            else:
                img_name = _get_img_name(img_src, img_i)

            img_download_path = _os.path.join(dir_download, img_name)

            # Download it
            if img_src.startswith(http):
                _urllib.urlretrieve(img_src, img_download_path)
            else:
                img_src_full = _os.path.join(dir_root, img_src)
                _shutil.copy2(img_src_full, img_download_path)

            # Add map to img_src_map
            img_publish_path = _os.path.join(dir_publish, img_name)
            img_src_map[img_src] = img_publish_path

        # Add <img alt='' /> attribute
        if img_alt:
            img_alt_val = _shc.call_or_get(img_alt, img_src, img_i)
            _ds.add_attr(img, {'alt': img_alt_val})

    # Translate <img src='' /> using img_src_map
    if translate_src:
        _ds.translate(imgs, 'src', img_src_map)

    return img_src_map

# -------------------------------------------------------------------------------


def _get_img_name(img_src, img_i):
    """
    Default img_name get function
    """

    # Get extension
    _, img_ext = _os.path.splitext(img_src)

    # Name images in order, starting from image01
    if img_i < 10:
        img_name = "image0{i}{ext}".format(i=img_i, ext=img_ext)
    else:
        img_name = "image{i}{ext}".format(i=img_i, ext=img_ext)

    return img_name
