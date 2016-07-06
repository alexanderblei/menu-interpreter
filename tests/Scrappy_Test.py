from expects import *
import mamba
# hack for now to import this module... there's definitely
# a more elegant way to do this

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

from Scrapyyyy import get_average_score, load_sentiment_words

'''
with describe("Scrapyyyy"):
    with describe("get_average_score"):
        with it("computes the average review score of a list"):
            score_range = [1,5,10,20]
            expect(get_average_score(score_range)).to(equal(9))

'''
class ScrapyyyyTest(unittest.TestCase):
    def test_get_average_score(self):
        score_range = [1,5,10,20]
        computed_average = get_average_score(score_range)
        self.assertEquals(computed_average,9)


if __name__ == '__main__':
    unittest.main()

