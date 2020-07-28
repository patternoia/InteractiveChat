#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from Settings_Module import MySettings
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Interactive Chat Overlay"
Website = ""
Description = "!say will post a message in the chat overlay"
Creator = "patternoia"
Version = "1.0.0.0"

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings

#   Create Settings Directory
directory = os.path.join(os.path.dirname(__file__), "Settings")
if not os.path.exists(directory):
    os.makedirs(directory)

#   Load settings
SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\\settings.json")
ScriptSettings = MySettings(SettingsFile)

if len(ScriptSettings.BadWords):
    ScriptSettings.BadWordList = ScriptSettings.BadWords.split(',')
else:
    ScriptSettings.BadWordList = []

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    if not data.IsChatMessage():
        return

    for word in ScriptSettings.BadWordList:
        if word in data.Message:
            return

    if ScriptSettings.Freedom:
        Parent.BroadcastWsEvent("EVENT_CHAT", json.dumps({'raw': data.RawData, 'user': data.User, 'message': data.Message, 'command': ''}))
        return

    if not data.GetParam(0).lower() == ScriptSettings.Command.lower():
        return

    #   Check if the propper command is used, the command is not on cooldown and the user has permission to use the command
    if Parent.HasPermission(data.User,ScriptSettings.Permission,ScriptSettings.Info):
        if Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User):
            if len(ScriptSettings.CooldownResponse):
                Parent.SendStreamMessage(ScriptSettings.CooldownResponse + ' / Remaining time ' + str(Parent.GetUserCooldownDuration(ScriptName,ScriptSettings.Command,data.User)) + ' seconds')
            return
        if Parent.IsOnCooldown(ScriptName,ScriptSettings.Command):
            if len(ScriptSettings.CooldownResponse):
                Parent.SendStreamMessage(ScriptSettings.CooldownResponse + ' / Remaining time ' + str(Parent.GetCooldownDuration(ScriptName,ScriptSettings.Command)) + ' seconds') 
            return

        if ScriptSettings.Cost > Parent.GetPoints(data.User):
            return
        else:
            Parent.RemovePoints(data.User, ScriptSettings.Cost)

        Parent.BroadcastWsEvent("EVENT_CHAT", json.dumps({'raw': data.RawData, 'user': data.User, 'message': data.Message, 'command': data.GetParam(0)}))
        if len(ScriptSettings.Response): Parent.SendStreamMessage(ScriptSettings.Response)    # Send your message to chat

        Parent.AddUserCooldown(ScriptName,ScriptSettings.Command,data.User,ScriptSettings.CooldownUser)  # Put the command on cooldown
        Parent.AddCooldown(ScriptName,ScriptSettings.Command,ScriptSettings.CooldownGlobal)  # Put the command on cooldown

    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters)
#---------------------------
# def Parse(parseString, userid, username, targetid, targetname, message):
#     if "$myparameter" in parseString:
#         return parseString.replace("$myparameter","I am a cat!")

#     return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.Reload(jsonData)
    Parent.BroadcastWsEvent("EVENT_SETTINGS_UPDATE", jsonData)
    if len(ScriptSettings.BadWords):
        ScriptSettings.BadWordList = ScriptSettings.BadWords.split(',')
    else:
        ScriptSettings.BadWordList = []
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return

def ClearChat():
    # by the time this method is called, the websocket event was already sent
    return
