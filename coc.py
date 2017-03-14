# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import *
import requests
import urllib.parse

#replace my token with your generated token on developer.clashofclans.com
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijg2ZGY3NjE3LWQ4ODEtNDkyYy05ODcwLTliMzMyNTUwZDM0MCIsImlhdCI6MTQ4OTM2MTU5MCwic3ViIjoiZGV2ZWxvcGVyL2M2MmY3MTEyLWEwYmUtZmRiMS00ZGFlLWUyNTQ4NGViMDE4NiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEyMi4xNzUuMjM5LjE5NSIsIjQ3LjI0Ny4xMi4xMTMiLCI0Ny4yNDcuNy4yMjMiLCI0Ny4yNDcuMy45MSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.NqeVQv9_dYMMNSha8Opy8DbIEEk9kVj48mp0MckrqY5kU964h6EE1z2qGaFpiibxDLL_3u4DW4x79D5uDSQ6zw"
LARGE_FONT = ("Verdana",10)
SEPARATOR = "----------------------------------------------------------------------------"

class coc:

	URL = "https://api.clashofclans.com/v1/clans/"

	def __init__(self,token):

		self.token = token
		self.auth = 'Bearer '+ token
	

	def getClansByName(self,name,warFreq="unknown",locationId=None,minMembers=2,maxMembers=50,minClanPoints=1,minClanLevel=2,limit=4):

		PARAMS = {'name':name,'warFrequency':warFreq,'locationId':locationId,'minMembers':max(2,minMembers),'maxMembers':min(50,maxMembers),'minClanPoints':max(1,minClanPoints),'minClanLevel':max(2,minClanLevel),'limit':limit}
		response = requests.get(url = self.URL, params = PARAMS, headers = {'Accept': 'application/json', 'authorization': self.auth})
		data = response.json()
		return data

	def printClansByName(self,name,warFreq="unknown",locationId=None,minMembers=2,maxMembers=50,minClanPoints=1,minClanLevel=2,limit=4):

		data = self.getClansByName(name,warFreq,locationId,minMembers,maxMembers,minClanPoints,minClanLevel,limit)
		for i in range(limit):
			print("\n")
			print("Name: ",data["items"][i]["name"])
			print("Tag: ",data["items"][i]["tag"])
			print("Clan Level: ",data["items"][i]["clanLevel"])
			print("Type: ",data["items"][i]["type"])
			print("Clan Points: ",data["items"][i]["clanPoints"])
			print("Number of members: ",data["items"][i]["members"])
			print("War Frequency: ",data["items"][i]["warFrequency"])
			print("Required Trophies: ",data["items"][i]["requiredTrophies"])
			try:
				if data["items"][i]["location"]["isCountry"] == True:
					print("Country: ",data["items"][i]["location"]["name"])
				else:
					print("Location: ",data["items"][i]["location"]["name"])
			except:
				pass
			print("\n")

	def getClanByTag(self,tag):

		tag=urllib.parse.quote_plus(tag)
		url = self.URL + tag
		response = requests.get(url = url, headers = {'Accept': 'application/json', 'authorization': self.auth})
		data = response.json()
		return data

	def printClanByTag(self,tag):

		data = self.getClanByTag(tag)
		print("Name: ",data["name"])
		print("Tag: ",data["tag"])
		print("Clan Level: ",data["clanLevel"])
		print("Type: ",data["type"])
		print("Clan Points: ",data["clanPoints"])
		print("Number of members: ",data["members"])
		print("War Frequency: ",data["warFrequency"])
		print("War Wins: ",data["warWins"])
		print("War Win Streak: ",data["warWinStreak"])
		print("Required Trophies: ",data["requiredTrophies"])
		try:
			if data["location"]["isCountry"] == True:
				print("Country: ",data["location"]["name"])
			else:
				print("Location: ",data["location"]["name"])
		except:
			pass

	def getWarLog(self,tag,limit = 10):

		tag=urllib.parse.quote_plus(tag)
		url = self.URL + tag +"/warlog"
		PARAMS = {'limit':limit}
		response = requests.get(url = url, params = PARAMS, headers = {'Accept': 'application/json', 'authorization': self.auth})
		data = response.json()
		return data

	def printWarLog(self,tag,limit = 10):

		data = self.getWarLog(tag,limit)
		print(data)

	def getPlayer(self,tag):

		tag=urllib.parse.quote_plus(tag)
		url = "https://api.clashofclans.com/v1/players/" + tag
		response = requests.get(url = url, headers = {'Accept': 'application/json', 'authorization': self.auth})
		data = response.json()
		return data

	def printPlayer(self,tag):

		data = self.getPlayer(tag)
		print(data)



