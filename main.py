from flask import Flask, flash, render_template, request, session, redirect, url_for
from .overflow_minimizer import minimize_overflow
from .input_validation import HomeForm

app = Flask(__name__)
# secret key must be defined to declare a user session
    # NOT NECESSARY TO KEEP SECRET FOR NOW
    # SECURITY HANDLED AT DEPLOYMENT LEVEL
app.secret_key = "secret"

# displays start screen of loader dispatch
# user enters # of loaders, # of doors, and starting door number
@app.route("/")
def home():
    form = HomeForm()

    return render_template("home.html", form=form)

# displays information about the loader dispatch algorithm
@app.route("/about")
def about():
    return render_template("about.html")

# user enters loader name and pph for each loader, and door fph
@app.route("/flow_redirect", methods=['POST'])
def flow_redirect():
    # store start door number for use in /dispatch
    session['start_door_num'] = int(request.values['start_door_num'])
    session['loaders_num'] = int(request.values['loaders_num'])
    session['doors_num'] = int(request.values['doors_num'])
    return redirect(url_for('flow'))

# redirect used for UX, browser back button works
@app.route("/flow", methods=['GET'])
def flow():
    return render_template(
        "flow.html",
        loaders_num= session['loaders_num'],
        doors_num= session['doors_num'],
        start_door_num= session['start_door_num']
    )

# returns loader assignments, area overflow, and individual overflow for each assignment
@app.route("/dispatch", methods=['POST'])
def dispatch():
    # get loader name and pph for overflow minimizer
    loader_dict = {
        request.values[f"name{i}"] : int(request.values[f"pph{i}"])
        for i in range(len(
            [name for name in request.form.keys() if name.startswith('name')]
        ))
    }

    # get door fphs for overflow minimizer
    door_array = [
        int(request.values[f"fph{i}"])
        for i in range(len(
            [door for door in request.form.keys() if door.startswith('fph')]
        ))
    ]

    # run overflow minimizer
    assignments, assignment_overflow, total_overflow = minimize_overflow(
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
        assignment_overflow= assignment_overflow,
        total_overflow= total_overflow
    )

if __name__ == "__main__":
    app.run()