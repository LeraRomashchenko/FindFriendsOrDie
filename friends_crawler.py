import logging
import vk_api_auth
import time
from people_sqlite import PeopleSqlite

# noinspection PyUnresolvedReferences
logging.config.fileConfig('log.ini')
log = logging.getLogger('crawler')

def get_friends(user_ids):
    log.info("getting friends, sleeping 1 sec")
    time.sleep(1)
    req = """
        var res = [];
        var ids = [%s];
        var i = 0;
        while (i < ids.length) {
            res.push({
                id: ids[i],
                friends: API.friends.get({user_id: ids[i]}).items,
                images: API.photos.getAll({owner_id: ids[i]}).items@.photo_130
            });
            i = i + 1;
        }
        return res;
    """ % ",".join(map(str, user_ids))
    result = api.execute(code=req)
    if result:
        people = [{
            "id": p["id"] or [],
            "friends": p["friends"] or [],
            "images": p["images"] or []
        } for p in result]
        log.info("got response: %s people, %s friends, %s images" % (len(people), sum(len(p["friends"]) for p in people), sum(len(p["images"]) for p in people)))
        return people
    else:
        log.info("got no response: %s" % result)
        raise Exception("got no response")


api = vk_api_auth.login_to_api(log)
log.info("starting")

with PeopleSqlite("people.db", log) as db:
    db.add_unloaded_person(58071469)
    while True:
        top_10_unloaded = db.get_unloaded_people_ids(10)
        if not top_10_unloaded:
            # we've downloaded the whole vk
            break
        friends = get_friends(top_10_unloaded)
        db.load_people(friends)
        log.info("%s people in db" % db.stat())

    log.info("end")
