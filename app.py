from flask import Flask, render_template
from flask import request
import threeoneone as threeOneOne

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        print ("POST DETECTED")
        user_location = request.form ["loc"]
        accessibility_input = request.form["accessibility"]
        print (accessibility_input)
        complaint_reason = request.form["Complaint Type"]
        route_num = request.form["Route Number"] 
        route_dir = request.form["Route Direction"]
        stop_id = request.form ["stop_id"]
        incident_date_input = request.form["date"]
        incident_time_input = request.form ["time"]
        first_name_input = request.form["first_name"]
        last_name_input = request.form["last_name"]
        threeOneOne.run_selenium(user_location, complaint_reason, accessibility_input, route_num, route_dir, stop_id, incident_date_input, incident_time_input, first_name_input, last_name_input)
        return render_template("submit.html", route_num = route_num, first_name_input = first_name_input)
    else:
        home()



if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug = True)
