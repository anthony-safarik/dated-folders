#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 08:34:18 2020

@author: anthonysafarik
"""

import subprocess
import os
import shutil

def check_output(cmd):
    try:
        output = subprocess.check_output(cmd)
        return output
    except:
        return ''

def get_exif_date_all(inpath):
    '''
    alternate, slower way that checks each tag on each acceptable extension
    '''
    (basename, ext) = os.path.splitext(inpath)
    #exts = ['.JPG','.ARW','.MP4','.MOV','.AVI']
    tags = ['-QuickTime:CreateDate','-EXIF:CreateDate','-RIFF:DateTimeOriginal','-XMP:CreateDate','File:FileModifyDate']
    #if ext.upper() in exts:
    for tag in tags:
        output = ''
        output = check_output(['exiftool',tag,'-d', '%Y-%m-%d', '-s', '-s', '-s',inpath])
        if len(output)==11:
            output = str(output)[2:12]
            break
    if output: print (output,inpath,'T')

def get_exif_date_by_ext(inpath):

    (basename, ext) = os.path.splitext(inpath)

    photo_exts = ['.JPG','.ARW']
    qt_exts = ['.MP4','.MOV']
    video_exts = ['.AVI']

    #tags = ['-QuickTime:CreateDate','-EXIF:CreateDate','-RIFF:DateTimeOriginal','-XMP:CreateDate','File:FileModifyDate']

    output = ''

    if ext.upper() in photo_exts:
        output = check_output(['exiftool','-EXIF:CreateDate','-d', '%Y-%m-%d', '-s', '-s', '-s',inpath])
        tag_to_id ='-EXIF:CreateDate'
    elif ext.upper() in qt_exts:
        output = check_output(['exiftool','-QuickTime:CreateDate','-d', '%Y-%m-%d', '-s', '-s', '-s',inpath])
        tag_to_id ='-QuickTime:CreateDate'
    elif ext == '.avi':
        output = check_output(['exiftool','-XMP:CreateDate','-d', '%Y-%m-%d', '-s', '-s', '-s',inpath])
        tag_to_id ='-XMP:CreateDate'
    elif ext == '.AVI':
        output = check_output(['exiftool','-RIFF:DateTimeOriginal','-d', '%Y-%m-%d', '-s', '-s', '-s',inpath])
        tag_to_id ='-RIFF:DateTimeOriginal'
    if not len(output)==11:
        output = check_output(['exiftool','-File:FileModifyDate','-d', '%Y-%m-%d', '-s', '-s', '-s',inpath])
        tag_to_id ='-File:FileModifyDate'
    if len(output)==11:
        print (tag_to_id)
        return str(output)[2:12]
    else:
        return ''


    #(basename, ext) = os.path.splitext(fname)

def make_dated_folders(inpath,outpath):
    for path, dirs, files in os.walk(inpath):
        for fname in files:
            fpath = path+os.path.sep+fname
            date = get_exif_date_by_ext(fpath)
            if date:
                date_folder = outpath+os.path.sep+date[0:4]+os.path.sep+date
                dst_fpath = date_folder+os.path.sep+fname
                if not os.path.exists(date_folder):
                    os.makedirs(date_folder)
                if os.path.exists(dst_fpath):
                    print('path exists... ',dst_fpath)
                else:
                    try:
                        shutil.move(fpath, dst_fpath)
                        print (dst_fpath)
                    except:
                        print ('could not move...',fname)
            else:
                print('could not extract date...',fname)

inpath = input('enter inpath... ')
outpath = input('enter outpath... ')
make_dated_folders(inpath,outpath)
