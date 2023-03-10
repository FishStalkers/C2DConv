import os


class Crawler:
    def __init__(self, startpath):
        self.startpath = startpath

    def crawlPaths(self):
        json_paths = []
        img_paths = []
        txt_paths = []
        for root, dirs, files in os.walk(self.startpath):
            for file in files:
                path = os.path.join(root, file)
                if file.endswith(".json"):
                    json_paths.append(path)
                elif file.endswith(".jpg"):
                    img_paths.append(path)
                elif file.endswith(".txt"):
                    txt_paths.append(path)
        return json_paths, img_paths, txt_paths
