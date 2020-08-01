'''''
Simple program that checks e-mail every 15 minutes for a torrent link, downloads
that torrent and sends confirmation sms after it's all done.
'''''

import schedule, imaplib, imapclient, pyzmail, subprocess, traceback
from twilio.rest import Client

imaplib._MAXLINE = 10000000

'''''
Sends sms using Twilio to desired phone number.
'''''
def smsConfirm():
    accountSID = 'xxx'
    authToken = 'xxx'
    twilioCli = Client(accountSID, authToken)
    myTwilioNumber = 'xxx'
    myCellPhone = 'xxx'
    message = twilioCli.messages.create(body='It\'s done, master.',
                                        from_=myTwilioNumber,
                                        to=myCellPhone)

'''''
Logs into an e-mail, checks for an e-mail with subject 'torrent', if password 
matches it opens torrent client with a link inside. In case of 
error traceback is written. At the end it deletes the e-mail.
'''''
def torrentDonwloader():
    try:
        imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
        imapObj.login('xxx', sys.argv[1])
        imapObj.select_folder('INBOX', readonly=False)
        UIDs = imapObj.search(['SUBJECT torrent'])
        rawMessages = imapObj.fetch(UIDs, ['BODY[]'])

        for rawMessage in rawMessages.items:
            message = pyzmail.PyzMessage.factory(rawMessage['BODY[]'])
            text = message.text_part.get_payload().decode\
                (message.text_part.charset)
            password = text['password']
            if password != 'xxx':
                continue
            link = text['link']
            qbProcess = subprocess.Popen(['C:\\Program Files (x86)\\'
                                              'qBittorrent\\'
                                              'qbittorrent.exe', link])
            qbProcess.wait()
            smsConfirm()

    except:
        errorFile = open('errorInfo.txt', 'a')
        errorFile.write(traceback.format_exc())
        errorFile.close()


    imapObj.delete_messages(UIDs)
    imapObj.expunge()
    imapObj.logout()

schedule.every(15).minutes.do(torrentDonwloader)