import httplib, urllib, urllib2
from bs4 import BeautifulSoup
import cookielib
import time

import sys

botUserName = 'p4r4digm'
botPassword = 'para6015'
wikiURL = 'http://amishsmp.wikia.com'
loginToken = ""
cj = cookielib.CookieJar()
wikiOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

wpStarttime = 0
wpEdittime = 0

logLocation = '/home/bladeque/bot/botlog'

def getWikiSoup(url, params=None):
	print "[GETPOST]" + wikiURL + url
	return BeautifulSoup(wikiOpener.open(wikiURL + url, params).read())

def login():
	print "[Action] Logging in..."
	
	#submit once to get login token
	params = urllib.urlencode({'username': botUserName, 'password': botPassword})
	soup = getWikiSoup('/wiki/Special:UserLogin', params)
	loginToken = soup.find_all(attrs={'name':'loginToken'})[1].attrs['value']

	#login with correct token
	params = urllib.urlencode({'username':botUserName,'password':botPassword, 'loginToken':loginToken, 'keeploggedin':1})
	getWikiSoup('/wiki/Special:UserLogin', params)
	if checkLoginStatus(): 
		print '[Result] Successfully logged in.'

def checkLoginStatus():
	soup = getWikiSoup("")
	return len(soup.find_all('a', accesskey='.')) > 0



def scrapePlayerData(): 
	opener = urllib2.build_opener(urllib2.HTTPHandler())
	r = opener.open('http://www.amishsmp.net/player.php?playerName=p4r4digm')
	return r.read()


def getPlayerInfoUsers():
	print "[Action] Determining number of players using the info pane."
	soup = getWikiSoup("/wiki/Category:Uses_Player_Info")
	playerTags = soup.find_all('div', attrs={'class':'mw-content-ltr'})[0].find_all('a')
	newPlayerList = []
	
	for tag in playerTags:
		str = tag.attrs['title']
		if str.count('User:') > 0:
			str = str.replace('User:', '').lower()
			newPlayerList.append(str)
	
	print "[Result] %s users found." %(len(newPlayerList))
	return newPlayerList


class Player:
	def __init__(self):
		self.data = []



def getPlayerList():
	nameList = getPlayerInfoUsers()

	print "[Action] Retrieving Character List..."
	page = scrapePlayerData().lower()
	
	players = {}

	for name in nameList:
		pos = page.rfind(name)
		if pos > -1:
			start = page.rfind('<tr class=\"player-list-row\">', 0, pos)
			end = page.find('</tr>', pos)
			
			str = (page[start:end]+'</tr>').replace('td>', 'div>')
			tag = BeautifulSoup(str)

			player = Player()
		
			player.karma = tag.find_all('div')[0].string
			player.name = tag.find_all('div')[1].string
			player.lastseen = tag.find_all('div')[2].string
			player.timeplayed = tag.find_all('div')[3].string
			player.lastpvp = tag.find_all('div')[4].string
			player.reviveon = tag.find_all('div')[5].string

			players[player.name] = player

	return players



def submit(str):
	print "[Action] Editing Template Page..."
	params = urllib.urlencode({'wpMinoredit':'1', 'wpTextbox1':str}) 
	soup = getWikiSoup('/wiki/Template:PlayerInfo?action=submit', params)
	
	editToken = soup.find_all('input', attrs={'name':'wpEditToken'})[0].attrs['value']
	autoSummary = soup.find_all('input', attrs={'name':'wpAutoSummary'})[0].attrs['value']

	wpEdittime = int(time.strftime('%Y%m%d%H%M%S', time.localtime()))
	params = urllib.urlencode({ \
			'wpStarttime':wpStarttime, \
			'wpEdittime':wpEdittime, \
			'wpMinoredit':'1', \
			'wpTextbox1':str, \
			'wpEditToken':editToken, \
			'wpAutoSummary':autoSummary})

	soup = getWikiSoup('/wiki/Template:PlayerInfo?action=submit', params)

	print '[Result] Wiki changes submitted.'
	return soup;

