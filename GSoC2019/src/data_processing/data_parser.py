import pandas as pd
from utils import *
import sys
import logging

"""Command to run the script: python data_parser.py _path_to_tsv_file """

SOURCES_TARGETS = [] #array that will store DataFrames with source,target and value columns

def get_sources_links(row):
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
	chunk["value"] = chunk["value"].astype(int)
	chunk = chunk.nlargest(10, "value") #take the top 10 outgoing links
	SOURCES_TARGETS.append(chunk)

def convert_targets_to_nodes(df):
	rows = []
	for row in df.itertuples():
		new_row = {}
		new_row["domain_name"] = row.target
		new_row["provider_domain"] = "Domain not available"
		new_row["images"] = 0
		new_row["cc_licenses"] = ""
		new_row["links_qty"] = 0
		new_row["licenses_qty"] = 0
		new_row["node_size"] = 10
		rows.append(new_row)
	
	df_result = pd.DataFrame(rows)
	return df_result

filepath = sys.argv[1]
filename = filepath.strip().split("/")[-1]
filename = filename.split(".")[0]


logging.basicConfig(format='%(asctime)s: [%(levelname)s - Processing TSV file] =======> %(message)s', level=logging.INFO)

df = pd.read_csv(filepath, header=None, names=["domain_name","provider_domain","images","links","cc_licenses","licenses_qty"], sep="\t", converters={"links":LinksReader, "cc_licenses":LicensesReader})

#delete rows with no links and/or licenses 
df.dropna(inplace=True)

#Calculate total outgoing links by domain
df["links_qty"] = df.apply(extract_links_len, axis=1)

df["licenses_qty"] = df["licenses_qty"].astype(int)

#apply scaling factor for the licenses_qty to determine the node size
max_licenses_qty = float(df["licenses_qty"].max())
max_node_size    = 100
min_node_size    = 10
df["node_size"] = df["licenses_qty"].apply(lambda col: max(min_node_size, int((col/max_licenses_qty) * max_node_size)))

#delete domains with less than 10 outgoing links
#Prune nodes that do not meet the necessary licenses amount, given a threshold
df = df.nlargest(50, "licenses_qty")

#generate sources and links mini DataFrames
logging.info("Generating the links DataFrame")

for row in df.itertuples():
	get_sources_links(row)

#build the DataFrame of links
df_links = pd.concat(SOURCES_TARGETS)

#delete circular links
df_links = df_links[df_links["source"]!=df_links["target"]]
print("Links df shape with circular links")
print(df_links.shape)

logging.info("Generating the nodes DataFrame")

#the initial DataFrame becomes a DataFrame with nodes non-repeated
df_nodes = df.drop(columns=["links"])
print("Nodes df with only provider domains shape")
print(df_nodes.shape)


logging.info("Extracting target domains that will added to the nodes DataFrame")
#drop duplicated target nodes
targets = df_links["target"].to_frame()
print(targets.shape)
targets.drop_duplicates(inplace=True) 
print(targets.shape)
#Get the target nodes that are not in the nodes DataFrame
nodes_to_concat = targets.merge(df_nodes["domain_name"], left_on="target", right_on="domain_name", how='left', indicator=True)
nodes_to_concat = nodes_to_concat[nodes_to_concat["_merge"]=="left_only"]

#Create other df with targets, adding the required features of a node
df_target_nodes = convert_targets_to_nodes(nodes_to_concat)

#Add target nodes to the nodes DataFrame
frames = [df_nodes, df_target_nodes]
df_all_nodes = pd.concat(frames)
print("Nodes df total shape")
print(df_all_nodes.shape)

#Generate the final file
logging.info("Generating the json file")
toJSON(df_all_nodes,df_links)