# -*- coding: utf-8 -*-
from email import contentmanager
from math import fabs
from linepy import *
#from thrift import*
from datetime import datetime
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse
os.chdir(r'C:\Users\家龢\Desktop\ProtectBot-Ver-1.0')
 
cl = LINE() 
k1 = LINE() 
k2 = LINE()
k4 = LINE()
k3 = LINE() 

Xu = False
initate = []


clMID = cl.profile.mid
k1MID = k1.profile.mid
k2MID = k2.profile.mid
k3MID = k3.profile.mid
k4MID = k4.profile.mid

Bots = [clMID,k1MID,k2MID,k3MID,k4MID]

oepoll = OEPoll(cl)
banOpen = codecs.open("ban.json","r","utf-8")
groupOpen = codecs.open("temp.json","r","utf-8")
ban = json.load(banOpen)
gp = json.load(groupOpen)
#==============================================================================#
def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@XuQingTW "
    if mids == []:
        raise Exception("Invaliod mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
            textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    cl.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)

def restartBot():
    print ("[ INFO ] BOT RESETTED")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)
def botJoin(to):
    G = cl.getGroup(to)
    G.preventedJoinByTicket = False
    cl.updateGroup(G)
    Ticket = cl.reissueGroupTicket(op.param1)
    k1.acceptGroupInvitationByTicket(to,Ticket)
    k2.acceptGroupInvitationByTicket(to,Ticket)
    k3.acceptGroupInvitationByTicket(to,Ticket)
    k4.acceptGroupInvitationByTicket(to,Ticket)
    G.preventedJoinByTicket = True
    cl.updateGroup(G)
