from flask import (Flask, render_template, request)
from datetime import datetime
import requests
app = Flask(__name__)
BASE_URL = "http://127.0.0.1:5000/tasks"

# @app.get("/<name>")
# def main(name):
#     out= ""
#     for number in range(1,7):
#         out+="<h%s>Hello, %s</h%s>\n" %(number, name, number)
#     return out

@app.get("/")
def main():
    timestamp=datetime.now().strftime("%F %H:%M:%S")
    return render_template("home.html", ts=timestamp)

@app.get("/about")
def about_page():
    return render_template("about.html")

@app.get("/tasks")
def display_all_tasks():
    resp = requests.get(BASE_URL)
    if resp.status_code==200:
        task_list= resp.json().get("tasks")
        return render_template("list.html", tasks=task_list)
    return render_template("error.html", err=resp.status_code), resp.status_code

@app.get("/tasks/<int:pk>")
def display_task(pk):
    url= "%s/%s" % (BASE_URL, pk)
    resp = requests.get(url)
    if resp.status_code ==200:
        task = resp.json().get("task")
        return render_template("detail.html", task=task)
    return render_template("error.html", err=resp.status_code), resp.status_code

@app.get("/tasks/new")
def new_task_form():
    return render_template("new.html")

@app.post("/tasks/new")
def create_task():
    task_data = request.form
    task_json = {
        "summary" : task_data.get("summary"),
        "description": task_data.get("description")
    }
    resp = requests.post(BASE_URL, json=task_json)
    if resp.status_code==204:
        return render_template("success.html", message="New task created")
    return render_template("error.html", err=resp.status_code), resp.status_code


@app.route("/tasks/<int:pk>", methods=["DELETE", "POST"])
def delete_task(pk):
    url= "%s/%s" % (BASE_URL, pk)
    resp = requests.delete(url)
    if resp.status_code == 204:
        return render_template("success.html", message="Task deleted")
    return render_template("error.html", err=resp.status_code), resp.status_code

    
    
    