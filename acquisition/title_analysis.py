import praw
from nltk.corpus import stopwords
import math
import base64
import hashlib
client = praw.Reddit(client_id='VnTHCdkO69qP-w',
                     client_secret='fJhct05p0F9zcuj1FMOBgIuDKtg',
                     user_agent='script:com.xomb.sensus:v0.1')


garbage = set(stopwords.words('english'))
garbage.update('a')
garbage.update(',')
garbage.update('.')
garbage.update(':')



strippedTitleArray = []
titleToScoreArray = []

def getPosts(client, subreddit, limit=1000):
	postList = client.subreddit(subreddit).top(limit=limit)
	return postList

def parseTitles(postList, cleanGarbage = True, returnAsWordArray = True):
	titlesArray = []
	
	counter = 0
	for post in postList:
		if post.score > 0:
			post.title = post.title.replace('"', '')
			post.title = post.title.replace("'", '')
			post.title = post.title.replace(",", "")
			cleaned = list(filter(lambda p: not p in garbage, post.title.split()) if returnAsWordArray else post.title)
			titlesArray.append(cleaned)
			titleToScoreArray.append(1.0 - (1.0 / math.log1p(post.score)))
			counter+=1
	return titlesArray

def reduceTitles(titlesArray, limit = 8):
	reducedTitles = []
	for title in titlesArray:

		if len(title) >= 8:
			reducedTitle = []
			for i in range(0,8):
				reducedTitle.append(title[i])
		else:
			reducedTitle = title
			for i in range(len(title),8):
				reducedTitle.append("null")
		reducedTitles.append(reducedTitle)

	return reducedTitles

def numericalHashFromWord(word):
	INPUT_TYPE = str((type(word))).replace('<', '').replace('>', '').replace('class', '').replace("'", "").replace(' ', '')
	if (INPUT_TYPE == "int") or (INPUT_TYPE == "float"):
		return word

	if (INPUT_TYPE == "str"):
		return float(int.from_bytes(word.encode(), 'little')) / (10001269.0)

	raise TypeError("ERROR: numericalHashFromWord() only accepts str,int, or long as float")
	

def generateCSV(reducedTitleArray, filename):
	with open(filename, 'a') as output:
		counter = 0;
		for title in reducedTitleArray:
			csvString = ""
			print(title)
			for word in range(0, len(title) - 1):
				if word == "null":
					holder = 0
				else:
					holder=numericalHashFromWord(title[word])
				csvString = csvString + str(holder) + ","

			holder = numericalHashFromWord(title[len(title) -1]) if (title[len(title) - 1] != "null") else 0
	
			csvString = csvString + str(holder) + "," + str(titleToScoreArray[counter]) + "\n"
			output.write(csvString)
			print(csvString)
			counter+=1

if __name__ == '__main__':
	post_list = getPosts(client, 'worldnews')
	title_list = parseTitles(post_list)
	reduced_title_list = reduceTitles(title_list)
	generateCSV(reduced_title_list, 'test_output.csv')
	

	



# for post in client.subreddit('news').hot(limit=10):
# 	totalposts = totalposts + 1
# 	clean = ""
# 	cleanArray = filter(lambda w: not w in garbage, post.title.split())
# 	cleanArray = filter(lambda w: w.strip("'"), cleanArray)


# 	strippedTitleArray.append(cleanArray)

# total = 0
# for cleanedTitle in strippedTitleArray:

# 	total = total + len(cleanedTitle)

# titlesArray = []

# for cleanTitle in strippedTitleArray:
# 	human_readable = ""
# 	if len(cleanTitle) >= 8:
# 		for i in range(0, 8):
# 			human_readable = human_readable + " " + cleanTitle[i]
# 	else:
# 		for i in range(0, len(cleanTitle)):
# 			human_readable = human_readable + " " + cleanedTitle[i]

# 	titlesArray.append(human_readable)

# for readable in titlesArray:
# 	print(readable)

