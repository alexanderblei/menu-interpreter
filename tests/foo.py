import urllib
​
def replace_google_with_foo():
    result = urllib.urlopen("http://www.yelp.com")
    words = result.read().split(" ")
    result_words = []
    for word in words:
        if word.strip() == "googlr":
            result_words.append("foo")
        else:
            result_words.append(word)
    return result_words
​
if __name__ == '__main__':
    foo()