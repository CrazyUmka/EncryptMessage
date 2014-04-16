__author__ = 'Grigory'
#coding:UTF-8
import os
import fnmatch


class PhotosUser(object):

    mask_file = '*.jpg'

    def __init__(self, dir_photos=r'C:\Users\Grigory\Pictures\Backgrounds Wallpapers Hd1'):
        self.dir = dir_photos
        self.photos_user = []

    def read_all_photos(self, directory=None):
        if directory == None:
            directory = self.dir
        for name in os.listdir(directory):
            path = os.path.join(directory, name)
            if os.path.isfile(path):
                if fnmatch.fnmatch(path, self.mask_file):
                    self.photos_user.append(path)
            else:
                self.read_all_photos(path)


if __name__ in '__main__':
    cwd = os.getcwdb()
    print("Вы находитесь в директории: " + str(cwd))
    # dir_photos = input("Выберите папку с фотографиями:")
    photos = PhotosUser()
    photos.read_all_photos()
    for path_photo in photos.photos_user:
        print(path_photo)
