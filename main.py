import os.path
import shutil
from threading import Thread


class File:
    def __init__(self, path: str):
        self.path = path
        self.name, self.extention = os.path.splitext(os.path.basename(path))
        self.create = os.path.getctime(path)

    def remove_to_folder(self, folder: str):
        full_name = self.name + self.extention
        if not os.path.exists(folder):
            os.mkdir(folder)
        destination = os.path.join(folder, full_name.lower())
        shutil.move(self.path, destination)

    def delete(self):
        os.remove(self.path)


class Folder:
    def __init__(self, path: str):
        self.path = path
        self.name = os.path.basename(path)
        self.create = os.path.getctime(path)


    def get_files(self) -> list[File]:
        files = []
        for root, _, filenames in os.walk(self.path):
            for filename in filenames:
                path = os.path.join(root, filename)
                files.append(File(path))
        return files

    def move_files_to_folder(self):
        threads = []
        files= self.get_files()
        for file in files:
            thread = Thread(target= file.remove_to_folder, args=(os.path.join(self.path, file.extention), ), name = str(file))
            thread.start()
            threads.append(thread)
        for thread in threads:
            print(thread.name)
            thread.join()



class Sorter:
    def __init__(self, folder:Folder):
        self.folder = folder

    def sort_files(self):
        self.folder.move_files_to_folder()



if __name__ == "__main__":
    folder = Folder("/Users/isinka/PycharmProjects/clean_bot/thrash")
    processor = Sorter(folder)
    processor.sort_files()


