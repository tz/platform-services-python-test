import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class UsersHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        # If we were building a public API, this would need to be adjusted
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8000")

    @coroutine
    def get(self):
        if self.request.method == "GET":
            url_args = self.request.path.split("/")
            query = {}
            if len(url_args) == 3:
                email = url_args[2]
                query = {"email":email}

            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            db.users.remove()
            db.users.insert({
                "email": "jimbob@thebobsociety.com",
                "points": 102,
                "tier": "A",
                "tier_name": "5% off purchase",
                "next_tier": "B",
                "next_tier_name": "10% off purchase",
                "next_tier_progress": ".5",

                })
            db.users.insert({
                "email": "bobby@thebobsociety.com",
                "points": 102,
                "tier": "A",
                "tier_name": "5% off purchase",
                "next_tier": "B",
                "next_tier_name": "10% off purchase",
                "next_tier_progress": ".5",

                })
            db.users.insert({
                "email": "bob@thebobsociety.com",
                "points": 103,
                "tier": "A",
                "tier_name": "5% off purchase",
                "next_tier": "B",
                "next_tier_name": "10% off purchase",
                "next_tier_progress": ".5",

                })
            db.users.insert({
                "email": "robert@thebobsociety.com",
                "points": 101,
                "tier": "A",
                "tier_name": "5% off purchase",
                "next_tier": "B",
                "next_tier_name": "10% off purchase",
                "next_tier_progress": ".5",

                })
            users = list(db.users.find(query, {"_id": 0}))
            self.write(json.dumps(users))
        elif self.request.method == "PUT":
            self.write(json.dumps(self.request))
        else:
            self.write(json.dumps({"error":"404"}))
