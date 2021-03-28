import json,re,codecs
from app import app
from flask import render_template, request
from flask import jsonify

trie = {}

def getpairs(code):
    # initializations
    k = 0
    c = code[:1]
    
    # pulling trie dict from file
    with open('./code/book') as js:  
        trie = json.load(js)
    addr = trie[c][code]
    
    # opening file to retrieved address
    f = codecs.open('./code/%s' %c,'r','utf-8')
    lines = f.readlines()[addr:]
    # calculating limits of lines to retrieve
    for k,line in enumerate(lines):
        if line[:2] == '>>':
            break
    return lines[:k] # final required set

def clean(text):
    # cleaning input text for bigram search
    text_clean = re.sub("[!\.\?\(\)\'/\"\-\:\[\]\|]+"," P ",text)
    text_clean = text_clean.replace(",","")
    # Markovian pair i.e. last 2 words alone from input
    return text_clean.split()[-2:]

@app.route('/')
def index():
    return render_template('inslic.html')

@app.route('/fn', methods=['POST'])
def suggest():
    code = request.form['code']
    text = request.form['text']
    lines = getpairs(code)
    text = clean(text)
    a = text[0] # for 1-skip-2-gram support
    b = text[1] # for normal bigram
    sug = [] # word suggestions
    temp = ''
    for line in lines:
        if line[:1] == '>':
            temp = line[1:-2]
        elif line[:-2] == a or line[:-2] == b:
            if len(sug) == 0 or sug[-1] != temp:
                sug.append(temp)
    return jsonify(sug)