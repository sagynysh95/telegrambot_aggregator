from pymongo import MongoClient
from datetime import datetime


db_client = MongoClient("mongodb://localhost:27017/")

current_db = db_client["mongo_db"]
collection = current_db["data"]


async def toDatetime(date):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")


async def func1(start, end, group):
    global query
    if group == "month":
        query = collection.aggregate([
            {"$match": {
                "dt": {"$gte": start, "$lte": end}
            }},
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-01T00:00:00", "date": "$dt"}},
                "total": {"$sum": "$value"}
            }},
            {"$sort": {"_id": 1}}
        ])
    elif group == "day":
        query = collection.aggregate([
            {"$match": {
                "dt": {"$gte": start, "$lte": end}
            }},
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%dT00:00:00", "date": "$dt"}},
                "total": {"$sum": "$value"}
            }},
            {"$sort": {"_id": 1}}
        ])
    elif group == "hour":
        query = collection.aggregate([
            {"$match": {
                "dt": {"$gte": start, "$lte": end}
            }},
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%dT%H:00:00", "date": "$dt"}},
                "total": {"$sum": "$value"}
            }},
            {"$sort": {"_id": 1}}
        ])

    data_dict = {"dataset": [], "labels": []}
    # data_dict[] = []
    # data_dict["labels"] = []

    for i in query:
        date = await toDatetime(i["_id"])
        data_dict["dataset"].append(i["total"])
        data_dict["labels"].append(date.isoformat())

    return data_dict
