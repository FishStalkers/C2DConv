import os
import shutil
import zipfile


class Unzipper:
    def __init__(self, file, targetdir="./unzipped"):
        self.file = file
        self.targetdir = targetdir
        self.outputdir = os.path.splitext(file)[0]
        self.errors = 0

    def unzip(self):
        self.unzipSingle()
        self.unzipRecursive()

        if self.errors > 0:
            print(f"Continuing without {self.errors} erring zip files")

    def unzipSingle(self):
        zip_ref = zipfile.ZipFile(self.file, "r")
        zip_ref.extractall(self.targetdir)
        zip_ref.close()

    def unzipRecursive(self):
        targetdir = os.path.join(self.targetdir, self.outputdir)

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
        shutil.rmtree(self.targetdir)
