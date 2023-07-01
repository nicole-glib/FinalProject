from classes.Media import Media
from pymongo import MongoClient
import gridfs

client = MongoClient('localhost', 27017)

db = client.ElinoysDB

fs = gridfs.GridFS(db)

movies_col = db.Movies

class Movie(Media):
    def __init__(self, name, video_id):
        super().__init__(name)
        self.video_id = video_id

    def delete_movie(self):
        fs.delete(self.video_id)
        movies_col.delete_one({'video_id': self.video_id})
