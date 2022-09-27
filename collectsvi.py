#!/usr/bin/python3
import requests
import urllib
import pymysql
from operator import itemgetter
from config import Config
import os
from multiprocessing import Pool
import time


def get_soup(u):
    user_agent = {'User-agent':'Mozilla/5.0'}
    html = requests.get(u, headers = user_agent)
    return html.content

def getcursor(db="STV"):
    return pymysql.connect(host = Config.host, user = Config.user,
                           password = Config.password, database = "STV",
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

def getjson(u):
    uf = u+":formatted"
    j = requests.get(u)
    return j.json()

def run():
    update_db()
    #u = "https://www.google.co.il/maps/@32.1289361,34.7932176,3a,75y,196.92h,96.86t/data=!3m6!1e1!3m4!1ssKTQRBMaSJohdS6zs58C6g!2e0!7i13312!8i6656?hl=en"
    #get_urls()
    #process_url(u)

def get_urls():
    todo = list()
    basepath = "/home/kartikeya/Dropbox/work/gstvs/static/collected/"
    for k in os.listdir(basepath):
        path = basepath + k
        if len(os.listdir(path)) < 504:
            todo.append(k)
    urls = list()
    for line in open("addresses.csv","r").readlines():
        if len(line.split('"')) >= 2:
            if "www.google.com" in line.split('"')[1]:
                urls.append((line.split('"')[1], todo))

    for u in urls:
        process_url(u)

def update_db(swatch="staggered_balconies"):
    basepath = "/home/kartikeya/Dropbox/work/gstvs/static/collected/"
    conn = getcursor(db="STV")
    cursor = conn.cursor()
    q = "insert into " + swatch + " (pid, sel, upd, label) values\
    (%s,%s,%s,%s) on duplicate key update sel=%s, upd=%s, label=%s"

    for rec in os.listdir(basepath):
        print(rec)
        for f in os.listdir(basepath + "/" + rec):
            pk = "|".join([rec,f]).replace(".jpg","")
            row = pk, 0, 0, 0
            cursor.execute(q, row + row[1:])
            #print(row)
    conn.commit()
    conn.close()



def process_url(u):
    u, todo = u
    st = time.time()
    pars = u.split("/")[-2]
    data = parsedat(pars)
    imgurlbase = "https://maps.googleapis.com/maps/api/streetview"
    urls = list()
    for p in range(0, 45, 5):
        for f in range(15, 135, 15):
            for h_ in range(-45, 46, 15):
                h = float(data['heading']) + h_
                loc = "?size=400x400&location="+str(data["latitude"]) + "," + str(data["longitude"])
                rest = "&fov="+ str(f) + "&heading=" + str(h) + "&pitch=" + str(p) + "&key=" + Config.google_api_key
                imgurl = imgurlbase+loc+rest
                dirname = "|".join([str(x) for x in [data['latitude'], data['longitude']]])
                if dirname not in todo: continue
                fname = "|".join([str(x) for x in [ f, h, p]])
                basepath = "/home/kartikeya/work/gstvs/static/collected/"
                #if os.path.exists(basepath+dirname): continue
                if not os.path.exists(basepath + dirname):
                    os.makedirs(basepath + dirname)
                fpath = basepath + dirname + "/" + fname + ".jpg"
                store_img((imgurl, fpath))
                #print(fpath)
                #urls.append((imgurl, fpath))

    p = Pool(8)
    p.map(store_img, urls)
    p.close()
    en = time.time()
    print(data, "in", round(en-st,2), "seconds.")

def store_img(arg):
    imgurl, fpath = arg
    print(imgurl)
    opener = urllib.request.URLopener()
    opener.addheader("User-agent", "Mozilla/5.0")
    opener.retrieve(imgurl, fpath)
    #print(fpath)

def parsedat(pars):
    #['@32.1289361', '34.7932176', '3a', '75y', '196.92h', '96.86t']
    lat, lon,_,fov,h,t = pars.split(",")
    lat = lat.replace("@","")
    fov = fov.replace("y","")
    h = h.replace("h","")
    t = t.replace("t","")
    data = dict()
    data["latitude"] = lat
    data["longitude"] = lon
    data["fov"] = fov
    data["heading"] = h
    data["pitch"] = "0"
    return data
 

if __name__ == "__main__":
    run()

