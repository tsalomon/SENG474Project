"""
Author:		Matthew Cairns - V00709952 & Tim Salomonsson - V00807959
Created:	12-Mar-2019 09:40:11
Filename:	downloader.py
Description:  We downloaded the 1.5TB dataset over time using this script to manage it.
"""

# TO RUN: python downloader.py [NUMBER OF APKS] [MAX BANDWIDTH TO USE IN GB] [LOCAL PATH TO STORE FILES]

import random, os, sys, argparse

from utils.apk_filenames import parse_filenames, get_undetected_filenames, \
    get_detected_filenames
from utils.permissions import *
from utils.sftp import *


LOCAL_UNDETECTED = 'undetected/'
LOCAL_DETECTED = 'detected/'

def choose_n_items(items, n):
    # If we have less then n items left return them
    if len(items) <= n:
        return items

    # Choose n unique items
    choices = []
    while n > 0:
        c = random.choice(items)
        if c not in choices:
            n -= 1
            choices.append(c)

    return choices


def diff(A, B):
    B = set(B)
    return [item for item in A if item not in B]


def download_list(sftp, items, bandwidth_limit, server_path, local_path):
    sftp.chdir(server_path)
    downloaded = []
    size = 0

    i = 1
    for current_item in items:
        print('%s downloading %d of %d: %s' % (local_path[:-1], i, len(items),current_item[:12]+"..."+current_item[-16:]))
        size += sftp.stat(current_item).st_size
        if size >= bandwidth_limit and bandwidth_limit > -1:
            break
        sftp.get(current_item, local_path + current_item)
        downloaded.append(current_item)
        i += 1

    sftp.chdir('..')

    return size, downloaded


def get_apks(sftp, apk_amount, bandwidth_limit, local_path):
    amount_downloaded = 0

    parse_filenames
    undetected = get_undetected_filenames()
    detected = get_detected_filenames()

    if apk_amount == -1:
        apk_amount = len(undetected) + len(detected)

    already_downloaded = get_downloaded(local_path)

    undetected = choose_n_items(diff(undetected, already_downloaded), apk_amount)
    detected = choose_n_items(diff(detected, already_downloaded), apk_amount)

    size, undetected_downloads = download_list(sftp, undetected, bandwidth_limit, UNDETECTED_PATH, local_path +LOCAL_UNDETECTED)
    amount_downloaded += size

    size, detected_downloads = download_list(sftp, detected, bandwidth_limit, DETECTED_PATH, local_path + LOCAL_DETECTED)
    amount_downloaded += size

    return (amount_downloaded, undetected_downloads, detected_downloads)


def get_downloaded(local_path):
    dirs = os.listdir(local_path + LOCAL_UNDETECTED)
    dirs += os.listdir(local_path + LOCAL_DETECTED)
    return dirs


def main():
    parser = argparse.ArgumentParser("simple_example")
    parser.add_argument("apk_num", help="How many APKs should we download? -1 for unlimited", type=int)
    parser.add_argument("max_bandwidth", help="What is the max amount of data you want in GB?  -1 for unlimited", type=int)
    parser.add_argument("local_path", help="Path to store apks", type=str)
    args = parser.parse_args()
    print("Saving apks to ", args.local_path)


    if args.max_bandwidth != -1:
        args.max_bandwidth = args.max_bandwidth * 1000000000

    print('Connecting to koodous...')
    sftp = connect_koodous()
    sftp.chdir(APKS_PATH)
    print('Connected')

    (amount_downloaded, undetected_downloads, detected_downloads) = get_apks(sftp, args.apk_num, args.max_bandwidth, args.local_path)
    print("Downloaded apks, size: %.2f GB\n" % (amount_downloaded/1000000000))
    print("\t   num detected: %d\n" % (len(detected_downloads)))
    print("\t num undetected: %d\n" % (len(undetected_downloads)))


if __name__ == '__main__':
    main()
