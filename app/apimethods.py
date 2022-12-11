import requests, json

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
        placeOfBirth = "borned in "+placeOfBirth
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
    if hairColor != "No Hair":
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
    bio = f'{FullName} or {name} is a {alignedment} aligned character {placeOfBirth}. {name} has the appearance of a {race}{gender} {height} {weight}with {eyeColor} eyes and {hairColor}. {pronoun} works as a {occupation}. {pronoun} first appeared in {firstAppearance} by {publisher}. {pronoun} is affiliated {groupAffiliation}.'
    image = data["images"]["md"]
    return [name, powerstats, bio, image]

# print(hero_info(9))