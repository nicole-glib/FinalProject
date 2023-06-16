from classes.Media import Media


class Movie(Media):
    def __init__(self, name, video_id):
        super().__init__(name)
        self.video_id = video_id