def generateWikiPlayerEntry(player):

	return ("{{#ifeq:{{{user}}}|%(name)s|{{infobox|Box title={{{user}}}|"
		"image{{#if:{{{image|}}}||NULL}}={{{image}}}|"
		"caption{{#if:{{{caption|}}}||NULL}}={{{caption}}}|"
		"Row 1 title=Karma|Row 1 info=%(karma)s|"
		"Row 2 title=Time Played|Row 2 info=%(timeplayed)s|"
		"Row 3 title=Last Seen|Row 3 info=%(lastseen)s|"
		"Row 4 title=Last PvP Engagement|Row 4 info=%(pvp)s|"
		"Row 5 title=Revives In|Row 5 info=%(revive)s|"
		"Row 6 title{{#if:{{{showDeaths|}}}||NULL}}=Deaths|"
		"Row 6 info{{#if:{{{showDeaths|}}}||NULL}}=%(deaths)s|"
		"Row {{#expr: 6+{{#ifeq:{{{showDeaths|}}}|Yes|1|0}}}} title{{#if:{{{showKills|}}}||NULL}}=Kills|"
		"Row {{#expr: 6+{{#ifeq:{{{showDeaths|}}}|Yes|1|0}}}} info{{#if:{{{showKills|}}}||NULL}}=%(kills)s|"
		"Row {{#expr: 6+{{#ifeq:{{{showDeaths|}}}|Yes|1|0}}+{{#ifeq:{{{showKills|}}}|Yes|1|0}}}} title=Last Updated|"
		"Row {{#expr: 6+{{#ifeq:{{{showDeaths|}}}|Yes|1|0}}+{{#ifeq:{{{showKills|}}}|Yes|1|0}}}} info=[[Template:PlayerInfo|%(updated)s]]}}|}}") \
		% \
		{'name': player.name, \
		'karma': player.karma, \
		'timeplayed': player.timeplayed, \
		'lastseen':player.lastseen, \
		'pvp':player.lastpvp, \
		'revive':player.reviveon, \
		'deaths':'Coming Soon', \
		'kills':'Coming Soon', \
		'updated':time.strftime('%Y%m%d%H%M%S', time.localtime())}


def generateWikiPage():
	players = getPlayerList()

	print "[Action] Generating Wiki Page..."
	str = ("This template makes it easy to add a useful info pane to your userpage.  " 
		"It is automatically updated by a bot that scrapes player information from "
		"the amishsmp website and formats it into a customizable template.\n\n"
		"The bot and page are both managed by [[User:P4r4digm|P4r4digm]].  Please direct any questions to p4r4digm@gmail.com.\n\n"
		"Once you add the template, it will not populate until the next time the bot runs.  This is to cut down on the "
		"amount of data being pulled from the site.  There are close to nine thousand users so only users whose names appear in "
		"the \"Uses Player Info\" Category will have their data migrated to this template.\n\n" 
		"You can update the bot yourself!  By clicking here.\n\n"
		"==Usage==\n"
		"The template is used in the following way:\n\n"
		"{{(}}{{(}}PlayerInfo{{!}}<br/>\n"
		"user = \'\'Username (Must match your wiki profile name)\'\' {{!}}<br/>\n"
		"image = \'\'Optional. Example: Image:AirClan.png\'\' {{!}}<br/>\n"
		"caption = \'\'Optional\'\' {{!}}<br/>\n"
		"showKills = \'\'Optional, Yes or No (case-sensitive)\'\' {{!}}<br/>\n"
		"showDeaths = \'\'Optional, Yes or No (case-sensitive)\'\' <br/>\n"
		"{{)}}{{)}}\n\n"
		"==Example==\n"
		"{{PlayerInfo|\n"
		"user=p4r4digm|\n"
		"caption=This is a caption!|\n"
		"image=Image:AirClan.png|\n"
		"showKills=Yes}}\n\n")
	
	
	str += "<onlyinclude>"
	for player in players.values():
		str  += generateWikiPlayerEntry(player)
	
	str += "[[Category:Uses Player Info]]"
	str += "</onlyinclude>"
	return str
	
class printWrapper:
	def __init__(self):
		self.content = []
	def write(self, string):
		fobj = open(logLocation, 'a')
		fobj.write(string)
		fobj.close()
	def flush(self):
		pass

def run():
	wpStarttime = int(time.strftime('%Y%m%d%H%M%S', time.localtime()))

	fobj = printWrapper()
	sys.stdout = fobj

	
	f = open(logLocation, 'r')
	lines = f.readlines()
	f.close()

	if lines[len(lines)-1].count('[Done]') == 0:
		print '[ERROR] Attempted execution.  Bot is already running.'
		return

	print '[Action] Checking Login Status...'
	if checkLoginStatus():
		print '[Result] Already logged in.'
	else:
		login()
	
	str = generateWikiPage()
	submit(str)
	print "[Result] Process Complete"
	print "[Done] Last ran " + time.strftime("%A, %B %d at %I:%M::%S %p %Z", time.localtime())


if __name__ == "__main__":
	run()
