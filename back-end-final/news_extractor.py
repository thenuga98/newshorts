from newsapi import NewsApiClient
from urllib.request import Request, urlopen
#from scalpl import Cut
import nltk
import heapq
import re
import bs4 as bs  
import urllib.request  
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
import json

app = Flask(__name__)
app.config["DEBUG"] = True

CORS(app)

@app.route('/search', methods=['GET'])
def api_all():
    if 'keyword' in request.args:
        keyword = str(request.args['keyword'])
    
    #<---------Module 1: Getting the article sources--------->

    #Input: A keyword

    #Try searching for 'kashmir'
    op=[]
    newsapi = NewsApiClient(api_key="31c2edb4d9fc427883767fdff4aaf173")
    # keyword = input("Enter keyword: ");

    #This one returns a lot of articles, 10K+!
    #result = newsapi.get_everything(q=keyword)

    #This returns top hits
    result = newsapi.get_top_headlines(q=keyword)
    urls=[]
    #print(result.keys())
    #print(result['articles'][0].keys())
    #Output: A URL list
    print('Fetching URLs...')
    l = 0
    if len(result['articles']) >= 10:
        l = 10
    else: 
        l = len(result['articles'])
    for i in range(l):
        urls.append(result['articles'][i]['url'])
        

    #<---------Module 2: Creating article files--------->

    #Input: A URL list

    print('Preprocessing...')
    for url in urls: 
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        article = urlopen(req).read()
        #scraped_data = urllib.request.urlopen(url)  
        #article = scraped_data.read()

        parsed_article = bs.BeautifulSoup(article,'lxml')

        paragraphs = parsed_article.find_all('p')

        article_text = ""

        for p in paragraphs:  
            article_text += p.text
        file_name="article"+str(urls.index(url))+".txt"
        #Output: Clean, preprocessed text files of articles
        print("Created file " + file_name + "...")
        with open(file_name, 'w', encoding='utf-8') as f:
            print(article_text, file=f)
            
            
    #<---------Module 3: Summarization--------->

    #Input: Clean, preprocessed text files of articles

    print("Summarizing...")
    for i in range(len(urls)):
        art={}
        art['url'] = result['articles'][i]['url']
        art['source'] = result['articles'][i]['source']['name']
        art['title'] = result['articles'][i]['title']
        file_name="article"+str(i)+".txt"
        with open(file_name, 'r', encoding='utf-8') as myfile:
            article_text = myfile.read()

        # Removing Square Brackets and Extra Spaces
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)  
        article_text = re.sub(r'\s+', ' ', article_text) 

        # Removing special characters and digits
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )  
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

        #Sentence tokenization
        sentence_list = nltk.sent_tokenize(article_text)  

        #Find weighted frequency of occurence
        stopwords = nltk.corpus.stopwords.words('english')

        word_frequencies = {}  
        for word in nltk.word_tokenize(formatted_article_text):  
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():  
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

        sentence_scores = {}  
        for sent in sentence_list:  
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

        summary = ' '.join(summary_sentences)  
        #Output: Summary of articles
        print("\nSUMMARY:\n\n"+summary)
        art['summary']=summary
        summ=summary.casefold()
        sum=summ.rsplit(" ")
        
        
    #<---------Module 4: Finding bias--------->

    #Input: Summary of article, keywords for each specturm

        score=0
        rights=[]
        with open("right.txt") as file:
            rights = [line.strip() for line in file]
        lefts=[]
        with open("left.txt") as file:
            lefts = [line.strip() for line in file]
        for word in sum:
            for wr in rights:
                if(word == wr):
                    score-=10
        for word in sum:
            for wl in lefts:
                if(word == wl):
                    score+=10
        #Output: Bias score
        print("\n\n\nBIAS:\n")
        if((score>0)&(score<=20)):
            print("\nThe article is Moderate Leftist")
            art['bias']="Moderate Leftist"
        elif(score>0):
            print("\nThe article is Leftist")
            art['bias']="Leftist"
        if((score<0)&(score>=-20)):
            print("\nThe article is Moderate Rightist")
            art['bias']="Moderate Rightist"
        elif(score<0):
            print("\nThe article is Rightist")
            art['bias']="Rightist"
        if(score==0):
            print("\nThe article is neutral")
            art['bias']="Neutral"
        op.append(art)
    print(op)
    #json_op=json.dumps(op)
    return jsonify(op)
            
app.run()       

    
