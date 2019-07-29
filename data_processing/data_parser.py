import pandas as pd
from utils import *
import sys
import logging

filename = sys.argv[1]

chunksize = 5000
logging.basicConfig(format='%(asctime)s: [%(levelname)s - Process Data] =======> %(message)s', level=logging.INFO)

total_df = pd.DataFrame()

filename = expandToSourcesTargets(filename)
total_df = pd.DataFrame()
for chunk in pd.read_csv(filename, sep="\t", escapechar="\\", chunksize=chunksize):
	#Return to step 1: remove circular links
	df = chunk[chunk["source"]!=chunk["target"]]

	#Step 4. Aggregate the data (sum all images and total links) group by domain
	df.groupby("source").sum().reset_index()
	total_df = pd.concat([total_df,df])

convertToJSON(total_df)


