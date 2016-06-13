from bs4 import BeautifulSoup
import urllib
import xlwt
import sys
import xlrd
import re
from pprint import pprint

def get_search_url(city, restaurant):
    query_parameters = {
        "find_loc": city,
        "find_desc": restaurant,
        "ns": 1
    }
    return "http://www.yelp.com/search?{0}".format(urllib.urlencode(query_parameters))

def get_restaurant_page_url(search_url):
    show_search_source=urllib.urlopen(search_url).read()
    parse_search_source=BeautifulSoup(show_search_source,"html.parser")
    request_search_descriptions=parse_search_source.find_all("div" , class_="search-result natural-search-result")
    show_formated_search_url=(request_search_descriptions[0].a['href']).split("?",1)
    return show_formated_search_url[0]


def count_review_pages(restaurant_url):
    restaurant_home_url = "http://www.yelp.com{0}".format(restaurant_url)
    show_homepage_source = urllib.urlopen(restaurant_home_url).read()
    parse_homepage_source = BeautifulSoup(show_homepage_source,"html.parser")
    request_page_count   = parse_homepage_source.find_all("div" , class_="page-of-pages")
    create_total_page_string = str(request_page_count[0])[72:-10].split("of")
    return int(create_total_page_string[1])

def get_review_descriptions(restaurant_url,total_review_pages):
    page_number_count = 0
    parsed_restaurant_reviews = []
    for i in range(0,total_review_pages):
        restaurant_home_url = "http://www.yelp.com{0}?start={1}".format(restaurant_url,page_number_count)
        show_restaurant_source = urllib.urlopen(restaurant_home_url).read()
        parse_resturant_source = BeautifulSoup(show_restaurant_source,"html.parser")
        parsed_restaurant_reviews += parse_resturant_source.find_all(itemprop="description")
        page_number_count=page_number_count+20
    return parsed_restaurant_reviews

def find_description_keywords(food_search_key,all_reviews_list):
    sentences_from_each_review=[]
    review_id = 0
    for individual_review in all_reviews_list:
        matched_word_sentence=""
        description_sentence_count=0
        order_of_last_matched_word=0
        it_key = "off"
        for description_sentence in re.split('!|>|\.',str(individual_review)):
            if (" it ".upper() in description_sentence.upper() or ".it ".upper() in description_sentence.upper()) or food_search_key.upper() in description_sentence.upper():
                if description_sentence_count==(order_of_last_matched_word+1) and description_sentence_count!=0 and it_key == "on":
                    matched_word_sentence=matched_word_sentence+"."+"------->"+description_sentence.upper()
                elif food_search_key.upper() in description_sentence.upper():
                    it_key = "on"
                    order_of_last_matched_word=description_sentence_count
                    matched_word_sentence=matched_word_sentence+"."+(description_sentence)
            description_sentence_count=description_sentence_count+1
        if len(matched_word_sentence)>1:
            sentences_from_each_review.append(matched_word_sentence)
    review_match_details=[]
    for detail in sentences_from_each_review:
        review_id=review_id+1
        review_match_dict={"review_details":detail}
        review_match_details.append(review_match_dict)
    return sentences_from_each_review


#for x in find_description_keywords("the burger",get_review_descriptions(get_restaurant_page_url(get_search_url('chicago', 'au cheval')),2)):
#    print " "
#    print x
#sys.exit()

def load_sentiment_words(file_name):
    word_score_buckets = xlrd.open_workbook(file_name)
    word_match_spreadsheet = word_score_buckets.sheet_by_index(0)
    flat_file_word_list=[]
    for column_number in range(0,word_match_spreadsheet.ncols):
        if column_number > 10:
            word_score = 10.00-column_number
        elif column_number < 8:
            word_score = column_number+1.00
        else:
            word_score=0.00
        word_list = word_match_spreadsheet.col_values(column_number)[1:]
        word_list =[word for word in word_list if word !="XXXXXXXXXX"]
        word_data = [{"keyword": word, "score": word_score} for word     in word_list]
        flat_file_word_list+=word_data
    return flat_file_word_list

def get_average_score(scoring_list):
    aggregate_score=0
    word_count = len(scoring_list)
    for scored_word in scoring_list:
        if scored_word['score']==8:
            aggregate_score=8
            word_count=1
        else:
            aggregate_score+=scored_word['score']
    return aggregate_score/float(word_count)

def food_scoring_formula(matched_sentence_reviews):
    compiled_score_list = []
    keyword_database = load_sentiment_words("Sentiment_Words.xlsx")
    for individual_review in matched_sentence_reviews:
        current_review = {}
        current_review['review_text']=individual_review
        individual_score_list = []
        for scoring_words in keyword_database:
            if scoring_words["keyword"].upper() in unicode(str(individual_review),"utf-8").upper():
                individual_score_list.append(scoring_words)
        filtered_score_list = [word for word in individual_score_list if word["score"]!=0]
        if len(filtered_score_list)!=0:
            current_review["key_scoring_words"]=individual_score_list
            current_review["average_score"]= get_average_score(filtered_score_list)
            compiled_score_list.append(current_review)
    return compiled_score_list

def yelp_scraper(restaurant, dish, city, logger):
    search_url = get_search_url(city, restaurant)
    restaurant_page_url = get_restaurant_page_url(search_url)
    review_descriptions = get_review_descriptions(restaurant_page_url,5)
    description_keywords = find_description_keywords(dish,review_descriptions)
    score_food = food_scoring_formula(description_keywords)
    return score_food

def yelp_scrape_raw(restaurant, dish, city, logger):
    search_url = get_search_url(city, restaurant)
    restaurant_page_url = get_restaurant_page_url(search_url)
    review_descriptions = get_review_descriptions(restaurant_page_url,1)
    description_keywords = find_description_keywords(dish,review_descriptions)
    return description_keywords

def overall_average(all_reviews):
    aggregate_score = 0
    for review in all_reviews:
        aggregate_score += review["average_score"]
    return aggregate_score/float(len(all_reviews))



### how to get decimals ??

    ##########################################################
    # Write the resulting lines to a spreadsheet            ##
    # each different search will create a new sheet         ##
    ##########################################################


 #   wbk = xlwt.Workbook()
 #   sheet = wbk.add_sheet('findings')
 #   row = 0
 #   col=0

   # for line in Exporter:
   #     L = unicode(str(line), 'utf-8')
   #     sheet.write(row,col,L)
   #     row += 1
   # wbk.save(Export_Name)

#if __name__ == '__main__':
#    yelp_scraper('high five ramen', 'ramen', 'Chicago')