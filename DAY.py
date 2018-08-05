# -*- coding: utf-8 -*-

from LineAPI.linepy import *
from gtts import gTTS
from bs4 import BeautifulSoup
from datetime import datetime
from googletrans import Translator
import ast, codecs, json, os, pytz, re, random, requests, sys, time, urllib.parse

listApp = ["CHROMEOS", "DESKTOPWIN", "DESKTOPMAC", "IOSIPAD", "WIN10"]
try:
	for app in listApp:
		try:
			try:
				with open("DAY.txt", "r") as token:
					authToken = token.read()
					if not authToken:
						client = LINE()
						with open("DAY.txt","w") as token:
							token.write(client.authToken)
						continue
					client = LINE(authToken, speedThrift=False, appName="{}\t2.1.5\DEDESHOP\t11.2.5".format(app))
				break
			except Exception as error:
				print(error)
				if error == "REVOKE":
					exit()
				elif "auth" in error:
					continue
				else:
					exit()
		except Exception as error:
			print(error)
except Exception as error:
	print(error)
with open("DAY.txt", "w") as token:
    token.write(str(client.authToken))
    print ("\n[ ALHAMDULILLAH SUKSES LOG IN ]\n[ DEDE SHOP CENTRE ]\n\n[ BOT START ]")
clientMid = client.profile.mid
clientStart = time.time()
clientPoll = OEPoll(client)

languageOpen = codecs.open("language.json","r","utf-8")
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("setting.json","r","utf-8")
unsendOpen = codecs.open("unsend.json","r","utf-8")

language = json.load(languageOpen)
read = json.load(readOpen)
settings = json.load(settingsOpen)
unsend = json.load(unsendOpen)

def restartBot():
	print ("[ INFO ] BOT RESTARTED")
	python = sys.executable
	os.execl(python, python, *sys.argv)

def logError(text):
    client.log("[ ERROR ] {}".format(str(text)))
    tz = pytz.timezone("Asia/Jakarta")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow,"(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]: hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k): bln = bulan[k-1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
    with open("errorLog.txt","a") as error:
        error.write("\n[{}] {}".format(str(time), text))

def timeChange(secs):
	mins, secs = divmod(secs,60)
	hours, mins = divmod(mins,60)
	days, hours = divmod(hours,24)
	weeks, days = divmod(days,7)
	months, weeks = divmod(weeks,4)
	text = ""
	if months != 0: text += "%02d Bulan" % (months)
	if weeks != 0: text += " %02d Minggu" % (weeks)
	if days != 0: text += " %02d Hari" % (days)
	if hours !=  0: text +=  " %02d Jam" % (hours)
	if mins != 0: text += " %02d Menit" % (mins)
	if secs != 0: text += " %02d Detik" % (secs)
	if text[0] == " ":
		text = text[1:]
	return text

def command(text):
	pesan = text.lower()
	if settings["setKey"] == True:
		if pesan.startswith(settings["keyCommand"]):
			cmd = pesan.replace(settings["keyCommand"],"")
		else:
			cmd = "Undefined command"
	else:
		cmd = text.lower()
	return cmd

