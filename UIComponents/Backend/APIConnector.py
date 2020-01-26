#Python request generator

'''
Script by Zachary Hughes

Pulls random items from a D&D RESTful API, which itself pulls from the
official SRD for D&D 5e. Current iteration just posts depending on input,
but final iteration will have GUI to generate random encounters, enemies,
loot, etc.

Sources:
GitHub: https://github.com/adrpadua/5e-srd-api
API Portal: http://www.dnd5eapi.co/

'''

import requests, random, pprint, json, sys, linecache
from PyQt5 import QtCore
from fuzzywuzzy import fuzz, process

#fuzzy match ratio threshold
threshold = 90

#printer
printer = pprint.PrettyPrinter()

#text separator
SEPARATOR = '------------------'

RESTRICT_LIST = ["slug", "index", "key", "url", "id", "_id"]

#base URL to post to
URL_BASE = 'http://dnd5eapi.co/api/'

#extra base URL for magic items and specifically weapons
URL_BASE_EXTRA = 'https://api.open5e.com/'

#url tuple
URL_TUPLE = (URL_BASE,URL_BASE_EXTRA)

#redefined terms for readability's sake, as keys will be displayed as buttons
#value is API endpoint and which API to pull from
TERMS = {
    'ability score':('ability-scores',0),
    'class':('classes',0),
    'condition':('conditions',0),
    'damage type':('damage-types',0),
    'equipment category':('equipment-categories',0),
    'equipment':('equipment',0),
    'feature':('features',0),
    'language':('languages',0),
    #'level by class':('levels',0),   #unfortunately not working
    'magic school':('magic-schools',0),
    'monster':('monsters',0),
    'proficiency':('proficiencies',0),
    'race':('races',0),
    'skill':('skills',0),
    'spellcasting':('spellcasting',0),
    'spell':('spells',0),
    'starting equipment':('startingequipment',0),
    'subclass':('subclasses',0),
    'subrace':('subraces',0),
    'trait':('traits',0),
    'weapon property':('weapon-properties',0),
    'weapons specifically':('weapons',1),
    'magic item':('magicitems',1)
    }

'''
Gets the full set of items given an endpoint

pullEnd: endpoint of API
URL: URL for RESTAPI to pull from
'''
def getEndpoint(pullEnd, URL):
    ret = requests.get(URL + pullEnd)
    if ret.status_code != 200:
        raise Exception('Failed response Status Code: ' + str(ret.status_code) + ' for: ' + URL + pullEnd)
    return ret


'''
Searches the given category with the input term

category: the category to search

term: the term used to search

bar: a bar to emit to if given

text: a textbox to print to if given

'''
def searchTerm(category, term, bar=None, text=None):
    #first, retrieve json endpoint
    jsonResponse = {}
    #update if possible
    if bar is not None: bar.emit(20)
    try:
        #get list
        jsonResponse = getItemByEndpoint(category, False, True)
    #if fail, say so
    except Exception as e:
        if bar is not None: bar.emit(100)
        if text is not None: text.setPlainText(str(e))
        return
    #update if possible
    if bar is not None: bar.emit(40)
    try:
        #search and return
        ret = searchJson(jsonResponse, term)
        #if this is a step between, get the real thing
        if 'url' in ret:
            #request the actual endpoint, shave off erroneous /api/ on return
            ret = getItemByEndpoint(ret['url'].split('/api/')[1], custom=True, rawOutput=True)
        if bar is not None: bar.emit(100)
        if text is not None: text.setPlainText(formatJson(ret))
    #if fail, say so
    except Exception as e:
        if bar is not None: bar.emit(100)
        if text is not None: text.setPlainText(str(e))
    

'''
Searches the resulting JSON for appropriate match, drills deepr if need be

'''
def searchJson(jsonResponse, stringInput):
    res = max(jsonResponse, key= 
                lambda x: 101 if x['name'] == stringInput else fuzz.token_set_ratio(x['name'], stringInput))
    #the function above returns 101 on exact matches, else fuzzy matching by intersection set on the user input
    return res

'''
Gets an item given user input

inpt: user input, must be string and must point back to endpoint, else error is thrown

custom: whether the input is custom or not

rawOutput: should the output return be raw, default false to string return
'''
def getItemByEndpoint(inpt, custom=False, rawOutput=False):
    if type(inpt) != type('l'):
        raise Exception('Endpoint must be type string')
    elif inpt not in TERMS and not custom:
        raise Exception('Endpoint not in terms list')
    
    #get endpoint by user input and the API associated with that endpoint
    if not custom:
        response = getEndpoint(TERMS[inpt][0], URL_TUPLE[ TERMS[inpt][1] ])
        
        #good to go, select items from the list
        x = response.json()['results'] if 'results' in response.json() else response.json()
        return formatJson(x) if not rawOutput else x
    
    else:
        try:
            print(URL_BASE+inpt)
            response = getEndpoint(inpt, URL_BASE)
            x = response.json()['results'] if 'results' in response.json() else response.json()
            return formatJson(x) if not rawOutput else x
            
        except Exception as e1:
            try:
                response = getEndpoint(inpt, URL_BASE_EXTRA)
                x = response.json()['results'] if 'results' in response.json() else response.json()
                return formatJson(x) if not rawOutput else x
            
            except Exception as e2:
                raise Exception('Custom endpoint not found in either DB.\n\nPerhaps it has not yet been added to the database or your input was malformatted.')


'''
Formats the input json for a readable format

json: an input dictionary

'''
def formatJson(json):
    retString = ""
    gen = {key:value for (key,value) in json.items() if key not in RESTRICT_LIST}
    for (key, value) in gen.items():
        retString += key.replace("_", " ").capitalize() + ": "
        #if value is a dictionary, format the subdictionary independently
        if type(value) == dict or type(value) == list:
            retString += "\n" + SEPARATOR*2 + "\n" + formatElement(value,1) + "\n"
        else:
            retString += formatElement(value)
    return retString

'''
Formats a single line depending on its key value

value: the value given from the json return

depth: the tab depth of the printout

'''
def formatElement(value, depth=0):
    #if this new value is a list, put each new item on its own line
    if type(value) == list:
        #return "\t" + "\n\t".join(value) + "\n"
        ret = ""
        for item in value:
            ret += formatElement(item, depth)
        return ret
    elif type(value) == dict:
        #else if dict associate key with value
        ret = "\t"*depth + SEPARATOR + "\n"
        #always print name and description first
        if 'name' in value:
            ret += "\t"*depth + "Name: " + str(value.pop('name')) + "\n"
        if 'desc' in value:
            ret += "\t"*depth + "Description: " + str(value.pop('desc')) + "\n"
        #loop over remaining elements and add them to the return string
        gen = {key:item for (key,item) in value.items() if key not in RESTRICT_LIST}
        for (key, item) in gen.items():
            if type(item) == list or type(item) == dict:
                ret += "\t"*depth + key.replace("_"," ").capitalize() + ": \n" + formatElement(item, depth+1)
            else:
                ret += "\t"*depth + key.replace("_"," ").capitalize() + ": " + str(item) + "\n"
        return ret
    else:
        #else just put it down
        return "\t"*depth + str(value) + "\n"
        
