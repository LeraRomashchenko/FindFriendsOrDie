import sqlite3


class PeopleSqlite:
    def __init__(self, filename, log):
        self.log = log
        self.conn = sqlite3.connect(filename)
        c = self.conn.cursor()
        log.info("creating tables if not exist")
        c.execute("create table if not exists people"
                  "("
                  "person_id int primary key,"
                  "is_loaded int"
                  ")")
        c.execute("create table if not exists friends"
                  "("
                  "person_id int,"
                  "friend_id int,"
                  "unique (person_id, friend_id)"
                  ")")
        c.execute("create table if not exists images"
                  "("
                  "image_id integer primary key,"  # integer primary keys auto-increment (int ones don't)
                  "person_id int,"
                  "image_url text,"
                  "is_recognized int,"
                  "unique (person_id, image_url)"
                  ")")
        c.execute("create table if not exists faces"
                  "(image_id int, features text)")
        log.info("tables: %s", self.stat())
        self.conn.commit()

    def add_unloaded_person(self, person_id):
        c = self.conn.cursor()
        c.execute("insert or ignore into people (person_id, is_loaded) values (?, 0)", [person_id])
        self.conn.commit()

    def get_unloaded_people_ids(self, top_n):
        c = self.conn.cursor()
        return (id for (id,) in c.execute("select person_id from people where is_loaded = 0 "
                                          "order by rowid limit ?", [top_n]))

    def get_unrecognized_images(self, top_n):
        c = self.conn.cursor()
        return ((img_id, url) for (img_id, url) in
                c.execute("select image_id, image_url from images "
                          "where is_recognized = 0 order by rowid limit ?",
                          [top_n]))

    def add_faces(self, img_id, faces_features):
        c = self.conn.cursor()
        self.log.info("adding %s faces from %s" % (len(faces_features), img_id))
        c.execute("update images set is_recognized = 1 where image_id = ?", [img_id])
        c.executemany("insert into faces (image_id, features) values (?, ?)",
                      list((img_id, ",".join("%.3g" % round(f, 2) for f in face_features))
                           for face_features in faces_features))
        self.conn.commit()

    def load_people(self, people):
        c = self.conn.cursor()
        self.log.info("loading %s people" % (len(people)))
        c.executemany("update people set is_loaded = 1 where person_id = ?", ((p["id"],) for p in people))
        c.executemany("insert or ignore into friends (person_id, friend_id) values (?, ?)",
                      ((p["id"], fid) for p in people for fid in p["friends"]))
        c.executemany("insert or ignore into images (person_id, image_url, is_recognized) values (?, ?, 0)",
                      ((p["id"], url) for p in people for url in p["images"]))
        c.executemany("insert or ignore into people (person_id, is_loaded) values (?, 0)",
                      ((fid,) for p in people for fid in p["friends"]))
        self.conn.commit()

    def dump(self):
        c = self.conn.cursor()
        return {
            'people': list(c.execute("select * from people")),
            'friends': list(c.execute("select * from friends")),
            'images': list(c.execute("select * from images")),
            'faces': list(c.execute("select * from faces")),
        }

    def stat(self):
        c = self.conn.cursor()
        return {
            'loaded': list(c.execute("select count(distinct person_id) from people where is_loaded = 1"))[0][0],
            'unloaded': list(c.execute("select count(distinct person_id) from people where is_loaded = 0"))[0][0],
            'images': list(c.execute("select count(image_url) from images"))[0][0],
            'images_dist': list(c.execute("select count(distinct image_url) from images"))[0][0],
            'friends': list(c.execute("select count(*) from friends"))[0][0]
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
