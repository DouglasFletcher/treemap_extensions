

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
import pandas as pd

# project base
os.chdir("..")
location = os.getcwd()
os.chdir(location + "\\python")

# =========
# functions
# =========
infile = location + "\\csv\\treemap_contribsrolled.csv"
outfile = location + "\\json\\treemap_contribs.json"

def readdatadict(infile):
	# =======================
	# read data to dictionary
	# input: csv file
	# output: list of dicts
	# =======================
	print("reading csv data...")
	outdata = []
	exceptions = 0
	with open(infile) as fileref:
		for (i, row) in enumerate(fileref):
			try:
				# drop chars
				row = row.replace("\n", "")
				# get header
				if i == 0:
					header = row.split(",")
				# pass empty lines
				elif len(row.strip()) == 0:
					pass
				# all other convert to dict
				else:
					rowlist = row.split(",")
					dictdat = dict(zip(header, rowlist))
					outdata.append(dictdat)
			except:
				exceptions += 1
	print("note: exception row reads: %s \n" %(exceptions))
	return outdata


def maptojsonlevels(indata, CONKEY, LEVEL1, LEVEL2, LEVEL3):
	# =================================
	# map data to json hierracy
	# input: csv data, level dimensions
	# output: json mapping
	# =================================
	print("mapping data to json format..." + "\n")
	# initialize
	jsonout = {"name": "inputdata", "children": []}
	# keep track of added keys
	listkeyvals = []
	# level3 values - static
	levl3keys = LEVEL3.keys()
	for dictval in indata:
		# get level1 val
		lvl1val = dictval[LEVEL1].strip()
		# get level2 val
		lvl2val = dictval[LEVEL2].strip()
		# conversion key
		lvlconvert = dictval[CONKEY].strip()
		# get contribution
		contrib = float(dictval["contribution"])
		# keep track of added keys
		dictlvl3 = set()
		# do for each meta levels
		for levl3key in levl3keys:
			# group level keys
			lvl3grp1 = dictval[LEVEL3[levl3key][0]]
			lvl3grp2 = dictval[LEVEL3[levl3key][1]]
			lvl3val = str(str(lvl3grp1) + str(lvl3grp2)).strip()
			# key value
			currentkeyval = (lvl1val, lvl2val, levl3key)
			# if key not exist then __init__
			if currentkeyval not in listkeyvals:
				jsonout["children"].append({"name": (lvl1val, lvl2val, levl3key)
					, "children": 
					[
						{"name": lvl3val, "conkey": lvlconvert, "value": contrib}
					]
				})
				# keep track of keys aready added
				listkeyvals.append(currentkeyval)

			# if key exists than append value
			else:
				# get relevant key
				getkeychildren = jsonout["children"]
				# find relevant key name
				for (listpos, dictkeys) in enumerate(getkeychildren):
					# if correct key name need to update children
					if cmp(dictkeys["name"], currentkeyval) == 0:
						# update with new children values
						jsonout["children"][listpos]["children"] \
						+= [{"name": lvl3val, "conkey": lvlconvert, "value": contrib}]
						# if found (given keys unique) go to next row
						break
	# converted format return
	return jsonout


def aggregate_json(jsonout):
	# =======================================
	# aggregate mappings
	# e.g. children: 
	# {'site1': 1, 'site1': 1} = {'site1': 2}
	# =======================================
	print("aggregating json format..." + "\n")
	# for each key mapping
	jsonagg = jsonout
	for (listpos, namemap) in enumerate(jsonagg["children"]):
		# get children elements
		childobjs = namemap["children"]
		# convert to dframe
		childpnds = pd.DataFrame(childobjs)
		# create converions level aggregations
		conLvlContrib = childpnds.groupby(["name","conkey"]).agg(sum).to_dict()['value']
		# create total level aggregations
		childpnds["conkey"] = "Total"
		totLvlContrib = childpnds.groupby(["name","conkey"]).agg(sum).to_dict()['value']
		# combined output
		allLvlContrib = dict(totLvlContrib.items() + conLvlContrib.items())
		# convert tuple to list
		preppeddict = []
		for key, value in allLvlContrib.items():
			preppeddict += [{"name": key[0], "conkey": key[1], "value": value}]
		# update children
		jsonagg["children"][listpos]["children"] = preppeddict
	# return value
	return jsonagg


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
	LEVEL1 = "attribution method"
	LEVEL2 = "RecordType"
	LEVEL3 = {
		  "Group1": ["Site","SearchMatchType"]
		, "Group2": ["CampaignMap","CampaignMapSearch"]
		, "Group3": ["CampaignType","SearchCategory"]
	}

	# process daten
	outdata = readdatadict(infile)
	jsonout = maptojsonlevels(outdata, CONKEY, LEVEL1, LEVEL2, LEVEL3)
	jsonprp = aggregate_json(jsonout)
	write_output(jsonprp, outfile)

	print("--- %s seconds ---" % (time.time() - start_time))




