import twitter, os, time, sys, random
from random import randint


api=twitter.Api(consumer_key ='',
consumer_secret='',
access_token_key= '',
access_token_secret='')


LATESTFILE = 'dinosays_latest.txt'
LOGFILE = 'dinosays_log.txt'

os.chdir('/Users/Helen/twitter')

# possible replies
statuses = (' roarrrr!', ' RRROOOOAAAARRR!!!!', ' roar!', ' ROAR!',' RRRRRRRooooooaaaaaarrrr!!!!!', ' meow!', ' ROAR ROAR RRROOOOARRR!',' ROARRRR!')

# grab the last ID that the bot replied to, so it doesn't reply to earlier posts. (spam prevention measure)
if os.path.exists(LATESTFILE):
    fp = open(LATESTFILE)
    lastid = fp.read().strip()
    fp.close()

    if lastid == '':
        lastid = 0
else:
    lastid = 0

# read in the file of users we've already responded to
fp = open(LOGFILE)
alreadyMessaged = fp.readlines()
fp.close()
for i in range(len(alreadyMessaged)):
    if alreadyMessaged[i].strip() == '':
        continue

    alreadyMessaged[i] = alreadyMessaged[i].split('|')[1]
alreadyMessaged.append('DinosSayRoar') # don't reply to myself

# perform the search
results = api.GetSearch('dinosaurs', since_id=lastid)
print 'Found %s results.' % (len(results))
if len(results) == 0:
    print 'Nothing to reply to. Quitting.'
    sys.exit()
repliedTo = []
if len(results) > (len(statuses) * len(ment)):
    results = random.sample(results, (len(statuses) * len(ment)))



for statusObj in results:
    statusObj.created_at = statusObj.created_at[:-11] + statusObj.created_at[25:]
    postTime = time.mktime(time.strptime(statusObj.created_at, '%a %b %d %H:%M:%S %Y'))

    if time.time() - (24*60*60) < postTime and statusObj.user.screen_name not in alreadyMessaged and '@DinosSayRoar' not in statusObj.text.lower():
        if [True for x in alreadyMessaged if ('@' + x).lower() in statusObj.text.lower()]:
            print 'Skipping because it\'s a mention: @%s - %s' % (statusObj.user.screen_name.encode('ascii', 'replace'), statusObj.text.encode('ascii', 'replace'))
            continue

        try:
            print 'Posting in reply to @%s: %s' % (statusObj.user.screen_name.encode('ascii', 'replace'), statusObj.text.encode('ascii', 'replace'))
            api.PostUpdate('@%s' % (statusObj.user.screen_name) + statuses[randint(1, len(statuses))] , in_reply_to_status_id=statusObj.id)
            repliedTo.append( (statusObj.id, statusObj.user.screen_name, statusObj.text.encode('ascii', 'replace')) )
            time.sleep(1)
        except Exception:
            print "Unexpected error:", sys.exc_info()[0:2]


fp = open(LATESTFILE, 'w')
fp.write(str(max([x.id for x in results])))
fp.close()

fp = open(LOGFILE, 'a')
fp.write('\n'.join(['%s|%s|%s' % (x[0], x[1], x[2]) for x in repliedTo]) + '\n')
fp.write('\n')
fp.close()