def backupData():
	try:
		backup = read
		f = codecs.open('read.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		backup = settings
		f = codecs.open('setting.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		backup = unsend
		f = codecs.open('unsend.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		return True
	except Exception as error:
		logError(error)
		return False

def menuPub():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
		menuPub=   "╭━━━━━━━━━━━━━━━━╮" + "\n" + \
                "┃ DEDE SHOP PUBLIC BOT" + "\n" + \
                "┃           PUBLIC MENU" + "\n" + \
                "┣•━━━━━━━━━━━━━━━━" + "\n" + \
                "┣│✪│•" + key + "Me" + "\n" + \
                "┣│✪│•" + key + "MyMid" + "\n" + \
                "┣│✪│•" + key + "MyName" + "\n" + \
                "┣│✪│•" + key + "MyBio" + "\n" + \
                "┣│✪│•" + key + "MyPic" + "\n" + \
                "┣│✪│•" + key + "MyVid" + "\n" + \
                "┣│✪│•" + key + "MyCover" + "\n" + \
                "┣│✪│•" + key + "MyProfile" + "\n" + \
                "┣│✪│•" + key + "GetName (Tag)" + "\n" + \
                "┣│✪│•" + key + "GetBio (Tag)" + "\n" + \
                "┣│✪│•" + key + "GetPic (Tag)" + "\n" + \
                "┣│✪│•" + key + "GetVid (Tag)" + "\n" + \
                "┣│✪│•" + key + "GetCover (Tag)" + "\n" + \
                "┣│✪│•" + key + "/info" + "\n" + \
                "┣│✪│•" + key + "InstaInfo_Name" + "\n" + \
                "┣│✪│•" + key + "InstaStory_Name" + "\n" + \
                "┣│✪│•" + key + "Gambar_Text" + "\n" + \
                "┣│✪│•" + key + "Play (Song/Singer)" + "\n" + \
                "┣│✪│•" + key + "Translator" + "\n" + \
                "┣│✪│•" + key + "Cst On/Off" + "\n" + \
                "┣│✪│•" + key + "Cctv On/Off" + "\n" + \
                "┣│✪│•" + key + "Reader" + "\n" + \
                "┣│✪│•" + key + "Ginfo" + "\n" + \
                "┣│✪│•" + key + "GName" + "\n" + \
                "┣│✪│•" + key + "info On/Off" + "\n" + \
                "┣│✪│•" + key + "GPicture" + "\n" + \
                "┣│✪│•" + key + "Tag Name" + "\n" + \
                "┣│✪│•" + key + "Pendinglist" + "\n" + \
	            "┣•━━━━━━━━━━━━━━━━" + "\n" + \
                "┃    DEDE SHOP CENTRE™" + "\n" + \
                "┃       CREATOR : DEDE" + "\n" + \
                "╰━━━━━━━━━━━━━━━━╯"
	return menuPub
	
def menuHelp():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
		menuHelp =   "╭━━━━━━━━━━━━━━━━╮" + "\n" + \
                "┃   SELFBOT MAIN MENU" + "\n" + \
                "┣•━━━━━━━━━━━━━━━━" + "\n" + \
                "┣│✪│•" + key + "Self\n" + \
                "┣│✪│•" + key + "Setting\n" + \
                "┣│✪│•" + key + "Group\n" + \
                "┣│✪│•" + key + "Media\n" + \
		        "┣│✪│•" + key + "Translate\n" + \
		        "┣•━━━━━━━━━━━━━━━━" + "\n" + \
                "┃       DOTS AUTO BOT" + "\n" + \
                "┃COPYRIGHT : DEDE SHOP" + "\n" + \
                "╰━━━━━━━━━━━━━━━━╯"
	return menuHelp
	
def menuSelf():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
		menuSelf =   "╭━━━━━━━━━━━━━━━━╮" + "\n" + \
                "┃     SELFBOT SERVICE" + "\n" + \
                "┣•━━━━━━━━━━━━━━━━" + "\n" + \
                "┣│✪│•" + key + "Turn off" + "\n" + \
		        "┣│✪│•" + key + "Restart" + "\n" + \
		        "┣│✪│•" + key + "Runtime" + "\n" + \
		        "┣│✪│•" + key + "Speed" + "\n" + \
		        "┣│✪│•" + key + "Status" + "\n" + \
		        "┣│✪│•" + key + "Cpp" + "\n" + \
		        "┣│✪│•" + key + "CName:_Text" + "\n" + \
                "┣│✪│•" + key + "CBio:_Text" + "\n" + \
                "┣│✪│•" + key + "Me" + "\n" + \
                "┣│✪│•" + key + "MyMid" + "\n" + \
                "┣│✪│•" + key + "MyName" + "\n" + \
                "┣│✪│•" + key + "MyBio" + "\n" + \
                "┣│✪│•" + key + "MyPic" + "\n" + \
                "┣│✪│•" + key + "MyVid" + "\n" + \
                "┣│✪│•" + key + "MyCover" + "\n" + \
                "┣│✪│•" + key + "MyProfile" + "\n" + \
                "┣│✪│•" + key + "GetMid_Tag" + "\n" + \
                "┣│✪│•" + key + "GetName_Tag" + "\n" + \
                "┣│✪│•" + key + "GetBio_Tag" + "\n" + \
                "┣│✪│•" + key + "GetPic_Tag" + "\n" + \
                "┣│✪│•" + key + "GetVid_Tag" + "\n" + \
                "┣│✪│•" + key + "GetCover_Tag" + "\n" + \
                "┣│✪│•" + key + "Clone_Tag" + "\n" + \
                "┣│✪│•" + key + "Restore" + "\n" + \
                "┣│✪│•" + key + "Mybackup" + "\n" + \
                "┣│✪│•" + key + "Myfriend" + "\n" + \
                "┣│✪│•" + key + "Steal_Nomor" + "\n" + \
                "┣│✪│•" + key + "/info" + "\n" + \
                "┣│✪│•" + key + "BlockList" + "\n" + \
                "┣│✪│•" + key + "Fbc" + "\n" + \
                "┣│✪│•" + key + "Bcg:_Text" + "\n" + \
                "┣│✪│•" + key + "Mimic_On/Off" + "\n" + \
                "┣│✪│•" + key + "MicList" + "\n" + \
                "┣│✪│•" + key + "MicAdd_Tag" + "\n" + \
                "┣│✪│•" + key + "Micdel_Tag" + "\n" + \
                "┣•━━━━━━━━━━━━━━━━" + "\n" + \
                "┃       DOTS AUTO BOT" + "\n" + \
                "╰━━━━━━━━━━━━━━━━╯"
	return menuSelf
	
def menuGroup():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
		menuGroup =   "╭━━━━━━━━━━━━━━━━╮" + "\n" + \
                "┃       GROUP SERVICE" + "\n" + \
                "┣•━━━━━━━━━━━━━━━━" + "\n" + \
                "┣│✪│•" + key + "CGName:_Text" + "\n" + \
                "┣│✪│•" + key + "CGPicture" + "\n" + \
                "┣│✪│•" + key + "GCreator" + "\n" + \
                "┣│✪│•" + key + "GID" + "\n" + \
                "┣│✪│•" + key + "GName" + "\n" + \
                "┣│✪│•" + key + "GPicture" + "\n" + \
                "┣│✪│•" + key + "OQR" + "\n" + \
                "┣│✪│•" + key + "CQR" + "\n" + \
                "┣│✪│•" + key + "GList" + "\n" + \
                "┣│✪│•" + key +  "Boss" + "\n" + \
                "┣│✪│•" + key +  "Cctv_On/Off" + "\n" + \
                "┣│✪│•" + key +  "Reader" + "\n" + \
                "┣│✪│•" + key + "Tag Name" + "\n" + \
                "┣│✪│•" + key + "Pendinglist" + "\n" + \
                "┣│✪│•" + key + "GInfo" + "\n" + \
                "┣•━━━━━━━━━━━━━━━━" + "\n" + \
                "┃       DOTS AUTO BOT" + "\n" + \
                "╰━━━━━━━━━━━━━━━━╯"
	return menuGroup
	
def menuSetting():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
		menuSetting =   "╭━━━━━━━━━━━━━━━━╮" + "\n" + \
                "┃      SETTING SERVICE" + "\n" + \
                "┣•━━━━━━━━━━━━━━━━" + "\n" + \
                "┣│✪│SetKey_On/Off" + "\n" + \
                "┣│✪│•" + key + "AutoAdd_On/Off" + "\n" + \
                "┣│✪│•" + key + "AutoJoin_On/Off" + "\n" + \
                "┣│✪│•" + key + "JoinTicket_On/Off" + "\n" + \
                "┣│✪│•" + key + "AutoRead_On/Off" + "\n" + \
                "┣│✪│•" + key + "AutoRespon_On/Off" + "\n" + \
                "┣│✪│•" + key + "Info_On/Off" + "\n" + \
                "┣│✪│•" + key + "TL_On/Off" + "\n" + \
                "┣│✪│•" + key + "Cst_On/Off" + "\n" + \
                "┣│✪│•" + key + "SKey:_Text" + "\n" + \
                "┣│✪│•" + key + "SMess:_Text" + "\n" + \
                "┣│✪│•" + key + "SRespon:_Text" + "\n" + \
                "┣│✪│•" + key + "SJoin:_Text" + "\n" + \
                "┣•━━━━━━━━━━━━━━━━" + "\n" + \
                "┃       DOTS AUTO BOT" + "\n" + \
                "╰━━━━━━━━━━━━━━━━╯"
	return menuSetting
	
def menuMedia():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
		menuMedia =    "╭━━━━━━━━━━━━━━━━╮" + "\n" + \
                "┃           FUN SERVICE" + "\n" + \
                "┣•━━━━━━━━━━━━━━━━" + "\n" + \
                "┣│✪│•" + key + "InstaInfo_Name" + "\n" + \
                "┣│✪│•" + key + "InstaStory_Name" + "\n" + \
                "┣│✪│•" + key + "Quotes" + "\n" + \
                "┣│✪│•" + key + "Gambar_Text" + "\n" + \
                "┣│✪│•" + key + "Play_Text" + "\n" + \
                "┣│✪│•" + key + "Lyric_Text" + "\n" + \
                "┣│✪│•" + key + "Yvideo_Text" + "\n" + \
	            "┣•━━━━━━━━━━━━━━━━" + "\n" + \
                "┃       DOTS AUTO BOT" + "\n" + \
                "╰━━━━━━━━━━━━━━━━╯"
	return menuMedia
	
def menuTTS():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuTTS =	"╭━━━━━━━━━━━━━━━━╮" + "\n" + \
	            "┃      TEXT TO SPEECH" + "\n" + \
                "┣•━━━━━━━━━━━━━━━━" + "\n" + \
				"┣│✪│•" + + key + "Say-af : Afrikaans" + "\n" + \
				"┣│✪│•" + + key + "Say-sq : Albanian" + "\n" + \
				"┣│✪│•" + + key + "Say-ar : Arabic" + "\n" + \
				"┣│✪│•" + + key + "Say-hy : Armenian" + "\n" + \
				"┣│✪│•" + + key + "Say-bn : Bengali" + "\n" + \
				"┣│✪│•" + + key + "Say-ca : Catalan" + "\n" + \
				"┣│✪│•" + + key + "Say-zh : Chinese" + "\n" + \
				"┣│✪│•" + + key + "Say-zh-cn : Chinese (Mandarin/China)" + "\n" + \
				"┣│✪│•" + + key + "Say-zh-tw : Chinese (Mandarin/Taiwan)" + "\n" + \
				"┣│✪│•" + + key + "Say-zh-yue : Chinese (Cantonese)" + "\n" + \
				"┣│✪│•" + + key + "Say-hr : Croatian" + "\n" + \
				"┣│✪│•" + + key + "Say-cs : Czech" + "\n" + \
				"┣│✪│•" + + key + "Say-da : Danish" + "\n" + \
				"┣│✪│•" + + key + "Say-nl : Dutch" + "\n" + \
				"┣│✪│•" + + key + "Say-en : English" + "\n" + \
				"┣│✪│•" + + key + "Say-en-au : English (Australia)" + "\n" + \
				"┣│✪│•" + + key + "Say-en-uk : English (United Kingdom)" + "\n" + \
				"┣│✪│•" + + key + "Say-en-us : English (United States)" + "\n" + \
				"┣│✪│•" + + key + "Say-eo : Esperanto" + "\n" + \
				"┣│✪│•" + + key + "Say-fi : Finnish" + "\n" + \
				"┣│✪│•" + + key + "Say-fr : French" + "\n" + \
				"┣│✪│•" + + key + "Say-de : German" + "\n" + \
				"┣│✪│•" + + key + "Say-el : Greek" + "\n" + \
				"┣│✪│•" + + key + "Say-hi : Hindi" + "\n" + \
				"┣│✪│•" + + key + "Say-hu : Hungarian" + "\n" + \
				"┣│✪│•" + + key + "Say-is : Icelandic" + "\n" + \
				"┣│✪│•" + + key + "Say-id : Indonesian" + "\n" + \
				"┣│✪│•" + + key + "Say-it : Italian" + "\n" + \
				"┣│✪│•" + + key + "Say-ja : Japanese" + "\n" + \
				"┣│✪│•" + + key + "Say-km : Khmer (Cambodian)" + "\n" + \
				"┣│✪│•" + + key + "Say-ko : Korean" + "\n" + \
				"┣│✪│•" + + key + "Say-la : Latin" + "\n" + \
				"┣│✪│•" + + key + "Say-lv : Latvian" + "\n" + \
				"┣│✪│•" + + key + "Say-mk : Macedonian" + "\n" + \
				"┣│✪│•" + + key + "Say-no : Norwegian" + "\n" + \
				"┣│✪│•" + + key + "Say-pl : Polish" + "\n" + \
				"┣│✪│•" + + key + "Say-pt : Portuguese" + "\n" + \
				"┣│✪│•" + + key + "Say-ro : Romanian" + "\n" + \
				"┣│✪│•" + + key + "Say-ru : Russian" + "\n" + \
				"┣│✪│•" + + key + "Say-sr : Serbian" + "\n" + \
				"┣│✪│•" + + key + "Say-si : Sinhala" + "\n" + \
				"┣│✪│•" + + key + "Say-sk : Slovak" + "\n" + \
				"┣│✪│•" + + key + "Say-es : Spanish" + "\n" + \
				"┣│✪│•" + + key + "Say-es-es : Spanish (Spain)" + "\n" + \
				"┣│✪│•" + + key + "Say-es-us : Spanish (United States)" + "\n" + \
				"┣│✪│•" + + key + "Say-sw : Swahili" + "\n" + \
				"┣│✪│•" + + key + "Say-sv : Swedish" + "\n" + \
				"┣│✪│•" + + key + "Say-ta : Tamil" + "\n" + \
				"┣│✪│•" + + key + "Say-th : Thai" + "\n" + \
				"┣│✪│•" + + key + "Say-tr : Turkish" + "\n" + \
				"┣│✪│•" + + key + "Say-uk : Ukrainian" + "\n" + \
				"┣│✪│•" + + key + "Say-vi : Vietnamese" + "\n" + \
				"┣│✪│•" + + key + "Say-cy : Welsh" + "\n" + \
				"┣•━━━━━━━━━━━━━━━━" + "\n" + \
                "┃       DOTS AUTO BOT" + "\n" + \
                "╰━━━━━━━━━━━━━━━━╯"
	return menuTTS

def menuTranslate():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuTranslate =	"╭━━━━━━━━━━━━━━━━╮" + "\n" + \
	                   "┃      T R A N S L A T O R" + "\n" + \
                       "┣•━━━━━━━━━━━━━━━━" + "\n" + \
                       "┣│✪│•Tr-af : afrikaans" + "\n" + \
                       "┣│✪│•Tr-sq : albanian" + "\n" + \
                       "┣│✪│•Tr-am : amharic" + "\n" + \
                       "┣│✪│•Tr-ar : arabic" + "\n" + \
                       "┣│✪│•Tr-hy : armenian" + "\n" + \
                       "┣│✪│•Tr-az : azerbaijani" + "\n" + \
                       "┣│✪│•Tr-eu : basque" + "\n" + \
                       "┣│✪│•Tr-be : belarusian" + "\n" + \
                       "┣│✪│•Tr-bn : bengali" + "\n" + \
                       "┣│✪│•Tr-bs : bosnian" + "\n" + \
                       "┣│✪│•Tr-bg : bulgarian" + "\n" + \
                       "┣│✪│•Tr-ca : catalan" + "\n" + \
                       "┣│✪│•Tr-ceb : cebuano" + "\n" + \
                       "┣│✪│•Tr-ny : chichewa" + "\n" + \
                       "┣│✪│•Tr-zh-cn : chinese (simplified)" + "\n" + \
                       "┣│✪│•Tr-zh-tw : chinese (traditional)" + "\n" + \
                       "┣│✪│•Tr-co : corsican" + "\n" + \
                       "┣│✪│•Tr-hr : croatian" + "\n" + \
                       "┣│✪│•Tr-cs : czech" + "\n" + \
                       "┣│✪│•Tr-da : danish" + "\n" + \
                       "┣│✪│•Tr-nl : dutch" + "\n" + \
                       "┣│✪│•Tr-en : english" + "\n" + \
                       "┣│✪│•Tr-eo : esperanto" + "\n" + \
                       "┣│✪│•Tr-et : estonian" + "\n" + \
                       "┣│✪│•Tr-tl : filipino" + "\n" + \
                       "┣│✪│•Tr-fi : finnish" + "\n" + \
                       "┣│✪│•Tr-fr : french" + "\n" + \
                       "┣│✪│•Tr-fy : frisian" + "\n" + \
                       "┣│✪│•Tr-gl : galician" + "\n" + \
                       "┣│✪│•Tr-ka : georgian" + "\n" + \
                       "┣│✪│•Tr-de : german" + "\n" + \
                       "┣│✪│•Tr-el : greek" + "\n" + \
                       "┣│✪│•Tr-gu : gujarati" + "\n" + \
                       "┣│✪│•Tr-ht : haitian creole" + "\n" + \
                       "┣│✪│•Tr-ha : hausa" + "\n" + \
                       "┣│✪│•Tr-haw : hawaiian" + "\n" + \
                       "┣│✪│•Tr-iw : hebrew" + "\n" + \
                       "┣│✪│•Tr-hi : hindi" + "\n" + \
                       "┣│✪│•Tr-hmn : hmong" + "\n" + \
                       "┣│✪│•Tr-hu : hungarian" + "\n" + \
                       "┣│✪│•Tr-is : icelandic" + "\n" + \
                       "┣│✪│•Tr-ig : igbo" + "\n" + \
                       "┣│✪│•Tr-id : indonesian" + "\n" + \
                       "┣│✪│•Tr-ga : irish" + "\n" + \
                       "┣│✪│•Tr-it : italian" + "\n" + \
                       "┣│✪│•Tr-ja : japanese" + "\n" + \
                       "┣│✪│•Tr-jw : javanese" + "\n" + \
                       "┣│✪│•Tr-kn : kannada" + "\n" + \
                       "┣│✪│•Tr-kk : kazakh" + "\n" + \
                       "┣│✪│•Tr-km : khmer" + "\n" + \
                       "┣│✪│•Tr-ko : korean" + "\n" + \
                       "┣│✪│•Tr-ku : kurdish (kurmanji)" + "\n" + \
                       "┣│✪│•Tr-ky : kyrgyz" + "\n" + \
                       "┣│✪│•Tr-lo : lao" + "\n" + \
                       "┣│✪│•Tr-la : latin" + "\n" + \
                       "┣│✪│•Tr-lv : latvian" + "\n" + \
                       "┣│✪│•Tr-lt : lithuanian" + "\n" + \
                       "┣│✪│•Tr-lb : luxembourgish" + "\n" + \
                       "┣│✪│•Tr-mk : macedonian" + "\n" + \
                       "┣│✪│•Tr-mg : malagasy" + "\n" + \
                       "┣│✪│•Tr-ms : malay" + "\n" + \
                       "┣│✪│•Tr-ml : malayalam" + "\n" + \
                       "┣│✪│•Tr-mt : maltese" + "\n" + \
                       "┣│✪│•Tr-mi : maori" + "\n" + \
                       "┣│✪│•Tr-mr : marathi" + "\n" + \
                       "┣│✪│•Tr-mn : mongolian" + "\n" + \
                       "┣│✪│•Tr-my : myanmar (burmese)" + "\n" + \
                       "┣│✪│•Tr-ne : nepali" + "\n" + \
                       "┣│✪│•Tr-no : norwegian" + "\n" + \
                       "┣│✪│•Tr-ps : pashto" + "\n" + \
                       "┣│✪│•Tr-fa : persian" + "\n" + \
                       "┣│✪│•Tr-pl : polish" + "\n" + \
                       "┣│✪│•Tr-pt : portuguese" + "\n" + \
                       "┣│✪│•Tr-pa : punjabi" + "\n" + \
                       "┣│✪│•Tr-ro : romanian" + "\n" + \
                       "┣│✪│•Tr-ru : russian" + "\n" + \
                       "┣│✪│•Tr-sm : samoan" + "\n" + \
                       "┣│✪│•Tr-gd : scots gaelic" + "\n" + \
                       "┣│✪│•Tr-sr : serbian" + "\n" + \
                       "┣│✪│•Tr-st : sesotho" + "\n" + \
                       "┣│✪│•Tr-sn : shona" + "\n" + \
                       "┣│✪│•Tr-sd : sindhi" + "\n" + \
                       "┣│✪│•Tr-si : sinhala" + "\n" + \
                       "┣│✪│•Tr-sk : slovak" + "\n" + \
                       "┣│✪│•Tr-sl : slovenian" + "\n" + \
                       "┣│✪│•Tr-so : somali" + "\n" + \
                       "┣│✪│•Tr-es : spanish" + "\n" + \
                       "┣│✪│•Tr-su : sundanese" + "\n" + \
                       "┣│✪│•Tr-sw : swahili" + "\n" + \
                       "┣│✪│•Tr-sv : swedish" + "\n" + \
                       "┣│✪│•Tr-tg : tajik" + "\n" + \
                       "┣│✪│•Tr-ta : tamil" + "\n" + \
                       "┣│✪│•Tr-te : telugu" + "\n" + \
                       "┣│✪│•Tr-th : thai" + "\n" + \
                       "┣│✪│•Tr-tr : turkish" + "\n" + \
                       "┣│✪│•Tr-uk : ukrainian" + "\n" + \
                       "┣│✪│•Tr-ur : urdu" + "\n" + \
                       "┣│✪│•Tr-uz : uzbek" + "\n" + \
                       "┣│✪│•Tr-vi : vietnamese" + "\n" + \
                       "┣│✪│•Tr-cy : welsh" + "\n" + \
                       "┣│✪│•Tr-xh : xhosa" + "\n" + \
                       "┣│✪│•Tr-yi : yiddish" + "\n" + \
                       "┣│✪│•Tr-yo : yoruba" + "\n" + \
                       "┣│✪│•Tr-zu : zulu" + "\n" + \
                       "┣│✪│•Tr-fil : Filipino" + "\n" + \
                       "┣│✪│•Tr-he : Hebrew" + "\n" + \
                       "┣•━━━━━━━━━━━━━━━━" + "\n" + \
                       "┃       DOTS AUTO BOT" + "\n" + \
                       "╰━━━━━━━━━━━━━━━━╯"
	return menuTranslate

def clientBot(op):
	try:
		if op.type == 0:
			print ("[ 0 ] END OF OPERATION")
			return

		if op.type == 5:
			print ("[ 5 ] NOTIFIED ADD CONTACT")
			if settings["autoAdd"] == True:
				client.findAndAddContactsByMid(op.param1)
			client.sendMention(op.param1, settings["autoAddMessage"], [op.param1])

		if op.type == 13:
			print ("[ 13 ] NOTIFIED INVITE INTO GROUP")
			if settings["autoJoin"] and clientMid in op.param3:
				client.acceptGroupInvitation(op.param1)
				client.sendMention(op.param1, settings["autoJoinMessage"], [op.param2])

		if op.type == 25:
			try:
				print("[ 25 ] SEND MESSAGE")
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				cmd = command(text)
				setKey = settings["keyCommand"].title()
				if settings["setKey"] == False:
					setKey = ''
				if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
					if msg.toType == 0:
						if sender != client.profile.mid:
							to = sender
						else:
							to = receiver
					elif msg.toType == 1:
						to = receiver
					elif msg.toType == 2:
						to = receiver
					if msg.contentType == 0:
						if cmd == "turn off":
							client.sendMessage(to, "➧ Bot Di Nonaktifkan")
							sys.exit("[ INFO ] BOT SHUTDOWN")
							return
						elif cmd == "restart":
							client.sendMessage(to, "➧ Restarting Dots System\n➧ Tunggu 30 Detik")
							restartBot()
						elif cmd == "speed":
							start = time.time()
							client.sendMessage(to, "➧ Checking Dots Speed")
							elapsed_time = time.time() - start
							client.sendMessage(to, "➧ Speed Result : \n   {} Detik".format(str(elapsed_time)))
						elif cmd == "runtime":
							timeNow = time.time()
							runtime = timeNow - clientStart
							runtime = timeChange(runtime)
							client.sendMessage(to, "➧ Status : Aktif\n➧ Sistem : Normal\n➧ Activ Time :  \n   {}".format(str(runtime)))
						elif cmd.startswith("setkey: "):
							sep = text.split(" ")
							key = text.replace(sep[0] + " ","")
							if " " in key:
								client.sendMessage(to, "➧ Jangan menggunakan spasi")
							else:
								settings["keyCommand"] = str(key).lower()
								client.sendMessage(to, "➧ Success Changing Set Ket To : \n   {} ".format(str(key).lower()))
						elif cmd == "help":
							helpMessage = menuHelp()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "https://timeline.line.me/post/_dZNo9tm3E3PH0dURm6N9Rf_pYxmFJO2uASn_y7Q/1153217318709030407"
							client.sendFooter(to, helpMessage, icon, name, link)
						elif cmd == "self":
							helpSelf = menuSelf()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "https://timeline.line.me/post/_dZNo9tm3E3PH0dURm6N9Rf_pYxmFJO2uASn_y7Q/1153217318709030407"
							client.sendFooter(to, helpSelf, icon, name, link)
						elif cmd == "group":
							helpGroup = menuGroup()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "https://timeline.line.me/post/_dZNo9tm3E3PH0dURm6N9Rf_pYxmFJO2uASn_y7Q/1153217318709030407"
							client.sendFooter(to, helpGroup, icon, name, link)
						elif cmd == "setting":
							helpSetting = menuSetting()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "https://timeline.line.me/post/_dZNo9tm3E3PH0dURm6N9Rf_pYxmFJO2uASn_y7Q/1153217318709030407"
							client.sendFooter(to, helpSetting, icon, name, link)
						elif cmd == "media":
							helpMedia = menuMedia()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "https://timeline.line.me/post/_dZNo9tm3E3PH0dURm6N9Rf_pYxmFJO2uASn_y7Q/1153217318709030407"
							client.sendFooter(to, helpMedia, icon, name, link)
						elif cmd == "tts":
							helpTTS = menuTTS()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "https://timeline.line.me/post/_dZNo9tm3E3PH0dURm6N9Rf_pYxmFJO2uASn_y7Q/1153217318709030407"
							client.sendFooter(to, helpTTS, icon, name, link)
						elif cmd == "translate":
							helpTranslate = menuTranslate()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "https://timeline.line.me/post/_dZNo9tm3E3PH0dURm6N9Rf_pYxmFJO2uASn_y7Q/1153217318709030407"
							client.sendFooter(to, helpTranslate, icon, name, link)
						
						elif cmd == "status":
							try:
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃       SELFBOT STATUS\n┣•━━━━━━━━━━━━━━━━"
								if settings["autoAdd"] == True: ret_ += "\n┣• Auto Add : ON"
								else: ret_ += "\n┣• Auto Add : OFF"
								if settings["autoJoin"] == True: ret_ += "\n┣• Auto Join : ON"
								else: ret_ += "\n┣• Auto Join : OFF"
								if settings["autoJoin"] == True: ret_ += "\n┣• Join Ticket : ON"
								else: ret_ += "\n┣• Join Ticket : OFF"
								if settings["autoRead"] == True: ret_ += "\n┣• Auto Read : ON"
								else: ret_ += "\n┣• Auto Read : OFF"
								if settings["autoRespon"] == True: ret_ += "\n┣• Auto Respon : ON"
								else: ret_ += "\n┣• Auto Respon : OFF"
								if settings["checkContact"] == True: ret_ += "\n┣• Check Contact : ON"
								else: ret_ += "\n┣• Check Contact : OFF"
								if settings["checkPost"] == True: ret_ += "\n┣• Check Post : ON"
								else: ret_ += "\n┣• Check Post : OFF"
								if settings["checkSticker"] == True: ret_ += "\n┣• Check Sticker : ON"
								else: ret_ += "\n┣• Check Sticker : OFF"
								ret_ +="\n┣•━━━━━━━━━━━━━━━━\n┃        DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
								client.sendMessage(to, str(ret_))
							except Exception as error:
								logError(error)
						elif cmd == "autoadd on":
							if settings["autoAdd"] == True:
								client.sendMessage(to, "➧ Auto add aktif")
							else:
								settings["autoAdd"] = True
								client.sendMessage(to, "➧ Auto add aktif")
						elif cmd == "autoadd off":
							if settings["autoAdd"] == False:
								client.sendMessage(to, "➧ Auto add nonaktif")
							else:
								settings["autoAdd"] = False
								client.sendMessage(to, "➧ Auto add nonaktif")
						elif cmd == "autojoin on":
							if settings["autoJoin"] == True:
								client.sendMessage(to, "➧ Auto join aktif")
							else:
								settings["autoJoin"] = True
								client.sendMessage(to, "➧ Auto join aktif")
						elif cmd == "autojoin off":
							if settings["autoJoin"] == False:
								client.sendMessage(to, "➧ Auto join nonaktif")
							else:
								settings["autoJoin"] = False
								client.sendMessage(to, "➧ Auto join nonaktif")
						elif cmd == "jointicket on":
							if settings["autoJoinTicket"] == True:
								client.sendMessage(to, "➧ Auto join ticket aktif")
							else:
								settings["autoJoinTicket"] = True
								client.sendMessage(to, "➧ Auto join ticket aktif")
						elif cmd == "autojointicket off":
							if settings["autoJoinTicket"] == False:
								client.sendMessage(to, "➧ Auto join ticket nonaktif")
							else:
								settings["autoJoinTicket"] = False
								client.sendMessage(to, "➧ Auto join ticket nonaktif")
						elif cmd == "autoread on":
							if settings["autoRead"] == True:
								client.sendMessage(to, "➧ Auto read aktif")
							else:
								settings["autoRead"] = True
								client.sendMessage(to, "➧ Auto read aktif")
						elif cmd == "autoread off":
							if settings["autoRead"] == False:
								client.sendMessage(to, "➧ Auto read nonaktif")
							else:
								settings["autoRead"] = False
								client.sendMessage(to, "➧ Auto read nonaktif")
						elif cmd == "respon on":
							if settings["autoRespon"] == True:
								client.sendMessage(to, "➧ Auto respon tag aktif")
							else:
								settings["autoRespon"] = True
								client.sendMessage(to, "➧ Auto respon tag aktif")
						elif cmd == "respon off":
							if settings["autoRespon"] == False:
								client.sendMessage(to, "➧ Auto respon tag nonaktif")
							else:
								settings["autoRespon"] = False
								client.sendMessage(to, "➧ Auto respon tag nonaktif")
						elif cmd == "info on":
							if settings["checkContact"] == True:
								client.sendMessage(to, "➧ Check details contact aktif")
							else:
								settings["checkContact"] = True
								client.sendMessage(to, "➧ Check details contact aktif")
						elif cmd == "info off":
							if settings["checkContact"] == False:
								client.sendMessage(to, "➧ Check details contact nonaktif")
							else:
								settings["checkContact"] = False
								client.sendMessage(to, "➧ Check details contact nonaktif")
						elif cmd == "tl on":
							if settings["checkPost"] == True:
								client.sendMessage(to, "➧ Check details post aktif")
							else:
								settings["checkPost"] = True
								client.sendMessage(to, "➧ Check details post aktif")
						elif cmd == "tl off":
							if settings["checkPost"] == False:
								client.sendMessage(to, "➧ Check details post nonaktif")
							else:
								settings["checkPost"] = False
								client.sendMessage(to, "➧ Check details post nonaktif")
						elif cmd == "cst on":
							if settings["checkSticker"] == True:
								client.sendMessage(to, "➧ Check details sticker aktif")
							else:
								settings["checkSticker"] = True
								client.sendMessage(to, "➧ Check details sticker aktif")
						elif cmd == "cst off":
							if settings["checkSticker"] == False:
								client.sendMessage(to, "➧ Check details sticker nonaktif")
							else:
								settings["checkSticker"] = False
								client.sendMessage(to, "➧ Check details sticker nonaktif")
						elif cmd.startswith("smess: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["autoAddMessage"] = txt
								client.sendMessage(to, "➧ Success changing to : \n   {}".format(txt))
							except:
								client.sendMessage(to, "➧ Failed")
						elif cmd.startswith("setrespon: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["autoResponMessage"] = txt
								client.sendMessage(to, "➧ Success changing to : \n   {}".format(txt))
							except:
								client.sendMessage(to, "➧ Failed")
						elif cmd.startswith("setjoin: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["autoJoinMessage"] = txt
								client.sendMessage(to, "➧ Success changing to : \n   {}".format(txt))
							except:
								client.sendMessage(to, "➧ Failed")
						elif cmd.startswith("cname: "):
							sep = text.split(" ")
							name = text.replace(sep[0] + " ","")
							if len(name) <= 20:
								profile = client.getProfile()
								profile.displayName = name
								client.updateProfile(profile)
								client.sendMessage(to, "➧ Success changing name to :\n   {}".format(name))
						elif cmd.startswith("cbio: "):
							sep = text.split(" ")
							bio = text.replace(sep[0] + " ","")
							if len(bio) <= 500:
								profile = client.getProfile()
								profile.statusMessage = bio
								client.updateProfile(profile)
								client.sendMessage(to, "➧ Success changing bio to :\n   {}".format(bio))
						elif cmd == "me":
							client.sendMention(to, "@!", [sender])
							client.sendContact(to, sender)
							contact = client.getContact(sender)
							cover = client.getProfileCoverURL(sender)
							client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
							client.sendImageWithURL(to, cover)
						elif cmd == "myprofile":
							contact = client.getContact(sender)
							cover = client.getProfileCoverURL(sender)
							result = "╭━━━━━━━━━━━━━━━━╮\n┃       DETAIL PROFILE\n╰━━━━━━━━━━━━━━━━╯"
							result += "\n ➧  Display Name : \n   @!"
							result += "\n ➧  Status Message : \n   {}".format(contact.statusMessage)
							result += "\n╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
							client.sendMention(to, result, [sender])
							client.sendMessage(to, "➧ Profil Picture")
							client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
							client.sendMessage(to, "➧ Cover Picture")
							client.sendImageWithURL(to, cover)
						elif cmd == "mymid":
							contact = client.getContact(sender)
							client.sendMention(to, "@!\n➧ Your Mid :\n   {}".format(contact.mid), [sender])
						elif cmd == "myname":
							contact = client.getContact(sender)
							client.sendMention(to, "@!\n➧ Your display name :\n   {}".format(contact.displayName), [sender])
						elif cmd == "mybio":
							contact = client.getContact(sender)
							client.sendMention(to, "➧ @!\n➧ Your Status Message :\n   {}".format(contact.statusMessage), [sender])
						elif cmd == "mypic":
							contact = client.getContact(sender)
							client.sendMessage(to, "➧ Your Picture Covet :")
							client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
						elif cmd == "myvid":
							contact = client.getContact(sender)
							if contact.videoProfile == None:
								return client.sendMessage(to, "➧ Anda tidak menggunakan video profile")
							client.sendVideoWithURL(to, "http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
						elif cmd == "mycover":
							cover = client.getProfileCoverURL(sender)
							client.sendMessage(to, "➧ Your Cover Picture :")
							client.sendImageWithURL(to, str(cover))
						elif cmd.startswith("getmid "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									client.sendMention(to, "@! \n➧ Mid :\n   {}".format(ls), [ls])
						elif cmd.startswith("getname "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendMention(to, "@! \n➧ Display Name :\n   {}".format(contact.displayName), [ls])
						elif cmd.startswith("getbio "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendMention(to, "@! \n➧ Status Message :\n   {}".format(contact.statusMessage), [ls])
						elif cmd.startswith("getpic "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendMessage(to, "➧ Picture Profile :")
									client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
						elif cmd.startswith("getvid "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									if contact.videoProfile == None:
										return client.sendMention(to, "@!\n➧ Tidak menggunakan video profile", [ls])
									client.sendMessage(to, "➧ Video Profil :")
									client.sendVideoWithURL(to, "http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
						elif cmd.startswith("getcover "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									cover = client.getProfileCoverURL(ls)
									client.sendMessage(to, "➧ Picture Cover :")
									client.sendImageWithURL(to, str(cover))
						elif cmd.startswith("clone "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									client.cloneContactProfile(ls)
									client.sendContact(to, sender)
									client.sendMessage(to, "➧ Berhasil clone profile")
						elif cmd == "restore":
							try:
								clientProfile = client.getProfile()
								clientProfile.displayName = str(settings["myProfile"]["displayName"])
								clientProfile.statusMessage = str(settings["myProfile"]["statusMessage"])
								clientPictureStatus = client.downloadFileURL("http://dl.profile.line-cdn.net/{}".format(str(settings["myProfile"]["pictureStatus"])), saveAs="LineAPI/tmp/backupPicture.bin")
								coverId = str(settings["myProfile"]["coverId"])
								client.updateProfile(clientProfile)
								client.updateProfileCoverById(coverId)
								client.updateProfilePicture(clientPictureStatus)
								client.sendMessage(to, "➧ Berhasil restore profile")
								client.sendContact(to, sender)
								client.deleteFile(clientPictureStatus)
							except Exception as error:
								logError(error)
								client.sendMessage(to, "➧ Gagal restore profile")
						elif cmd == "mybackup":
							try:
								clientProfile = client.getProfile()
								settings["myProfile"]["displayName"] = str(clientProfile.displayName)
								settings["myProfile"]["statusMessage"] = str(clientProfile.statusMessage)
								settings["myProfile"]["pictureStatus"] = str(clientProfile.pictureStatus)
								coverId = client.getProfileDetail()["result"]["objectId"]
								settings["myProfile"]["coverId"] = str(coverId)
								client.sendMessage(to, "➧ Berhasil backup profile")
							except Exception as error:
								logError(error)
								client.sendMessage(to, "➧ Gagal backup profile")
						elif cmd == "myfriend":
							contacts = client.getAllContactIds()
							num = 0
							result = "╭━━━━━━━━━━━━━━━━╮\n┃        F R I E N D L I S T\n┣•━━━━━━━━━━━━━━━━"
							for listContact in contacts:
								contact = client.getContact(listContact)
								num += 1
								result += "\n┣ {}. {}".format(num, contact.displayName)
							result += "\n┣•━━━━━━━━━━━━━━━━\n┃  Total  Friend : {} ".format(len(contacts)) + "\n╰━━━━━━━━━━━━━━━━╯"
							client.sendMessage(to, result)
						elif cmd.startswith("steal "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							contacts = client.getAllContactIds()
							try:
								listContact = contacts[int(query)-1]
								contact = client.getContact(listContact)
								cover = client.getProfileCoverURL(listContact)
								result = "╭━━━━━━━━━━━━━━━━╮\n┃         DETAIL PROFILE\n╰━━━━━━━━━━━━━━━━╯"
								result += "\n ➧  Display Name : \n   @!"
								result += "\n ➧  Mid : \n   {}".format(contact.mid)
								result += "\n ➧  Status Message : \n   {}".format(contact.statusMessage)
								result += "\n╭━━━━━━━━━━━━━━━━╮\n┃       DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
								client.sendMention(to, result, [contact.mid])
							except Exception as error:
								logError(error)
						elif cmd == "blocklist":
							blockeds = client.getBlockedContactIds()
							num = 0
							result = "╭━━━━━━━━━━━━━━━━╮\n┃     BLOCKED ACCOUNT\n┣•━━━━━━━━━━━━━━━━"
							for listBlocked in blockeds:
								contact = client.getContact(listBlocked)
								num += 1
								result += "\n┣ {}. {}".format(num, contact.displayName)
							result += "\n┣•━━━━━━━━━━━━━━━━\n┃ Total Blocked :  {} ".format(len(blockeds)) + "\n╰━━━━━━━━━━━━━━━━╯"
							client.sendMessage(to, result)
						elif cmd.startswith("fbc: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							contacts = client.getAllContactIds()
							for contact in contacts:
								client.sendMessage(contact, "➧ Maap numpang broadcast : \n{}".format(str(txt)))
							client.sendMessage(to, "➧ Berhasil broadcast ke {} teman".format(str(len(contacts))))
						elif cmd.startswith("cgname: "):
							if msg.toType == 2:
								sep = text.split(" ")
								groupname = text.replace(sep[0] + " ","")
								if len(groupname) <= 20:
									group = client.getGroup(to)
									group.name = groupname
									client.updateGroup(group)
									client.sendMessage(to, "➧ Berhasil mengubah nama group menjadi : \n   {}".format(groupname))
						elif cmd == "oqr":
							if msg.toType == 2:
								group = client.getGroup(to)
								group.preventedJoinByTicket = False
								client.updateGroup(group)
								groupUrl = client.reissueGroupTicket(to)
								client.sendMessage(to, "➧ Berhasil membuka QR Group\n\nGroupURL : line://ti/g/{}".format(groupUrl))
						elif cmd == "cqr":
							if msg.toType == 2:
								group = client.getGroup(to)
								group.preventedJoinByTicket = True
								client.updateGroup(group)
								client.sendMessage(to, "➧ Berhasil menutup QR Group")
						elif cmd == "gpic":
							if msg.toType == 2:
								group = client.getGroup(to)
								groupPicture = "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus)
								client.sendMessage(to, "➧ Group Cover :")
								client.sendImageWithURL(to, groupPicture)
						elif cmd == "gname":
							if msg.toType == 2:
								group = client.getGroup(to)
								client.sendMessage(to, "➧ Nama Group : {}".format(group.name))
						elif cmd == "gid":
							if msg.toType == 2:
								group = client.getGroup(to)
								client.sendMessage(to, "➧ Group ID :\n   {}".format(group.id))
						elif cmd == "mygroup":
							groups = client.getGroupIdsJoined()
							ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃         M Y    G R O U P\n┣•━━━━━━━━━━━━━━━━"
							no = 0
							for gid in groups:
								group = client.getGroup(gid)
								no += 1
								ret_ += "\n┣ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
							ret_ += "\n┣•━━━━━━━━━━━━━━━━\n┃ Total Groups : {} ".format(str(len(groups))) + "\n╰━━━━━━━━━━━━━━━━╯"
							client.sendMessage(to, str(ret_))
						elif cmd == "tag name":
							if msg.toType == 2:
								group = client.getGroup(to)
								num = 0
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃          TAG BY NAME\n┣•━━━━━━━━━━━━━━━━"
								for contact in group.members:
									num += 1
									ret_ += "\n┣ {}. {}".format(num, contact.displayName)
								ret_ += "\n┣•━━━━━━━━━━━━━━━━\n┃ Total Members : {} ".format(len(group.members)) + "\n╰━━━━━━━━━━━━━━━━╯"
								client.sendMessage(to, ret_)
						elif cmd == "pendinglist":
							if msg.toType == 2:
								group = client.getGroup(to)
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃         PENDING LIST\n┣•━━━━━━━━━━━━━━━━"
								no = 0
								if group.invitee is None or group.invitee == []:
									return client.sendMessage(to, "➧ Tidak ada pendingan")
								else:
									for pending in group.invitee:
										no += 1
										ret_ += "\n┣ {}. {}".format(str(no), str(pending.displayName))
									ret_ += "\n┣•━━━━━━━━━━━━━━━━\n┃ Total Pending : {} ".format(str(len(group.invitee))) + "\n╰━━━━━━━━━━━━━━━━╯"
									client.sendMessage(to, str(ret_))
						elif cmd == "ginfo":
							group = client.getGroup(to)
							try:
								try:
									groupCreator = group.creator.mid
								except:
									groupCreator = "Tidak Ada (Hapus Akun)"
								if group.invitee is None:
									groupPending = "0"
								else:
									groupPending = str(len(group.invitee))
								if group.preventedJoinByTicket == True:
									groupQr = "Tertutup"
									groupTicket = "Tidak Ada"
								else:
									groupQr = "Terbuka"
									groupTicket = "https://line.me/R/ti/g/{}".format(str(client.reissueGroupTicket(group.id)))
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃            GROUP INFO\n╰━━━━━━━━━━━━━━━━╯"
								ret_ += "\n ➧ Nama Group : \n   {}".format(group.name)
								ret_ += "\n ➧ Pembuat : \n   @!"
								ret_ += "\n ➧ Jumlah Member : {}".format(str(len(group.members)))
								ret_ += "\n ➧ Jumlah Pending : {}".format(groupPending)
								ret_ += "\n ➧ Group Qr : {}".format(groupQr)
								ret_ += "\n ➧ Group ID : \n   {}".format(group.id)
								ret_ += "\n ➧ Group Ticket : \n   {}".format(groupTicket)
								ret_ += "\n╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
								client.sendMention(to, str(ret_), [groupCreator])
								client.sendMessage(to, "➧ Group Cover Picture")
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus))
							except:
								pass
								
						elif cmd.startswith("bcg: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							groups = client.getGroupIdsJoined()
							for group in groups:
								client.sendMessage(group, "➧ Maap numpang broadcast : \n   {}".format(str(txt)))
							client.sendMessage(to, "➧ Berhasil broadcast ke : {} group".format(str(len(groups))))
						
						elif cmd == 'boss':
							group = client.getGroup(to)
							midMembers = [contact.mid for contact in group.members]
							midSelect = len(midMembers)//300
							for mentionMembers in range(midSelect+1):
								no = 0
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃   MENTION MEMBERS\n┣•━━━━━━━━━━━━━━━━"
								dataMid = []
								for dataMention in group.members[mentionMembers*300 : (mentionMembers+1)*300]:
									dataMid.append(dataMention.mid)
									no += 1
									ret_ += "\n┣ {}. @!".format(str(no))
								ret_ += "\n┣•━━━━━━━━━━━━━━━━\n┃ Total Members : {} ".format(str(len(dataMid))) + "\n╰━━━━━━━━━━━━━━━━╯"
								client.sendMention(to, ret_, dataMid)
						elif cmd == "cctv on":
							tz = pytz.timezone("Asia/Jakarta")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							readTime = "➧ " + hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\n➧ Jam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
							if to in read['readPoint']:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								read['readPoint'][to] = msg_id
								read['readMember'][to] = []
								client.sendMessage(to, "➧ Cctv Aktif")
							else:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								read['readPoint'][to] = msg_id
								read['readMember'][to] = []
								client.sendMessage(to, "➧ Set reading point : \n{}".format(readTime))
						elif cmd == "cctv off":
							tz = pytz.timezone("Asia/Jakarta")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							readTime = "➧ " + hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\n➧ Jam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
							if to not in read['readPoint']:
								client.sendMessage(to,"➧ Cctv Nonaktif")
							else:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								client.sendMessage(to, "➧ Delete reading point : \n{}".format(readTime))
						elif cmd == "reader":
							if to in read['readPoint']:
								if read["readMember"][to] == []:
									return client.sendMessage(to, "Tidak Ada Sider")
								else:
									no = 0
									result = "╭━━━━━━━━━━━━━━━━╮\n┃            LIST SIDER\n┣•━━━━━━━━━━━━━━━━"
									for dataRead in read["readMember"][to]:
										no += 1
										result += "\n┣ {}. @!".format(str(no))
									result += "\n┣•━━━━━━━━━━━━━━━━\n┃ Total Sider : {} ".format(str(len(read["readMember"][to]))) + "\n╰━━━━━━━━━━━━━━━━╯"
									client.sendMention(to, result, read["readMember"][to])
									read['readMember'][to] = []
						elif cmd == "cpp":
							settings["changePictureProfile"] = True
							client.sendMessage(to, "➧ Silahkan kirim gambarnya")
						elif cmd == "cgpicture":
							if msg.toType == 2:
								if to not in settings["changeGroupPicture"]:
									settings["changeGroupPicture"].append(to)
								client.sendMessage(to, "➧ Silahkan kirim gambarnya")
						elif cmd == "mimic on":
							if settings["mimic"]["status"] == True:
								client.sendMessage(to, "➧ Reply message aktif")
							else:
								settings["mimic"]["status"] = True
								client.sendMessage(to, "➧ Berhasil mengaktifkan reply message")
						elif cmd == "mimic off":
							if settings["mimic"]["status"] == False:
								client.sendMessage(to, "➧ Reply message nonaktif")
							else:
								settings["mimic"]["status"] = False
								client.sendMessage(to, "➧ Berhasil menonaktifkan reply message")
						elif cmd == "miclist":
							if settings["mimic"]["target"] == {}:
								client.sendMessage(to, "➧ Tidak Ada Target")
							else:
								no = 0
								result = "╭━━━━━━━━━━━━━━━━╮\n┃          MIMIC LIST\n┣•━━━━━━━━━━━━━━━━"
								target = []
								for mid in settings["mimic"]["target"]:
									target.append(mid)
									no += 1
									result += "\n┣ {}. @!".format(no)
								result += "\n┣•━━━━━━━━━━━━━━━━\n┃ Total Mimic : {} ".format(str(len(target))) + "\n╰━━━━━━━━━━━━━━━━╯"
								client.sendMention(to, result, target)
						elif cmd.startswith("micadd "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									try:
										if ls in settings["mimic"]["target"]:
											client.sendMessage(to, "➧ Target sudah ada dalam list")
										else:
											settings["mimic"]["target"][ls] = True
											client.sendMessage(to, "➧ Berhasil menambahkan target")
									except:
										client.sendMessage(to, "➧ Gagal menambahkan target")
						elif cmd.startswith("micdel "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									try:
										if ls not in settings["mimic"]["target"]:
											client.sendMessage(to, "➧ Target sudah tidak didalam list")
										else:
											del settings["mimic"]["target"][ls]
											client.sendMessage(to, "➧ Berhasil menghapus target")
									except:
										client.sendMessage(to, "➧ Gagal menghapus target")

						elif cmd.startswith("instainfo"):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							url = requests.get("http://corrykalam.pw/api/instagram.php?username={}".format(search))
							data = url.json()
							icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/599px-Instagram_icon.png"
							name = "Instagram"
							link = "https://www.instagram.com/{}".format(data["result"]["username"])
							result = "╭━━━━━━━━━━━━━━━━╮\n┃   INSTAGRAM INFO\n╰━━━━━━━━━━━━━━━━╯"
							result += "\n ➧ Name : {}".format(data["result"]["name"])
							result += "\n ➧ Username : {}".format(data["result"]["username"])
							result += "\n ➧ Bio : {}".format(data["result"]["bio"])
							result += "\n ➧ Follower : {}".format(data["result"]["follower"])
							result += "\n ➧ Following : {}".format(data["result"]["following"])
							result += "\n ➧ Private : {}".format(data["result"]["private"])
							result += "\n ➧ Post : {}".format(data["result"]["mediacount"])
							result += "\n╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
							client.sendImageWithURL(to, data["result"]["url"])
							client.sendFooter(to, result, icon, name, link)
						elif cmd.startswith("instastory "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							cond = query.split(" ")
							search = str(cond[0])
							if len(cond) == 2:
								url = requests.get("http://rahandiapi.herokuapp.com/instastory/{}?key=betakey".format(search))
								data = url.json()
								num = int(cond[1])
								if num <= len(data["url"]):
									search = data["url"][num - 1]
									if search["tipe"] == 1:
										client.sendImageWithURL(to, str(search["link"]))
									elif search["tipe"] == 2:
										client.sendVideoWithURL(to, str(search["link"]))
						elif cmd == "quotes":
							url = requests.get("https://botfamily.faith/api/quotes/?apikey=beta")
							data = url.json()
							result = "╭━━━━━━━━━━━━━━━━╮\n┃             Q U O T E S\n╰━━━━━━━━━━━━━━━━╯"
							result += "\n ➧ Author : {}".format(data["result"]["author"])
							result += "\n ➧ Category : {}".format(data["result"]["category"])
							result += "\n ➧ Quote : {}".format(data["result"]["quote"])
							result += "\n╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
							client.sendMessage(to, result)
						elif cmd.startswith("say-"):
							sep = text.split("-")
							sep = sep[1].split(" ")
							lang = sep[0]
							if settings["setKey"] == False:
								txt = text.lower().replace("say-" + lang + " ","")
							else:
								txt = text.lower().replace(settings["keyCommand"] + "say-" + lang + " ","")
							if lang not in language["gtts"]:
								return client.sendMessage(to, "➧ Bahasa {} tidak ditemukan".format(lang))
							tts = gTTS(text=txt, lang=lang)
							tts.save("line/tmp/tts-{}.mp3".format(lang))
							client.sendAudio(to, "line/tmp/tts-{}.mp3".format(lang))
							client.deleteFile("line/tmp/tts-{}.mp3".format(lang))
						elif cmd.startswith("yvideo "):
							sep = text.split("|")
							txt = msg.text.replace(sep[0] + " ","")
							cond = txt.split(" ")
							search = cond[0]
							url = requests.get("http://api.w3hills.com/youtube/search?keyword={}&api_key=86A7FCF3-6CAF-DEB9-E214-B74BDB835B5B".format(search))
							data = url.json()
							if len(cond) == 1:
								no = 0
								result = "╭━━━━━━━━━━━━━━━━╮\n┃   YOUTUBE SEARCH\n╰━━━━━━━━━━━━━━━━╯"
								for anu in data["videos"]:
									no += 1
									result += "\n ➧ {}. {}".format(str(no),str(anu["title"]))
								result += "\n╭━━━━━━━━━━━━━━━━╮\n┃ Total Result : {} ".format(str(len(data["videos"]))) + "\n╰━━━━━━━━━━━━━━━━╯"
								client.sendMessage(to, result)
								client.sendMessage(to, "➧ Untuk melihat info video : \n➧ Silahkan ketik :  {}Yvideo {}|_(Nomor)".format(str(setKey), str(search)))
							elif len(cond) == 2:
								num = int(str(cond[1]))
								if num <= len(data):
									search = data["videos"][num - 1]
									ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃          YOUTUBE INFO\n╰━━━━━━━━━━━━━━━━╯"
									ret_ += "\n ➧ Channel : {}".format(str(search["publish"]["owner"]))
									ret_ += "\n ➧ Title : {}".format(str(search["title"]))
									ret_ += "\n ➧ Release : {}".format(str(search["publish"]["date"]))
									ret_ += "\n ➧ Viewers : {}".format(str(search["stats"]["views"]))
									ret_ += "\n ➧ Likes : {}".format(str(search["stats"]["likes"]))
									ret_ += "\n ➧ Dislikes : {}".format(str(search["stats"]["dislikes"]))
									ret_ += "\n ➧ Rating : {}".format(str(search["stats"]["rating"]))
									ret_ += "\n ➧ Description : {}".format(str(search["description"]))
									ret_ += "\n ➧ [ {} ]".format(str(search["webpage"]))
									ret_ += "\n╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
									client.sendImageWithURL(to, str(search["thumbnail"]))
									client.sendMessage(to, str(ret_))
						elif cmd.startswith("gambar "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							url = requests.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(txt))
							data = url.json()
							client.sendImageWithURL(to, random.choice(data["result"]))
						elif cmd.startswith("play "):
							sep = text.split("|")
							query = text.replace(sep[0] + " ","")
							cond = query.split("|")
							search = str(cond[0])
							url = requests.get("http://api.ntcorp.us/joox/search?q={}".format(str(search)))
							data = url.json()
							if len(cond) == 1:
								num = 0
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃        MUSIC RESULT\n╰━━━━━━━━━━━━━━━━╯"
								for music in data["result"]:
									num += 1
									ret_ += "\n ➧ {}. {}".format(str(num), str(music["single"]))
								ret_ += "\n╭━━━━━━━━━━━━━━━━╮\n┃       Total Music : {} ".format(str(len(data["result"])) + " \n╰━━━━━━━━━━━━━━━━╯")
								ret_ += "\n\n➧ Untuk memutar music : \n➧ Silahkan ketik :  {}Play {}|_(Nomor)".format(str(setKey), str(search))
								client.sendMessage(to, str(ret_))
							elif len(cond) == 2:
								num = int(cond[1])
								if num <= len(data["result"]):
									music = data["result"][num - 1]
									url = requests.get("http://api.ntcorp.us/joox/song_info?sid={}".format(str(music["sid"])))
									data = url.json()
									ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃          DETAIL MUSIC\n╰━━━━━━━━━━━━━━━━╯"
									ret_ += "\n ➧ Title : {}".format(str(data["result"]["song"]))
									ret_ += "\n ➧ Album : {}".format(str(data["result"]["album"]))
									ret_ += "\n ➧ Size : {}".format(str(data["result"]["size"]))
									ret_ += "\n╭━━━━━━━━━━━━━━━━╮\n┃       DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
									client.sendImageWithURL(to, str(data["result"]["img"]))
									client.sendMessage(to, str(ret_))
									client.sendMessage(to, "➧ Downloading Audio...")
									client.sendAudioWithURL(to, str(data["result"]["mp3"][0]))
									client.sendMessage(to, "➧ Selamat Mendengarkan")
								                   
						elif cmd.startswith("lyric "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							cond = txt.split("|")
							query = cond[0]
							with requests.session() as web:
								web.headers["user-agent"] = "Mozilla/5.0"
								url = web.get("https://www.musixmatch.com/search/{}".format(urllib.parse.quote(query)))
								data = BeautifulSoup(url.content, "html.parser")
								result = []
								for trackList in data.findAll("ul", {"class":"tracks list"}):
									for urlList in trackList.findAll("a"):
										title = urlList.text
										url = urlList["href"]
										result.append({"title": title, "url": url})
								if len(cond) == 1:
									ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃           MUSIC RESULT\n┣•━━━━━━━━━━━━━━━━"
									num = 0
									for title in result:
										num += 1
										ret_ += "\n┣ {}. {}".format(str(num), str(title["title"]))
									ret_ += "\n┣•━━━━━━━━━━━━━━━━\n┃ Total Lyric : {} ".format(str(len(result)) + " \n╰━━━━━━━━━━━━━━━━╯")
									ret_ += "\n\n➧ Untuk melihat liriknya : \n➧ Silahkan ketik : {}Lyric {}|_(Nomor)".format(str(setKey), str(query))
									client.sendMessage(to, ret_)
								elif len(cond) == 2:
									num = int(cond[1])
									if num <= len(result):
										data = result[num - 1]
										with requests.session() as web:
											web.headers["user-agent"] = "Mozilla/5.0"
											url = web.get("https://www.musixmatch.com{}".format(urllib.parse.quote(data["url"])))
											data = BeautifulSoup(url.content, "html5lib")
											for lyricContent in data.findAll("p", {"class":"mxm-lyrics__content "}):
												lyric = lyricContent.text
												client.sendMessage(to, lyric)
						elif cmd.startswith("tr-"):
							sep = text.split("-")
							sep = sep[1].split(" ")
							lang = sep[0]
							if settings["setKey"] == False:
								txt = text.lower().replace("tr-" + lang + " ","")
							else:
								txt = text.lower().replace(settings["keyCommand"] + "tr-" + lang + " ","")
							if lang not in language["googletrans"]:
								return client.sendMessage(to, "➧ Bahasa {} tidak ditemukan".format(lang))
							translator = Translator()
							result = translator.translate(txt, dest=lang)
							client.sendMessage(to, result.text)
						if text.lower() == "mykey":
							client.sendMessage(to, "➧ Keycommand yang diset saat ini : \n   {}".format(str(settings["keyCommand"])))
						elif text.lower() == "setkey on":
							if settings["setKey"] == True:
								client.sendMessage(to, "➧ Setkey telah aktif")
							else:
								settings["setKey"] = True
								client.sendMessage(to, "➧ Berhasil mengaktifkan setkey")
						elif text.lower() == "/info":
							if settings["checkContact"] == True:
								client.sendMessage(to, "➧ Kirim Kotaknya")
							else:
								settings["checkContact"] = True
								client.sendMessage(to, "➧ Kirim Kotaknya")
						elif text.lower() == "setkey off":
							if settings["setKey"] == False:
								client.sendMessage(to, "➧ Setkey telah nonaktif")
							else:
								settings["setKey"] = False
								client.sendMessage(to, "➧ Berhasil menonaktifkan setkey")
						if text is None: return
						if "/ti/g/" in msg.text.lower():
							if settings["autoJoinTicket"] == True:
								link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
								links = link_re.findall(text)
								n_links = []
								for l in links:
									if l not in n_links:
										n_links.append(l)
								for ticket_id in n_links:
									group = client.findGroupByTicket(ticket_id)
									client.acceptGroupInvitationByTicket(group.id,ticket_id)
									client.sendMessage(to, "➧ Berhasil masuk ke group %s" % str(group.name))
					elif msg.contentType == 1:
						if settings["changePictureProfile"] == True:
							path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-cpp.bin".format(time.time()))
							settings["changePictureProfile"] = False
							client.updateProfilePicture(path)
							client.sendMessage(to, "➧ Berhasil mengubah foto profile")
							client.deleteFile(path)
						if msg.toType == 2:
							if to in settings["changeGroupPicture"]:
								path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-cgp.bin".format(time.time()))
								settings["changeGroupPicture"].remove(to)
								client.updateGroupPicture(to, path)
								client.sendMessage(to, "➧ Berhasil mengubah foto group")
								client.deleteFile(path)
					elif msg.contentType == 7:
						if settings["checkSticker"] == True:
							stk_id = msg.contentMetadata['STKID']
							stk_ver = msg.contentMetadata['STKVER']
							pkg_id = msg.contentMetadata['STKPKGID']
							ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃          DETAIL STICKER\n╰━━━━━━━━━━━━━━━━╯"
							ret_ += "\n  ➧ STK_ID : {}".format(stk_id)
							ret_ += "\n  ➧ STK_PKG : {}".format(pkg_id)
							ret_ += "\n  ➧ STK_VER : {}".format(stk_ver)
							ret_ += "\n  ➧ STK_URL : \n   line://shop/detail/{}".format(pkg_id)
							ret_ += "\n╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
							client.sendMessage(to, str(ret_))
					elif msg.contentType == 13:
						if settings["checkContact"] == True:
							try:
								contact = client.getContact(msg.contentMetadata["mid"])
								cover = client.getProfileCoverURL(msg.contentMetadata["mid"])
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃      DETAIL CONTACT\n╰━━━━━━━━━━━━━━━━╯"
								ret_ += "\n ➧ Nama : {}".format(str(contact.displayName))
								ret_ += "\n ➧ MID : {}".format(str(msg.contentMetadata["mid"]))
								ret_ += "\n ➧ Bio : \n   {}".format(str(contact.statusMessage))
								ret_ += "\n╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
								client.sendMessage(to, str(ret_))
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus)))
								client.sendImageWithURL(to, cover)
							except:
								client.sendMessage(to, "➧ Kontak tidak valid")
					elif msg.contentType == 13:
						if settings["checkContact"] == True:
							try:
								dd.findAndAddContactsByMid(target)
								contact = client.getContact(target)
								cover = client.getProfileCoverURL(target)
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃      DETAIL CONTACT\n╰━━━━━━━━━━━━━━━━╯"
								ret_ += "\n ➧ Nama : {}".format(str(contact.displayName))
								ret_ += "\n ➧ MID : {}".format(str(msg.contentMetadata["mid"]))
								ret_ += "\n ➧ Bio : \n   {}".format(str(contact.statusMessage))
								ret_ += "\n╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
								client.sendMessage(to, str(ret_))
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus)))
								client.sendImageWithURL(to, cover)
							except:
								client.sendMessage(to, "➧ Kontak tidak valid")
								
					elif msg.contentType == 16:
						if settings["checkPost"] == True:
							try:
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃          DETAIL POST\n╰━━━━━━━━━━━━━━━━╯"
								if msg.contentMetadata["serviceType"] == "GB":
									contact = client.getContact(sender)
									auth = "\n ➧ Penulis : {}".format(str(contact.displayName))
								else:
									auth = "\n ➧ Penulis : {}".format(str(msg.contentMetadata["serviceName"]))
								purl = "\n ➧ URL : \n   {}".format(str(msg.contentMetadata["postEndUrl"]).replace("line://","https://line.me/R/"))
								ret_ += auth
								ret_ += purl
								if "mediaOid" in msg.contentMetadata:
									object_ = msg.contentMetadata["mediaOid"].replace("svc=myhome|sid=h|","")
									if msg.contentMetadata["mediaType"] == "V":
										if msg.contentMetadata["serviceType"] == "GB":
											ourl = "\n ➧ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
											murl = "\n ➧ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(msg.contentMetadata["mediaOid"]))
										else:
											ourl = "\n ➧ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
											murl = "\n ➧ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(object_))
										ret_ += murl
									else:
										if msg.contentMetadata["serviceType"] == "GB":
											ourl = "\n ➧ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
										else:
											ourl = "\n ➧ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
									ret_ += ourl
								if "stickerId" in msg.contentMetadata:
									stck = "\n ➧ Stiker : https://line.me/R/shop/detail/{}".format(str(msg.contentMetadata["packageId"]))
									ret_ += stck
								if "text" in msg.contentMetadata:
									text = "\n ➧ Tulisan : {}".format(str(msg.contentMetadata["text"]))
									ret_ += text
								ret_ += "\n╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
								client.sendMessage(to, str(ret_))
							except:
								client.sendMessage(to, "➧ Post tidak valid")
			except Exception as error:
				logError(error)
				
#PUBLIC BOT START
		if op.type == 26:
			try:
				print("[ 26 ] SEND MESSAGE")
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				cmd = command(text)
				setKey = settings["keyCommand"].title()
				if settings["setKey"] == False:
					setKey = ''
				if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
					if msg.toType == 0:
						if sender != client.profile.mid:
							to = sender
						else:
							to = receiver
					elif msg.toType == 1:
						to = receiver
					elif msg.toType == 2:
						to = receiver
					if msg.contentType == 0:
						if cmd == "turn bot ogffff":
							client.sendMessage(to, "➧ Bot Di Nonaktifkan")
							sys.exit("[ INFO ] BOT SHUTDOWN")
							return
						
						elif cmd == "salam":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Wa alaikum salam kk\n➧ Semoga kk selalu dalam lindungan Allah\n➧ Serta selalu diberikan yg terbaik dr yang\n   paling baik\n\n➧ Amiin yaa robbal alamiin...")
						elif cmd == "assalamualaikum":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Wa alaikum salam kk\n➧ Semoga kk selalu dalam lindungan Allah\n➧ Serta selalu diberikan yg terbaik dr yang\n   paling baik\n\n➧ Amiin yaa robbal alamiin...")
						elif cmd == "assalamu'alaikum":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Wa alaikum salam kk\n➧ Semoga kk selalu dalam lindungan Allah\n➧ Serta selalu diberikan yg terbaik dr yang\n   paling baik\n\n➧ Amiin yaa robbal alamiin...")
						elif cmd == "asalamualaikum":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Wa alaikum salam kk\n➧ Semoga kk selalu dalam lindungan Allah\n➧ Serta selalu diberikan yg terbaik dr yang\n   paling baik\n\n➧ Amiin yaa robbal alamiin...")
						elif cmd == "mikum":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Wa alaikum salam kk\n➧ Semoga kk selalu dalam lindungan Allah\n➧ Serta selalu diberikan yg terbaik dr yang\n   paling baik\n\n➧ Amiin yaa robbal alamiin...")
						elif cmd == "pagi":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Selamat pagi juga kk \n➧ Semoga hari ini bs lbh baik \n   dr hr kemarin\n\n➧ Amiin...")
						elif cmd == "met pagi":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Selamat pagi juga kk \n➧ Semoga hari ini bs lbh baik \n   dr hr kemarin\n\n➧ Amiin...")
						elif cmd == "mat pagi":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Selamat pagi juga kk \n➧ Semoga hari ini bs lbh baik \n   dr hr kemarin\n\n➧ Amiin...")
						elif cmd == "selamat pagi":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Selamat pagi juga kk \n➧ Semoga hari ini bs lbh baik \n   dr hr kemarin\n\n➧ Amiin...")
						elif cmd == "pagi kk":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Selamat pagi juga kk \n➧ Semoga hari ini bs lbh baik \n   dr hr kemarin\n\n➧ Amiin...")
						elif cmd == "siang":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Met siang n met beraktifitas kk \n➧ Semoga selalu diberi kelancaran \n   n kemudahan di setiap apa yg kk kerjakan\n\n➧ Amiin...")
						elif cmd == "met siang":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Met siang n met beraktifitas kk \n➧ Semoga selalu diberi kelancaran \n   n kemudahan di setiap apa yg kk kerjakan\n\n➧ Amiin...")
						elif cmd == "mat siang":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Met siang n met beraktifitas kk \n➧ Semoga selalu diberi kelancaran \n   n kemudahan di setiap apa yg kk kerjakan\n\n➧ Amiin...")
						elif cmd == "selamat siang":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Met siang n met beraktifitas kk \n➧ Semoga selalu diberi kelancaran \n   n kemudahan di setiap apa yg kk kerjakan\n\n➧ Amiin...")
						elif cmd == "siang kk":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Met siang n met beraktifitas kk \n➧ Semoga selalu diberi kelancaran \n   n kemudahan di setiap apa yg kk kerjakan\n\n➧ Amiin...")
						elif cmd == "sore":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Met sore juga kk \n➧ Cepet mandi gih,,,udah sore kk...\n➧ Kk bau banget,,,taukkkkk...\n\n➧ Wakakakakakakakak...")
						elif cmd == "met sore":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Met sore juga kk \n➧ Cepet mandi gih,,,udah sore kk...\n➧ Kk bau banget,,,taukkkkk...\n\n➧ Wakakakakakakakak...")
						elif cmd == "mat sore":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Met sore juga kk \n➧ Cepet mandi gih,,,udah sore kk...\n➧ Kk bau banget,,,taukkkkk...\n\n➧ Wakakakakakakakak...")
						elif cmd == "selamat sore":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Met sore juga kk \n➧ Cepet mandi gih,,,udah sore kk...\n➧ Kk bau banget,,,taukkkkk...\n\n➧ Wakakakakakakakak...")
						elif cmd == "selamat sore semua":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Met sore juga kk \n➧ Cepet mandi gih,,,udah sore kk...\n➧ Kk bau banget,,,taukkkkk...\n\n➧ Wakakakakakakakak...")
						elif cmd == "malam":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Met malam n met rehat kk \n➧ Semoga yg kita kerjakan hari ini \n   menghasilkan sesuatu yg barokah...\n\n➧ Amiin...")
						elif cmd == "met malam":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Met malam n met rehat kk \n➧ Semoga yg kita kerjakan hari ini \n   menghasilkan sesuatu yg barokah...\n\n➧ Amiin...")
						elif cmd == "mat malam":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Met malam n met rehat kk \n➧ Semoga yg kita kerjakan hari ini \n   menghasilkan sesuatu yg barokah...\n\n➧ Amiin...")
						elif cmd == "selamat malam":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Met malam n met rehat kk \n➧ Semoga yg kita kerjakan hari ini \n   menghasilkan sesuatu yg barokah...\n\n➧ Amiin...")
						elif cmd == "met malam semua":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Met malam n met rehat kk \n➧ Semoga yg kita kerjakan hari ini \n   menghasilkan sesuatu yg barokah...\n\n➧ Amiin...")
						elif cmd == "sepi":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Iya nih,,,sepi amat room nya...\n➧ Kali ajja dah pada kojom ama anuhnya\n➧ Makanya jangan ngejomblo teruss....\n➧ Biar ada temennya...")
						elif cmd == "sepi amat":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Iya nih,,,sepi amat room nya...\n➧ Kali ajja dah pada kojom ama anuhnya\n➧ Makanya jangan ngejomblo teruss....\n➧ Biar ada temennya...")
						elif cmd == "sepi amat roomnya":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Iya nih,,,sepi amat room nya...\n➧ Kali ajja dah pada kojom ama anuhnya\n➧ Makanya jangan ngejomblo teruss....\n➧ Biar ada temennya...")
						elif cmd == "sepi roomya":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Iya nih,,,sepi amat room nya...\n➧ Kali ajja dah pada kojom ama anuhnya\n➧ Makanya jangan ngejomblo teruss....\n➧ Biar ada temennya...")
						elif cmd == "anjay":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Dihhh.... Ngomongnya yg sopan dong\n➧ Kagak malu apa di baca banyak orang")
						elif cmd == "anjayy":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Dihhh.... Ngomongnya yg sopan dong\n➧ Kagak malu apa di baca banyak orang")
						elif cmd == "njay":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Dihhh.... Ngomongnya yg sopan dong\n➧ Kagak malu apa di baca banyak orang")
						elif cmd == "njir":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Dihhh.... Ngomongnya yg sopan dong\n➧ Kagak malu apa di baca banyak orang")
						elif cmd == "njirr":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Dihhh.... Ngomongnya yg sopan dong\n➧ Kagak malu apa di baca banyak orang")
						elif cmd == "njirrr":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Dihhh.... Ngomongnya yg sopan dong\n➧ Kagak malu apa di baca banyak orang")
						elif cmd == "sue":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Apamu yg sueek kk...???\n➧ Atw sue ora jamu..??? Xixixixi")
						elif cmd == "suee":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Apamu yg sueek kk...???\n➧ Atw sue ora jamu..??? Xixixixi")
						elif cmd == "sueee":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Apamu yg sueek kk...???\n➧ Atw sue ora jamu..??? Xixixixi")
						elif cmd == "suek":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Apamu yg sueek kk...???\n➧ Atw sue ora jamu..??? Xixixixi")
						elif cmd == "suekk":
							client.sendMention(to, "@!", [sender])
							client.sendMessage(to, "➧ Apamu yg sueek kk...???\n➧ Atw sue ora jamu..??? Xixixixi")
						
						elif cmd == "menu":
							helpPub = menuPub()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "https://timeline.line.me/post/_dZNo9tm3E3PH0dURm6N9Rf_pYxmFJO2uASn_y7Q/1153217318709030407"
							client.sendFooter(to, helpPub, icon, name, link)
						elif cmd == "translator":
							helpTranslate = menuTranslate()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "https://timeline.line.me/post/_dZNo9tm3E3PH0dURm6N9Rf_pYxmFJO2uASn_y7Q/1153217318709030407"
							client.sendFooter(to, helpTranslate, icon, name, link)
						
						elif cmd == "info on":
							if settings["checkContact"] == True:
								client.sendMessage(to, "➧ Check details contact aktif")
							else:
								settings["checkContact"] = True
								client.sendMessage(to, "➧ Check details contact aktif")
						elif cmd == "info off":
							if settings["checkContact"] == False:
								client.sendMessage(to, "➧ Check details contact nonaktif")
							else:
								settings["checkContact"] = False
								client.sendMessage(to, "➧ Check details contact nonaktif")
						
						elif cmd == "cst on":
							if settings["checkSticker"] == True:
								client.sendMessage(to, "➧ Check details sticker aktif")
							else:
								settings["checkSticker"] = True
								client.sendMessage(to, "➧ Check details sticker aktif")
						elif cmd == "cst off":
							if settings["checkSticker"] == False:
								client.sendMessage(to, "➧ Check details sticker nonaktif")
							else:
								settings["checkSticker"] = False
								client.sendMessage(to, "➧ Check details sticker nonaktif")
						
						elif cmd == "me":
							client.sendMention(to, "@!", [sender])
							client.sendContact(to, sender)
							contact = client.getContact(sender)
							cover = client.getProfileCoverURL(sender)
							client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
							client.sendImageWithURL(to, cover)
						elif cmd == "myprofile":
							contact = client.getContact(sender)
							cover = client.getProfileCoverURL(sender)
							result = "╭━━━━━━━━━━━━━━━━╮\n┃       DETAIL PROFILE\n╰━━━━━━━━━━━━━━━━╯"
							result += "\n ➧  Display Name : \n   @!"
							result += "\n ➧  Status Message : \n   {}".format(contact.statusMessage)
							result += "\n╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
							client.sendMention(to, result, [sender])
							client.sendMessage(to, "➧ Profil Picture")
							client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
							client.sendMessage(to, "➧ Cover Picture")
							client.sendImageWithURL(to, cover)
						elif cmd == "mymid":
							contact = client.getContact(sender)
							client.sendMention(to, "@!\n➧ Your Mid :\n   {}".format(contact.mid), [sender])
						elif cmd == "myname":
							contact = client.getContact(sender)
							client.sendMention(to, "@!\n➧ Your display name :\n   {}".format(contact.displayName), [sender])
						elif cmd == "mybio":
							contact = client.getContact(sender)
							client.sendMention(to, "➧ @!\n➧ Your Status Message :\n   {}".format(contact.statusMessage), [sender])
						elif cmd == "mypic":
							contact = client.getContact(sender)
							client.sendMessage(to, "➧ Your Picture Covet :")
							client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
						elif cmd == "myvid":
							contact = client.getContact(sender)
							if contact.videoProfile == None:
								return client.sendMessage(to, "➧ Anda tidak menggunakan video profile")
							client.sendVideoWithURL(to, "http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
						elif cmd == "mycover":
							cover = client.getProfileCoverURL(sender)
							client.sendMessage(to, "➧ Your Cover Picture :")
							client.sendImageWithURL(to, str(cover))
						elif cmd.startswith("getmid "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									client.sendMention(to, "@! \n➧ Mid :\n   {}".format(ls), [ls])
						elif cmd.startswith("getname "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendMention(to, "@! \n➧ Display Name :\n   {}".format(contact.displayName), [ls])
						elif cmd.startswith("getbio "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendMention(to, "@! \n➧ Status Message :\n   {}".format(contact.statusMessage), [ls])
						elif cmd.startswith("getpic "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendMessage(to, "➧ Picture Profile :")
									client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
						elif cmd.startswith("getvid "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									if contact.videoProfile == None:
										return client.sendMention(to, "@!\n➧ Tidak menggunakan video profile", [ls])
									client.sendMessage(to, "➧ Video Profil :")
									client.sendVideoWithURL(to, "http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
						elif cmd.startswith("getcover "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									cover = client.getProfileCoverURL(ls)
									client.sendMessage(to, "➧ Picture Cover :")
									client.sendImageWithURL(to, str(cover))
						
						elif cmd == "gpic":
							if msg.toType == 2:
								group = client.getGroup(to)
								groupPicture = "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus)
								client.sendMessage(to, "➧ Group Cover :")
								client.sendImageWithURL(to, groupPicture)
						elif cmd == "gname":
							if msg.toType == 2:
								group = client.getGroup(to)
								client.sendMessage(to, "➧ Nama Group : {}".format(group.name))
						elif cmd == "gid":
							if msg.toType == 2:
								group = client.getGroup(to)
								client.sendMessage(to, "➧ Group ID :\n   {}".format(group.id))
						
						elif cmd == "tag name":
							if msg.toType == 2:
								group = client.getGroup(to)
								num = 0
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃          TAG BY NAME\n┣•━━━━━━━━━━━━━━━━"
								for contact in group.members:
									num += 1
									ret_ += "\n┣ {}. {}".format(num, contact.displayName)
								ret_ += "\n┣•━━━━━━━━━━━━━━━━\n┃ Total Members : {} ".format(len(group.members)) + "\n╰━━━━━━━━━━━━━━━━╯"
								client.sendMessage(to, ret_)
						elif cmd == "pendinglist":
							if msg.toType == 2:
								group = client.getGroup(to)
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃         PENDING LIST\n┣•━━━━━━━━━━━━━━━━"
								no = 0
								if group.invitee is None or group.invitee == []:
									return client.sendMessage(to, "➧ Tidak ada pendingan")
								else:
									for pending in group.invitee:
										no += 1
										ret_ += "\n┣ {}. {}".format(str(no), str(pending.displayName))
									ret_ += "\n┣•━━━━━━━━━━━━━━━━\n┃ Total Pending : {} ".format(str(len(group.invitee))) + "\n╰━━━━━━━━━━━━━━━━╯"
									client.sendMessage(to, str(ret_))
						elif cmd == "ginfo":
							group = client.getGroup(to)
							try:
								try:
									groupCreator = group.creator.mid
								except:
									groupCreator = "Tidak Ada (Hapus Akun)"
								if group.invitee is None:
									groupPending = "0"
								else:
									groupPending = str(len(group.invitee))
								if group.preventedJoinByTicket == True:
									groupQr = "Tertutup"
									groupTicket = "Tidak Ada"
								else:
									groupQr = "Terbuka"
									groupTicket = "https://line.me/R/ti/g/{}".format(str(client.reissueGroupTicket(group.id)))
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃            GROUP INFO\n╰━━━━━━━━━━━━━━━━╯"
								ret_ += "\n ➧ Nama Group : \n   {}".format(group.name)
								ret_ += "\n ➧ Pembuat : \n   @!"
								ret_ += "\n ➧ Jumlah Member : {}".format(str(len(group.members)))
								ret_ += "\n ➧ Jumlah Pending : {}".format(groupPending)
								ret_ += "\n ➧ Group Qr : {}".format(groupQr)
								ret_ += "\n ➧ Group Ticket : \n   {}".format(groupTicket)
								ret_ += "\n╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
								client.sendMention(to, str(ret_), [groupCreator])
								client.sendMessage(to, "➧ Group Cover Picture")
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus))
							except:
								pass
							
						elif cmd == "cctv on":
							tz = pytz.timezone("Asia/Jakarta")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							readTime = "➧ " + hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\n➧ Jam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
							if to in read['readPoint']:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								read['readPoint'][to] = msg_id
								read['readMember'][to] = []
								client.sendMessage(to, "➧ Cctv Aktif")
							else:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								read['readPoint'][to] = msg_id
								read['readMember'][to] = []
								client.sendMessage(to, "➧ Set reading point : \n{}".format(readTime))
						elif cmd == "cctv off":
							tz = pytz.timezone("Asia/Jakarta")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							readTime = "➧ " + hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\n➧ Jam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
							if to not in read['readPoint']:
								client.sendMessage(to,"➧ Cctv Nonaktif")
							else:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								client.sendMessage(to, "➧ Delete reading point : \n{}".format(readTime))
						elif cmd == "reader":
							if to in read['readPoint']:
								if read["readMember"][to] == []:
									return client.sendMessage(to, "Tidak Ada Sider")
								else:
									no = 0
									result = "╭━━━━━━━━━━━━━━━━╮\n┃            LIST SIDER\n┣•━━━━━━━━━━━━━━━━"
									for dataRead in read["readMember"][to]:
										no += 1
										result += "\n┣ {}. @!".format(str(no))
									result += "\n┣•━━━━━━━━━━━━━━━━\n┃ Total Sider : {} ".format(str(len(read["readMember"][to]))) + "\n╰━━━━━━━━━━━━━━━━╯"
									client.sendMention(to, result, read["readMember"][to])
									read['readMember'][to] = []
						
						elif cmd.startswith("instainfo"):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							url = requests.get("http://corrykalam.pw/api/instagram.php?username={}".format(search))
							data = url.json()
							icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/599px-Instagram_icon.png"
							name = "Instagram"
							link = "https://www.instagram.com/{}".format(data["result"]["username"])
							result = "╭━━━━━━━━━━━━━━━━╮\n┃   INSTAGRAM INFO\n╰━━━━━━━━━━━━━━━━╯"
							result += "\n ➧ Name : {}".format(data["result"]["name"])
							result += "\n ➧ Username : {}".format(data["result"]["username"])
							result += "\n ➧ Bio : {}".format(data["result"]["bio"])
							result += "\n ➧ Follower : {}".format(data["result"]["follower"])
							result += "\n ➧ Following : {}".format(data["result"]["following"])
							result += "\n ➧ Private : {}".format(data["result"]["private"])
							result += "\n ➧ Post : {}".format(data["result"]["mediacount"])
							result += "\n╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
							client.sendImageWithURL(to, data["result"]["url"])
							client.sendFooter(to, result, icon, name, link)
						elif cmd.startswith("instastory "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							cond = query.split(" ")
							search = str(cond[0])
							if len(cond) == 2:
								url = requests.get("http://rahandiapi.herokuapp.com/instastory/{}?key=betakey".format(search))
								data = url.json()
								num = int(cond[1])
								if num <= len(data["url"]):
									search = data["url"][num - 1]
									if search["tipe"] == 1:
										client.sendImageWithURL(to, str(search["link"]))
									elif search["tipe"] == 2:
										client.sendVideoWithURL(to, str(search["link"]))
						
						elif cmd.startswith("yvideo "):
							sep = text.split("|")
							txt = msg.text.replace(sep[0] + " ","")
							cond = txt.split(" ")
							search = cond[0]
							url = requests.get("http://api.w3hills.com/youtube/search?keyword={}&api_key=86A7FCF3-6CAF-DEB9-E214-B74BDB835B5B".format(search))
							data = url.json()
							if len(cond) == 1:
								no = 0
								result = "╭━━━━━━━━━━━━━━━━╮\n┃   YOUTUBE SEARCH\n╰━━━━━━━━━━━━━━━━╯"
								for anu in data["videos"]:
									no += 1
									result += "\n ➧ {}. {}".format(str(no),str(anu["title"]))
								result += "\n╭━━━━━━━━━━━━━━━━╮\n┃ Total Result : {} ".format(str(len(data["videos"]))) + "\n╰━━━━━━━━━━━━━━━━╯"
								client.sendMessage(to, result)
								client.sendMessage(to, "➧ Untuk melihat info video : \n➧ Silahkan ketik :  {} {}| (Nomor Video)".format(str(setKey), str(search)))
							elif len(cond) == 2:
								num = int(str(cond[1]))
								if num <= len(data):
									search = data["videos"][num - 1]
									ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃          YOUTUBE INFO\n╰━━━━━━━━━━━━━━━━╯"
									ret_ += "\n ➧ Channel : {}".format(str(search["publish"]["owner"]))
									ret_ += "\n ➧ Title : {}".format(str(search["title"]))
									ret_ += "\n ➧ Release : {}".format(str(search["publish"]["date"]))
									ret_ += "\n ➧ Viewers : {}".format(str(search["stats"]["views"]))
									ret_ += "\n ➧ Likes : {}".format(str(search["stats"]["likes"]))
									ret_ += "\n ➧ Dislikes : {}".format(str(search["stats"]["dislikes"]))
									ret_ += "\n ➧ Rating : {}".format(str(search["stats"]["rating"]))
									ret_ += "\n ➧ Description : {}".format(str(search["description"]))
									ret_ += "\n ➧ [ {} ]".format(str(search["webpage"]))
									ret_ += "\n╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
									client.sendImageWithURL(to, str(search["thumbnail"]))
									client.sendMessage(to, str(ret_))
						elif cmd.startswith("gambar "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							url = requests.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(txt))
							data = url.json()
							client.sendImageWithURL(to, random.choice(data["result"]))
						elif cmd.startswith("play "):
							sep = text.split("|")
							query = text.replace(sep[0] + " ","")
							cond = query.split("|")
							search = str(cond[0])
							url = requests.get("http://api.ntcorp.us/joox/search?q={}".format(str(search)))
							data = url.json()
							if len(cond) == 1:
								num = 0
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃        MUSIC RESULT\n╰━━━━━━━━━━━━━━━━╯"
								for music in data["result"]:
									num += 1
									ret_ += "\n ➧ {}. {}".format(str(num), str(music["single"]))
								ret_ += "\n╭━━━━━━━━━━━━━━━━╮\n┃       Total Music : {} ".format(str(len(data["result"])) + " \n╰━━━━━━━━━━━━━━━━╯")
								ret_ += "\n\n➧ Untuk memutar music : \n➧ Silahkan ketik :  {} {}| (Nomor Lagu)".format(str(setKey), str(search))
								client.sendMessage(to, str(ret_))
							elif len(cond) == 2:
								num = int(cond[1])
								if num <= len(data["result"]):
									music = data["result"][num - 1]
									url = requests.get("http://api.ntcorp.us/joox/song_info?sid={}".format(str(music["sid"])))
									data = url.json()
									ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃          DETAIL MUSIC\n╰━━━━━━━━━━━━━━━━╯"
									ret_ += "\n ➧ Title : {}".format(str(data["result"]["song"]))
									ret_ += "\n ➧ Album : {}".format(str(data["result"]["album"]))
									ret_ += "\n ➧ Size : {}".format(str(data["result"]["size"]))
									ret_ += "\n╭━━━━━━━━━━━━━━━━╮\n┃       DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
									client.sendImageWithURL(to, str(data["result"]["img"]))
									client.sendMessage(to, str(ret_))
									client.sendMessage(to, "➧ Downloading Audio...")
									client.sendAudioWithURL(to, str(data["result"]["mp3"][0]))
									client.sendMessage(to, "➧ Selamat Mendengarkan")
								
						elif cmd.startswith("tr-"):
							sep = text.split("-")
							sep = sep[1].split(" ")
							lang = sep[0]
							if settings["setKey"] == False:
								txt = text.lower().replace("tr-" + lang + " ","")
							else:
								txt = text.lower().replace(settings["keyCommand"] + "tr-" + lang + " ","")
							if lang not in language["googletrans"]:
								return client.sendMessage(to, "➧ Bahasa {} tidak ditemukan".format(lang))
							translator = Translator()
							result = translator.translate(txt, dest=lang)
							client.sendMessage(to, result.text)
						
						elif text.lower() == "/info":
							if settings["checkContact"] == True:
								client.sendMessage(to, "➧ Kirim Kotaknya")
							else:
								settings["checkContact"] = True
								client.sendMessage(to, "➧ Kirim Kotaknya")
						
					elif msg.contentType == 7:
						if settings["checkSticker"] == True:
							stk_id = msg.contentMetadata['STKID']
							stk_ver = msg.contentMetadata['STKVER']
							pkg_id = msg.contentMetadata['STKPKGID']
							ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃        DETAIL STICKER\n╰━━━━━━━━━━━━━━━━╯"
							ret_ += "\n  ➧ STK_ID : {}".format(stk_id)
							ret_ += "\n  ➧ STK_PKG : {}".format(pkg_id)
							ret_ += "\n  ➧ STK_VER : {}".format(stk_ver)
							ret_ += "\n  ➧ STK_URL : \n   line://shop/detail/{}".format(pkg_id)
							ret_ += "\n╭━━━━━━━━━━━━━━━━╮\n┃        DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
							client.sendMessage(to, str(ret_))
					elif msg.contentType == 13:
						if settings["checkContact"] == True:
							try:
								contact = client.getContact(msg.contentMetadata["mid"])
								cover = client.getProfileCoverURL(msg.contentMetadata["mid"])
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃       DETAIL CONTACT\n╰━━━━━━━━━━━━━━━━╯"
								ret_ += "\n ➧ Nama : {}".format(str(contact.displayName))
								ret_ += "\n ➧ Bio : \n   {}".format(str(contact.statusMessage))
								ret_ += "╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
								client.sendMessage(to, str(ret_))
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus)))
								client.sendImageWithURL(to, cover)
							except:
								client.sendMessage(to, "➧ Kontak tidak valid")
					elif msg.contentType == 13:
						if settings["checkContact"] == True:
							try:
								dd.findAndAddContactsByMid(target)
								contact = client.getContact(target)
								cover = client.getProfileCoverURL(target)
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃      DETAIL CONTACT\n╰━━━━━━━━━━━━━━━━╯"
								ret_ += "\n ➧ Nama : {}".format(str(contact.displayName))
								ret_ += "\n ➧ MID : {}".format(str(msg.contentMetadata["mid"]))
								ret_ += "\n ➧ Bio : \n   {}".format(str(contact.statusMessage))
								ret_ += "\n╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
								client.sendMessage(to, str(ret_))
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus)))
								client.sendImageWithURL(to, cover)
							except:
								client.sendMessage(to, "➧ Kontak tidak valid")
								
					elif msg.contentType == 16:
						if settings["checkPost"] == True:
							try:
								ret_ = "╭━━━━━━━━━━━━━━━━╮\n┃          DETAIL POST\n╰━━━━━━━━━━━━━━━━╯"
								if msg.contentMetadata["serviceType"] == "GB":
									contact = client.getContact(sender)
									auth = "\n ➧ Penulis : {}".format(str(contact.displayName))
								else:
									auth = "\n ➧ Penulis : {}".format(str(msg.contentMetadata["serviceName"]))
								purl = "\n ➧ URL : \n   {}".format(str(msg.contentMetadata["postEndUrl"]).replace("line://","https://line.me/R/"))
								ret_ += auth
								ret_ += purl
								if "mediaOid" in msg.contentMetadata:
									object_ = msg.contentMetadata["mediaOid"].replace("svc=myhome|sid=h|","")
									if msg.contentMetadata["mediaType"] == "V":
										if msg.contentMetadata["serviceType"] == "GB":
											ourl = "\n ➧ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
											murl = "\n ➧ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(msg.contentMetadata["mediaOid"]))
										else:
											ourl = "\n ➧ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
											murl = "\n ➧ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(object_))
										ret_ += murl
									else:
										if msg.contentMetadata["serviceType"] == "GB":
											ourl = "\n ➧ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
										else:
											ourl = "\n ➧ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
									ret_ += ourl
								if "stickerId" in msg.contentMetadata:
									stck = "\n ➧ Stiker : https://line.me/R/shop/detail/{}".format(str(msg.contentMetadata["packageId"]))
									ret_ += stck
								if "text" in msg.contentMetadata:
									text = "\n ➧ Tulisan : {}".format(str(msg.contentMetadata["text"]))
									ret_ += text
								ret_ += "\n╭━━━━━━━━━━━━━━━━╮\n┃         DOTS AUTO BOT \n╰━━━━━━━━━━━━━━━━╯"
								client.sendMessage(to, str(ret_))
							except:
								client.sendMessage(to, "➧ Post tidak valid")
			except Exception as error:
				logError(error)
		if op.type == 26:
			try:
				print("[ 26 ] RECEIVE MESSAGE")
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
					if msg.toType == 0:
						if sender != client.profile.mid:
							to = sender
						else:
							to = receiver
					elif msg.toType == 1:
						to = receiver
					elif msg.toType == 2:
						to = receiver
					if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
						if msg.contentType == 0:
							client.sendMessage(to, text)
						elif msg.contentType == 1:
							path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-mimic.bin".format(time.time()))
							client.sendImage(to, path)
							client.deleteFile(path)
					if msg.contentType == 0:
						if settings["autoRead"] == True:
							client.sendChatChecked(to, msg_id)
						if sender not in clientMid:
							if msg.toType != 0 and msg.toType == 2:
								if 'MENTION' in msg.contentMetadata.keys()!= None:
									names = re.findall(r'@(\w+)', text)
									mention = ast.literal_eval(msg.contentMetadata['MENTION'])
									mentionees = mention['MENTIONEES']
									for mention in mentionees:
										if clientMid in mention["M"]:
											if settings["autoRespon"] == True:
												client.sendMention(sender, settings["autoResponMessage"], [sender])
											break
						if text is None: return
						if "/ti/g/" in msg.text.lower():
							if settings["autoJoinTicket"] == True:
								link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
								links = link_re.findall(text)
								n_links = []
								for l in links:
									if l not in n_links:
										n_links.append(l)
								for ticket_id in n_links:
									group = client.findGroupByTicket(ticket_id)
									client.acceptGroupInvitationByTicket(group.id,ticket_id)
									client.sendMessage(to, "➧ Berhasil masuk ke group %s" % str(group.name))
			except Exception as error:
				logError(error)

	except Exception as error:
		logError(error)
		if op.type == 55:
			print ("[ 55 ] NOTIFIED READ MESSAGE")
			if op.param1 in read["readPoint"]:
				if op.param2 not in read["readMember"][op.param1]:
					read["readMember"][op.param1].append(op.param2)
	except Exception as error:
		logError(error)
		
def run():
	while True:
		ops = clientPoll.singleTrace(count=50)
		if ops != None:
			for op in ops:
				try:
					clientBot(op)
				except Exception as error:
					logError(error)
				clientPoll.setRevision(op.revision)

if __name__ == "__main__":
	run()
