from flask import render_template, redirect, request, url_for, session
import mysql.connector
from datetime import datetime  

con = mysql.connector.connect(host="localhost",user="root", password="pragati@123",use_pure=True,database="music_storedb")


PLAN_PRICES = {
    "Free": 0,
    "Monthly": 199,
    "Yearly": 999
}

def homepage():
    cursor = con.cursor()
    sql = "select * from category"
    cursor.execute(sql)
    cats = cursor.fetchall()

    sql = "select * from Songs"
    cursor.execute(sql)
    songs = cursor.fetchall()

    return render_template("homepage.html", cats=cats, songs=songs)

def ViewSongs(cid):
    sql = "select * from Songs where cid=%s"
    val = (cid,)
    cursor = con.cursor()
    cursor.execute(sql, val)
    songs = cursor.fetchall()
    sql = "select * from category"
    cursor.execute(sql)
    cats = cursor.fetchall()

    return render_template("homepage.html", cats=cats, songs=songs)

def ViewDetails(song_id):
    cursor = con.cursor()
    if request.method == "GET":
        sql = "select * from Songs where song_id=%s"
        val = (song_id,)
        cursor.execute(sql, val)
        song = cursor.fetchone()
        sql = "select * from category"
        cursor.execute(sql)
        cats = cursor.fetchall()
        return render_template("ViewDetails.html", cats=cats, song=song)
    else:
        if "uname" in session:
            song_id = request.form.get("song_id")
            username = session["uname"]
            plan = request.form.get("subscription_plan")

           
            price = PLAN_PRICES.get(plan, 0)

            
            sql = "select count(*) from myplaylist where username=%s and song_id=%s and subscription_plan=%s"
            val = (username, song_id, plan)
            cursor.execute(sql, val)
            count = cursor.fetchone()[0]
            if count == 1:
                return "This item with same plan already exists in playlist"
            else:
               
                sql = "insert into myplaylist(song_id, username, subscription_plan, subtotal) values (%s,%s,%s,%s)"
                val = (song_id, username, plan, price)
                cursor.execute(sql, val)
                con.commit()
                return "Item added to Playlist"
        else:
            return redirect(url_for("login"))

def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        uname = request.form.get("uname")
        pwd = request.form.get("pwd")
        sql = "select count(*) from user_info where username=%s"
        val = (uname,)
        cursor = con.cursor()
        cursor.execute(sql, val)
        count = cursor.fetchone()[0]
        if count == 1:
            return "User already exists"
        else:
            sql = "insert into user_info values (%s,%s)"
            val = (uname, pwd)
            cursor.execute(sql, val)
            con.commit()
            return "User created.."

def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        uname = request.form.get("uname")
        pwd = request.form.get("pwd")
        sql = "select count(*) from user_info where username=%s and password=%s"
        val = (uname, pwd)
        cursor = con.cursor()
        cursor.execute(sql, val)
        count = cursor.fetchone()[0]
        if count == 1:
            session["uname"] = uname
            return redirect(url_for("homepage"))
        else:
            return redirect(url_for("login"))

def logout():
    if "uname" in session:
        session.clear()
        return redirect(url_for("homepage"))
    else:
        return redirect(url_for("login"))

def showplaylist():
    if request.method == "GET":
        username = session["uname"]

        cursor = con.cursor()
        sql = "select * from myplaylist_vw where username=%s"
        cursor.execute(sql, (username,))
        items = cursor.fetchall()

        sql = "select * from category"
        cursor.execute(sql)
        cats = cursor.fetchall()
        sql = "select sum(subtotal) from myplaylist_vw where username=%s"
        cursor.execute(sql, (username,))
        total = cursor.fetchone()[0] or 0

        session["total"] = total
        return render_template("showplaylist.html", cats=cats, items=items, total=total)

    else:
        action = request.form.get("action")
        mid = request.form.get("item_id")

        if action == "delete":
            sql = "delete from myplaylist where id=%s"
            val = (mid,)
            cursor = con.cursor()
            cursor.execute(sql, val)
            con.commit()

        return redirect(url_for("showplaylist"))



def payment():
    if request.method == "GET":
        return render_template("make_payment.html")
    else:
        card_no = request.form.get("card_no")
        cvv = request.form.get("cvv")
        expiry = request.form.get("expiry")
        cursor = con.cursor()

        sql = "select count(*) from account_details where cardno=%s and cvv=%s and expiry=%s"
        val = (card_no, cvv, expiry)
        cursor.execute(sql, val)
        count = cursor.fetchone()[0]

        if count == 1:
            
            sql = "update account_details set balance = balance-%s where cardno=%s"
            val = (session["total"], card_no)
            cursor.execute(sql, val)

            
            sql = "update account_details set balance = balance+%s where cardno=%s"
            val = (session["total"], '4321')
            cursor.execute(sql, val)

            
            # sql = "update myplaylist set subscription_plan is not null where username=%s"
            # val = (session["uname"],)
            # cursor.execute(sql, val)

            con.commit()
            session.pop("total")

            return render_template("payment_status.html", status="success")
        else:
            return render_template("payment_status.html", status="failed")