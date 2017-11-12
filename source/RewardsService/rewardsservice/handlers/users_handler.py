import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class UsersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        db.users.remove()
        db.users.insert({
            "email": "bob@thebobsociety.com",
            "points": 101,
            "tier": "A",
            "tier_name": "5% off purchase",
            "next_tier": "B",
            "next_tier_name": "10% off purchase",
            "next_tier_progress": ".5",

            })
        users = list(db.users.find({}, {"_id": 0}))
        # self.write(json.dumps(users))
        url_args = self.request.path.split("/")
        if len(url_args) == 3:
            uid = int(url_args[2])
        self.write(json.dumps(users) + json.dumps(uid))
