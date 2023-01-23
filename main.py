from flask import Flask, redirect, url_for, render_template, request
import json

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        loaders_num = request.form["loaders_num"]
        doors_num = request.form["doors_num"]
        start_door_num = request.form["start_door_num"]
        return redirect(url_for(
            "flow",
            loaders_num= loaders_num,
            doors_num= doors_num,
            start_door_num= start_door_num
        ))
    else:
        return render_template("index.html")

@app.route("/<loaders_num>/<doors_num>/<start_door_num>", methods=["POST", "GET"])
def flow(loaders_num, doors_num, start_door_num):
    if request.method == "POST":
        loader_dict = {
            request.form[f"name{i}"] : request.form[f"pph{i}"]
            for i in range(int(loaders_num))
        }
        door_array = [
            request.form[f"fph{i}"]
            for i in range(int(doors_num))
        ]
        data = {
            'loader_dict': loader_dict,
            'door_array': door_array
        }
        data = json.dumps(data)

        return redirect(url_for(
            "dispatch",
            data= data
        ))
    else:
        return render_template(
            "flow.html",
            loaders_num= int(loaders_num),
            doors_num= int(doors_num),
            start_door_num= int(start_door_num)
        )

@app.route("/dispatch/<data>")
def dispatch(data):
    loader_dict = data['loader_dict']
    door_array = data['door_array']
    return print(f"{loader_dict}\n{door_array}")

if __name__ == "__main__":
    app.run(debug=True)