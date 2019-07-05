import re
from tldextract import extract

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