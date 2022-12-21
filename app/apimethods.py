import requests, json
import os

def hero_info(hero_id):
    url = f"https://akabab.github.io/superhero-api/api/id/{hero_id}.json"
    data = json.loads(requests.get(url).text)
    FullName = data["biography"]["fullName"]
    name = data["name"]
    powerstats = data["powerstats"]
    #print(powerstats)
    alignedment = data["biography"]["alignment"]
    placeOfBirth = data["biography"]["placeOfBirth"]
    if placeOfBirth == "-":
        placeOfBirth = ""
    else:
        placeOfBirth = "born in "+placeOfBirth
    gender = data["appearance"]["gender"]
    if(gender == "Male"):
        pronoun = "He"
    else:
        pronoun = "she"
    race = data["appearance"]["race"]
    height = data["appearance"]["height"][0]
    if height != "-":
        height = "with the height of "+ height + " "
    else:
        height = ""
    if race == None:
        race = ""
    else:
        race = race + " "
    weight = data["appearance"]["weight"][0]
    if weight == "- lb":
        weight = ""
    else:
        weight = "and weighing " + weight + " "
    eyeColor = data["appearance"]["eyeColor"]
    hairColor = data["appearance"]["hairColor"]
    if not(hairColor == "No Hair"):
        hairColor = hairColor + " hair"
    if eyeColor == "-":
        eyeColor = "No"
    occupation = data["work"]["occupation"]
    firstAppearance = data["biography"]["firstAppearance"]
    publisher = data["biography"]["publisher"]
    groupAffiliation = data["connections"]["groupAffiliation"]
    if groupAffiliation == "-":
        groupAffiliation = "with no one"
    else:
        groupAffiliation = "as a " + groupAffiliation
    if alignedment =="-":
        alignedment = "neutral"
    if occupation == "-":
        occupation = "does not have another job"
    else:
        occupation = f"works as a {occupation}"
    if firstAppearance == "-":
        firstAppearance = "a comic"
    if not(FullName == ""):
        print("a")
        print(FullName)
        FullName = FullName + " or "
    bio = f'{FullName} {name} is a {alignedment} aligned character {placeOfBirth}. {name} has the appearance of a {race}{gender} {height} {weight}with {eyeColor} eyes and {hairColor}. {pronoun} {occupation}. {pronoun} first appeared in {firstAppearance} by {publisher}. {pronoun} is affiliated {groupAffiliation}.'
    image = data["images"]["md"]
    return [name, powerstats, bio, image]

def poke_info(poke_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}/"
    data = json.loads(requests.get(url).text)
    name = data['name']
    species = data['species']['name']
    # name = name.capitalize()
    height = data['height']
    weight = data['weight']

    url_evolve_from= f"https://pokeapi.co/api/v2/pokemon-species/{poke_id}/"
    data_evolve_from = json.loads(requests.get(url_evolve_from).text)
    if data_evolve_from['evolves_from_species'] is None:
        evolves_from = "no pokemon"
    else:
        evolves_from = data_evolve_from['evolves_from_species']['name']

    url_evolve_to = data_evolve_from['evolution_chain']['url']
    data_evolve_to = json.loads(requests.get(url_evolve_to).text)
    data_temp = data_evolve_to['chain']
    while(data_temp['species']['name'] != species):
        # print(data_temp['species']['name'])
        # print(name)
        data_temp = data_temp['evolves_to'][0]
    if len(data_temp['evolves_to']) == 0:
        evolves_to = "no further evolutions"
    else:
        evolves_to = data_temp['evolves_to'][0]['species']['name']

    held_items_temp = data['held_items']
    held_items = ""
    if len(held_items_temp) == 0:
        held_items = 'no items'
    for i in held_items_temp:
        temp = i['item']['name']
        temp = temp.replace('-',' ')
        if held_items_temp.index(i) != len(held_items_temp) - 1 and len(held_items_temp) != 1:
            held_items += temp + ', '
        else:
            held_items += temp

    types_temp = data['types']
    types = []
    for i in types_temp:
        types.append(i['type']['name'])
    if len(types) == 1:
        types_str = types[0]
    else:
        types_str = types[0] + " and " + types[1]

    stats = data['stats']
    base_stats = {}
    for i in stats:
        base_stats[i['stat']['name']] = i['base_stat']

    sprite = data['sprites']['front_default']

    url_location = f"https://pokeapi.co/api/v2/pokemon/{poke_id}/encounters"
    data_location = json.loads(requests.get(url_location).text)
    locations = ""
    if len(data_location) == 0:
        locations = "no natural locations"
    for i in data_location:
        temp = i['location_area']['name']
        temp = temp.replace('-',' ')
        if data_location.index(i) != len(data_location) - 1 and len(data_location) != 1:
            locations += temp + ', '
        else:
            locations += temp



    bio = f"{name.capitalize()} is a {types_str} type pokemon. It is {height} decimeters tall and weighs {weight} hectograms. {name.capitalize()} can evolve into {evolves_to} and evolves from {evolves_from}. It can hold {held_items} and can be found at {locations}."
    return [name, types, base_stats, bio, sprite]

def get_rand_jokes():
    url = "https://dad-jokes.p.rapidapi.com/random/joke?count=5"
    wd = os.path.dirname(os.path.realpath(__file__))
    file = open(wd + "/keys/key_DadJokes.txt", "r")
    apiKey = file.read()
    # print(apiKey)
    headers = {
        "X-RapidAPI-Key": f"{apiKey}",
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers).json()
    jokes = {}
    try:
        for i in range(5):
            id = response.get('body')[i]['_id']
            setup = response.get('body')[i]['setup']
            punchline = response.get('body')[i]['punchline']
            nsfw = response.get('body')[i]['NSFW']
            jokes[i] = [id, setup, punchline, nsfw]
    except:
        pass
    return jokes
