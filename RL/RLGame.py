import requests
import json
from RLHeader import *

class RLGame():
    def __init__(self, gwurl, scoreurl, reseturl, otp, teamId, userId, apiKey):
        self.gwurl = gwurl
        self.scoreurl = scoreurl
        self.reseturl = reseturl
        self.otp = otp
        self.teamId = teamId
##        self.userId = userId
##        self.apiKey = apiKey
        self.headers = {
          'x-api-key': apiKey,
          'userId': userId,
          'User-Agent': 'PostmanRuntime/7.31.3'
        }

    def GetRuns(self, count):
        payload={}

        response = requests.request("GET", self.scoreurl+"?type=runs&teamId="+self.teamId+"&count="+count,
                                    headers=self.headers, data=payload)

        return eval(response.text)

    def GetLocation(self):
        payload={}

        response = requests.request("GET", self.gwurl+"?type=location&teamId="+self.teamId,
                                    headers=self.headers, data=payload)

        return eval(response.text)

    def EnterWorld(self, worldId):
        payload={'type': 'enter',
        'worldId': worldId,
        'teamId': self.teamId}
        files=[

        ]

        response = requests.request("POST", self.gwurl, headers=self.headers, data=payload, files=files)

        return eval(response.text)

    def MakeMove(self, move, worldId):
        payload={'type': 'move',
        'worldId': worldId,
        'teamId': self.teamId,
        'move': move}
        files=[

        ]

        response = requests.request("POST", self.gwurl, headers=self.headers, data=payload, files=files)

        return json.loads(response.text)
##        return eval(response.text)

    def GetScore(self):
        payload={}

        response = requests.request("GET", self.scoreurl+"?type=score&teamId="+self.teamId,
                                    headers=self.headers, data=payload)

        return eval(response.text)

    def ResetMyTeam(self):
        payload={}

        response = requests.request("GET", self.reseturl+"?teamId="+self.teamId+"&otp="+self.otp,
                                    headers=self.headers, data=payload)

        return eval(response.text)


# main function
if __name__ == '__main__':
    
    RL = RLGame(GWURL, SCOREURL, RESETURL, OTP, TEAMID, USERID, APIKEY)
    dict = RL.GetRuns(str(1))
    print(dict)
    dict = RL.GetLocation()
    print(dict)
    dict = RL.EnterWorld('0')
    print(dict)
    dict = RL.MakeMove('N', '0')
    print(dict)
    dict = RL.GetScore()
    print(dict)
    dict = RL.ResetMyTeam()
    print(dict)