def backupData():
    try:
        backup = ban
        f = codecs.open('ban.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = gp
        f = codecs.open('group.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
def logError(text):
    cl.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def helpmessage():
    helpMessage = """╔═══════
╠  XuQingTWの Bot
╠══✪〘 Help 〙✪═══
╠➥ Speed-速度
╠➥ Join-分身入防
╠➥ bye-解除防護
╠➥ adminadd @-新增群管
╠➥ admindel @-刪除群管
╠➥ GM-查看本群管理者
╠➥ Banlist-黑單
╠➥ Adminlist-權限者清單
╚〘XuQingTW更新版本〙"""
    return helpMessage
def helpmessagetag():
    helpMessageTag ="""╔═══════
╠  XuQingTWの Bot
╠══✪〘 Help 〙✪═══
╠➥ adminadd @-新增群管
╠➥ admindel @-刪除群管
╠➥ adminlist-查看本群管理者
╠➥ Restart-重新啟動
╠➥ Tk @-多標踢人
╠➥ Gc mid-MID查票
╠➥ Add @-新增權限
╠➥ Del @-刪除權限
╠➥ A mid (times)-加票
╠➥ Ban:mid-MID黑單
╠➥ Ban-友資黑單
╠➥ Ban @-標注黑單
╠➥ Unban:mid-MID黑單
╠➥ Unban-友資黑單
╠➥ Unban @-標注黑單
╠➥ Speed-速度
╠➥ Join-分身入防
╠➥ @bye-解除防護
╠➥ Banlist-黑單
╠➥ Adminlist-權限者清單
╠➥ Clear ban-清除黑單
╠➥ cb-全群掃黑
╠➥ Kill ban-當前群組掃黑
╚〘XuQingTW更新版本〙"""
    return helpMessageTag
def helpn():
    helpN = """╔═══════
╠  XuQingTWの Bot
╠══✪〘 Help 〙✪═══
╠➥ Speed-速度
╠➥ adminlist-查看本群管理者
╚〘XuQingTW更新版本〙"""
    return helpN
def backupData():
    try:
        json.dump(gp,codecs.open('temp.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        json.dump(ban, codecs.open('ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False



wait = {
    "ban" : False,
    "unban" : False,
    "add" : False,
    "del" : False
}


def lineBot(op):
    global Xu,gp
    try:
        if op.type == 0:
            return
        if op.type == 5:
            #cl.findAndAddContactsByMid(op.param1) 自動加好友
            cl.sendMessage(op.param1, "你好 {} 謝謝你加我為好友".format(str(cl.getContact(op.param1).displayName)))

        if op.type == 11:
            print ("[ 11 ] Change Group settings")
            bot = random.choice([cl,k1,k2,k3,k4])
            G = cl.getGroup(op.param1)
            if op.param1 in gp["mention"]:
                sendMention(op.param1, "通知 @! 更改群組設定",[op.param2])
            if op.param1 in gp["qrprotect"]:
                if op.param2 in ban["admin"] or op.param2 in ban["owners"]:
                    pass
                else:
                    gs = cl.getGroup(op.param1)
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    ban["blacklist"][op.param2] = True
                    gs.preventJoinByTicket = True
                    cl.updateGroup(gs)
                    bot.updateGroup(G)
                    bot.kickoutFromGroup(op.param1,[op.param2])
        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
            if clMID in op.param3:
                if op.param2 in ban["owners"]:
                    cl.acceptGroupInvitation(op.param1)
                    botJoin(op.param1)
                    gMembMids = [contact.mid for contact in G.members]
                    matched_list = []
                    for tag in ban["blacklist"]:
                        if tag in gMembMids:
                            matched_list.append(str(tag))
                    if matched_list == []:
                        return
                    for jj in matched_list:
                        bot = random.choice([cl,k1,k2,k3,k4])
                        bot.kickoutFromGroup(op.param1,[jj])
                else:
                    cl.acceptGroupInvitation(op.param1)
                    cl.sendMessage(op.param1,"您沒有權限")
                    cl.leaveGroup(op.param1)
                    if k1MID in op.param3:
                    	k1.rejectGroupInvitation(op.param1)
                    if k2MID in op.param3:
                    	k2.rejectGroupInvitation(op.param1)
                    if k3MID in op.param3:
                    	k3.rejectGroupInvitation(op.param1)
                    if k4MID in op.param3:
                    	k4.rejectGroupInvitation(op.param1)                    
                    elif op.param2 in ban["admin"] or op.param2 in Bots or op.param2 in ban["owners"]:
                        pass
                    else:
                        bot = random.choice([cl,k1,k2,k3,k4])
                        G=bot.getGroup(op.param1)
                        matched_list = []
                        for tag in ban["blacklist"]:
                            if tag in op.param3:
                                matched_list.append(str(tag))
                        if matched_list == []:
                            return
                        for mid in matched_list:
                            bot.cancelGroupInvitation(op.param1,[mid])
        if op.type == 17:
            if op.param1 in ban["blacklist"]:
                bot=random.choice([cl.k1,k2,k3,k4])
                bot.kickoutFromGroup(op.param1,[op.param1])
                cl.sendMessage(op.param1,"Blacklist user joined")
            if op.param1 in "cb5c4058cd35096d3f0a6db8068e729b2":
                name = str(cl.getGroup(op.param1).name)
                sendMention(op.param1, "歡迎(=ﾟᗜﾟ)ﾉ @! 記事本有 公會+攻略+翻譯 可以多看看唷!"+name,[op.param2])
        if op.type ==19:
            a = 0
            if op.param2 in ban["admin"] or op.param2 in ban["owners"]:
                xxx=[op.param2]
                xxx.append(op.param3)
                sendMention(op.param1,"通知, @! 踢掉了 @!", mids=xxx)
                if op.param3 in clMID or op.param3 in k1MID or op.param3 in k2MID or op.param3 in k3MID or op.param3 in k4MID:
                    while (a<5):
                        try:
                            bot = random.choice([cl,k1,k2,k3,k4])
                            G = bot.getGroup(op.param1)
                            G.preventedJoinByTicket = False
                            bot.updateGroup(G)
                            Ticket = bot.reissueGroupTicket(op.param1)
                            cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                            k1.acceptGroupInvitationByTicket(op.param1,Ticket)
                            k2.acceptGroupInvitationByTicket(op.param1,Ticket)
                            k3.acceptGroupInvitationByTicket(op.param1,Ticket)
                            k4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        except:
                            a+=1
                            pass
                        else:
                            break
                    G = bot.getGroup(op.param1)
                    G.preventedJoinByTicket = True
                    bot.updateGroup(G)
            elif op.param3 in clMID or op.param3 in k1MID or op.param3 in k2MID or op.param3 in k3MID or op.param3 in k4MID:
                while (a<5):
                    try:
                        bot = random.choice([cl,k1,k2,k3,k4])
                        bot.kickoutFromGroup(op.param1,[op.param2])
                        G = bot.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        bot.updateGroup(G)
                        Ticket = bot.reissueGroupTicket(op.param1)
                        cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                        k1.acceptGroupInvitationByTicket(op.param1,Ticket)
                        k2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        k3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        k4.acceptGroupInvitationByTicket(op.param1,Ticket)
                    except:
                        a+=1
                        pass
                    else:
                        break
                try:
                    ban["blacklist"][op.param2] = True
                    G = bot.getGroup(op.param1)
                    G.preventedJoinByTicket = True
                    bot.updateGroup(G)
                except:
                    pass
            elif G.id in gp["pretect"]:
                bot = random.choice([cl,k1,k2,k3,k4])
                G=cl.getGroup(op.param1)
                if G.id in gp["s"] and op.param2 in gp["s"][G.id]:
                    pass
                else:
                    bot.kickoutFromGroup(op.param1,[op.param2])
                    ban["blacklist"][op.param2] = True




        if op.type == 24:
            print ("[ 24 ] NOTIFIED LEAVE ROOM")
            if clMID in op.param3:
                cl.leaveRoom(op.param1)
            if k1MID in op.param3:
                k1.leaveRoom(op.param1)
            if k2MID in op.param3:
                k2.leaveRoom(op.param1)
            if k3MID in op.param3:
                k3.leaveRoom(op.param1)
            if k4MID in op.param3:
                k4.leaveRoom(op.param1)
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
            if sender in sender:
                if text.lower() =='報數':
                    cl.sendMessage(to,"1")
                    k1.sendMessage(to,"2")
                    k2.sendMessage(to,"3")
                    k3.sendMessage(to,"4")
                    k4.sendMessage(to,"5")
                elif text.lower() == 'speed':
                    start = time.time()
                    cl.sendMessage(to, "計算中...")
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,format(str(elapsed_time)))
                elif text.lower() == 'adminlist':
                    G = cl.getGroup(to)
                    if G.id not in gp["s"] or gp["s"][G.id]==[]:
                        cl.sendMessage(to,"無群管!")
                    else:
                        mc = "╔══[ Group Manager ]"
                        for mi_d in gp["s"][G.id]:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")
                elif text.lower() == 'help':
                    if sender in ban["admin"]:
                        helpMessage = helpmessage()
                        cl.sendMessage(to, str(helpMessage))
                    elif sender in ban["owners"]:
                        helpMessageTag = helpmessagetag()
                        cl.sendMessage(to, str(helpMessageTag))
                    else:
                        helpN = helpn()
                        cl.sendMessage(to, str(helpN))
                elif text.lower() in ['tagall']:
                    
                    if sender in ban["admin"] or sender in ban["owners"]:
                        G = cl.getGroup(msg.to)
                        nama = [contact.mid for contact in G.members]
                        k = len(nama)//20
                        for a in range(k+1):
                            txt = u''
                            s=0
                            b=[]
                            for i in G.members[a*20 : (a+1)*20]:
                                b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                                s += 7
                                txt += u'@XuQi \n'
                            cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        cl.sendMessage(to, "總共 {} 人".format(str(len(nama))))
                    else:
                        cl.sendMessage(to,"請三個成員或管理員打+1之後才會執行")
                        initate.append(sender)
                        
                elif text.lower() in ['+1'] and len(initate) > 0:
                    if sender  not in ban["admin"] and sender  not in ban["owners"]:
                        if sender not in initate:
                            initate.append(sender)
                            cl.sendMessage(to,"您已經成功+1")
                            if len(initate) >=4:
                                Xu = True
                        else:
                            contact = cl.getContact(sender)
                            sendMention(to,"@! 您已經成功+1過了",[contact.mid])
                    if Xu == True:
                        G = cl.getGroup(msg.to)
                        nama = [contact.mid for contact in G.members]
                        k = len(nama)//20
                        for a in range(k+1):
                            txt = u''
                            s=0
                            b=[]
                            for i in G.members[a*20 : (a+1)*20]:
                                b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                                s += 7
                                txt += u'@XuQi \n'
                            cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        cl.sendMessage(to, "總共 {} 人".format(str(len(nama))))
                        initate.clear()
                elif text.lower() in ['n'] and len(initate) > 0:
                        cl.sendMessage(msg.to, "成功取消")
                        initate.clear()

            if sender in ban["admin"] or sender in ban["owners"]:
                if text.lower() in ['bye']:
                    cl.sendMessage(msg.to, "確定退出？\ N（y / n）")
                    wait['bye'][msg.to] = sender

                elif text.lower() == 'save':
                    backupData()
                    cl.sendMessage(to,"儲存設定成功!")
                elif text.lower() in ["Y","y","N","n"]:
                    if msg._from== wait['bye'][msg.to]:
                        if text.lower() in ['y']:
                            cl.sendMessage(msg.to, "我知道了")
                            cl.leaveGroup(msg.to)
                            k1.leaveGroup(msg.to)
                            k2.leaveGroup(msg.to)
                            k3.leaveGroup(msg.to)
                            k4.leaveGroup(msg.to)
                            del wait['bye'][msg.to]
                        elif text.lower() in ['n'] and len(wait['wait']) > 0:
                            cl.sendMessage(msg.to, "了解了")
                            del wait['bye'][msg.to]
                    else:
                        pass
                elif text.lower() == 'join':
                    botJoin(msg.to)
                elif text.lower() == 'banlist':
                    if ban["blacklist"] == {}:
                        cl.sendMessage(msg.to,"無黑單成員!")
                    else:
                        mc = "[ Black List ]"
                        for mi_d in ban["blacklist"]:
                            if ban["blacklist"][mi_d] == True:
                                mc += "\n↬ "+cl.getContact(mi_d).displayName+"\n"+str(mi_d)
                            else:
                            	mc += "\n↬ "+cl.getContact(mi_d).displayName+"\n"+str(mi_d)+"[baned]"
                        cl.sendMessage(msg.to,mc + "\n[ Finish ]")
##########################################################################################################################################
                elif text.lower() in ['groupinfo','ginfo']:
                    group = cl.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "不明"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "無"
                    else:
                        gQr = "開啟"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ 群組資料 ]"
                    ret_ += "\n╠ 群組名稱 : {}".format(str(group.name))
                    ret_ += "\n╠ 群組 Id : {}".format(group.id)
                    ret_ += "\n╠ 創建者 : {}".format(str(gCreator))
                    ret_ += "\n╠ 群組人數 : {}".format(str(len(group.members)))
                    ret_ += "\n╠ 邀請中 : {}".format(gPending)
                    ret_ += "\n╠ 網址狀態 : {}".format(gQr)
                    ret_ += "\n╠ 群組網址 : {}".format(gTicket)
                    ret_ += "\n╚══[ 完 ]"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
                elif text.lower() == 'about':
                    ret_ = "╔══[ 關於使用者 ]"
                    ret_ += "\n╠ 使用者名稱 : {}".format(cl.getContact(sender).displayName)
                    if sender in cl.getAllContactIds():ret_ += "\n╠ 與本帳關係 : 好友"
                    else:ret_ += "\n╠ 與本帳關係 : 普通"
                    if sender in ban["owners"]:ret_ += "\n╠ 使用者權限 : 最高(擁有者)"
                    elif sender in ban["admin"]:ret_ += "\n╠ 使用者權限 : 部分(權限者)"
                    elif sender in ban["blacklist"]:ret_ += "\n╠ 使用者權限 : 黑單者"
                    else:ret_ += "\n╠ 使用者權限 : 基本"
                    ret_ += "\n╠ 詳細功能請打help"
                    ret_ += "\n╠ 擁有者 : 星曈"
                    ret_ += "\n╚══[ 感謝您的使用 ]"
                    cl.sendMessage(to, str(ret_))
                elif text.lower() == 'set':
                    try:
                        ret_ = "╔══[ 本機設定 ]"
                        if gp["autoAdd"] == True: ret_ += "\n╠ 自動加入好友 ✅"
                        else: ret_ += "\n╠ 自動加入好友 ❌"
                        if gp["autoLeave"] == True: ret_ += "\n╠ 自動退出副本 ✅"
                        else: ret_ += "\n╠ 自動退出副本 ❌"
                        if gp["autoRead"] == True: ret_ += "\n╠ 自動已讀 ✅"
                        else: ret_ += "\n╠ 自動已讀 ❌"
                        if gp["getmid"] == True: ret_ += "\n╠ 獲取友資詳情 ✅"
                        else: ret_ += "\n╠ 獲取友資詳情 ❌"
                        if gp["timeline"] == True: ret_ += "\n╠ 文章預覽 ✅"
                        else: ret_ += "\n╠ 文章預覽 ❌"
                        if gp["detectMention"] ==True: ret_+="\n╠ 標註偵測 ✅"
                        else: ret_ += "\n╠ 標註偵測 ❌"
                        if msg.toType==2:
                            ret_ += "\n╠══[ 本群設定 ]"
                            G = cl.getGroup(msg.to)
                            ret_ += "\n╠ 群組名稱 : {}".format(str(G.name))
                            if G.id in gp["protect"] : ret_+="\n╠ 踢人保護 ✅"
                            else: ret_ += "\n╠ 踢人保護 ❌"
                            if G.id in gp["qrprotect"] : ret_+="\n╠ 網址保護 ✅"
                            else: ret_ += "\n╠ 網址保護 ❌"
                            if G.id in gp["invprotect"] : ret_+="\n╠ 邀請保護 ✅"
                            else: ret_ += "\n╠ 邀請保護 ❌"
                            if G.id in gp["mention"] : ret_ += "\n╠ 群組狀況提示 ✅"
                            else: ret_ += "\n╠ 群組狀況提示 ❌"
                        ret_ += "\n╚[ 完 ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
            if sender in ban["owners"] and sender in ban["owners"]:
                if msg.text.lower().startswith("adminadd ") or msg.text.lower().startswith("add "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    if inkey not in ban["admin"] and inkey not in ban["blacklist"] and inkey not in ban["owners"]: 
                        ban["admin"].append(str(inkey))
                        cl.sendMessage(to, "獲得權限！")
                        json.dump(ban, codecs.open('bot/ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                elif msg.text.lower().startswith("admindel ") or msg.text.lower().startswith("del "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    if inkey in ban["admin"]:
                        ban["admin"].remove(str(inkey))
                        cl.sendMessage(to, "取消權限！")
                        json.dump(ban, codecs.open('bot/ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                elif text.lower() == 'lg':
                        groups = cl.groupsTalkException
                        ret_ = "[群組列表]"
                        no = 0 + 1
                        for gid in groups:
                            group = cl.getGroup(gid)
                            ret_ += "\n {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n[總共 {} 個群組]".format(str(len(groups)))
                        cl.sendMessage(to, str(ret_))
                elif text.lower() == 'restart':
                    cl.sendMessage(to, "重新啟動中...")
                    cl.sendMessage(to, "開始重啟")
                    restartBot()
                if text.lower() == 'restart':
                    cl.sendMessage(to, "重啟成功，請重新登入")
                    restartBot()
                
################################################################################################################################################
                    
                elif text.lower() == 'clear ban':
                    for mi_d in ban["blacklist"]:
                        ban["blacklist"] = {}
                    cl.sendMessage(to, "已清空黑名單")
                elif text.lower().startswith("tk "):
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    targets = []
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        if target in ban["owners"]:
                            pass
                        else:
                            try:
                                kicker=random.choice([k1,k2,k3,k4])
                                kicker.kickoutFromGroup(to,[target])
                            except:
                                pass
                elif text.lower() == 'cb' or text.lower() == 'chack ban':
                    gid = cl.getGroupIdsJoined() 
                    for i in gid:
                        group=cl.getGroup(i)
                        gMembMids = [contact.mid for contact in group.members] 
                        ban_list = [] 
                        for tag in ban["blacklist"]: 
                            ban_list += filter(lambda str: str == tag, gMembMids) 
                        if ban_list == []: 
                            cl.sendMessage(i, "沒有黑名單") 
                        else: 
                            for jj in ban_list: 
                                bot = random.choice([cl,k1,k2,k3,k4]) 
                                bot.kickoutFromGroup(i, [jj]) 
                            cl.sendMessage(i, "掃黑結束") 
                elif text.lower() == 'kill ban':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        matched_list = []
                        for tag in ban["blacklist"]:
                            matched_list+=filter(lambda str: str == tag, gMembMids)
                        if matched_list == []:
                            cl.sendMessage(to, "沒有黑名單")
                        else:
                            bot = random.choice([cl,k1,k2,k3,k4])
                            for jj in matched_list:
                                bot.kickoutFromGroup(to, [jj])
                            cl.sendMessage(to, "黑名單以踢除")
                elif text.lower().startswith("add "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    if inkey not in ban["admin"]:
                        ban["admin"].append(str(inkey))
                        cl.sendMessage(to, "已獲得權限！")
                    else:
                        cl.sendMessage(to,"already")
                elif text.lower().startswith("del "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    if inkey in ban["admin"]:
                        ban["admin"].remove(str(inkey))
                        cl.sendMessage(to, "已取消權限！")
                    else:
                    	cl.sendMessage(to,"user is not in admin")
                elif text.lower() == 'add':
                    wait["add"] = True
                    cl.sendMessage(to,"Please send a contact")
                elif text.lower() == 'del':
                    wait["del"] = True
                    cl.sendMessage(to,"Please send a Contact")
                elif text.lower().startswith("a "):
                    x = text.split(" ")
                    ban["admin"].append(x[1])
                    if len(x) ==2:
                        if x[1] not in ban["user"]:
                            ban["user"][x[1]] = 1
                            cl.sendMessage(to,"ok")
                        else:
                            ban["user"][x[1]] +=1
                            cl.sendMessage(to,"ok")
                    elif len(x) ==3:
                        if x[1] not in ban["user"]:
                            ban["user"][x[1]] = int(x[2])
                            cl.sendMessage(to,"ok")
                        else:
                            ban["user"][x[1]] +=int(x[2])
                            cl.sendMessage(to,"ok")
                    backupData()
                elif text.lower().startswith("ban "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ban["blacklist"][target] = True
                            cl.sendMessage(msg.to,"已加入黑單!")
                            break
                        except:
                            cl.sendMessage(msg.to,"添加失敗 !")
                            break
                elif text.lower().startswith("ban:"):
                    txt = text.replace("Ban:","")
                    try:
                        ban["blacklist"][txt] = True
                        cl.sendMessage(msg.to,"已加入黑單!")
                    except:
                        cl.sendMessage(msg.to,"添加失敗 !" +txt)
                elif text.lower().startswith("unban:"):
                    txt = text.replace("Unban:","")
                    try:
                        del ban["blacklist"][txt]
                        cl.sendMessage(msg.to,"已刪除黑單!")
                    except:
                        cl.sendMessage(msg.to,"刪除失敗 !" +txt)
                elif text.lower().startswith("unban "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ban["blacklist"][target] =False
                            cl.sendMessage(msg.to,"刪除成功 !")
                            break
                        except:
                            cl.sendMessage(msg.to,"刪除失敗 !")
                            break
                elif text.lower() == 'ban':
                    wait["ban"] = True
                    cl.sendMessage(to,"Please send a contact")
                elif text.lower() == 'unban':
                    wait["unban"] = True
                    cl.sendMessage(to,"Please send a Contact")
        if op.type == 25 or op.type ==26:
            msg = op.message
            if msg.contentType == 13:
                if wait["ban"] == True:
                    if msg._from in ban["owners"]:
                        if msg.contentMetadata["mid"] in ban["blacklist"]:
                           cl.sendmessage(msg.to,"already")
                           wait["ban"] = False
                        else:
                           ban["blacklist"][msg.contentMetadata["mid"]] = True
                           wait["ban"] = False
                           cl.sendMessage(msg.to,"成功新增黑單")
                elif wait["unban"] == True:
                    if msg._from in ban["owners"]:
                        if msg.contentMetadata["mid"] not in ban["blacklist"]:
                           cl.sendmessage(msg.to,"already")
                           wait["unban"] = False
                        else:
                           del ban["blacklist"][msg.contentMetadata["mid"]]
                           wait["unban"] = False
                           cl.sendMessage(msg.to,"成功移除黑單")
                elif wait["add"] == True:
                    if msg._from in ban["owners"]:
                        if msg.contentMetadata["mid"] in ban["admin"]:
                           cl.sendmessage(msg.to,"already")
                           wait["add"] = False
                        else:
                           ban["admin"].append(str(msg.contentMetadata["mid"]))
                           wait["add"] = False
                           cl.sendMessage(msg.to,"成功新增黑單")
                elif wait["del"] == True:
                    if msg._from in ban["owners"]:
                        if msg.contentMetadata["mid"] not in ban["admin"]:
                           cl.sendmessage(msg.to,"already")
                           wait["del"] = False
                        else:
                           ban["admin"].remove(str(msg.contentMetadata["mid"]))
                           wait["del"] = False
                           cl.sendMessage(msg.to,"成功移除黑單")
#                else:
#                    cl.sendMessage(msg.to,str(msg.contentMetadata["mid"]))
################################################################################################################################################
            if sender in ban["owners"]:
                if text.lower() == 'prompt on':
                    if msg.toType ==2:
                        G = cl.getGroup(msg.to)
                        gp["mention"][G.id] = True
                        cl.sendMessage(to, "群組狀況提示開啟")
                elif text.lower() == 'prompt off':
                    if msg.toType ==2 :
                        G = cl.getGroup(msg.to)
                        try:
                            del gp["mention"][G.id]
                            cl.sendMessage(to, "群組狀況提示關閉")
                        except:
                            cl.sendMessage(to, "群組狀況設定未開起")
                elif text.lower() == 'protect on':
                    if msg.toType ==2:
                        G = cl.getGroup(msg.to)
                        gp["protect"][G.id] = True
                        cl.sendMessage(to, "踢人保護開啟")
                elif text.lower() == 'protect off':
                    if msg.toType ==2 :
                        G = cl.getGroup(msg.to)
                        try:
                            del gp["protect"][G.id]
                            cl.sendMessage(to, "踢人保護關閉")
                        except:
                            cl.sendMessage(to, "目前沒有開喲")
                elif text.lower() == 'detect on':
                    gp["detectMention"] = True
                    cl.sendMessage(to, "已開啟標註偵測")
                elif text.lower() == 'detect off':
                    gp["detectMention"] = False
                    cl.sendMessage(to, "已開啟標註偵測")
                elif text.lower() == 'qrprotect on':
                    if msg.toType ==2:
                        G = cl.getGroup(msg.to)
                        gp["qrprotect"][G.id] = True
                        cl.sendMessage(to, "網址保護開啟")
                elif text.lower() == 'qrprotect off':
                    if msg.toType ==2 :
                        G = cl.getGroup(msg.to)
                        try:
                            del gp["qrprotect"][G.id]
                            cl.sendMessage(to, "網址保護關閉")
                        except:
                            cl.sendMessage(to, "未開起")
                elif text.lower() == 'invprotect on':
                    if msg.toType ==2:
                        G = cl.getGroup(msg.to)
                        gp["invprotect"][G.id] = True
                        cl.sendMessage(to, "邀請保護開啟")
                elif text.lower() == 'invprotect off':
                    if msg.toType ==2 :
                        G = cl.getGroup(msg.to)
                        try:
                            del gp["invprotect"][G.id]
                            cl.sendMessage(to, "邀請保護關閉")
                        except:
                            cl.sendMessage(to, "未開起")
                elif text.lower() == 'pro on':
                    if msg.toType ==2:
                        G = cl.getGroup(msg.to)
                        gp["protect"][G.id] = True
                        gp["qrprotect"][G.id] = True
                        gp["invprotect"][G.id] = True
                        cl.sendMessage(to, "踢人保護開啟")
                        cl.sendMessage(to, "網址保護開啟")
                        cl.sendMessage(to, "邀請保護開啟")
                elif text.lower() == 'pro off':
                    if msg.toType ==2:
                        G = cl.getGroup(msg.to)
                        try:
                            del gp["protect"][G.id]
                            cl.sendMessage(to, "踢人保護關閉")
                        except:
                            pass
                        try:
                            del gp["qrprotect"][G.id]
                            cl.sendMessage(to, "網址保護關閉")
                        except:
                            pass
                        try:
                            del gp["invprotect"][G.id]
                            cl.sendMessage(to, "邀請保護關閉")
                        except:
                            pass
#########################################################################################################
    except Exception as error:
        logError(error)
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
