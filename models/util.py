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

    speech = result["results"][0]['lexicalEntries'][0]['lexicalCategory']['id']
    definition = result["results"][0]['lexicalEntries'][0]['entries'][0]["senses"][0]['definitions'][0]
    example = ""

    for word in result["results"][0]['lexicalEntries'][0]['entries'][0]["senses"]:
        if word.get("examples"):
            example = word['examples'][0]['text']
            break
        else:
            break

    return speech, definition ,example



