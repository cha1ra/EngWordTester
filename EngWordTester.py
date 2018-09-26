# -*- coding: utf-8 -*-
#https://glosbe.com/a-api APIを用いた 単語帳システム開発
#cha1ra 2018.03.02
#MIT Lisense

import urllib.request
import json

#追記
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#APIで情報を取得していきます
def getInformation(phrase):

	fromLanguage = 'en'
	destLanguage = 'ja'

	jsonDictionary = createJsonDictionary('translate', fromLanguage, destLanguage, phrase)

	#戻り値
	returnContents = {'meanings':[],'definition':[], 'examples':[], 'examplesja':[]}

	#カウンター。和訳を5個だけ格納するために使用。
	counter = 0

	tuc = jsonDictionary['tuc']
	for i in range(len(tuc)):
		if 'phrase' in tuc[i] and counter<5:
		 	returnContents['meanings'].append(tuc[i]['phrase']['text'])
		 	counter += 1
		elif 'authors' in tuc[i]:
			if tuc[i]['authors'] == [60172]:
				returnContents['definition'].append(tuc[i]['meanings'][0]['text'])

	jsonDictionary = createJsonDictionary('tm', fromLanguage, destLanguage, phrase)
	examples = jsonDictionary['examples']
	counter = 0
	for j in range(len(examples)):
		if 'first' in examples[j]:
			returnContents['examples'].append(examples[j]['first'])
			returnContents['examplesja'].append(examples[j]['second'])
			counter+=1
			if counter==3:
				break

	return returnContents

#URL生成部分
def createJsonDictionary(what, fromLanguage, destLanguage, phrase):
	url =  'https://glosbe.com/gapi/'+\
	what +\
	'?from=' + fromLanguage + \
	'&dest=' + destLanguage + \
	'&phrase=' + phrase +\
	'&format=json&page=1&pretty=true'

	resource = urllib.request.urlopen(url)
	jsonData = resource.read()
	jsonDictionary = json.loads(jsonData)
	return jsonDictionary


#main関数
if __name__ == '__main__':
	print('\n\n■■■ English Checker (仮)■■■\n\n')
	print('知りたい英単語を入力してね♪')
	phrase = input('>> ')
	print('---------------------------')
	print(phrase + '　とは！')
	print('---------------------------\n\n')

	contents = getInformation(phrase)

	print('■例文')
	for h in range(len(contents['examples'])):
		print('　・' + contents['examples'][h])
	print('\n')


	#英語の意味
	print('■意味（英文）')
	for i in range(len(contents['definition'])):
		print('　・' + contents['definition'][i])

	print('\n\n日本語訳わかったかな？正解は・・・ Press any key')
	input()

	print('■正解')
	for j in range(5):
		print(contents['meanings'][j] + ', ', end='')
	print('　…など！当たってたかな？\nちなみに例文の意味はこちら↓\n')

	print('■例文')
	for h in range(len(contents['examplesja'])):
		print('　・' + contents['examplesja'][h])
	print('\n')


	print('---------------------------')
