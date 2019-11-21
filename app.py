from flask import Flask, jsonify, render_template, redirect

# Import pymongo library, which connect Flask app to Mongo database.
from flask_pymongo import PyMongo 

# Import python script that execute our scraping code 
import scrape_mars



#################################################
# Flask Setup
#################################################

# Create instance of Flask app
app = Flask(__name__)


#################################################
# Database Setup
#################################################


# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_mars_app")



#################################################
# Flask Routes
#################################################

# Set route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

