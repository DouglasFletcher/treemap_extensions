

from __future__ import print_function

# ===========================
# == douglas fletcher
# == 2016.06.03
# == get data to json format
# ===========================
import sys
import os
import json
import csv
import time
from pandas import read_csv, DataFrame, Panel
import pprint

# project base
os.chdir("..")
location = os.getcwd()
os.chdir(location + "\\python")

# =========
# functions
# =========
infile = location + "\\csv\\treemap_contribsrolled_test.csv"
outfile = location + "\\json\\treemap_contribs_test.json"


def readdatadict(infile):
	# ===================
	# read data to dframe
	# input: csv file
	# output: dframe
	# ===================
	print("reading csv data...")
	#dframe = read_csv(infile).head(5)
	dframe = read_csv(infile)
	return dframe



def csvToDictVal(dframe, CONKEY, LEVEL1, LEVEL2, LEVEL3):
	# ===================
	# create aggregations
	# input: dframe
	# output: dframe
	# ===================
	# __init return json value
	jsonout = {"name": "inputdata", "children": []}
	# get aggregation levels
	for key in list(LEVEL3.keys()):
		agglevel1, agglevel2 = LEVEL3[key][0], LEVEL3[key][1]
		# create aggregation
		dframeAgg = dframe.groupby(
			[CONKEY, LEVEL1, LEVEL2, agglevel1, agglevel2]
			, as_index = False
		)['contribution'].sum() 
		# keep track of key values
		keyList = []
		for row in dframeAgg.iterrows():
			rowAsDict = row[1].to_dict() 
			# create key value
			keyVal = (rowAsDict[CONKEY], key, rowAsDict[LEVEL2])
			nameVal = str(rowAsDict[agglevel1]+" "+rowAsDict[agglevel2]).strip() 
			contrib = rowAsDict["contribution"]
			methodT = rowAsDict[LEVEL1].strip()
			# __init__ key value
			if keyVal not in keyList:
				# create dimension
				graphAdd = {"name": list(keyVal)
					, "children": [{"name": nameVal, "method": methodT, "value": contrib}] 
				}
				# add dimension
				jsonout["children"].append(graphAdd)
				# keep track of dimension
				keyList.append(keyVal)
			# in keyvalue exists add value 
			else:
				# get relevant key
				getkeychildren = jsonout["children"]
				for (listpos, dictkeys) in enumerate(getkeychildren):
					# if correct key name need to update children
					if (tuple(dictkeys["name"])>keyVal)- \
					(tuple(dictkeys["name"])<keyVal) == 0:
						# update with new children values
						jsonout["children"][listpos]["children"] \
						+= [{"name": nameVal, "method": methodT, "value": contrib}]
						# if found (given keys unique) go to next row
						break
	return jsonout



def editChildrenValue(jsonIn):
	# =========================
	# sum "method" value to 
	# one record e.g. 
	# "key": 
	# {"method1":1,"method2":2}
	# input: dict
	# output: dict
	# =========================
	pp = pprint.PrettyPrinter(depth=8, indent=2)
	jsonOut = {"name": "inputdata", "children": []}
	# aggregate methods into one record
	dataLevel = jsonIn["children"]
	# new data __init
	newChildVals = []
	newChildDict = {}
	methodTypes = set()
	for dictVal in dataLevel:
		# children values need to be aggregated to put methods in same value
		childData = dictVal["children"]	
		nameData = dictVal["name"]
		# aggregate to nested value
		keyMemory = []
		newVal = {}
		for childVal in childData:
			name, method, values = childVal["name"], childVal["method"], childVal["value"]
			# check if created
			if name not in keyMemory:
				newVal[name] = {method: values}
				keyMemory.append(name)
			else:
				newVal[name] = dict(list(newVal[name].items())+list({method: values}.items()))   
			# get unique method types
			methodTypes.add(method)
		# convert to list of dicts
		childOut = []
		for name in newVal.keys():
			# dict values
			dictSave = newVal[name]
			# first check if both contrib types exist e.g. method1 & method2
			# if not exist add weight of zero this is for javascript to work
			keyVals = list(dictSave.keys())
			for method in list(methodTypes):
				if method not in keyVals:
					dictSave[method] = 0  
			# data point out
			childOut.append({"name": name, "value": dictSave})
		# save new record
		jsonOut["children"].append({"name": nameData, "children": childOut}) 
	return jsonOut





def write_output(jsonout, path):
	# ==================
	# write to json file
	# ==================
	print("writing json output...")
	with open(path, "w") as outfile:
		json.dump(jsonout, outfile, indent=4)
	outfile.close()



if __name__ == "__main__":

	# ===============
	# == process data
	# ===============
	start_time = time.time()

	# column references
	CONKEY = "success type"
	LEVEL1 = "attribution_method"
	LEVEL2 = "RecordType"
	LEVEL3 = {
		  "Group1": ["Site","SearchMatchType"]
		, "Group2": ["CampaignMap","CampaignMapSearch"]
		, "Group3": ["CampaignType","SearchCategory"]
	}

	# process daten
	print("reading data..")
	outdata = readdatadict(infile)

	# create aggregations
	print("processing data..")
	jsonAgg1 = csvToDictVal(outdata, CONKEY, LEVEL1, LEVEL2, LEVEL3)
	jsonAgg2 = editChildrenValue(jsonAgg1)

	# write data
	print("writing data..")
	write_output(jsonAgg2, outfile)

	print("--- %s seconds ---" % (time.time() - start_time))




