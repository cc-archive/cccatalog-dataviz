import pandas as pd
from utils import *
import sys
import logging


SOURCES_TARGETS = [] #array that will store DataFrames with source,target and value columns

def get_sources_links(row):
	#chunk = pd.DataFrame(columns=["source","target","value"])
	rows = []
	links = row.links
	domain_name = row.domain_name
	for k,v in links.items():
		new_row = {}
		new_row["source"] = domain_name #the link source is the domain name
		new_row["target"] = k #the link target is a key of the links dictionary 
		new_row["value"] = v #the weight of the link is given by the value of the key
		rows.append(new_row)

	chunk = pd.DataFrame(rows)
	SOURCES_TARGETS.append(chunk)

filename = "/home/belen/part-00000.tsv"

logging.basicConfig(format='%(asctime)s: [%(levelname)s - Processing TSV file] =======> %(message)s', level=logging.INFO)

df = pd.read_csv(filename, header=None, names=["domain_name","provider_domain","images","links","cc_licenses","licenses_qty"], sep="\t", converters={"links":LinksReader, "cc_licenses":LicensesReader})
#delete rows with no links and/or licenses 
df = df.dropna(subset=['links', 'cc_licenses'])
#Calculate total outgoing links by domain
df["links_qty"] = df.apply(extract_links_len, axis=1)
#delete domains with less than 10 outgoing links
df = df[df["links_qty"] >= 10]

#generate sources and links mini DataFrames
logging.info("Generating the links data frame")

for row in df.itertuples():
	get_sources_links(row)

#build the DataFrame of links
df_links = pd.concat(SOURCES_TARGETS)
print(df_links.head(5))
print(df_links.shape)

logging.info("Generating the nodes data frame")

#the initial data frame becomes a DataFrame with nodes non-repeated
df_nodes = df.drop(columns=["links"])
print(df_nodes.head(5))
print(df_nodes.shape)

#delete circular links
df_links = df_links[df_links["source"]!=df_links["target"]]
print(df_links.head(5))
print(df_links.shape)

logging.info("Generating the json file")

#Keep the rows where targets are domains with licensed content
#meaning domains that are in the nodes df
df_links = df_links.loc[df_links["target"].isin(df_nodes["domain_name"].values.tolist())]
print(df_links.shape)

#Generate the final file
toJSON(df_nodes,df_links)



