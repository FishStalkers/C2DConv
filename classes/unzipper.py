import os
import shutil
import zipfile


class Unzipper:
    """
    Utility class that contains methods for unzipping a zip file and
    all inner zips.
    """

    def __init__(self, file, targetdir="./unzipped"):
        """
        Initialize new unzipper object.

        file: path of zip file to unzip
        targetdir: path of directory to unzip to, default is ./unzipped
        returns: None
        """
        self.file = file
        self.targetdir = targetdir
        self.errors = 0

    def unzip(self):
        """
        Driver function that unzips the initialized zip file and all inner
        zips. Prints errors and continues if any zip files fail to unzip.

        returns: None
        """
        self.unzipSingle()
        self.unzipRecursive()

        if self.errors > 0:
            print(f"Continuing without {self.errors} erring zip files")

    def unzipSingle(self):
        """
        Unzips the initialized zip file to the target directory.

        returns: None
        """
        zip_ref = zipfile.ZipFile(self.file, "r")
        zip_ref.extractall(self.targetdir)
        zip_ref.close()

    def unzipRecursive(self):
        """
        Crawls the target directory for zip files after the initial zip file
        has been unzipped. Unzips all found inner zip files and deletes them.

        returns: None
        """
        targetdir = os.path.join(self.targetdir, os.path.splitext(self.file)[0])

        for root, dirs, files in os.walk(targetdir):
            for file in files:
                if file.endswith(".zip"):
                    file_path = os.path.join(root, file)
                    out_path = os.path.join(root, os.path.splitext(file)[0])
                    try:
                        zip_ref = zipfile.ZipFile(file_path, "r")
                        zip_ref.extractall(out_path)
                        zip_ref.close()
                    except:
                        print("Error extracting file: " + file_path)
                        self.errors += 1
                    finally:
                        os.remove(file_path)

    def cleanup(self):
        """
        Removes the target directory and all files and directories within it.

        returns: None
        """
        shutil.rmtree(self.targetdir)
