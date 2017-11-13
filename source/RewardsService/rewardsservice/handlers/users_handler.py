import json
import tornado.web
import pymongo

from pymongo import MongoClient
from tornado.gen import coroutine


class UsersHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        # If we were building a public API, this would need to be adjusted
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8000")
        # Chrome sends an OPTIONS request before the PUT request
        # The options() method should handle this, but this will get things working for now
        self.set_header("Access-Control-Allow-Methods", "OPTIONS, GET, PUT")

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
            # db.users.remove()
            # db.users.insert_one({
            #     "email": "jimbob@thebobsociety.com",
            #     "points": 102,
            #     "tier": "A",
            #     "tier_name": "5% off purchase",
            #     "next_tier": "B",
            #     "next_tier_name": "10% off purchase",
            #     "next_tier_progress": ".5",
            #
            #     })
            # db.users.insert_one({
            #     "email": "bobby@thebobsociety.com",
            #     "points": 102,
            #     "tier": "A",
            #     "tier_name": "5% off purchase",
            #     "next_tier": "B",
            #     "next_tier_name": "10% off purchase",
            #     "next_tier_progress": ".5",
            #
            #     })
            # db.users.insert_one({
            #     "email": "bob@thebobsociety.com",
            #     "points": 103,
            #     "tier": "A",
            #     "tier_name": "5% off purchase",
            #     "next_tier": "B",
            #     "next_tier_name": "10% off purchase",
            #     "next_tier_progress": ".5",
            #
            #     })
            # db.users.insert_one({
            #     "email": "robert@thebobsociety.com",
            #     "points": 101,
            #     "tier": "A",
            #     "tier_name": "5% off purchase",
            #     "next_tier": "B",
            #     "next_tier_name": "10% off purchase",
            #     "next_tier_progress": ".5",
            #
            #     })
            users = list(db.users.find(query, {"_id": 0}))
            self.write(json.dumps(users))

    @coroutine
    def put(self):
        total = self.get_body_argument('total');
        if (int(total) < 0):
            return
        url_args = self.request.path.split("/")
        if len(url_args) != 3:
            return

        points = int(total) #no credit for cents
        email = url_args[2]

        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        query = {"email":email}
        user = db.users.find_one(query, {"_id": 0})
        new_points = int(user['points']) + points

        # Defaults / out of range fillers
        # highest_achieved = {"rewardName": "None", "tier": "None", "points":})
        # next_tier = {"rewardName": "None", "tier": "None"})


        # Get best matching tier
        for r in db.rewards.find({'points': {'$lt': new_points}}, {"_id": 0}).sort("points",pymongo.DESCENDING).limit(1):
            highest_achieved = r
        for r in db.rewards.find({'points': {'$gt': new_points}}, {"_id": 0}).sort("points",pymongo.ASCENDING).limit(1):
            next_tier = r

        if next_tier['rewardName'] == 'None':
            progress = 'None'
        else :
            progress = '.1'


        new_data = {
            'points':new_points,
            "tier": highest_achieved['tier'],
            "tier_name": highest_achieved['rewardName'],
            "next_tier": next_tier['tier'],
            "next_tier_name": next_tier['rewardName'],
            "next_tier_progress": ".5", #@todo
        }
        db.users.update_one(query, {'$set': new_data})

        self.write(json.dumps(new_data))
        # self.write(json.dumps({"put":"ok","oldpts":points,"newpts":new_points}))


    @coroutine
    def options(self):
        return None
