'''
Created on Feb 26, 2019

@author: Timothy
'''

import downloader, os
from permissions import *

LOCAL_PATH = "seng474data/"  # update this when necessary

def isBadZip(file):
    
    try:
        with ZipFile(file, 'r') as apk:
            apk.read(MANIFEST)
            return False
    except BadZipFile:
        return True


def removeBadZips():
    
    count_undetected = 0
    count_detected = 0
    path = LOCAL_PATH + downloader.LOCAL_UNDETECTED
    for file in os.listdir(path):
        if isBadZip(path+file):
            os.remove(path + file)
            count_undetected += 1

    path = LOCAL_PATH + downloader.LOCAL_DETECTED
    for file in os.listdir(path):
        if isBadZip(path+file):
            os.remove(path + file)
            count_detected += 1

    return count_undetected,count_detected



def getPermissionSets():
    
    unique_set = set()
    undetected = []     # TODO: convert to dict of dicts
    detected = []       # TODO: convert to dict of dicts
    detected_files = []
    undetected_files = []
    
    #undetected
    path = LOCAL_PATH + downloader.LOCAL_UNDETECTED
    for file in os.listdir(path):
        undetected_files.append(file)
        permissions = extractPermissions(path + file)
        undetected.append(permissions)

        for perm in permissions:
            unique_set.add(perm)

    #detected
    path = LOCAL_PATH + downloader.LOCAL_DETECTED
    for file in os.listdir(path):
        detected_files.append(file)
        permissions = extractPermissions(path + file)
        detected.append(permissions)

        for perm in permissions:
            unique_set.add(perm)
    
    return (unique_set, undetected, undetected_files, detected, detected_files)
    
    
def buildDataset():
    unique_set, undetected, undetected_files, detected, detected_files = getPermissionSets()
    data = {}  # filename: [list of perms]
    
   
    #undetected
    file_index = 0
    for file in undetected_files:
        data[file] = {}
        data[file]["type"] = 0 
        
        for perm in unique_set:
            if perm in undetected[file_index]:
                data[file][perm] = 1
            else:
                data[file][perm] = 0

        file_index +=1
        
    #detected
    file_index = 0
    for file in detected_files:
        data[file] = {}
        data[file]["type"] = 1
        
        for perm in unique_set:
            if perm in detected[file_index]:
                data[file][perm] = 1
            else:
                data[file][perm] = 0

        file_index +=1

    return data

def main():
    count_undetected, count_detected = removeBadZips()
    print("Removed %d bad undetected zips." % count_undetected)
    print("Removed %d bad detected zips." % count_detected)

    print("Data set [dict of dicts]:")
    #data[apkFilename][permission] = 0 or 1
    #data[apkFilename][permission] = 0 or 1

    data = buildDataset()
    print(data)

    
if __name__ == '__main__':
    main()
