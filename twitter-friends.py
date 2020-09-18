import tweepy
import sqlite3

conn = sqlite3.connect('./friends_twitter.sqlite')
cur = conn.cursor()

cur.executescript(
    '''
        CREATE TABLE IF NOT EXISTS People(
        id INTEGER PRIMARY KEY ,
        name TEXT UNIQUE ,
        retrieved INTEGER 
    );
    
    CREATE TABLE IF NOT EXISTS Follows(
    from_id INTEGER ,
    to_id INTEGER ,
    UNIQUE (from_id, to_id)
    )
    '''
)

keys = {}
with open('../Keys/keys.txt') as k:
    for line in k:
        split = line.split(":")
        keys[split[0]] = split[1].strip()

auth = tweepy.OAuthHandler(keys['API key'], keys['API key secret'])
auth.set_access_token(keys['Access token'], keys['Access token secret'])

api = tweepy.API(auth)

while True:
    acct = input("Enter the users screen_name or 'quit': ")
    if acct == 'quit':
        break
    if len(acct) < 1:
        cur.execute('SELECT id, name FROM People WHERE retrieved=0 LIMIT 1')
        try:
            (id, acct) = cur.fetchone()
        except:
            print('No un-retrieved twitter account found')
            continue
    else:
        cur.execute('SELECT id FROM People WHERE name = ? LIMIT 1', (acct,))
        try:
            id = cur.fetchone()[0]
        except:
            cur.execute('INSERT OR IGNORE INTO People (name, retrieved) VALUES (?, 0)', (acct,))
            conn.commit()
            if cur.rowcount != 1:
                print('Error inserting account:', acct)
                continue
            id = cur.lastrowid

    try:
        friends = tweepy.Cursor(api.friends, acct)
        cur.execute('UPDATE People SET retrieved = 1 WHERE name=?', (acct,))
    except:
        print('Cannot retrieve the account:', acct)
        break

    countnew = 0
    countold = 0
    try:
        for friend in friends.items(100):
            print(friend.screen_name)
            cur.execute('SELECT id FROM People WHERE name = ? LIMIT 1', (friend.screen_name,))
            try:
                friend_id = cur.fetchone()[0]
                countold += 1
            except:
                cur.execute('INSERT OR IGNORE INTO People (name, retrieved) VALUES (?, 0)', (friend.screen_name, ))
                conn.commit()
                if cur.rowcount != 1:
                    print("Error inserting account:", friend.screen_name)
                    continue
                friend_id = cur.lastrowid
                countnew += 1
            cur.execute('INSERT OR IGNORE INTO Follows (from_id, to_id) VALUES (?, ?)', (id, friend_id))
            print('New Accounts =', countnew, '| Revisited=', countold)
            conn.commit()
    except tweepy.error.RateLimitError:
        print("Rate Limit Exceeded, please try again later...\t:(")
        quit()

cur.close()
