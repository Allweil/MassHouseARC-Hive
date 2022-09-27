#!/usr/bin/python3
from flask import Flask, render_template, flash, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from config import Config
import requests
import urllib
from bs4 import BeautifulSoup
import time
import pymysql
from operator import itemgetter
import random


application = Flask(__name__)
application.secret_key = Config.SECRET_KEY
application.config.from_object(Config)

def get_soup(u):
    user_agent = {'User-agent':'Mozilla/5.0'}
    html = requests.get(u, headers = user_agent)
    return html.content

def getcursor(db="STV"):
    return pymysql.connect(host = Config.host, user = Config.user,
                           password = Config.password, database = "STV",
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

@application.route("/stvs/list")
def list_recs():
    conn = getcursor()
    cursor = conn.cursor()
    cursor.execute("select f,addr from records")
    data = sorted([(str(i['f']),i['addr']) for i in cursor.fetchall()], reverse=True)
    return render_template("list.html", data=data)

@application.route("/stvs/view")
@application.route("/stvs/view/<rec>")
def view(rec=1562503117602):
    data = dict()
    data["id"] = rec
    conn = getcursor()
    cursor = conn.cursor()
    cursor.execute("select * from records where f=%s",rec)
    keys = "mg","vl","pa","tf","sb","fb","fc","cr","mof"
    for i in cursor.fetchall():
        lat, lng = float(i['lat']), float(i['lng'])
        f,p,h = int(i['fov']),int(i['pit']),int(i['h'])
        addr = i['addr']
        data["lat"] = lat
        data["lng"] = lng
        data["fov"] = f
        data["pitch"] = p
        data["heading"] = h
        data["addr"] = addr
        data["labels"] = dict()
        for k in keys:
            data["labels"][k] = int(i[k])

    imgsrc = str(rec) + ".jpg"
    data["img"] = imgsrc

    return render_template("view.html", data=data)
    pass

@application.route("/stvs/markup/<swatch>", methods=["GET", "POST"])
def staggered_balconies(swatch="staggered_balconies"):
    data = get_random_entries(swatch=swatch)
    form = MarkupForm()
    if form.validate_on_submit():
        l0 = form.l0.data
        l1 = form.l1.data
        l2 = form.l2.data
        l3 = form.l3.data
        l4 = form.l4.data
        l5 = form.l5.data
        l6 = form.l6.data
        l7 = form.l7.data
        l8 = form.l8.data
        vals = [l0, l1, l2, l3, l4, l5, l6, l7, l8]
        vals = [1 if x else 0 for x in vals]
        records = []
        for i, _ in enumerate(data['imgs']):
            records.append((data['imgs'][i], vals[i]))
        form.l0.data = 0
        form.l1.data = 0
        form.l2.data = 0
        form.l3.data = 0
        form.l4.data = 0
        form.l5.data = 0
        form.l6.data = 0
        form.l7.data = 0
        form.l8.data = 0
        update_records(records, swatch)
        redirect("/stvs/markup/" + swatch)
    return render_template("markup.html", data=data, form=form)

@application.route("/stvs/markup_detailed/<swatch>", methods=["GET", "POST"])
def staggered_balconies_detailed(swatch="staggered_balconies"):
    data = get_random_entries(swatch=swatch)
    form = MarkupFormDetailed()
    if form.validate_on_submit():
        l0 = form.l0.data
        l0a = form.l0a.data
        l0b = form.l0b.data
        l0c = form.l0c.data
        l0d = form.l0d.data
        l0e = form.l0e.data

        l1 = form.l1.data
        l1a = form.l1a.data
        l1b = form.l1b.data
        l1c = form.l1c.data
        l1d = form.l1d.data
        l1e = form.l1e.data

        l2 = form.l2.data
        l2a = form.l2a.data
        l2b = form.l2b.data
        l2c = form.l2c.data
        l2d = form.l2d.data
        l2e = form.l2e.data

        l3 = form.l3.data
        l3a = form.l3a.data
        l3b = form.l3b.data
        l3c = form.l3c.data
        l3d = form.l3d.data
        l3e = form.l3e.data

        l4 = form.l4.data
        l4a = form.l4a.data
        l4b = form.l4b.data
        l4c = form.l4c.data
        l4d = form.l4d.data
        l4e = form.l4e.data

        l5 = form.l5.data
        l5a = form.l5a.data
        l5b = form.l5b.data
        l5c = form.l5c.data
        l5d = form.l5d.data
        l5e = form.l5e.data

        l6 = form.l6.data
        l6a = form.l6a.data
        l6b = form.l6b.data
        l6c = form.l6c.data
        l6d = form.l6d.data
        l6e = form.l6e.data

        l7 = form.l7.data
        l7a = form.l7a.data
        l7b = form.l7b.data
        l7c = form.l7c.data
        l7d = form.l7d.data
        l7e = form.l7e.data


        l8 = form.l8.data
        l8a = form.l8a.data
        l8b = form.l8b.data
        l8c = form.l8c.data
        l8d = form.l8d.data
        l8e = form.l8e.data

        vals = [[l0,l0a, l0b, l0c,l0d,l0e],
                [l1,l1a, l1b, l1c,l1d,l1e],
                [l2,l2a, l2b, l2c,l2d,l2e],
                [l3,l3a, l3b, l3c,l3d,l3e],
                [l4,l4a, l4b, l4c,l4d,l4e],
                [l5,l5a, l5b, l5c,l5d,l5e],
                [l6,l6a, l6b, l6c,l6d,l6e],
                [l7,l7a, l7b, l7c,l7d,l7e],
                [l8,l8a, l8b, l8c,l8d,l8e]]
        tvals = []
        for val in vals:
            print(val)
            sub = [1 if x else 0 for x in val]
            print(sub)
            tvals.append(sub)
        print(tvals)

        records = []
        for i, _ in enumerate(data['imgs']):
            records.append((data['imgs'][i], tvals[i]))
        form.l0.data = 0
        form.l0a.data = 0
        form.l0b.data = 0
        form.l0c.data = 0
        form.l0d.data = 0
        form.l0e.data = 0

        form.l1.data = 0
        form.l1a.data = 0
        form.l1b.data = 0
        form.l1c.data = 0
        form.l1d.data = 0
        form.l1e.data = 0

        form.l2.data = 0
        form.l2a.data = 0
        form.l2b.data = 0
        form.l2c.data = 0
        form.l2d.data = 0
        form.l2e.data = 0

        form.l3.data = 0
        form.l3a.data = 0
        form.l3b.data = 0
        form.l3c.data = 0
        form.l3d.data = 0
        form.l3e.data = 0

        form.l4.data = 0
        form.l4a.data = 0
        form.l4b.data = 0
        form.l4c.data = 0
        form.l4d.data = 0
        form.l4e.data = 0

        form.l5.data = 0
        form.l5a.data = 0
        form.l5b.data = 0
        form.l5c.data = 0
        form.l5d.data = 0
        form.l5e.data = 0

        form.l6.data = 0
        form.l6a.data = 0
        form.l6b.data = 0
        form.l6c.data = 0
        form.l6d.data = 0
        form.l6e.data = 0

        form.l7.data = 0
        form.l7a.data = 0
        form.l7b.data = 0
        form.l7c.data = 0
        form.l7d.data = 0
        form.l7e.data = 0

        form.l8.data = 0
        form.l8a.data = 0
        form.l8b.data = 0
        form.l8c.data = 0
        form.l8d.data = 0
        form.l8e.data = 0

        update_records_det(records, swatch)

        redirect("/stvs/markup_detailed/" + swatch)
    return render_template("markup1.html", data=data, form=form)


def update_records(records, swatch):
    dbconn = getcursor(db="STV")
    cursor = dbconn.cursor()
    q = "insert into " + swatch + " (pid, upd, label) values (%s, %s, %s)\
    on duplicate key update upd=%s, label=%s"
    for (pid, label) in records:
        cursor.execute(q, (pid, 1, label, 1, label))
    dbconn.commit()
    dbconn.close()

def update_records_det(records, swatch):
    dbconn = getcursor(db="STV")
    cursor = dbconn.cursor()
    q = "insert into " + swatch + " (pid, upd, label,a,b,c,d,e) values (%s,\
    %s,%s,%s,%s,%s,%s,%s)\
    on duplicate key update upd=%s, label=%s,a=%s,b=%s,c=%s,d=%s,e=%s"
    for (pid, labs) in records:
        l,a,b,c,d,e=labs
        row = pid,1,l,a,b,c,d,e,1,l,a,b,c,d,e
        cursor.execute(q, row)
    dbconn.commit()
    dbconn.close()


def get_random_entries(swatch="staggered_balconies"):
    data = dict()
    dbconn = getcursor(db="STV")
    cursor = dbconn.cursor()
    cursor.execute("select pid, sel, upd from " + swatch)
    fs = {(str(i['pid']), int(i['sel']), int(i['upd'])) for i in cursor.fetchall()}
    data['total_imgs'] = len(fs)
    el = [x for x in fs if x[1] == 0]
    data['img_todo'] = len(el)
    selected = [x[0] for x in random.sample(el, 9)]
    data['imgs'] = selected
    data['swatch'] = swatch
    for rec in selected:
        cursor.execute("insert into " + swatch + " (pid, sel) values (%s, %s)\
                       on duplicate key update sel=%s", (rec, 1, 1))
    dbconn.commit()
    dbconn.close()
    return data

@application.route("/", methods=["GET","POST"])
@application.route("/stvs", methods=["GET","POST"])
@application.route("/stvs/collect", methods=["GET","POST"])
def collect():
    data = dict()
    form = Address()
    if form.validate_on_submit():
        address = form.address.data
        base = "https://maps.googleapis.com/maps/api/geocode/json?address=" 
        fov = form.fov.data
        pitch = form.pitch.data
        heading = form.heading.data
        final = form.final.data
        if address and not final:
            u = base + address + "&key=" + Config.google_api_key
            json = getjson(u)
            if json["status"] == "OK":
                results = json["results"][0]
                data["formatted_address"] = results["formatted_address"]
                data["latitude"] = results["geometry"]["location"]["lat"]
                data["longitude"] = results["geometry"]["location"]["lng"]
                data["fov"] = fov
                data["pitch"] = pitch
                data["heading"] = heading
            else:
                flash("Result for address requested is {}".format(json["status"]))
                return redirect("/stvs/collect")
        elif address and final:
            mg = form.multigrid.data
            vl = form.villa.data
            ga = form.parasite.data
            tf = form.threedfac.data
            sb = form.stagbal.data
            fb = form.fakebal.data
            fc = form.fakecol.data
            cr = form.col.data
            mof = form.morethanfour.data
            fov = form.fov.data
            pi = form.pitch.data
            he = form.heading.data
            frow = mg,vl,ga,tf,sb,fb,fc,cr,mof

            features = list()
            for f in frow:
                if f == False: features.append(0)
                elif f == True: features.append(1)
            u = base + address + "&key=" + Config.google_api_key
            json = getjson(u)
            if json["status"] == "OK":
                results = json["results"][0]
                lat = results["geometry"]["location"]["lat"]
                lon = results["geometry"]["location"]["lng"]
                data["formatted_address"] = results["formatted_address"]
                data["latitude"] = lat
                data["longitude"] = lon
                data["fov"] = fov
                data["pitch"] = pitch
                data["heading"] = heading
                imgurlbase = "https://maps.googleapis.com/maps/api/streetview"
                loc = "?size=400x400&location="+str(data["latitude"]) + "," + str(data["longitude"])
                rest = "&fov="+fov+"&heading="+heading+"&pitch="+pitch+"&key="+Config.google_api_key
                imgurl = imgurlbase+loc+rest
                timestamp = int(time.time()*1000)
                fpath = "/home/kartikeya/work/gstvs/static/stvs/" + str(timestamp) + ".jpg"
                urllib.request.urlretrieve(imgurl, fpath)
                addr = data["formatted_address"]
                ident = timestamp,addr,lat,lon,fov,pi,he
                row = list(ident) + features
                data["record"] = timestamp
                save_record_to_database(row)

    return render_template("research.html", form=form, data=data)

def save_record_to_database(row):
    conn = getcursor()
    cursor = conn.cursor()
    q = "insert into records (f,addr,lat,lng,fov,pit,h,mg,vl,pa,tf,sb,fb,fc,cr,mof)\
    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key\
    update f=%s,mg=%s,vl=%s,pa=%s,tf=%s,sb=%s,\
    fb=%s,fc=%s,cr=%s,mof=%s"
    timestamp,addr,lat,lon,fov,pi,he,mg,vl,ga,tf,sb,fb,fc,cr,mof = row
    dup = timestamp,mg,vl,ga,tf,sb,fb,fc,cr,mof
    cursor.execute(q,tuple(row)+dup)
    conn.commit()
    conn.close()

class MarkupForm(FlaskForm):
    l0 = BooleanField("l0")
    l1 = BooleanField("l1")
    l2 = BooleanField("l2")
    l3 = BooleanField("l3")
    l4 = BooleanField("l4")
    l5 = BooleanField("l5")
    l6 = BooleanField("l6")
    l7 = BooleanField("l7")
    l8 = BooleanField("l8")
    submit = SubmitField("Submit")

class MarkupFormDetailed(FlaskForm):
    l0 = BooleanField("l0")
    l0a = BooleanField("l0a")
    l0b = BooleanField("l0b")
    l0c = BooleanField("l0c")
    l0d = BooleanField("l0d")
    l0e = BooleanField("l0e")

    l1 = BooleanField("l1")
    l1a = BooleanField("l1a")
    l1b = BooleanField("l1b")
    l1c = BooleanField("l1c")
    l1d = BooleanField("l1d")
    l1e = BooleanField("l1e")


    l2 = BooleanField("l2")
    l2a = BooleanField("l2a")
    l2b = BooleanField("l2b")
    l2c = BooleanField("l2c")
    l2d = BooleanField("l2d")
    l2e = BooleanField("l2e")


    l3 = BooleanField("l3")
    l3a = BooleanField("l3a")
    l3b = BooleanField("l3b")
    l3c = BooleanField("l3c")
    l3d = BooleanField("l3d")
    l3e = BooleanField("l3e")


    l4 = BooleanField("l4")
    l4a = BooleanField("l4a")
    l4b = BooleanField("l4b")
    l4c = BooleanField("l4c")
    l4d = BooleanField("l4d")
    l4e = BooleanField("l4e")


    l5 = BooleanField("l5")
    l5a = BooleanField("l5a")
    l5b = BooleanField("l5b")
    l5c = BooleanField("l5c")
    l5d = BooleanField("l5d")
    l5e = BooleanField("l5e")


    l6 = BooleanField("l6")
    l6a = BooleanField("l6a")
    l6b = BooleanField("l6b")
    l6c = BooleanField("l6c")
    l6d = BooleanField("l6d")
    l6e = BooleanField("l6e")


    l7 = BooleanField("l7")
    l7a = BooleanField("l7a")
    l7b = BooleanField("l7b")
    l7c = BooleanField("l7c")
    l7d = BooleanField("l7d")
    l7e = BooleanField("l7e")


    l8 = BooleanField("l8")
    l8a = BooleanField("l8a")
    l8b = BooleanField("l8b")
    l8c = BooleanField("l8c")
    l8d = BooleanField("l8d")
    l8e = BooleanField("l8e")


    submit = SubmitField("Submit")



class Address(FlaskForm):
    address = StringField("address", validators=[DataRequired()])
    fov = StringField("field of view", validators=[DataRequired()], default=90)
    heading = StringField("heading", validators=[DataRequired()], default=235)
    pitch = StringField("pitch", validators=[DataRequired()],default=10)
    submit = SubmitField("Submit")
    multigrid = BooleanField("multigrid")
    villa = BooleanField("villa")
    parasite = BooleanField("parasite")
    safacade = BooleanField("standalone facade")
    threedfac = BooleanField("3D facade")
    stagbal = BooleanField("staggered balconies")
    fakebal = BooleanField("fake balconies")
    fakecol = BooleanField("fake columns")
    col = BooleanField("color")
    morethanfour = BooleanField("over four stories")
    final = BooleanField("Finalize entry")

def getjson(u):
    uf = u+":formatted"
    j = requests.get(u)
    return j.json()


if __name__ == "__main__":
    application.run(debug = True, host = "0.0.0.0", port=5000)


