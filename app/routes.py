from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import pymongo
from datetime import datetime
from database import mayor,issues,supervisor
from app import app

from bson import DBRef
from bson.son import SON

# @app.route("/")
# def home():
#     return render_template("home.html")

# Helper to convert non-serializable types
def clean_document(doc):
    cleaned = {}
    for key, value in doc.items():
        if isinstance(value, DBRef):
            cleaned[key] = str(value)  # Or value.id if you want just the reference ID
        elif isinstance(value, list):
            cleaned[key] = [str(v) if isinstance(v, DBRef) else v for v in value]
        elif isinstance(value, dict):
            cleaned[key] = clean_document(value)
        else:
            cleaned[key] = value
    return cleaned

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
    priority = issues.count_documents({"city": session["city"], "severity": "High"})
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

    total = issues.count_documents({"city": session["city"]})
    completed = issues.count_documents({"city": session["city"], "status": "Completed"})
    inprogress = issues.count_documents({"city": session["city"], "status": "In Progress"})  # Add this line to calculate in-progress repairs
    pending = issues.count_documents({"city": session["city"], "status": "Pending"})
    priority = issues.count_documents({"city": session["city"], "severity": "High"})
    pipeline = [
    {"$group": {"_id": "$city", "total": {"$sum": "$estimated_cost"}}}
    ]
    budget = list(issues.aggregate(pipeline))[0]["total"]
    print(budget)
    superv = len(issues.distinct("supervisor_name", {"city": session["city"]}))
    print("Total:", total, "Completed:", completed, "Pending:", pending, "Priority:", priority,"Budget:",budget,"Supervisor:",superv)
    

    return render_template("statistics.html", total=total, completed=completed, inprogress=inprogress, pending=pending, budget=budget,supervisor=superv)

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

    # Fetch data, exclude _id and resources
    raw_repairs = list(
        issues.find({"city": city}, {"_id": 0, "resources": 0})
              .sort([("id", pymongo.DESCENDING)])
              .limit(10)
    )

    # Clean each document for JSON serialization
    cleaned_repairs = [clean_document(doc) for doc in raw_repairs]

    return jsonify(cleaned_repairs)

@app.route("/repair_reports")
def repair_reports():
    if not session.get("name"):
        return redirect(url_for("auth.login"))

    return render_template("repair_reports.html")



@app.route("/getsupervisors")
def get_supervisors():
    if not session.get("name"):
        return redirect(url_for("auth.login"))

    try:
        city = session["city"]

        pipeline = [
            {"$match": {
                "city": city
            }},
            {"$group": {
                "_id": "$supervisor_name",
                "projects_assigned": {"$sum": 1},
                "projects_completed": {"$sum": {"$cond": [{"$eq": ["$status", "Completed"]}, 1, 0]}}
            }},
            {"$project": {
                "_id": 0,
                "name": "$_id",
                "projects_assigned": 1,
                "projects_completed": 1,
                "performance_rating": {
                    "$cond": [
                        {"$eq": ["$projects_assigned", 0]},
                        0,
                        {
                            "$round": [
                                {"$multiply": [{"$divide": ["$projects_completed", "$projects_assigned"]}, 5]}, 1
                            ]
                        }
                    ]
                },
                "area": {
                    "$literal": city
                }
            }}
        ]

        results = list(issues.aggregate(pipeline))
        return jsonify(results)

    except Exception as e:
        print("Error in get_supervisors:", e)
        return jsonify({"error": "Failed to retrieve supervisor data"}), 500



@app.route("/getlocations")
def get_locations():
    if not session.get("name"):
        return redirect(url_for("auth.login"))

    try:
        start_date_str = request.args.get("start_date")
        end_date_str = request.args.get("end_date")

        # Parse ISO format from HTML date input
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        city = session["city"]

        pipeline = [
            {"$match": {
                "city": city,
                "issueDate": {"$gte": start_date, "$lte": end_date}
            }},
            {"$group": {
                "_id": "$location",
                "total_repairs": {"$sum": 1},
                "completed": {"$sum": {"$cond": [{"$eq": ["$status", "Completed"]}, 1, 0]}},
                "in_progress": {"$sum": {"$cond": [{"$eq": ["$status", "In Progress"]}, 1, 0]}},
                "pending": {"$sum": {"$cond": [{"$eq": ["$status", "Pending"]}, 1, 0]}},
                "budget": {"$sum": "$estimated_cost"}
            }},
            {"$sort": SON([("budget", -1)])}
        ]

        results = list(issues.aggregate(pipeline))

        # Format results
        formatted_data = []
        for item in results:
            formatted_data.append({
                "name": item["_id"],
                "total_repairs": item["total_repairs"],
                "completed": item["completed"],
                "in_progress": item["in_progress"],
                "pending": item["pending"],
                "budget": item["budget"]
            })

        return jsonify(formatted_data)

    except Exception as e:
        print("Error in get_locations:", e)
        return jsonify({"error": "Error retrieving data"}), 500