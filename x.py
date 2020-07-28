# -*- coding: utf-8 -*-
# Line頭貼影片更換 作者:蒼 
# 請勿拿去做任何營利用途


from Cang.linepy import *
from Cang.akad.ttypes import Message
from Cang.akad.ttypes import ContentType as Type
from youtube_dl import YoutubeDL
import subprocess, youtube_dl
import subprocess as cmd
import os,sys

client = LINE()
#client = LINE("")
clientMid = client.profile.mid
clientProfile = client.getProfile()
clientSettings = client.getSettings()
clientPoll = OEPoll(client)
msg_dict = {}


def logout():
    client.auth.logoutZ()

def command(text):
    pesan = text.lower()
    cmd = text.lower()
    return cmd
	
def changeVideoAndPictureProfile(pict, vids):
    try:
        files = {'file': open(vids, 'rb')}
        obs_params = client.genOBSParams({'oid': clientMid, 'ver': '2.0', 'type': 'video', 'cat': 'vp.mp4', 'name': 'Hello_World.mp4'})
        data = {'params': obs_params}
        r_vp = client.server.postContent('{}/talk/vp/upload.nhn'.format(str(client.server.LINE_OBS_DOMAIN)), data=data, files=files)
        if r_vp.status_code != 201:
            return "Failed update profile"
        client.updateProfilePicture(pict, 'vp')
        return "Success update profile"
    except Exception as e:
        raise Exception("Error change video and picture profile %s"%str(e))

def clientBot(op):
    try:
        if op.type == 25:
            try:
                msg = op.message
                text = msg.text
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
                    if msg.contentType == 0:
                        if text is None:
                            return
                        else:
                            cmd = command(text)
                            if cmd == "help":
                                helpmsg = "╔══[ LineVideoProfileChanger V3.1]\n"
                                helpmsg += "╠可用命令:\n"
                                helpmsg += "╠Cvp:「YT影片連結」 (注意C大寫)\n " 
                                helpmsg += "╠cp (更換現有的影片)\n"
                                helpmsg += "╠══[ 使用方法 ]\n"
                                helpmsg += "╠cp 將影片放置在跟x.py同一目錄下(檔名為Video.mp4)\n"
                                helpmsg += "╠══[ 關於本bot ]\n"
                                helpmsg += "╠製作:好想大力抱住正太ㄛ\n"
                                helpmsg += "╠有任何Bug及疑問可至巴哈小屋提問\n"
                                helpmsg += "╠Link：https://home.gamer.com.tw/creationDetail.php?sn=4536583\n"
                                helpmsg += "╚══[ 感謝您的使用 ]"
                                client.sendMessage(to,str(helpmsg))
                            elif msg.text.startswith("Cvp:"):
                                link = msg.text.replace("Cvp:","")
                                contact = client.getContact(sender)
                                client.sendMessage(to, "狀態: 下載中...")
                                print("正在下載中...需耗時數分鐘")
                                pic = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
                                os.system('youtube-dl -o BotVideo.mp4 {}'.format(link))
                                pict = client.downloadFileURL(pic)
                                vids = "BotVideo.mp4"
                                changeVideoAndPictureProfile(pict, vids)
                                client.sendMessage(to, "成功替換頭像影片")
                                print("成功替換頭像影片 刪除影片完畢")
                                os.remove("BotVideo.mp4")         
                            elif msg.text.lower() == "cp":
                                contact = client.getContact(sender)
                                client.sendMessage(to, "狀態: 更換中...")
                                print("需耗時數分鐘")
                                pic = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
                                pict = client.downloadFileURL(pic)
                                vids = "Video.mp4"
                                changeVideoAndPictureProfile(pict, vids)
                                client.sendMessage(to, "成功替換頭像影片")
                                print("成功替換頭像影片 刪除影片完畢")
                                os.remove("Video.mp4")         
                            elif msg.text.lower().startswith("logout"):
                                print("正在登出")
                                client.sendMessage(to, "登出中....")
                                logout()
                                print("登出完畢")
                                sys.exit(0)
            except Exception as error:
                print(error)
    except Exception as error:
        print(error)

while True:
    try:
        ops = clientPoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                clientBot(op)
                clientPoll.setRevision(op.revision)
    except Exception as error:
        print(error)
