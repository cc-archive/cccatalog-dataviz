import re
from tldextract import extract
import json
import logging

LICENSES_NAMES = ["by","by-sa","by-nd","by-nc","by-nc-sa","by-nc-nd"]

def getLicense(_path):
    '''
    Function that returns the license and version of a given _path, or [None,None].
    '''
    
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
#print(getLicense("/licenses/by-nc-sa/2.5/deed.zh"))

def getDomainName(_provider_domain):
    res = extract(_provider_domain)
    return res.domain

def CustomParser(data):
    import json
    json_data = json.loads(data)
    return json_data


#this could be added to the loadParquetFiles() function in ExtractData.py
def expandToSourcesTargets(_file_path):
    stem_filename = _file_path.split(".")[0]
    out_file = open(stem_filename+"_extended.tsv","w")
    out_file.write("source\tcc_license\timages\ttarget\tvalue\n")
    with open(_file_path, 'r') as f:
        f.readline()
        while (True):
            line = f.readline()
            if line: 
                first_occurrence = True
                line = line.replace("\'", "\"")
                fields = line.split("\t")
                provider_domain = fields[0]
                #column 4 is the links field
                links = json.loads(fields.pop(3))
                for k,v in links.items():
                    if(not first_occurrence):
                        fields[2] = "0"  #this is for not multiplying the initial images quantity every time we create a new row
                    out_line = "\t".join(fields) #fields contain [provider_domain,cc_license,images]
                    out_line = out_line.strip()
                    out_line += k+"\t"+str(v)+"\n" #add the target and number of hrefs from the source to the target
                    out_file.write(out_line)
                    first_occurrence = False
            else:
                out_file.close()
                logging.info("END OF FILE")
                logging.info("END WRITING SOURCES-TARGETS FILE")
                return(stem_filename+"_extended.tsv")
    return None

def convertToJSON(_df):
    nodes_df = _df[["source","images"]]
    nodes_df = nodes_df.rename(index=str, columns={"source":"id"})
    nodes_dict = nodes_df.to_dict('records')
    links_df = _df[["source","target","value"]]
    links_dict = links_df.to_dict('records')
    total_data = {"nodes":nodes_dict, "links":links_dict}
    with open('graph_data_input_file.json', 'w') as file:
        file.write(json.dumps(total_data)) 
        logging.info("END")
  
