# entities = {"genre": "comedy", "year": 2020}
#filter = {"genre": {"$eq": "documentary"},"year": 2019}
entities = {"LOC": ["UK"],"PER": ["Vlad Diac", "Mihai Birsan"],"ORG": ["Nimble Nexus"],"MISC": ["Romania", "2020"]}

def build_filter(entities):
    filter = {}
    for key in entities:
        #if there is more than one entity of the same type, we need to use $in
        if len(entities[key]) > 1:
            filter[key] = {"$in": entities[key]}
        else:
            filter[key] = {"$eq": entities[key][0]}
    return filter

filter = build_filter(entities)
print(filter)
