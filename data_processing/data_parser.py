import pandas as pd
from utils import *
import sys
import logging

filename = sys.argv[1]

chunksize = 5000
logging.basicConfig(format='%(asctime)s: [%(levelname)s - Process Data] =======> %(message)s', level=logging.INFO)

total_df = pd.DataFrame()
for chunk in pd.read_csv(filename, sep="\t", escapechar="\\", chunksize=chunksize):
	#Step 1. Data cleansing and filtering
    #check if creativecommon.org is in the provider_domain and remove those rows
    df = chunk[chunk["provider_domain"]!="creativecommons.org"]

    #Step 2. Extract the CC License
    df["license_type"] = df["cc_license"].apply(getLicense)
    
    #delete rows without a valid CC license
    df = df.dropna()
    total_df = pd.concat([total_df,df])

total_df.to_csv("temp/"+filename,sep="\t", escapechar="\\", index=False)
logging.info("END OF PRUNING")

filename = expandToSourcesTargets("temp/"+filename)
total_df = pd.DataFrame()
for chunk in pd.read_csv(filename, sep="\t", escapechar="\\", chunksize=chunksize):
	#Return to step 1: remove circular links
	df = chunk[chunk["source"]!=chunk["target"]]

	#Step 3. Create a method to format the domain name in the 'provider_domain'
	df["source"] = df["source"].apply(getDomainName)

	#Step 4. Aggregate the data (sum all images and total links) group by domain
	df.groupby("source").sum()
	total_df = pd.concat([total_df,df])

convertToJSON(total_df)


    

    #temporarily write to file
    #logging.info('Write output to file')



