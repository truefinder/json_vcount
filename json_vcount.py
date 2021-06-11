#!/usr/bin/python3
# coding:utf8

import json
import base64
from urllib.parse import unquote
from optparse import OptionParser


def checkList(ele, prefix):
    for i in range(len(ele)):
        if (isinstance(ele[i], (list, tuple))):
            checkList(ele[i], prefix+"["+str(i)+"]")
 
        elif (isinstance(ele[i], str)):
            printField(ele[i], prefix+"["+str(i)+"]")
        else:
            checkDict(ele[i], prefix+"["+str(i)+"]")

def checkDict(jsonObject, prefix):
    for ele in jsonObject:
        if (isinstance(jsonObject[ele], dict)):
            checkDict(jsonObject[ele], prefix+"."+ele)

        elif (isinstance(jsonObject[ele], (list,tuple))):
            checkList(jsonObject[ele], prefix+"."+ele)

        elif (isinstance(jsonObject[ele], str)):
            printField(jsonObject[ele],  prefix+"."+ele)
        else:
            printField(jsonObject[ele],  prefix+"."+ele)

def checkTuple(jsonObject, prefix):
    for i in range(len(ele)):
        if (isinstance(ele[i], (list,tuple))):
            checkList(ele[i], prefix+"["+str(i)+"]")
        elif (isinstance(ele[i], str)):
            printField(ele[i], prefix+"["+str(i)+"]")
        else:
            checkDict(ele[i], prefix+"["+str(i)+"]")


output = [] 
def printField(ele, prefix):
	line= str(prefix) + ":" + str(ele ) 
	output.append(line) 
    #print (prefix, ":" , ele)



def main():

	usage = "usage: %prog [options] args"
	parser = OptionParser(usage)

	parser.add_option("-f", "--file", dest="file", help="ex) -f config.json")
	parser.add_option("-d", "--decode", dest="decode", help="none|urldecode|base64")

	(options, args) = parser.parse_args()

	if(options.file is None):
		parser.error("file is not defined")

	if(options.decode is None):
		parser.error("decode is not defined (none|urldecode|base64)")


	json_data = []
	f = open(options.file)
	raw_data = f.read()
	f.close()

	if (options.decode == 'urldecode'):
		decoded = unquote(raw_data) 

	elif (options.decode == 'base64'):
		decoded = base64.decode(raw_data) 
	else :
		decoded = raw_data 

	data = json.loads(decoded)

	#Iterating all the fields of the JSON
	for element in data:
	  #If Json Field value is a Nested Json
		if (isinstance(data[element], dict)):
			checkDict(data[element], element)
		#If Json Field value is a list
		elif (isinstance(data[element], (list,tuple))):
			checkList(data[element], element)
		#If Json Field value is a string
		elif (isinstance(data[element], str)):
			printField(data[element], element)

	i = 0 
	for line in output : 
		print(line) 
		i = i +1 

	print("========================================================") 
	print("Total count : " +  str(i) ) 

	
if __name__ == "__main__":
    main()

