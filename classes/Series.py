from classes.Media import Media


class Series(Media):
    def __init__(self, name, video_ids):
        super().__init__(name)
        self._video_ids = video_ids

    @property
    def video_ids(self):
        return self._video_ids

    @video_ids.setter
    def video_ids(self, video_ids):
        self._video_ids = video_ids

    def to_db_format(self):
        return {
            'name': self._name,
            'video_ids': self._video_ids
        }