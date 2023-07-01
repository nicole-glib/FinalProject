from classes.Media import Media


class Movie(Media):
    def __init__(self, name, video_id):
        super().__init__(name)
        self._video_id = video_id

    @property
    def video_id(self):
        return self._video_id

    @video_id.setter
    def video_id(self, id):
        self._video_id = id

    def to_db_format(self):
        return {
            'name': self._name,
            'video_id': self._video_id
        }

