import random
import pickle
from flask import Flask, render_template, request, session
from collections import Counter, OrderedDict

from datetime import datetime
import time
app = Flask(__name__)

def sortByValue(userDict):
    sort = sorted(userDict.items(), key = lambda t: t[1])
    print (sort)
   # return sort 
    
def randomWord():

    source_word = []
    rand_w = ''
    with open("words.txt") as words:
        for w in words:
            w1 = w.strip()
            len_w1 = len(w1)
            if len_w1 >= 7:
                source_word.append(w1)
            else:
                small_words = w1
    with open("my.pickle", "wb") as ph:
        pickle.dump(source_word, ph)
                       
    with open("my.pickle", "rb") as ph:
        d = pickle.load(ph)

    rand_w = random.choice(source_word)
    rand_w = rand_w.lower()
    return rand_w

def isItFromSource(source, valid , invalid_words):

    sourceWordLetterCount = Counter(source)
    print("INvalid word start" , invalid_words)
    for word in valid:
        wordLetterCount = Counter(word)
        for i in word:
            if wordLetterCount[i] > sourceWordLetterCount[i]:
               # if word not in invalid_words:
               invalid_words.append([word, " - is not from source"])
            break
    return invalid_words                
    
def validateWord(sourceWord, guessWord):
    guessDict=[]
    valid_words=[]
    invalid_words = []
    with open("words.txt") as wordsInDict:
        for word in wordsInDict:
            word1 = word.strip('\n')
            lenOfWord1 = len(word1)
            if lenOfWord1 >= 3:
                guessDict.append(word1.lower()) 
    with open("quessDict.pickle", "wb") as ph:
        pickle.dump(guessDict, ph)
    
    with open("quessDict.pickle", "rb") as ph:
        d = pickle.load(ph)

    for i in guessWord:
        if len(i) <3:
            #too short
            invalid_words.append([i, " - is too short "])
            
        elif i.strip(' ') in d:
            valid_words.append(i)
            if i == sourceWord:
                invalid_words.append([i, "- is the same as sourceWord "])
                           
        else:
             invalid_words.append([i, "- is not in dictionary"])
               
    w = isItFromSource(sourceWord, valid_words , invalid_words)
    print("2YYYY" , valid_words)
    k= {}
    for i in valid_words:
        if i in k:
            k[i] += 1
            invalid_words.append([i, "duplicate"])
                   
        else:
            k[i] = 1
       # if i not in valid_words:
        #    invalid_words.append([i, " - duplicate words not allowed"])
        #break
    s = []
    for i in s:
        if i not in s:
            s.append(i)
    print("SET ",s )    
    #valid_word = set(valid_words)
    #print("set", set(valid_words))
    #print(len(valid_words))
    #if(len(valid_word)<7):
        
        
   
              
    return invalid_words
    
def addUser(user, endTime):
    with open("use.pickle", "rb") as ph:
        userData = pickle.load(ph)
        
    print(userData)
   
    
    userData.update({user:endTime})
    print(type(userData))
    print(userData)
    #userData = sorted(userData.items(), key = lambda t: t[1])[:10]
   # OrderedDict(sorted(userData.items(), key=lambda t: t[0]), reverse = True)
    userDat = sortByValue(userData)
    #userData= sorted(userData.values())
    print("vlues",userDat)
    s = [(k, userData[k]) for k in sorted(userData, key=userData.get)]
    with open("use.pickle", "wb") as ph:
         pickle.dump(userData, ph)
   
   
    print ("ssss", s)
    return s
   
@app.route('/')
def startgame():
    
    #userData ={'inga':'0:00:11'}
    #print("vlues",userData)
    #with open("use.pickle", "wb") as ph:
    #     pickle.dump(userData, ph)
   
    return render_template('start.html',
                            title="Welcome to th Word Game", 
                            header="Press the button to start to play the game")  
@app.route('/startgame',methods=['POST', 'GET'])

def show_the_form() -> 'html': 
    
         
    
    session['startgame'] = datetime.now().strftime('%H:%M:%S')
    print(type( session['startgame']))
   # startgame = session['startgame']
    session['rand_w'] = randomWord()
    return render_template('form.html',
                           title="Word Game",
                           header="Your word is: "+session['rand_w'],
                         
                           timestampStart=session['startgame'])
                           
@app.route('/sendithere', methods=['POST'])
def process_the_data() -> str:
    data = []
    ret=''
    word1 = request.form['Word 1']
    word2 = request.form['Word 2']
    word3 = request.form['Word 3']
    word4 = request.form['Word 4']
    word5 = request.form['Word 5']
    word6 = request.form['Word 6']
    word7 = request.form['Word 7']
    data.append(word1.lower())
    data.append(word2.lower())
    data.append(word3.lower())
    data.append(word4.lower())
    data.append(word5.lower())
    data.append(word6.lower())
    data.append(word7.lower())
    startTime = request.form['timeStart']

   
    r=validateWord(session['rand_w'], data)
    print("R ",r)    
    if len(r) == 0:
       
        session['timeEnd'] =datetime.now().strftime('%H:%M:%S')
       
        print("Start " ,session['startgame'])
        print("End ", session['timeEnd'])
                
        FMT = '%H:%M:%S'
        tdelta = datetime.strptime(session['timeEnd'], FMT) - datetime.strptime(session['startgame'], FMT)
        
        print("difference ", tdelta)
        print(type(tdelta))
        return render_template('users.html',
        
                               endTime =tdelta)   
    else:
        return render_template('test.html',
                               title="Inga",
                               header="Words are wrong! Sorry: ",
                               result=r,
                               given_word=session['rand_w'])
        
                           
@app.route('/result', methods=['POST'])
def enterUserName():
    user = request.form['user']
    endTime = request.form['time']
   # userData = {user:endTime}
    top = addUser(user,endTime)
    
    return render_template('topPage.html',
                           theUser = user,
                           endTime = endTime, 
                           top=top)
app.secret_key = 'thisismysecretkey'
if (__name__ == '__main__'):
    app.run(debug=True)