class ClashofClans(tk.Tk):

	def __init__(self, *args, **kwargs):

		tk.Tk.__init__(self, *args, **kwargs)

		tk.Tk.wm_title(self, "Clash of Clans")

		container = tk.Frame(self)

		container.pack(side="top", fill="both", expand = True)

		container.grid_rowconfigure(0,weight=1)
		container.grid_columnconfigure(0,weight=1)

		self.frames = {}

		for F in (TownHall,ClanByName,ClanInfoByName,ClanByTag,ClanInfoByTag,Player,PlayerInfo):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(TownHall)

	def show_frame(self, cont):

		frame = self.frames[cont]
		frame.tkraise()

class TownHall(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		label = tk.Label(self,text="Town Hall", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		getClanByName = ttk.Button(self, text="Search Clan by Name",
			command=lambda: controller.show_frame(ClanByName))
		getClanByName.pack()

		getClanByTag = ttk.Button(self, text="Search Clan by Tag",
			command=lambda: controller.show_frame(ClanByTag))
		getClanByTag.pack()

		getPlayer = ttk.Button(self, text="Search Player by Tag",
			command=lambda: controller.show_frame(Player))
		getPlayer.pack()


class ClanByName(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self,parent)

		label = tk.Label(self,text="Search Clans:", font=LARGE_FONT)
		label.grid(pady=10,padx=10)

		goTH = ttk.Button(self, text="back to Town Hall",
			command=lambda: controller.show_frame(TownHall))
		goTH.grid(row=1,column=0)

		clanNameLabel = tk.Label(self,text="Clan Name:", font=LARGE_FONT)
		clanNameLabel.grid(row=3,column=0,pady=10,padx=10)

		clanNameEntry = tk.Entry(self)
		clanNameEntry.grid(row=3,column=3)

		minMembersLabel = tk.Label(self,text="Min Members:", font=LARGE_FONT)
		minMembersLabel.grid(row=4,column=0,pady=10,padx=10)

		minMembersEntry = tk.Entry(self)
		minMembersEntry.grid(row=4,column=3)

		maxMembersLabel = tk.Label(self,text="Max Members:", font=LARGE_FONT)
		maxMembersLabel.grid(row=5,column=0,pady=10,padx=10)

		maxMembersEntry = tk.Entry(self)
		maxMembersEntry.grid(row=5,column=3)

		minClanPointsLabel = tk.Label(self,text="Min Clan Points:", font=LARGE_FONT)
		minClanPointsLabel.grid(row=6,column=0,pady=10,padx=10)

		minClanPointsEntry = tk.Entry(self)
		minClanPointsEntry.grid(row=6,column=3)

		minClanLevelLabel = tk.Label(self,text="Min Clan Level:", font=LARGE_FONT)
		minClanLevelLabel.grid(row=7,column=0,pady=10,padx=10)

		minClanLevelEntry = tk.Entry(self)
		minClanLevelEntry.grid(row=7,column=3)

		def getInfo():

			clanName = clanNameEntry.get()
			if clanName == "":
				clanName = "Squirrel Ninja"
			try:
				minMembers = int(minMembersEntry.get())
			except:
				minMembers = 2
			try:
				maxMembers = int(maxMembersEntry.get())
			except:
				maxMembers = 50
			try:
				minClanPoints = int(minClanPointsEntry.get())
			except:
				minClanPoints = 2
			try:
				minClanLevel = int(minClanLevelEntry.get())
			except:
				minClanLevel = 2

			c = coc(TOKEN)
			ClanInfoByName.DATA = c.getClansByName(name=clanName, minMembers=minMembers, maxMembers=maxMembers, minClanPoints=minClanPoints, minClanLevel=minClanLevel)
			controller.show_frame(ClanInfoByName)

		search = ttk.Button(self, text="Search",
			command= getInfo )
		search.grid(row=8,column=5)

class ClanInfoByName(tk.Frame):
	DATA = {}
	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		cName=[]
		cTag=[]
		cMembers=[]
		cLevel=[]
		cMinTrophies=[]
		cType=[]
		cLocation=[]
		cSep=[]

		for i in range(4):

			cName.append(tk.Label(self,text="Clan Name :", font=LARGE_FONT))
			cName[i].grid(row=i*8+1,column=0)

			cTag.append(tk.Label(self,text="Clan Tag :", font=LARGE_FONT))
			cTag[i].grid(row=i*8+2,column=0)

			cMembers.append(tk.Label(self,text="Members:", font=LARGE_FONT))
			cMembers[i].grid(row=i*8+3,column=0)

			cLevel.append(tk.Label(self,text="Clan Level :", font=LARGE_FONT))
			cLevel[i].grid(row=i*8+4,column=0)

			cMinTrophies.append(tk.Label(self,text="Required Trophies :", font=LARGE_FONT))
			cMinTrophies[i].grid(row=i*8+5,column=0)

			cType.append(tk.Label(self,text="Type :", font=LARGE_FONT))
			cType[i].grid(row=i*8+6,column=0)

			cLocation.append(tk.Label(self,text="Clan Location :", font=LARGE_FONT))
			cLocation[i].grid(row=i*8+7,column=0)

			cSep.append(tk.Label(self,text=SEPARATOR, font=LARGE_FONT))
			cSep[i].grid(row=i*8+8,column=0,columnspan=3)

		quote = ""
		clanNameLabel=[]
		clanTagLabel=[]
		clanMembersLabel=[]
		clanLevelLabel=[]
		clanRTLabel=[]
		clanLocationLabel=[]
		clanTypeLabel=[]

		for  i in range(4):

			clanNameLabel.append(tk.Label(self,text=quote,font=LARGE_FONT))
			clanNameLabel[i].grid(row=i*8+1,column=1)

			clanTagLabel.append(tk.Label(self,text=quote,font=LARGE_FONT))
			clanTagLabel[i].grid(row=i*8+2,column=1)

			clanMembersLabel.append(tk.Label(self,text=quote,font=LARGE_FONT))
			clanMembersLabel[i].grid(row=i*8+3,column=1)

			clanLevelLabel.append(tk.Label(self,text=quote,font=LARGE_FONT))
			clanLevelLabel[i].grid(row=i*8+4,column=1)

			clanRTLabel.append(tk.Label(self,text=quote,font=LARGE_FONT))
			clanRTLabel[i].grid(row=i*8+5,column=1)

			clanLocationLabel.append(tk.Label(self,text=quote,font=LARGE_FONT))
			clanLocationLabel[i].grid(row=i*8+7,column=1)

			clanTypeLabel.append(tk.Label(self,text=quote,font=LARGE_FONT))
			clanTypeLabel[i].grid(row=i*8+6,column=1)

		getClan = ttk.Button(self, text="back to Town Hall",
			command=lambda: controller.show_frame(TownHall))
		getClan.grid(row=33,column=2)

		def refresh():

			clanName=[]
			clanTag=[]
			clanMembers=[]
			clanLevel=[]
			clanRT=[]
			clanLocation=[]
			clanType=[]

			for i in range(4):

				clanName.append(ClanInfoByName.DATA["items"][i]["name"])
				clanNameLabel[i] = tk.Label(self,text=clanName[i],font=LARGE_FONT)
				clanNameLabel[i].grid(row=i*8+1,column=1)

				clanTag.append(ClanInfoByName.DATA["items"][i]["tag"])
				clanTagLabel[i] = tk.Label(self,text=clanTag[i],font=LARGE_FONT)
				clanTagLabel[i].grid(row=i*8+2,column=1)

				clanMembers.append(ClanInfoByName.DATA["items"][i]["members"])
				clanMembersLabel[i] = tk.Label(self,text=clanMembers[i],font=LARGE_FONT)
				clanMembersLabel[i].grid(row=i*8+3,column=1)

				clanLevel.append(ClanInfoByName.DATA["items"][i]["clanLevel"])
				clanLevelLabel[i] = tk.Label(self,text=clanLevel[i],font=LARGE_FONT)
				clanLevelLabel[i].grid(row=i*8+4,column=1)

				clanRT.append(ClanInfoByName.DATA["items"][i]["requiredTrophies"])
				clanRT[i] = tk.Label(self,text=clanRT[i],font=LARGE_FONT)
				clanRT[i].grid(row=i*8+5,column=1)

				clanType.append(ClanInfoByName.DATA["items"][i]["type"])
				clanTypeLabel[i] = tk.Label(self,text=clanType[i],font=LARGE_FONT)
				clanTypeLabel[i].grid(row=i*8+6,column=1)

				try:
					clanLocation.append(ClanInfoByName.DATA["items"][i]["location"]["name"])
				except:
					clanLocation.append("Not Available")

				clanLocationLabel[i] = tk.Label(self,text=clanLocation[i],font=LARGE_FONT)
				clanLocationLabel[i].grid(row=i*8+7,column=1)

		update = ttk.Button(self, text="Refresh",
			command= refresh)
		update.grid(row=33,column=0)

class ClanByTag(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self,parent)

		label = tk.Label(self,text="Search Clans:", font=LARGE_FONT)
		label.grid(pady=10,padx=10)

		goTH = ttk.Button(self, text="back to Town Hall",
			command=lambda: controller.show_frame(TownHall))
		goTH.grid(row=1,column=0)

		clanTagLabel = tk.Label(self,text="Clan Tag:", font=LARGE_FONT)
		clanTagLabel.grid(row=3,column=0,pady=10,padx=10)

		clanTagEntry = tk.Entry(self)
		clanTagEntry.grid(row=3,column=3)

		def getInfo():

			clanTag = clanTagEntry.get()
			if clanTag == "":
				clanTag = "#LVGL8G2Q"
			c = coc(TOKEN)
			ClanInfoByTag.DATA = c.getClanByTag(clanTag)
			controller.show_frame(ClanInfoByTag)

		search = ttk.Button(self, text="Search",
			command= getInfo )
		search.grid(row=4,column=4)

class ClanInfoByTag(tk.Frame):

	DATA = {}
	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		cName=tk.Label(self,text="Clan Name :", font=LARGE_FONT)
		cName.grid(row=1,column=0)

		cTag=tk.Label(self,text="Clan Tag :", font=LARGE_FONT)
		cTag.grid(row=2,column=0)

		cPoints=tk.Label(self,text="Clan Points :", font=LARGE_FONT)
		cPoints.grid(row=4,column=0)

		cFreq=tk.Label(self,text="War Frequency :", font=LARGE_FONT)
		cFreq.grid(row=3,column=0)

		cWins=tk.Label(self,text="Total Wins :", font=LARGE_FONT)
		cWins.grid(row=5,column=0)

		cStreak=tk.Label(self,text="Win Streak :", font=LARGE_FONT)
		cStreak.grid(row=6,column=0)

		cMembers=tk.Label(self,text="Members:", font=LARGE_FONT)
		cMembers.grid(row=7,column=0)

		cLevel=tk.Label(self,text="Clan Level :", font=LARGE_FONT)
		cLevel.grid(row=8,column=0)

		cMinTrophies=tk.Label(self,text="Required Trophies :", font=LARGE_FONT)
		cMinTrophies.grid(row=9,column=0)

		cType=tk.Label(self,text="Type :", font=LARGE_FONT)
		cType.grid(row=10,column=0)

		cLocation=tk.Label(self,text="Clan Location :", font=LARGE_FONT)
		cLocation.grid(row=11,column=0)

		quote = ""

		clanNameLabel=tk.Label(self,text=quote,font=LARGE_FONT)
		clanNameLabel.grid(row=1,column=1)

		clanTagLabel=tk.Label(self,text=quote,font=LARGE_FONT)
		clanTagLabel.grid(row=2,column=1)

		clanPointsLabel=tk.Label(self,text=quote, font=LARGE_FONT)
		clanPointsLabel.grid(row=4,column=1)

		clanFreqLabel=tk.Label(self,text=quote, font=LARGE_FONT)
		clanFreqLabel.grid(row=3,column=1)

		clanWinsLabel=tk.Label(self,text=quote, font=LARGE_FONT)
		clanWinsLabel.grid(row=5,column=1)

		clanStreakLabel=tk.Label(self,text=quote, font=LARGE_FONT)
		clanStreakLabel.grid(row=6,column=1)

		clanMembersLabel=tk.Label(self,text=quote,font=LARGE_FONT)
		clanMembersLabel.grid(row=7,column=1)

		clanLevelLabel=tk.Label(self,text=quote,font=LARGE_FONT)
		clanLevelLabel.grid(row=8,column=1)

		clanRTLabel=tk.Label(self,text=quote,font=LARGE_FONT)
		clanRTLabel.grid(row=9,column=1)

		clanLocationLabel=tk.Label(self,text=quote,font=LARGE_FONT)
		clanLocationLabel.grid(row=11,column=1)

		clanTypeLabel=tk.Label(self,text=quote,font=LARGE_FONT)
		clanTypeLabel.grid(row=10,column=1)


		getClan = ttk.Button(self, text="back to Town Hall",
			command=lambda: controller.show_frame(TownHall))
		getClan.grid(row=12,column=2)

		def refresh():

			clanName=ClanInfoByTag.DATA["name"]
			clanNameLabel = tk.Label(self,text=clanName,font=LARGE_FONT)
			clanNameLabel.grid(row=1,column=1)

			clanTag=ClanInfoByTag.DATA["tag"]
			clanTagLabel = tk.Label(self,text=clanTag,font=LARGE_FONT)
			clanTagLabel.grid(row=2,column=1)

			clanPoints=ClanInfoByTag.DATA["clanPoints"]
			clanPointsLabel=tk.Label(self,text=clanPoints, font=LARGE_FONT)
			clanPointsLabel.grid(row=4,column=1)

			clanFreq=ClanInfoByTag.DATA["warFrequency"]
			clanFreqLabel=tk.Label(self,text=clanFreq, font=LARGE_FONT)
			clanFreqLabel.grid(row=3,column=1)

			clanWins=ClanInfoByTag.DATA["warWins"]
			clanWinsLabel=tk.Label(self,text=clanWins, font=LARGE_FONT)
			clanWinsLabel.grid(row=5,column=1)

			clanStreak=ClanInfoByTag.DATA["warWinStreak"]
			clanStreakLabel=tk.Label(self,text=clanStreak, font=LARGE_FONT)
			clanStreakLabel.grid(row=6,column=1)

			clanMembers=ClanInfoByTag.DATA["members"]
			clanMembersLabel = tk.Label(self,text=clanMembers,font=LARGE_FONT)
			clanMembersLabel.grid(row=7,column=1)

			clanLevel=ClanInfoByTag.DATA["clanLevel"]
			clanLevelLabel = tk.Label(self,text=clanLevel,font=LARGE_FONT)
			clanLevelLabel.grid(row=8,column=1)

			clanRT=ClanInfoByTag.DATA["requiredTrophies"]
			clanRT = tk.Label(self,text=clanRT,font=LARGE_FONT)
			clanRT.grid(row=9,column=1)

			clanType=ClanInfoByTag.DATA["type"]
			clanTypeLabel = tk.Label(self,text=clanType,font=LARGE_FONT)
			clanTypeLabel.grid(row=10,column=1)

			try:
				clanLocation=ClanInfoByTag.DATA["location"]["name"]
			except:
				clanLocation="Not Available"

			clanLocationLabel = tk.Label(self,text=clanLocation,font=LARGE_FONT)
			clanLocationLabel.grid(row=11,column=1)

		update = ttk.Button(self, text="Refresh",
			command= refresh)
		update.grid(row=12,column=0)

class Player(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self,parent)

		label = tk.Label(self,text="Search Player:", font=LARGE_FONT)
		label.grid(pady=10,padx=10)

		goTH = ttk.Button(self, text="back to Town Hall",
			command=lambda: controller.show_frame(TownHall))
		goTH.grid(row=1,column=0)

		playerTagLabel = tk.Label(self,text="Player Tag:", font=LARGE_FONT)
		playerTagLabel.grid(row=3,column=0,pady=10,padx=10)

		playerTagEntry = tk.Entry(self)
		playerTagEntry.grid(row=3,column=3)

		def getInfo():

			playerTag = playerTagEntry.get()
			if playerTag == "":
				playerTag = "#8YJUYYQPJ"
			c = coc(TOKEN)
			PlayerInfo.DATA = c.getPlayer(playerTag)
			controller.show_frame(PlayerInfo)

		search = ttk.Button(self, text="Search",
			command= getInfo )
		search.grid(row=4,column=4)

class PlayerInfo(tk.Frame):

	DATA = {}

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		pName=tk.Label(self,text="Player Name :", font=LARGE_FONT)
		pName.grid(row=1,column=0)

		pTag=tk.Label(self,text="Player Tag :", font=LARGE_FONT)
		pTag.grid(row=2,column=0)

		pExpLevel=tk.Label(self,text="Experience Level:", font=LARGE_FONT)
		pExpLevel.grid(row=3,column=0)

		pTHL=tk.Label(self,text="Town Hall Level :", font=LARGE_FONT)
		pTHL.grid(row=4,column=0)

		pCTrophies=tk.Label(self,text="Current Trophies :", font=LARGE_FONT)
		pCTrophies.grid(row=6,column=0)

		pBTrophies=tk.Label(self,text="Best Trophies :", font=LARGE_FONT)
		pBTrophies.grid(row=5,column=0)

		pLeague=tk.Label(self,text="League :", font=LARGE_FONT)
		pLeague.grid(row=7,column=0)

		pClan=tk.Label(self,text="Clan :", font=LARGE_FONT)
		pClan.grid(row=8,column=0)

		pClanTag=tk.Label(self,text="Clan Tag :", font=LARGE_FONT)
		pClanTag.grid(row=9,column=0)

		pClanLevel=tk.Label(self,text="Clan Level :", font=LARGE_FONT)
		pClanLevel.grid(row=10,column=0)

		quote = ""

		pNameLabel=tk.Label(self,text=quote, font=LARGE_FONT)
		pNameLabel.grid(row=1,column=1)

		pTagLabel=tk.Label(self,text=quote, font=LARGE_FONT)
		pTagLabel.grid(row=2,column=1)

		pExpLevelLabel=tk.Label(self,text=quote, font=LARGE_FONT)
		pExpLevelLabel.grid(row=3,column=1)

		pTHLLabel=tk.Label(self,text=quote, font=LARGE_FONT)
		pTHLLabel.grid(row=4,column=1)

		pCTrophiesLabel=tk.Label(self,text=quote, font=LARGE_FONT)
		pCTrophiesLabel.grid(row=6,column=1)

		pBTrophiesLabel=tk.Label(self,text=quote, font=LARGE_FONT)
		pBTrophiesLabel.grid(row=5,column=1)

		pLeagueLabel=tk.Label(self,text=quote, font=LARGE_FONT)
		pLeagueLabel.grid(row=7,column=1)

		pClanLabel=tk.Label(self,text=quote, font=LARGE_FONT)
		pClanLabel.grid(row=8,column=1)

		pClanTagLabel=tk.Label(self,text=quote, font=LARGE_FONT)
		pClanTagLabel.grid(row=9,column=1)

		pClanLevelLabel=tk.Label(self,text=quote, font=LARGE_FONT)
		pClanLevelLabel.grid(row=10,column=1)

		getClan = ttk.Button(self, text="back to Town Hall",
			command=lambda: controller.show_frame(TownHall))
		getClan.grid(row=12,column=2)

		def refresh():

			playerName = PlayerInfo.DATA["name"]
			pNameLabel=tk.Label(self,text=playerName, font=LARGE_FONT)
			pNameLabel.grid(row=1,column=1)

			playerTag = PlayerInfo.DATA["tag"]
			pTagLabel=tk.Label(self,text=playerTag, font=LARGE_FONT)
			pTagLabel.grid(row=2,column=1)

			playerExpLevel = PlayerInfo.DATA["expLevel"]
			pExpLevelLabel=tk.Label(self,text=playerExpLevel, font=LARGE_FONT)
			pExpLevelLabel.grid(row=3,column=1)

			playerTHL = PlayerInfo.DATA["townHallLevel"]
			pTHLLabel=tk.Label(self,text=playerTHL, font=LARGE_FONT)
			pTHLLabel.grid(row=4,column=1)

			playerCTrophies = PlayerInfo.DATA["trophies"]
			pCTrophiesLabel=tk.Label(self,text=playerCTrophies, font=LARGE_FONT)
			pCTrophiesLabel.grid(row=6,column=1)

			playerBTrophies = PlayerInfo.DATA["bestTrophies"]
			pBTrophiesLabel=tk.Label(self,text=playerBTrophies, font=LARGE_FONT)
			pBTrophiesLabel.grid(row=5,column=1)

			playerLeague = PlayerInfo.DATA["league"]["name"]
			pLeagueLabel=tk.Label(self,text=playerLeague, font=LARGE_FONT)
			pLeagueLabel.grid(row=7,column=1)

			playerClan = PlayerInfo.DATA["clan"]["name"]
			pClanLabel=tk.Label(self,text=playerClan, font=LARGE_FONT)
			pClanLabel.grid(row=8,column=1)	

			playerClanTag = PlayerInfo.DATA["clan"]["tag"]
			pClanTagLabel=tk.Label(self,text=playerClanTag, font=LARGE_FONT)
			pClanTagLabel.grid(row=9,column=1)

			playerClanLevel = PlayerInfo.DATA["clan"]["clanLevel"]
			pClanLevelLabel=tk.Label(self,text=playerClanLevel, font=LARGE_FONT)
			pClanLevelLabel.grid(row=10,column=1)

		update = ttk.Button(self, text="Refresh",
			command= refresh)
		update.grid(row=12,column=0)

app = ClashofClans()
app.mainloop()