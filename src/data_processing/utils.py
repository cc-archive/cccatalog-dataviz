import re
from tldextract import extract
import json
import logging
from os import path
import ast

LICENSES_NAMES = ["by","by-sa","by-nd","by-nc","by-nc-sa","by-nc-nd"]
TEMP_FOLDER = "temp"

def getLicense(_path):
    """Function that returns the license and version of a given _path, or [None,None]."""
    
    pattern   = re.compile('/(licenses|publicdomain)/([a-z\-?]+)/(\d\.\d)/?(.*?)')
    if pattern.match(_path.lower()):
        result  = re.search(pattern, _path.lower())
        license = result.group(2).lower().strip()
        version = result.group(3).strip()

        if result.group(1) == 'publicdomain':
            if license == 'zero':
                license = 'cc0';
            elif license == 'mark':
                license = 'pdm'
            else:
                logging.warning('License not detected!')
                return None

        elif (license == ''):
            logging.warning('License not detected!')
            return None

        return license

    return None

def getDomainName(_provider_domain):
    res = extract(_provider_domain)
    return res.domain

def LinksReader(data):
    """Helper function that loads the json of links to a DataFrame column"""
    data = data.replace("\'", "\"")

    try: 
        json_data = json.loads(data)
        return json_data
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        logging.info("Links json is invalid")
        return None
    #json_data = ast.literal_eval(data)

def LicensesReader(data):
    """Helper function that loads the json of cc_licences to a DataFrame column"""
    data = data.replace("(", "\"(")
    data = data.replace(")", ")\"")
    try: 
        json_data = json.loads(data)
        if(len(json_data)==0):
            logging.info("CC_license json is empty")
            return None
        return json_data
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        logging.info("CC_license json is invalid")
        return None
    return(json_data)

def LicensesQtyReader(data):
    return float(data)

def extract_links_len(row):
    domain_name = row["domain_name"]
    if(domain_name in row["links"]):
        del row["links"][domain_name]
    return len(list(row["links"].keys()))

def expandToSourcesTargets(_file_path):
    """Function that receives a tsv file path and returns the path of an extended and processed
    version of the same file. Input file must have the columns: provider_domain,cc_license,
    images and links. Output file contains the fields: source,cc_license,images,target and
    value. Circular links and rows that contain creativecommons.org as a provider_domain, 
    are excluded."""
    fname = path.basename(_file_path)
    stem_filename = fname.split(".")[0]
    output_fname = path.join(TEMP_FOLDER, stem_filename+"_extended.tsv")
    logging.info("Creating temporal file: "+output_fname)
    out_file = open(output_fname,"w")
    out_file.write("source\tcc_license\timages\ttarget\tvalue\n")

    with open(_file_path, 'r') as f:
        #read the header
        f.readline()

        while (True):
            line = f.readline()

            if line: 
                first_occurrence = True
                line = line.replace("\'", "\"") #for correct json structure
                fields = line.strip().split("\t")
                provider_domain = fields[0]
                #print(line)
                if(len(fields)!=4):
                    continue
                try:
                    links = json.loads(fields.pop(3)) #column 4 is the links field
                except ValueError:
                    continue

                #Get domain names from source (Step 3)
                fields[0] = getDomainName(fields[0]) 
                #Get the license
                fields[1] = getLicense(fields[1])

                #Verify the source is not creativecommons, and that the license is valid
                if(fields[0]=="creativecommons" or fields[1]==None):
                    continue

                for k,v in links.items():
                    #Get domain name from target (Step 3)
                    k = getDomainName(k)

                    if(not first_occurrence):
                        fields[2] = "0"  #for not multiplying the initial images quantity every time we create a new row

                    #Verify that source is different than target (avoid circular links) 
                    if(fields[0]!=k):
                        out_line = "\t".join(fields) #fields contain [provider_domain,cc_license,images]
                        out_line = out_line.strip()
                        out_line += "\t"+k+"\t"+str(v)+"\n" #add the target and number of hrefs from the source to the target
                        out_file.write(out_line)
                        first_occurrence = False
            else:
                out_file.close()
                logging.info("END OF FILE")
                logging.info("END WRITING SOURCES-TARGETS FILE")
                return(output_fname)

    return None

def toJSON(_df_nodes, _df_links):
    """Function that converts a dataframe to the expected file source format by force-d3, 
    in order to create the force-directed graph."""
    logging.info("CREATING NODES AND LINKS FILE")
    
    #Nodes list of dictionaries
    nodes_df = _df_nodes.rename(index=str, columns={"domain_name":"id"})
    nodes_dict = nodes_df.to_dict('records')
    
    #Links list of dictionaries
    links_dict = _df_links.to_dict('records')
    total_data = {"nodes":nodes_dict, "links":links_dict}

    #Join both lists
    with open('../fdg_input_file.json', 'w') as file:
        file.write(json.dumps(total_data)) 
        logging.info("END")