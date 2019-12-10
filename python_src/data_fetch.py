import requests, json, base64
import json, csv


clientId = ""
clientSK = ""

id_song = "11dFghVXANMlKmJXsNCbNl"


class Spotify:

    clientId = ""
    clientSK = ""
    token = ""
    header = ""
    base_url = "https://api.spotify.com/v1/"

    def __init__(self, ci, csk):
        self.clientId = ci
        self.clientSK = csk
        self.getToken()

    def getToken(self):
        url = "https://accounts.spotify.com/api/token"
        auth = base64.b64encode((self.clientId + ":" + self.clientSK).encode("utf-8"))
        header = {
            "Authorization" : "Basic " + str(auth, "utf-8"),
            "Content-type" : "application/x-www-form-urlencoded"
        }
        payload = {
            "grant_type" : "client_credentials"
        }
        response = requests.post(url, headers=header, data=payload).json()
        self.token = response["access_token"]
        head =  {
            "Authorization" : "Bearer " + self.token,
        }
        self.header = head

    def getCategories(self, num = 20):
        url = "https://api.spotify.com/v1/browse/categories?limit=20"
        response = requests.get(url, headers=self.header).json()
        cats = {}
        for it in response["categories"]["items"]:
            cats.update({it["id"] : it["href"]})
        return cats

    def getTrack(self):
        url = "https://api.spotify.com/v1/audio-features/06AKEBrKUckW0KREUWRnvT"
        response = requests.get(url, headers=self.header).json()
        print(response)

    def getPlaylists(self,category, num = 20):
        url = "https://api.spotify.com/v1/browse/categories/" + category + "/playlists?limit=20"
        response = requests.get(url, headers=self.header).json()
        print(response)
        plays = []
        for it in response["playlists"]["items"]:
            plays.append(it["id"])
        return plays

    def getPlaylistTracks(self,id):
        url = "https://api.spotify.com/v1/playlists/" + id + "/tracks"
        response = requests.get(url, headers=self.header).json()
        tracks = []
        for it in response["items"]:
            try:
                tracks.append(
                    {
                        "id":it["track"]["id"], 
                        "artist" : it["track"]["artists"][0]["name"], 
                        "name": it["track"]["name"], 
                        "popularity" : it["track"]["popularity"], 
                        "preview" :  it["track"]["preview_url"]
                    }
                )
            except:
                pass
        return tracks

    def getTrackFeatures(self, track_arr):
        url = "https://api.spotify.com/v1/audio-features"
        queries = []
        i =0 
        while i <= len(track_arr):
            temp = track_arr[i: i + 100]
            str = ",".join(temp)
            queries.append(str)
            i = i+ 100
        # print(queries)
        trackdetails = []
        for items in queries:
            url = "https://api.spotify.com/v1/audio-features/?ids=" + items 
            response = requests.get(url, headers=self.header).json()
            trackdetails.extend(response["audio_features"])
        return trackdetails

    def dataToFile(self):
        data = []
        with open('cat.txt') as f:
            for line in f:
                data.append(json.loads(line))
        categories = data[0]

        for key, value in categories.items():
            track = []
            for tracks in value:
                track.append(tracks["id"])
            track_desc = spotify.getTrackFeatures(track)
            print(len(value), len(track_desc))
            for i in range(len(value)):
                try:
                    value[i].update(track_desc[i]) 
                except:
                    pass
        print("abc")

        with open('final.txt', 'w') as file:
            file.write(json.dumps(categories))

class GenerateCSV:

    @staticmethod
    def generate_csv(filename='fianl.txt'):
        data = []
        with open(filename) as f:
            for line in f:
                data.append(json.loads(line))

        data = data[0]

        d = []
        for key, value in data.items():
            for values in value:
                values.update({"label": key})
                d.append(values)

        # with open('mycsvfile.csv', 'w') as f:
        #     w = csv.DictWriter(f, my_dict.keys())
        #     w.writeheader()
        #     w.writerow(my_dict)



        f = open('data.csv','w')
        w = csv.DictWriter(f,d[0].keys())
        w.writeheader()
        w.writerows(d)
        f.close()

        return



# print("connected")


# categories = spotify.getCategories(30)

# print("categories fetched")
# for key, value in categories.items():
#     categories[key] = spotify.getPlaylists(key,20)

# print("playlists fetched")
# print("write playlists to file")

# with open('play.txt', 'w') as file:
#     file.write(json.dumps(categories))

# data = []
# with open('play.txt') as f:
#     for line in f:
#         data.append(json.loads(line))

# categories = data[0]

# for key, value in categories.items():
#     tracks = []
#     for playlists in value:
#         tracks.extend(spotify.getPlaylistTracks(playlists))
#     categories[key] = tracks

# del categories["wellness"]

# for key, value in categories.items():
#     print(key, len(value))
#     if(len(value) == 0):
#         del categories[key]

# print("write categories file")
# with open('cat.txt', 'w') as file:
#     file.write(json.dumps(categories))

if __name__ == '__main__':
    spotify = Spotify(clientId,clientSK)
    spotify.dataToFile()
    GenerateCSV.generate_csv()