import os


class Crawler:
    """
    General purpose crawler class for crawling directories for json, image and txt files.
    Can be used to crawl any file structures.
    """

    def __init__(self, startpath):
        """
        Initialize new crawler object.

        startpath: path of directory crawl
        returns: None
        """
        self.startpath = startpath

    def crawlPaths(self):
        """
        Crawls the initialized directory for json, image and txt files.

        returns: lists of json, image and txt file paths in a tuple of the form (json_paths, img_paths, txt_paths)
        """
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
