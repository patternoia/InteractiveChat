import os
import codecs
import json


class MySettings(object):
	def __init__(self, settingsfile=None, Parent=None):
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8")
		except:
			self.Command = "!say"
			self.Response = ""
			self.Cost = 0
			self.CooldownUser = 10
			self.CooldownGlobal = 10
			self.CooldownResponse = "Wait!"
			self.Permission = "everyone"
			self.Info = ""
			self.ChannelId = 0
			self.BadWords = ""
			self.Bttv = True
			self.Freedom = False
			self.Direction = 'down'


	def Reload(self, jsondata):
		self.__dict__ = json.loads(jsondata, encoding="utf-8")
		return

	def Save(self, settingsfile):
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
				json.dump(self.__dict__, f, encoding="utf-8")
			with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
				f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
		except:
			Parent.Log(ScriptName, "Failed to save settings to file.")
		return