from flask import Flask, render_template, request
from Scrapyyyy import yelp_scraper, overall_average, yelp_scrape_raw
import sys


reload(sys)
sys.setdefaultencoding("utf-8")


app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def Home():
    if request.method == "GET":
        return render_template('about.html')
    else:
        app.logger.debug(request.form)

        restaurant = request.form['restaurant']
        dish = request.form['dish']
        city = request.form['city']

        raw_key_sentences  = yelp_scrape_raw(restaurant, dish, city, app.logger)
        reviews_dictionary = yelp_scraper(restaurant, dish, city, app.logger)
        average_score = overall_average(reviews_dictionary)

        app.logger.debug(raw_key_sentences)
        app.logger.debug(reviews_dictionary)

        return render_template("about2.html", restaurant=restaurant, city=city, dish=dish, reviews=reviews_dictionary, average=average_score)

#       return "Restaurant: {0} <br> City: {2} <br> Dish: {1}".format(restaurant, dish, city)


#quickstart walkthroughs in flask
# request object

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')