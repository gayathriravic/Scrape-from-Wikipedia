import wikipedia
import nltk
from nltk import  word_tokenize
import json


topic_to_noun = {}
def extract_nouns(content,topic):
    text = word_tokenize(content)
    text = nltk.pos_tag(text)
    for word in text:
        if word[1] == "NN":
            if word[0].lower() not in topic_to_noun:
                topic_to_noun[topic][word[0].lower()] = 1


def scrape_data(topics):
    for topic in topics:
        topic_to_noun[topic] = {}
        try:
            content = wikipedia.WikipediaPage(topic).content
        except wikipedia.exceptions.DisambiguationError as e:
            print("Error: {0}".format(e))
        extract_nouns(content,topic)
        try:
            external_links = wikipedia.WikipediaPage(topic).links
        except wikipedia.exceptions.DisambiguationError as e:
            print("Error: {0}".format(e))
        for links in external_links:   #follow the links and extract content
            try:
                link_content = wikipedia.WikipediaPage(links).content
            except wikipedia.exceptions.DisambiguationError as e:
                print("Error: {0}".format(e))
            extract_nouns(link_content,topic)
        print("--- Finished scraping topic! " + str(topic) + " ----")

        
def writeToFile():
    with open('wiki_extracts.txt', 'w') as outfile:
        json.dump(topic_to_noun, outfile, indent=4)
    print("Write complete!")


if __name__ == '__main__':

    list_of_topics = ["travel","computer","food","literature","politics"]
    scrape_data(list_of_topics)
    print("--------")
    print("finished scraping all the topics!")
    print("Let us write the result to a file!")
    writeToFile()
