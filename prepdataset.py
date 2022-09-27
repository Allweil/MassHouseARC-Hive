#!/usr/bin/python3
#from tensorflow import keras
import configuration as cg
import os,shutil, pymysql
from collections import defaultdict
from operator import itemgetter
import random
from struct import unpack
from tqdm import tqdm


def run():
    forvisl()
    #prepare_data(dset="dataset05")
    #train_and_evaluate()

def getcursor(db="CRICKET"):
    return pymysql.connect(host = cg.host, user = cg.user,
                           password = cg.password, database = db,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

def forvisl(feature="staggered_balconies"):
    outputpath="/home/kartikeya/Dropbox/work/programming/gstvs/static/dataforvisl"
    path="/home/kartikeya/Dropbox/work/programming/gstvs/static/collected/"
    conn =getcursor(db="STV")
    cursor = conn.cursor()
    labels = defaultdict(list)
    cursor.execute("select pid, label from " + feature + " where upd=1")
    results = cursor.fetchall()
    added = 0
    for x,i in enumerate(results):
        pid, label = str(i['pid']), int(i['label'])
        pidsplit = pid.split("|")
        dirname = "|".join(pidsplit[:2])
        fname = "|".join(pidsplit[2:]) + ".jpg"
        dirpath = os.path.join(path,dirname)
        srcpath = os.path.join(dirpath,fname)
        if not os.path.exists(srcpath): continue
        img = JPEG(srcpath)
        img.decode() 
        pidsplit = [feature] + pidsplit + [str(label)]
        fname = "|".join(pidsplit) + ".jpg"
        print(fname)
        #fname = feature+"|"+fname.replace(".jpg","").strip()+"|"+str(label)
        newpath = os.path.join(outputpath, fname)
        print(newpath)
        shutil.copyfile(src=srcpath, dst=newpath)
        added += 1
    print(added)


def prepare_data(feature="staggered_balconies",dset="dataset02", train=11500,
                 validate=2500):
    path = "/home/kartikeya/Dropbox/work/programming/gstvs/static/collected/"
    conn =getcursor(db="STV")
    cursor = conn.cursor()
    labels = defaultdict(list)
    cursor.execute("select pid, label from " + feature + " where upd=1")
    results = cursor.fetchall()
    random.shuffle(results)
    bads= 0
    added = 0
    for x,i in enumerate(results):
        pid, label = str(i['pid']), int(i['label'])
        pidsplit = pid.split("|")
        dirname = "|".join(pidsplit[:2])
        fname = "|".join(pidsplit[2:]) + ".jpg"
        dirpath = os.path.join(path,dirname)
        srcpath = os.path.join(dirpath,fname)
        if not os.path.exists(srcpath): continue
        img = JPEG(srcpath)
        try:
            img.decode() 
            if x < train and label==1:
                newpath="/home/kartikeya/Dropbox/work/programming/gstvs/static/{}/train/present"
            elif x < train and label==0:
                newpath="/home/kartikeya/Dropbox/work/programming/gstvs/static/{}/train/absent"
            elif x >= train and x < train+validate and label==1:
                newpath="/home/kartikeya/Dropbox/work/programming/gstvs/static/{}/validation/present"
            elif x >= train and x < train+validate and label==0:
                newpath="/home/kartikeya/Dropbox/work/programming/gstvs/static/{}/validation/absent"
            elif x >= train+validate and label==1:
                newpath="/home/kartikeya/Dropbox/work/programming/gstvs/static/{}/test/present"
            elif x >= train+validate and label==0:
                newpath="/home/kartikeya/Dropbox/work/programming/gstvs/static/{}/test/absent"
            newpath = os.path.join(newpath.format(dset), fname)
            shutil.copyfile(src=srcpath, dst=newpath)
            added += 1
        except:
            bads += 1
            print("Bad image.", srcpath)
    print(bads)

marker_mapping = {
    0xffd8: "Start of Image",
    0xffe0: "Application Default Header",
    0xffdb: "Quantization Table",
    0xffc0: "Start of Frame",
    0xffc4: "Define Huffman Table",
    0xffda: "Start of Scan",
    0xffd9: "End of Image"
}


class JPEG:
    def __init__(self, image_file):
        with open(image_file, 'rb') as f:
            self.img_data = f.read()
    
    def decode(self):
        data = self.img_data
        #print(data)
        while(True):
            marker, = unpack(">H", data[0:2])
            # print(marker_mapping.get(marker))
            if marker == 0xffd8:
                data = data[2:]
            elif marker == 0xffd9:
                return
            elif marker == 0xffda:
                data = data[-2:]
            else:
                lenchunk, = unpack(">H", data[2:4])
                data = data[2+lenchunk:]
            if len(data)==0:
                break

def clear_bad_images():
    bads = []
    for img in tqdm(images):
      image = osp.join(root_img,img)
      image = JPEG(image) 
      try:
        image.decode()   
      except:
        bads.append(img)


    for name in bads:
        os.remove(osp.join(root_img,name))

if __name__ == "__main__":
    run()

