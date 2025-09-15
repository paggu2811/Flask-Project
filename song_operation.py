from flask import render_template, redirect, request, url_for
import mysql.connector
import os
from werkzeug.utils import secure_filename


con = mysql.connector.connect(host="localhost",user="root",password="pragati@123", use_pure=True,database="music_storedb")

def addsong():
    if request.method == "GET":
        
        sql = "SELECT * FROM category"
        cursor = con.cursor()
        cursor.execute(sql)
        cats = cursor.fetchall()
        return render_template("addsong.html", cats=cats)
    
    else:
        cname = request.form.get("cname")
        subscription_plan = request.form.get("subscription_plan")
        description = request.form.get("description")
        cid = request.form.get("cid")

        
        image_file = request.files['image_url']
        image_filename = secure_filename(image_file.filename)
        image_folder = "static/Images"
        image_path = os.path.join(image_folder, image_filename)
        image_file.save(image_path)
        image_url = "Images/" + image_filename


        audio_file = request.files['audio_url']
        audio_filename = secure_filename(audio_file.filename)
        audio_folder = "static/Audios"
        audio_path = os.path.join(audio_folder, audio_filename)
        audio_file.save(audio_path)
        audio_url = "Audios/" + audio_filename

        
        sql = """
            INSERT INTO Songs (song_name, subscription_plan, description, image_url, audio_url, cid)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        val = (cname, subscription_plan, description, image_url, audio_url, cid)
        cursor = con.cursor()
        cursor.execute(sql, val)
        con.commit()

        return "Song Added Successfully with Subscription Plan!"

def showAllsong():
    sql = "SELECT * FROM song_cat_vw"
    cursor = con.cursor()
    cursor.execute(sql)
    songs = cursor.fetchall()
    return render_template("showAllsong.html", songs=songs)
