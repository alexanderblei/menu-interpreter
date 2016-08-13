import unittest
from flexmock import flexmock
from foo import replace_google_with_foo
import urllib
from expects import *

# hack for now to import this module... there's definitely
# a more elegant way to do this
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

from Scrapyyyy import get_average_score, load_sentiment_words, find_description_keywords

class ScrapyyyyTest(unittest.TestCase):

## 1. test the average scoring method to compute correctly ##

    def test_get_average_score(self):
        score_range=[1,5,10,20]
        score_range = [{"score":x} for x in score_range]
        computed_average = get_average_score(score_range)
        self.assertEquals(computed_average,9)
        self.assert

## 1. test the Excel file load to assign the proper score for each word ##
## 2. test the Excel file load to create the expected list of dictionaries ##

    def test_load_sentiment_words(self):
        sentiment_words = load_sentiment_words(os.path.join("fixtures","test_sentiment_words.xlsx"))
        self.assertIsInstance(sentiment_words,list,"The loaded file of sentiment words was not a list")
        for keyword in sentiment_words:
            self.assertEquals(keyword.keys(),["score","keyword"])
            self.assertIsInstance(keyword["score"],float)
            if keyword["keyword"]=="great":
                self.assertEquals(keyword["score"],4)

## 1. test if the review listing is returning as a list ##

    def test_find_description_keywords(self):
        keyword_sentences_all = open(os.path.join("fixtures","mock_review_list.txt"))
        keyword_sentences_all = keyword_sentences_all.read()
        test_reviews_list = []
        for sentence in str(keyword_sentences_all).split(','):
            test_reviews_list.append(sentence)
        print test_reviews_list
        test_keyword_finds = find_description_keywords("burger",test_reviews_list)
        self.assertIsInstance(test_keyword_finds,list,"The matched keywords did not return as a list")
        self.assertIn('taco',test_keyword_finds[0],"The input keyword was not found in the review listing")
        f.close()

class TestSomething(unittest.TestCase):
    def test_something(self):
        flexmock(urllib).should_receive("urlopen").and_return("response.html").once()
 #       fake_urlopen_response = replace_google_with_foo()
​'''
        print(result)
        expect(result).to(be_a(list))
        expect(len(result)).to(equal(4))
        expect(result).not_to(contain("google"))
​'''
if __name__ == '__main__':
    unittest.main()

