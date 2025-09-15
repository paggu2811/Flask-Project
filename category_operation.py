from flask import render_template,redirect,request,url_for
import mysql.connector


con = mysql.connector.connect(host="localhost",user="root",password="pragati@123",use_pure=True,database="music_storedb")

def addCategory1():
    if request.method == "GET":
        return render_template("addCategory1.html")
    
    else:
        cname = request.form.get("cname")
        sql = "insert into Category (cname) values (%s)"
        val = (cname,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        con.commit()
        
        return redirect(url_for("showAllCategory1"))
    
def showAllCategory1():
    sql="select * from Category"
    cursor=con.cursor()
    cursor.execute(sql)
    cats=cursor.fetchall()
    return render_template("showAllCategory1.html",cats=cats) 

def deleteCategory1(cid):
    if request.method=="GET":
        return render_template("deleteCategory1.html")
    else:
        action=request.form.get("action")
        print(action)
        if action=="Yes":
            sql="delete from Category where cid=%s"
            val=(cid,)
            cursor=con.cursor()
            cursor.execute(sql,val)
            con.commit()
        else:
            return "Hello"    
        return redirect(url_for("showAllCategory1"))

def editCategory1(cid):
    if request.method=="GET":
        sql="select * from Category where cid=%s"
        val=(cid,)
        cursor=con.cursor()
        cursor.execute(sql,val)
        cat=cursor.fetchone()
        return render_template("editCategory1.html",cat=cat)
    else:
        cname=request.form.get("cname")
        sql="update Category set cname=%s where cid=%s"
        val=(cname,cid)
        cursor=con.cursor()
        cursor.execute(sql,val)
        con.commit()
        return redirect("/showAllCategory1")
