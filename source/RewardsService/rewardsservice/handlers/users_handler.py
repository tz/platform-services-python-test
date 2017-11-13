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
            users = list(db.users.find(query, {"_id": 0}))
            self.write(json.dumps(users))

    @coroutine
    def put(self):
        total = self.get_body_argument('total');
        if (int(float(total)) < 0):
            total = 0   #we'll make the record anyway
        url_args = self.request.path.split("/")
        if len(url_args) != 3:
            return

        points = int(float(total)) #no credit for cents
        email = url_args[2]

        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        query = {"email":email}
        user = db.users.find_one(query, {"_id": 0})
        if user is None:
            new_points = points
            db.users.insert_one({
                "email": email,
                "points": 0,
                })
        else:
            new_points = int(user['points']) + points

        #Hack -- for some reason these reward tiers are getting deleted. Not sure why.
        r = db.rewards.find({'rewardName':'None'})
        if r.count() == 0:
            db.rewards.insert({"points": -1, "rewardName": "None", "tier": "None", "placeholder": "True"})
            db.rewards.insert({"points": 999999999999999, "rewardName": "None", "tier": "None", "placeholder": "True"})

        # Get best matching tier
        for r in db.rewards.find({'points': {'$lte': new_points}}, {"_id": 0}).sort("points",pymongo.DESCENDING).limit(1):
            highest_achieved = r
        for r in db.rewards.find({'points': {'$gt': new_points}}, {"_id": 0}).sort("points",pymongo.ASCENDING).limit(1):
            next_tier = r

        if next_tier['rewardName'] == 'None' or new_points == 0:
            progress = 0
        else:
            progress = (new_points - highest_achieved['points'])/(next_tier['points'] - highest_achieved['points'])
            progress = round(progress*100) #return a %

        new_data = {
            'points':new_points,
            "tier": highest_achieved['tier'],
            "tier_name": highest_achieved['rewardName'],
            "next_tier": next_tier['tier'],
            "next_tier_name": next_tier['rewardName'],
            "next_tier_progress": progress,
        }
        db.users.update_one(query, {'$set': new_data})

        self.write(json.dumps({"put":"ok", "ha": highest_achieved, "nt":next_tier}))


    @coroutine
    def options(self):
        return None
