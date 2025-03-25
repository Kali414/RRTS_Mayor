from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import pymongo

from db import mayor,complaint,issues
from app import app

# @app.route("/")
# def home():
#     return render_template("home.html")

@app.route('/mhome')
def mhome():
    if not session.get("name"):
        return redirect(url_for("auth.login"))  # Redirect if user is not logged in

    



    return render_template("mhome.html")


@app.route('/mdashboard')
def mdashboard():
    if not session.get("name"):
        return redirect(url_for("auth.login"))
        # These lines should be **outside** the if block to ensure they always execute
    total = issues.count_documents({"city": session["city"]})
    completed = issues.count_documents({"city": session["city"], "status": "Completed"})
    pending = issues.count_documents({"city": session["city"], "status": "Pending"})
    priority = issues.count_documents({"city": session["city"], "severity_level": "High"})
    print("Total:", total, "Completed:", completed, "Pending:", pending, "Priority:", priority)
    
    return render_template("mdashboard.html", total=total, completed=completed, priority=priority, pending=pending)

@app.route("/msettings")
def msettings():
    if not session.get("name"):
        return redirect(url_for("auth.login"))
    
    return render_template("msettings.html")

@app.route("/statistics")
def statistics():
    if not session.get("name"):
        return redirect(url_for("auth.login"))

    return render_template("statistics.html")

@app.route("/update_profile",methods=["POST"])
def update_profile():
    if not session.get("name"):
        return redirect(url_for("auth.login"))

    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        city=request.form["city"]
        curr_password=request.form["current_password"]
        new_password=request.form["new_password"]

        filterr={"_id":session["_id"]}
        change= {"$set": {"name":name,"email":email,"city":city,"password":new_password}}

        mayor.update_one(filterr,change)

        session["name"]=name
        session["email"]=email
        session["city"]=city

        return redirect(url_for("msettings"))
    
    return redirect(url_for("msettings"))


@app.route("/get_repairs")
def get_repairs():
    city = session.get("city", "DefaultCity")  # Replace with actual session value
    repairs = list(issues.find({"city": city})
               .sort([("id", pymongo.DESCENDING)])  # Ensures proper sorting
               .limit(10))
    
    return jsonify(repairs)


@app.route("/get_statistics/<start_date>/<end_date>")
def get_statistics(start_date,end_date):
    city = session.get("city", "DefaultCity")  # Replace with actual session value
    repairs = list(issues.find({"city": city},{"start_date":{'$gte': start_date, '$lte': end_date}})
               .sort([("id", pymongo.DESCENDING)]))  # Ensures proper sorting
    
    return jsonify(repairs)

@app.route("/repair_reports")
def repair_reports():
    if not session.get("name"):
        return redirect(url_for("auth.login"))

    return render_template("repair_reports.html")