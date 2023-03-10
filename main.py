from flask import Flask, redirect, url_for, render_template, request, session
import ote_minimizer

app = Flask(__name__)
# secret key must be defined to declare a user session
    # NOT NECESSARY TO KEEP SECRET FOR NOW
    # SECURITY HANDLED AT DEPLOYMENT LEVEL
app.secret_key = "secret"

# displays start screen of loader dispatch
# user enters # of loaders, # of doors, and starting door number
@app.route("/")
def home():
    return render_template("home.html")

# displays information about the loader dispatch algorithm
@app.route("/about")
def about():
    return render_template("about.html")

# user enters loader name and pph for each loader, and door fph
@app.route("/flow", methods=['POST'])
def flow():
    loaders_num = request.values['loaders_num']
    doors_num = request.values['doors_num']
    start_door_num = request.values['start_door_num']
    # store start door number for use in /dispatch
    session["start_door_num"] = int(start_door_num)

    return render_template(
        "flow.html",
        loaders_num= int(loaders_num),
        doors_num= int(doors_num),
        start_door_num= int(start_door_num)
    )

# returns loader assignments, OTEs, and individual OTEs for each assignment
@app.route("/dispatch", methods=['POST'])
def dispatch():
    # get loader name and pph for OTE minimizer
    loader_dict = {
        request.values[f"name{i}"] : int(request.values[f"pph{i}"])
        for i in range(len(
            [name for name in request.form.keys() if name.startswith('name')]
        ))
    }

    # get door fphs for OTE minimizer
    door_array = [
        int(request.values[f"fph{i}"])
        for i in range(len(
            [door for door in request.form.keys() if door.startswith('fph')]
        ))
    ]

    # run OTE minimizer
    assignments, assignment_otes, total_otes = ote_minimizer.minimize_ote(
        loader_dict, door_array
    )

    start_door_num = session["start_door_num"]
    loader_names = [name for name in assignments.keys()]
    # extract door assignments from lists as strings for HTML display
    door_assignments = [
        ', '.join([str(door + start_door_num) for door in doors])
        for doors in assignments.values()
    ]

    return render_template(
        'dispatch.html',
        loader_names= loader_names,
        door_assignments= door_assignments,
        assignment_otes= assignment_otes,
        total_otes= total_otes
    )

if __name__ == "__main__":
    app.run()