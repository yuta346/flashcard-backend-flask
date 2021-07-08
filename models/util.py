import requests
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)

app_id = "cd2bf3dd"
app_key = "33201d23b40488b6ecf7d40e61b3ef62"
LANGUAGE = "en-us"

class Error(Exception):
    pass

class WordNotFoundError(Error):
    pass

def get_dictionary_info(word):

    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + LANGUAGE + "/" + word.lower()

    try:
        response = requests.get(url, headers={"app_id": app_id, "app_key": app_key})

    except requests.ConnectionError:
        raise ConnectionError

    if response.status_code == 404:
        raise WordNotFoundError("word not found")

    result = response.json()
   
    word_info_list = []
    for i in range(len(result["results"][0]['lexicalEntries'][0]['entries'][0]["senses"])):
        
        word_info_dict = {"word":word}
        for key in result["results"][0]['lexicalEntries'][0]['entries'][0]["senses"][i]:
            if key == "definitions":
                word_info_dict["definition"] = result["results"][0]['lexicalEntries'][0]['entries'][0]["senses"][i]['definitions'][0]
                break
            else:
                word_info_dict["definition"] = None
        


        for key in result["results"][0]['lexicalEntries'][0]['entries'][0]["senses"][i]:
            if key == "shortDefinitions":
                word_info_dict["short_definition"] = result["results"][0]['lexicalEntries'][0]['entries'][0]["senses"][i]['shortDefinitions'][0]
                break
            else:
                word_info_dict["short_definition"] = None
        
        for word_key in result["results"][0]['lexicalEntries'][0]['entries'][0]["senses"][i]:
             if word_key == "examples":
                 word_info_dict["example"] = result["results"][0]['lexicalEntries'][0]['entries'][0]["senses"][i]['examples'][0]['text']
                 break
             else:
                word_info_dict["example"] = None
        word_info_list.append(word_info_dict)

    return word_info_list


# get_dictionary_info("apple")