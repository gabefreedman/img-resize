# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 23:01:54 2019

@author: Gabriel Freedman
"""

import os
import shutil
import PIL
from ctypes import windll
from PIL import Image, ExifTags, ImageOps


def images_in_dir(folder):
    """ Takes in name of directory to search for images. Returns dictionary
        with key : value pairs of relative_dir : absolute_dir pointing
        to image files.
    """
    valid_extensions = ('.jpg', '.jpeg', '.JPG', '.JPEG')
    
    rel_dir = [file for file in os.listdir(folder) if file.endswith(valid_extensions)]
    
    abs_dir = [folder + '\\' + image for image in rel_dir]
    
    imd = list(zip(rel_dir, abs_dir))
    
    return imd


def make_parallel_dir(folder, ident):
    """ Takes in name of directory containing images. Moves up to parent
        directory and creates new folder named after original directory plus
        an identifying string. Returns new folder path
    """
    
    parent_dir = os.path.normpath(folder + os.sep + os.pardir)
    
    folder_basename = os.path.relpath(folder, parent_dir)
    
    new_folder_name = folder_basename + '_' + ident
    
    folder_path = os.path.join(parent_dir, new_folder_name)
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
    
    os.mkdir(folder_path)
    return folder_path


def get_monitor_dpi():
    """ Retrieves DPI value for given monitor
    """
    
    LOGPIXELSX = 88
    LOGPIXELSY = 90
    dc = windll.user32.GetDC(0)
    h_dpi = windll.gdi32.GetDeviceCaps(dc, LOGPIXELSX)
    v_dpi = windll.gdi32.GetDeviceCaps(dc, LOGPIXELSY)
    windll.user32.ReleaseDC(0, dc)
    return h_dpi, v_dpi


def resize_image(image_tup, new_height, resize_folder, border):
    """ Resizes image I hope
    """
    i = Image.open(image_tup[1])
    
    try:
        for orientation in ExifTags.TAGS.keys(): 
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(i._getexif().items())
    
        if exif[orientation] == 3: 
            i = i.rotate(180, expand=True)
        elif exif[orientation] == 6: 
            i = i.rotate(270, expand=True)
        elif exif[orientation] == 8: 
            i = i.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    
    dpi = get_monitor_dpi()
    orig_size_px = i.size
    
    aspect_ratio = orig_size_px[0] / orig_size_px[1]
    
    new_height_px = new_height * dpi[0]
    new_width_px = new_height_px * aspect_ratio
    new_dims = (int(new_width_px), int(new_height_px))

    new_im = i.resize(new_dims, PIL.Image.ANTIALIAS)
    
    if border == 1:
        border_width_pt = 1
        border_width_px = int(border_width_pt * (dpi[0] / 72))
        new_im = ImageOps.expand(new_im, border=border_width_px)
    
    save_path = os.path.join(resize_folder, image_tup[0])
    new_im.save(save_path)
    i.close()

    return


def resize_all(folder, new_height, ident, border):
    imd = images_in_dir(folder)
    resize_folder = make_parallel_dir(folder, ident)
    for tup in imd:
        print(tup)
        resize_image(tup, new_height, resize_folder, border)
