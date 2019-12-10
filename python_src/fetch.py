import requests, json, base64
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
                tracks.append({"id":it["track"]["id"], "artist" : it["track"]["artists"][0]["name"], "name": it["track"]["name"], "popularity" : it["track"]["popularity"], "preview" :  it["track"]["preview_url"]})
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


spotify = Spotify(clientId,clientSK)

# print("connected")
# # data = ['2EyECcIQEsdFQoQRenrDcN', '5aGDIGKHrGAYJn33DsVdIF', '12NG9pyCWHHVU6qqi2eeY8', '1kCfP81Gj9wkbGkOpCkuZA', '7vIERuwVxmw24C1eKqbru7', '6lfMvOUpSYC0V2NFIsBLNI', '6C1fdB76jVoPCccAanw2dj', '6GeL3xpwOQ3wJu5qLMQJQc', '6QX9w5RIQvh20QrXuwbnFi', '3WNJcD4xvnHrt5q5RuzaeW', '02fMscVZ46N4l46yHZQkqT', '2MX3UFRtbMg7rqGxLjlP07', '3cn4bKSJShQzuoKMZ6XMis', '15SfsE8nukbTgfl8xu74d7', '3Uejh7R2Xq52oqrh8XOo5J', '0zMTiHXme9k2newg3Ir8Md', '7cw2yeC9wWZSuWwBjPTfwe', '6w938mZxCQfSjZRmwK329X', '32QACfMXvoSsiwxgulfIQU', '4QKV23A4GTDmZETzjtQI9c', '2JO3HwMRPeya8bXbtbyPcf', '0bHm2wFL0m7qZIlhO7PQu5', '6zQhANi5mDTELfSuUFPx4Q', '1i6N76fftMZhijOzFQ5ZtL', '2JzZ8UTEb1GGvR8Ra0Nfy2', '1y5LL9dpLXbCXNKKqw5wCJ', '0PDZ4Rgj36MxVgvoMv3sk5', '3yP0cohcr97BUNJcgvmSVg', '4OvQsAObGMF3dpkCV6DZzb', '1FL9DHDSED6lxNMDJUJQvB', '5p3JunprHCxClJjOmcLV8G', '5jzma6gCzYtKB1DbEwFZKH', '5moTxUGPZXgGmosl4rIELm', '16jUJ4RsmyQG8z3clJuUaz', '2UnY8ApZT4roi66n1LDAil', '7bx4zW72qdZKBb8p6g80jb', '78lgmZwycJ3nzsdgmPPGNx', '5ZgNecJcN9SSopnmCTlpXs', '5FTbeZMbUgKfaSaCN8bY09', '6HZ67VImxqr8aMBEEhblzf', '7bIQeY33PkduZRmR3h9BIY', '5YSI1311X8t31PBjkBG4CZ', '6Gi8vIT6In8RrT2eTKxoVR', '3W0xbvrZqaao3ZZEDhVQ0r', '4wZSxAXLNRFfQ0yyaCvHei', '0rme3FLbw5o1KLXpJzivjS', '0kqFlkmfvKzQ4QSmx5PZ1A', '6cFaRahEaLyew4ATx1QaUx', '1Qb2f8cDXorwKTbY0nQ0IH', '1aMxqU4b59JT5Y9Wtyusis', '0WNGPpmWqzPnk0psUhJ3SX', '6y4FVJwf09ssxuRnlEgXkp', '2hvOsGJc6qll4WzW8Ljqc3', '2QSD3K3b3BJ8DPhGhQfDPW', '21jBRxUvrWXTwBfGnQwyVy', '6FxD82u5P8yKohcYYDxyqw', '5QTxFnGygVM4jFQiBovmRo', '17GEcOhfo7rRr3wKumLHV2', '55TeO50ytH96i93yihdNJE', '1PwB9EADXS90I8LoewLXfl', '2h97II7QJZTBZv02HcocI7', '2yE3bwbhqypdsuhmv48Svn', '73HSIWZlSCfs4tqVkrGv7H', '7cdnq45E9aP2XDStHg5vd7', '0tsHAAhdxSzwHAeHHXKbsw', '6TNNMVpOgn8K5NoDC7alG6', '0ZfP7K8NoyJRjEfWWk8Mlv', '2sICTf5zrSZnTttimrcm2M', '0LzCSYjFxH3LKSU4UIeRBk', '4GRnCW4Alb5vcfptFytJdl', '4Ec8I6H20zu7F2vDdg90qP', '6RTh5BDes7y6KwC0rxW8WG', '0WghYc6JU0HbCvsgGlyqId', '3MFFDRC4wTN9JNGtzXsZlN', '5nYYu9UeWFZhjwFLJMfX77', '0ElRzK07sc9eszyk1ea9Ab', '3x0iCzjgf0v9lnwvAhU9P2', '3RZqcBz5WTWN2E5svMH162', '4Mj2GtsgUDaf43zxdw48hd', '3aInErz06eEAbRHMnsORR2', '3MmogIpfk1GVXRMmRjKLGI', '1wP1qnWy0cZWxnbWkzf9La', '0TaWdoJiAJoln9OQ1RbdNs', '00sydAz6PeOxYzwG1dRIPi', '7wLBPjReJhdkFtrGHgUcxG', '4lr8mubS2OpgJEOuPHx2rV', '0FnmRkP81O1I6oeOeU1xXS', '24M81fKyhTWBuYzczQMkOp', '5AdLu2shYmDMqt2pHaOEle', '6pXcyjABZyf6LKzL4wsj9k', '6e3qHQtKdbNhUVuuNNsyqD', '150NSrON3DeZM1aLyz3MoM', '5E5HYgxGMp3BPakHGfKfIB', '6ZWVeMysm8Q8zZu3lKnY2v', '7mxvuhmRrnQ31vHRm9A9qj', '2fWxcJeDQiLStdAdwF4ms6', '4l1Yx4GK7GU55Xtwl9we9U', '1vOgfMjWq10rW4h0U7yzO8', '5rJJnYeAeIsb0T4FkiaUvX', '4F797Kz0zqZiMxNcRdO8R2', '2rl3qVhTopu9De51tKCDUM', '2ngVZZGrIYAxyxaA2QcWTB', '65AABj5XsDcxGT92w3jK0o', '4wWQeafQ4q5WKafYIuUmY8', '0A8P76W8MXeulFGIHNWSG1', '716OZGLBg3vkNfMTpfbYm6', '0NyE3z63bQpiqDkx6DSjl0', '1ogk8gkNwRw9iHONH2CAna', '6z6i7ssJ5AIqSqhVcecJpa', '2XRT5pPoxTdudrcqfxHSvK', '01TyFEZu6mHbffsVfxgrFn', '14IN2apSi57uPG9hAC8kfL', '54H7CLmI5SE7wmhlE0THS5', '7b1aBkrngrTz8RXlkdQCay', '2DSxutganHw57vSdvmgjZt', '2Js2COGl7htc00CjZ2L2CO', '4soIPMs2XqUFu9roKupZ8I', '5P3JJGeG536cS1ciDnJsCk', '5KXPhIqiXPUBCxH3jyc10U', '5l4UVzmcW0vt2N7BXXS9M0', '41FUydVAeBuf0qLztk0d5j', '6jwZQIS9nPUQ7yCCouusqx', '5EUJ3wPl8KVTbsYgdsCixv', '66SPXY48GHqvedbRT7jBey', '66hEhjJ69nPkPyHCB5mANE', '5j375wUE1V53HpkKtiDKT2', '3HV9YnoYACjlrJ5CiZ3hLj', '46IEYjzyS37lltLLCDJbC0', '1B2SbIJqWWjMa7yGeeOWDp', '7eXDhsMpOFdsJWauZgq9qv', '1bnzho2GEO8gOg1j0a8Tnq', '5g6PqhkeTyARGPROM5Gosp', '6dDWdTZXJuDb5aMD3MC4eX', '4bMXxqBnfgHec86gvIJSb1', '0kBAFAVajRjCX8kXneVsZI', '5Pdsyk2NuTJ56mE97DmxmN', '2SIgKA7WTqDWQrcO8IP8Sc', '2Cw4Z95OdYBElmbdhj5EwU', '4QgIkSyVxv6FmsWO2dZz4J', '5jh147eWeuNyimT2Oo1A5J', '1pPesOxENcN3XdZGV3jOjs', '46YxybUOOH2MYRXBoHXUgw', '6jKDR323PynjvTkoWTNbqx', '4bFtkOCmHiRx6SjIAL1hdm', '7GfcvEme8J6sI3k8pNTU2Y', '7jqM0p5mYWqgwwVjdmWD8W', '2OGta1TI4EkWVR71xZBcfF', '7d9212orrSfVHQaSdesffl', '6D0RsrrwQ2YSYA9lv4lgz5', '2KeTrh78SDZCwwtmGlgncd', '5RyGi46ibm6UKnuDO5kpdO', '1l0CFINuN2Ug755WAxblxL', '4wf0EYJDLjaHoRXJ7fAvxm', '46Mq99aSEm1UoIg42pmCZm', '225WgsvbK6RoIH6Y7OhKP2', '19cprjSakswn0VsENCg6uu', '5I324DQSe589WK21l83G6X', '2OP0X9P8khKcUDtWUzCLHv', '1t3nMYYdEvbubaD5FMDglq', '4FDkX9JD3FzmttdfYI3JvS', '0K8N0F3efUhd55TxNGgmGD', '6PrTCr4WB1Pyf7Fk1Hd1Da', '75OoxBhx3J7ptBxmu4SqAi', '7cAkG4eP6QhXj3Sq3sdIfF', '71fC5JZdi0w1nTMnQomdsO', '5d9BthpFORCiN5S1lVGCSc', '68T6wCFarzNXU5dBywqc60', '5tJghWo8o7FYLtRDFpRg3R', '1Gij4Ja8h7W64VXi1Eqj6j', '21dr1PIP5wVs3OdpLaMkM3', '0cDpyfAXMCKgKEEnkYzb3D', '5rDzL33WiYowiXlZhwWvst', '2eN6V8hiaW2BB7ol4UVvYf', '0IhH5cuZdOg3eELZe4yVtk', '2s30KXFLxnyH9CHKoO3Yum', '0AACjaI0rxjufqxmsu6OfF', '3QNkkruVrn8sXLicRKg6P9', '5g2JXHcnhj6nmjzzE11G9P', '0v8UvAhruTvkA90MR7039n', '6urUaCWU3HXdalm0oZU1Cd', '7iJ5IuGJ7AX97KSrFfcREa', '2Y0xdEsWhfDAsvtMzFqJ73', '4Em5Dsf7FZheKNUuBvujzf', '6kCQsjFV3SubIrNTDkGrdr', '5zaVuOiil4YVgKLXEbya43']

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