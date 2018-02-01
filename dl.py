import requests
import simplejson


def request(cmd, opts=None):
    url = "http://www.carqueryapi.com/api/0.3/?callback=?&cmd=%s" % cmd
    if opts:
        for k, v in opts.items():
            url += "&%s=%s" % (k, v)

    print url
    data = requests.get(url).content
    print data
    json = data[4:-2]
    return simplejson.loads(json)


def getYears():
    #years = request("getYears")
    return range(1940, 2014)
    #return range(int(years["Years"]["min_year"]), int(years["Years"]["max_year"]))


def getMakes(year):
    makes = request(
        "getMakes",
        {
            "sold_in_us": "1",
            "year": year
            })
    return [make["make_id"] for make in makes["Makes"]]


def getModels(year, make):
    models = request(
        "getModels",
        {
            "sold_in_us": "1",
            "year": year,
            "make": make
            })
    if "Models" in models:
      return [model["model_name"] for model in models["Models"]]
    else:
      return []


def getTrims(year, make, model):
    data = request(
        "getTrims",
        {
            "sold_in_us": "1",
            "year": year,
            "make": make,
            "model": model
            })
    if "Trims" in data:
      return [trim for trim in data["Trims"]]
    else:
      return []

if __name__ == '__main__':
    data = []
    for year in getYears():
        print year
        for make in getMakes(year):
            print year, make
            for model in getModels(year, make):
                print year, make, model
                filename = "trims/%s%s%s.json" % (year, make, model)
                if os.path.exists(filename):
                  continue
                for trim in getTrims(year, make, model):
                    print trim
                    data.append(trim)

                    f = open(filename, 'w')
                    f.write(simplejson.dumps(trim))
                    f.close()

                    f = open('cardata.json', 'w')
                    f.write(simplejson.dumps(data))
                    f.close()

