#! /usr/bin/env python3.5

# Script for sending email notification for new tweet from python list of users #Stalking
# By Aleksandar Josifoski https://twitter.com/josifsk; https://frutarian-travellers.blogspot.mk; josifoski@gmail.com;
# 2018 January 21; February 4;
# Script is (*) depending (*) on using tweepy python module for twitter connection
# Most easy way to install from command line: pip3 install -U tweepy
# (*) as me for stalking not only tweets using tweetcaster app but also + replies from Lady Tar♡n https://twitter.com/tarynsouthern (*)
# Licence TA
# For local/server use

import tweepy
import re
import time
import codecs
import smtplib
import os
import sys
import datetime

# dir_in is input directory (where for example script is placed), change it accordingly
dir_in = "/home/ntra/Desktop/11QueenTar♡nJosifoski/tw_ins_fb_yt_notifiers/"

log = codecs.open(dir_in + 'twit_notifier_log.txt', 'a', 'utf-8')
nowlong = str(datetime.datetime.now())[:16].replace('-', '')

fnamehistoryid = "twit_notifier_historyid.txt"
if os.path.exists(dir_in + fnamehistoryid):
    fhis = codecs.open(dir_in + fnamehistoryid, "r", "utf-8")
    lhis = fhis.readlines()
    fhis.close()
    for index in range(len(lhis)):
        lhis[index] = lhis[index].strip()
    fhis = codecs.open(dir_in + fnamehistoryid, "a", "utf-8")
else:
    fhis = codecs.open(dir_in + fnamehistoryid, "w", "utf-8")
    lhis =  []

# To use program accordingly, you'll have to own twitter api keys, and here's how...
# If not already having twitter api keys, you can create new ones at https://apps.twitter.com (if you already have them
# you'll need only to see if permissions are set accordingly)
# This is once only, hit on Create New App, also important is your twitter account to have valid connnection with mobile,
# to have access to direct messages feature. (Meaning, twitter gives write/DM possibility only if you are real human with
# defined mobile in twitter settings. Program is with nothing android/iOS related)
# Give Application Details some Name, Description, for Website put https://google.com, skip Callback URL
# click on checkbox, Yes, I have read.. and hit on Create your Twitter application
# From there, click on Permissions and set them to Read, Write and Access direct messages, then going little down 
# hit Update Settings. Then from up menu click on Keys and Access Tokens
# Place Consumer Key (API Key), Consumer Secret (API Secret), Access Token, Access Token Secret in 
# first 4 lines in twitappkeys.dat file (you'll need to create it), and place twitappkeys.dat in same directory 
# where twit_notifier.py is
with codecs.open(dir_in + 'twitappkeys.dat', 'r', 'utf-8') as fkeys:
    lfkeys = fkeys.readlines()
    consumer_key = lfkeys[0].strip()
    consumer_secret = lfkeys[1].strip()
    access_key = lfkeys[2].strip()
    access_secret = lfkeys[3].strip()

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
print(nowlong + ' authenticated yes')
log.write(nowlong + ' authenticated yes' + os.linesep)

def strip_nasty_characters(input):
    if input:
        try:
            # Wide UCS-4 build
            myre = re.compile(u'['
            u'\U0001F300-\U0001F64F'
            u'\U0001F680-\U0001F6FF'
            u'\u2600-\u26FF\u2700-\u27BF]+',
            re.UNICODE)
        except re.error:
            # Narrow UCS-2 build
            myre = re.compile(u'('
            u'\ud83c[\udf00-\udfff]|'
            u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
            u'[\u2600-\u26FF\u2700-\u27BF])+',
            re.UNICODE)
        input = re.sub(myre, "", input)
    return input
    
# sending email credentials
# Change credentials accordingly, for sending email SMTP service will be needed.
# I personally have good experience with smtp2go.com
# You can use other smtp server, if you decide to use smtp2go, then you'll need to create
# zimsmtp2go.dat file and put smtp password there in first line
email_address_from = 'your_trivial_email@somewhere.com'
email_address_to = ['your_receive_email@yahoo.com']
password = open(dir_in + 'zimsmtp2go.dat').read().strip()
password = password.strip()
smtpServer = 'mail.smtp2go.com'
port = '587'

def sendemailnotify(lvsmtpServer, lvport, lvemail_address_from, lvpassword, lvemail_address_to):
    ''' function for sending email '''
    try:
        smtpObj = smtplib.SMTP(lvsmtpServer, lvport)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()
        smtpObj.login(lvemail_address_from, lvpassword)
    except Exception as esc:
        print(str(esc))
        log.write(nowlong + ' ' + str(esc) + os.linesep)

    listemail_address_to = lvemail_address_to

    FROM = lvemail_address_from
    TO =  listemail_address_to
    SUBJECT = 'New tweet from %s ' % cusers
    TEXT = 'New tweet from %s ' % cusers
    message = 'Subject: %s\n\n%s' % (SUBJECT, TEXT)

    try:
        smtpObj.sendmail(FROM, TO, message)
        print('message: ' + message + os.linesep + 'Notification email sent.')
        smtpObj.quit()
        
        log.write(nowlong + ' sucessfully email sent ')
        log.write('to: ' + str(email_address_to) + os.linesep)
    except Exception as esc:
        print(str(esc))
        log.write(nowlong + ' problem while sending email!' + os.linesep)

def get_tweets(user, num_of_tweets):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = user,count = num_of_tweets)

    ltweets = []
    for tweet in new_tweets:
        ltweets.append(tweet.id_str)

    return ltweets

def main():
    ''' main function '''
    global input_user
    global cusers
    global fhis
    global lnot
    bnew = False
    cusers = ''
    # refresh input_list, you can change twit_notifier_list.txt even while program is running
    input_list = []
    finput = codecs.open(dir_in + 'twit_notifier_list.txt', 'r', 'utf-8')
    for line in finput:
        if line.strip() != '':
            input_list.append(line.strip())
    finput.close()
    for input_user in input_list:
        print(input_user)
        log.write(nowlong + ' ' + input_user + os.linesep)
        l = get_tweets(input_user, 1)
        bpass = True
        for id in l:
            idmem = id
            if id in lhis:
                bpass = False
                
        if bpass:
            bnew = True
            cusers += input_user + ','
            # new tweet, save in fhis
            fhis.write(idmem + os.linesep)
            lhis.append(idmem)
    
    fhis.close()
    fhis = codecs.open(dir_in + fnamehistoryid, "a", "utf-8")
    cusers = cusers.strip(',')
    
    # refresh twit_notifier_ns.txt First line 1 for sending notification on laptop 0 not, second line 1 for sending email notification 0 not
    fns = codecs.open(dir_in + "twit_notifier_ns.txt", "r", "utf-8")
    lnot = fns.readlines()
    fns.close()    
    
    # if there is new tweet from any tracked users send notification email
    if bnew:
        # Following os.system("notify-send -t 5000000 '%s'" % notifystring) command is for sending notification also on computer
        # It's linux based, if you use other system, then set it as comment (or change script accordingly?)
        notifystring = 'tweet: ' + cusers
        if lnot[0].strip() == "1":
            os.system("notify-send -t 1100 '%s'" % notifystring)        
        if lnot[1].strip() == "1":
            sendemailnotify(smtpServer, port, email_address_from, password, email_address_to)

if __name__ == '__main__':
    while True:
        nowlong = str(datetime.datetime.now())[:16].replace('-', '')
        main()
        print('sleeping 2 min')
        log.close()
        log = codecs.open(dir_in + 'twit_notifier_log.txt', 'a', 'utf-8')
        time.sleep(120)
