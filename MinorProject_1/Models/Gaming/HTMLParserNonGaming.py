from selenium import webdriver
from bs4 import BeautifulSoup, Comment
import os
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import isGameSite

#**************House keeping*****************
fobject = open("scoreNonGaming.txt", "w")    #Emptying the score file
fobject.close()
#********************************************

fobjectLinks = open("NonGamingSites.txt", "r")
while True:
    inputLink = fobjectLinks.readline()
    print(inputLink.replace('\n', ''))
    if inputLink == '':
        break
            
    domain = inputLink.split('/')
    finalDomain = domain[0].replace('.', '_')
    print(finalDomain)

    try:
        driver = webdriver.Firefox()
        driver.get("https://"+inputLink)
        print(driver.title + '\n')
        html = driver.page_source
        driver.close()
        soup = BeautifulSoup(html, 'lxml')

        #Extract entire body's content
        bodyContent = soup.body
        #print(bodyContent)
    except Exception as e:
        print("Error: " + str(e))

    #Make new directory if it doesn't exist.
    dirName = finalDomain
    if not os.path.exists(dirName):
        os.makedirs(dirName)

    #Write the sites link in a file
    try:
        fobject = open(dirName+"/"+finalDomain+"_SiteLink.txt", "w")
        fobject.write(inputLink)
        fobject.close()
    except Exception as e:
        print("Error occurred: " + str(e))

    #Extract all the scripts in body
    try:
        scripts = soup.find_all('script')
        fobject = open(dirName+"/"+finalDomain+"_scripts.txt", "w")
        for i in range(0,len(scripts)):
            fobject.write(str(scripts[i])+"\n")
        fobject.close()
    except Exception as e:
        print("Error: " + str(e))

    try:
        fobject = open(dirName+"/"+finalDomain+"_bodyContent.txt", "w")
        for text in bodyContent:
            fobject.write(str(text))
        fobject.close()
    except Exception as e:
        print("Error: " + str(e))

    #Extract all the links in body
    try:
        linksInBody = bodyContent.find_all('a')
        fobject = open(dirName+"/"+finalDomain+"_linksInBody.txt", "w")
        for i in range(0,len(linksInBody)):
            fobject.write(str(linksInBody[i])+"\n")
        fobject.close()
    except Exception as e:
        print("Error: " + str(e))


    #Extract entire body content without tags
    try:
        garbageCounter = 0

        #Remove all script and style elements
        for script in bodyContent(["script", "style"]):
            script.decompose()

        bodyContentWithoutTags = bodyContent.get_text()
        fobject = open(dirName+"/"+finalDomain+"_bodyContentWithoutTags.txt", "w")
        for text in bodyContentWithoutTags:
            if text == '\n' or text == ' ':
                garbageCounter+=1
            else:
                garbageCounter=0

            if garbageCounter <= 1:
                fobject.write(str(text))
        fobject.close()
    except Exception as e:
        print("Error: " + str(e))

    #********************************************
    try:
        fobject = open(dirName+"/"+finalDomain+"_bodyContentWithoutTags.txt", "r")
        counter = 0
        no_of_words_to_scan = 1000
        loopCounter = 0
        while loopCounter < no_of_words_to_scan:
            line = fobject.readline()
            if line == '':
                break
            text = word_tokenize(line)
            pos = pos_tag(text)
            print(pos)
            for i in range(0, len(pos), 1):
                loopCounter+=1
                if pos[i][1][0] == 'N': #Send for check if NOUN
                    returnVal = isGameSite.find_in_database(pos[i][0])
                    if returnVal == 0:
                        counter+=1
                        print("No of hits: " + str(counter))
            
        fobject = open("scoreNonGaming.txt", "a+")
        fobject.write("Site Link: " + inputLink)
        fobject.write("No of hits: " + str(counter) + "\n")
        fobject.write("No of iterations: " + str(no_of_words_to_scan) + "\n")
        fobject.write("Score: " + str((counter/no_of_words_to_scan)*100) + "\n\n")
        fobject.close()

    except Exception as e:
        print(e)

fobjectLinks.close()
