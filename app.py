# Import Flask Dependencies

from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars


app = Flask(__name__)
mongo = PyMongo(app)

# Scrape and store data in MongoDB

@app.route("/")
def index():
    try:
        mars_data = mongo.db.mars.find_one()
        print("Data populated")
    except:
        mongo.db.mars.insert_one(scrape_mars.scrape())
        mars_data = mongo.db.mars.find_one()
        print("Exception!")
    return render_template("index.html", mars=mars_data)
    
# Scrape and store data in MongoDB

@app.route("/scrape")
def scrape():
    try:
        mongo.db.mars.find_one()
        mongo.db.mars.delete_one()
        mongo.db.mars.insert_one(scrape_mars.scrape())
    except:
        mongo.db.mars.insert_one(scrape_mars.scrape())
    
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)