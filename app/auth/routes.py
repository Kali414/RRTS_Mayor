from flask import  render_template, request, redirect, url_for, session

from database import mayor

from app.auth import auth

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
            
        user = mayor.find_one({"email": email, "password": password})
        
        if user:
            session["name"] = user["name"]
            session["role"]=user["role"]
            session["email"]=user["email"]
            session["number"]=user["number"]
            session["city"]=user["city"]
            session["state"]=user["state"]
            session['_id']=user["_id"]

            return redirect(url_for("mhome"))
                

        else:
            return redirect(url_for("auth.signup"))
        
            
    return render_template("login.html")


@auth.route("/signup" , methods=["GET","POST"])
def signup():
    if(request.method=="POST"):
        first_name=request.form.get("first")
        last_name=request.form.get("last")
        email=request.form.get("email")
        number=request.form.get("number")
        city=request.form.get("city")
        state=request.form.get("state")
        password=request.form.get("password")
        

        if(first_name and last_name and email and number and city and state and password):

            data={
                "name": first_name+" "+last_name,
                "email":email,
                "number":number,
                "city":city,
                "state":state,
                "password":password,
                "role":"Mayor"
            }

            user = mayor.find_one({"email": email, "password": password})
            if user:
                return redirect(url_for("auth.login"))

            last_doc = mayor.find_one(sort=[("_id", -1)])

            if last_doc is None:

                new_id = "M001"
            else:
                last_id = last_doc.get("_id")
                new_num = int(last_id[1:]) + 1
                new_id = "M" + str(new_num).zfill(3)

            data["_id"] = new_id
            mayor.insert_one(data)
            session["name"]=first_name+" "+last_name
            session["role"]="Mayor"
            session["email"]=email
            session["number"]=number
            session["city"]=city
            session["state"]=state
            session['_id']=new_id

            return redirect(url_for("mhome"))

            
        else:
            return redirect(url_for("signup"))

    return render_template("signup.html")


@auth.route('/logout')
def clear_session():
    session.clear()
    return redirect("https://roadcare.onrender.com/")