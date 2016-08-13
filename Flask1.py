from flask import Flask, render_template, request
from Scrapyyyy import Scrapyyyy
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def HomePage():
    if request.method == "GET":
        return render_template('home_page.html')
    else:
        app.logger.debug(request.form)

@app.route("/search", methods=["GET","POST"])
def Home():
    if request.method == "GET":
        return render_template('about.html')
    else:
        app.logger.debug(request.form)

        restaurant = request.form['restaurant']
        dish = request.form['dish']
        city = request.form['city']

        scraper_object = Scrapyyyy()
        reviews_dictionary = scraper_object.yelp_scraper(restaurant, dish, city, app.logger)
        average_score = scraper_object.overall_average(reviews_dictionary)

        return render_template("about2.html", restaurant=restaurant, city=city, dish=dish, reviews=reviews_dictionary, average=average_score)

@app.route("/Excel", methods=["GET","POST"])
def PopulateExcel():
    if request.method == "GET":
        return render_template('PopExcel.html')
    else:

        app.logger.debug(request.form)

        restaurant = request.form['restaurant']
        city = request.form['city']

        scraper_object = Scrapyyyy()
        write_reviews_to_excel = scraper_object.write_structured_reviews(restaurant,city)

        return render_template("popexcel_confirm.html",restaurant=restaurant, city=city)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')