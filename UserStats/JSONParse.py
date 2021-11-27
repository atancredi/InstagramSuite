import json

# list to dictionary
def Convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct

f = open("..\\data\\posts_localStorage.json", "r")
# deserailizing the data
data = json.loads(f.read())
print(data[0])

c = open("..\\data\\posts_localStorage_parsed.json", "w")

print("---------------")

f.close()
c.close()
