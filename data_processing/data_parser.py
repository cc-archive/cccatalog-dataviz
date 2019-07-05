import pandas as pd
from utils import *
import sys

filename = sys.argv[1]

chunksize = 5000
for chunk in pd.read_csv(filename, sep="\t", escapechar="\\", chunksize=chunksize):
	#Step 1. Data cleansing and filtering
    #check if creativecommon.org is in the provider_domain and remove those rows
    df = chunk[chunk["provider_domain"]!="creativecommons.org"]
    print("Creative Commons domains deleted")

    #Step 2. Extract the CC License
    df["license_type"] = df["cc_license"].apply(getLicense)
    
    #delete rows without a valid CC license
    df = df.dropna()
    print(df[["provider_domain","license_type"]].head(3))

    #Step 3. Create a method to format the domain name in the 'provider_domain'$
    #The following library may be helpful: tldextract


    #Step 4. Aggregate the data (sum all images and total links) group by 'prov$


    #temporarily write to file
    #logging.info('Write output to file')



