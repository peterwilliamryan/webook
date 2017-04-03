import requests
from beam import User
from time import sleep

POLL_INTERVAL = 10

STREAMERS = ["outcast", "towe102", "sonicman809"]
TEAMIDS = ["1748"]



discord_webhook ="https://discordapp.com/api/webhooks/XXXXXXXXXXXXXXXXX/XXXXXXXXXXXXXX?wait=true"


def checkUsers(streamers):
    try:
        f = open("./.beam-checker","r")
        online = f.read().strip().split(",")
        f.close()
    except IOError:
        online = []
    for u in streamers:
        if u.info['channel']['online'] and u.info["username"] not in online:
            online.append(u.info["username"])
            print "{} is online".format(u.info["username"])
            requests.post(discord_webhook, json={
                'content': "@here {} is now online: http://beam.pro/{}".format(u.info["username"], u.info["username"])
            })
        else:
            if not u.info['channel']['online'] and u.info["username"] in online:
                print "{} is offline".format(u.info["username"])
                online.remove(u.info["username"])

    f = open("./.beam-checker", "w")
    f.write(",".join(x for x in online))
    f.close()

def main():

    try:
        while True:
            check_users = []
            if TEAMIDS is not None:
                for team in TEAMIDS:
                    for u in User.getTeamUsers(team):
                        check_users.append(User(info=u))

            if len(STREAMERS) > 0:
                for s in STREAMERS:
                    check_users.append(User(s))

            checkUsers(check_users)
            sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        exit()


if __name__ == "__main__":
    main()
