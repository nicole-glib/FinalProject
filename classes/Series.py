from classes.Media import Media


class Series(Media):
    def __init__(self, name, video_ids):
        super().__init__(name)
        self.video_ids = video_ids