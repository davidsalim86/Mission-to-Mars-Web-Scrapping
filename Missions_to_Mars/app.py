from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_data_dict"
mongo = PyMongo(app)

scrape_data_dict = mongo.db.scrape_data_dict.find_one()

@app.route("/scrape")
def scraper():
    scrape_data_dict = mongo.db.scrape_data_dict
    scrape_data_dict_update = scrape_mars.scrape()
    scrape_data_dict.update({}, scrape_data_dict_update, upsert=True)
    return redirect("/")

@app.route("/")
def index():
    scrape_data_dict = mongo.db.scrape_data_dict.find_one()
    return render_template("index.html", scrape_data_dict=scrape_data_dict)

if __name__ == "__main__":
    app.run(debug=True)
