import vk
import logging
import grequests
from vk_api_auth import login_to_api

logging.config.fileConfig('log.ini')
log = logging.getLogger('load_vk_images')

def save_to_folder(resp, folder, name):
    with open("%s/%s"%(folder, name), "wb") as f:
        for chunk in resp.iter_content(1024):
            f.write(chunk)

log.info("starting")
api = login_to_api(log)
user = api.users.get(user_ids='leraromashenko')[0]
log.info("got user: %s" % user)
photos = api.photos.getAll(owner_id=user["id"], count=30, photo_sizes=1)["items"]
log.info("got %s photos (%s...)" % (len(photos), photos[0]))

log.info("downloading images")
results = grequests.imap(grequests.get(p["sizes"][4]["src"], stream=True) for p in photos)
log.info("saving images")

for i, im in enumerate(results):
    if im != None:
        log.info("response for %s %s"% (im.url, im.status_code))
        log.info("saving image %s of %s" % (i + 1, len(photos)))
        save_to_folder(im, "imgs", "%s.jpg" % i)
    else:
        log.info("got None for request %s" % i)
