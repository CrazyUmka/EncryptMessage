__author__ = 'Grigory'
#coding: UTF-8

import vk
import getpass
import sys
from work_dir import PhotosUser
from steganography_jpeg import JpegDecode, DecryptError
import requests


class QueryError(Exception):
    pass


class EmailError(Exception):
    pass


class UserQuery(object):
    def __init__(self):
        self.lib_vk = UserQuery._connect_vk()
        self.photo_user = UserQuery._library_image()

    @staticmethod
    def _connect_vk():
        print u'Welcome!\nSetup project!!!\nFirst step: 1.Connect profile vk!'
        user_name = raw_input(u'Email: ').decode('utf8')
        try:
            UserQuery._test_correct_email(user_name)
        except EmailError as message:
            print message
            print u"Correct your personal data"
            choice = raw_input(u'Exit program or repeat?(y/n): ').decode('utf8')
            if not u'y' in choice:
                sys.exit()
            else:
                UserQuery._connect_vk()

        password = getpass.getpass().decode('utf8')
        print u'Connect API VK APP... Please wait...'
        try:
            lib_vk = vk.VK(user_name, password)
            print u'Connected established.'
            print u'Get list your friends... Please wait...'
            lib_vk.friends_get()
            print u'Status OK...'
            return lib_vk
        except vk.VKError as message:
            print message
            print u"Correct your personal data or repeat query server"
            choice = raw_input(u'Exit program or repeat?(y/n): ').decode('utf8')
            if not u'y' in choice:
                sys.exit()
            else:
                UserQuery._connect_vk()

    @staticmethod
    def _library_image():
        print u'\nNext step setup!'
        library = raw_input(u'2.Enter image library: ').decode('utf8')
        work_lib = PhotosUser(library)
        work_lib.read_all_photos()
        return work_lib

    def user_menu(self):
        list_command = [self._send_message, self._get_message, sys.exit]
        print u'Setup Successful.'
        while True:
            choice = raw_input(
                u'\nMenu Project:\n1.Send message encryption JPEG file\n2.Decryption message\n3.Exit\nYour choice: ').decode('utf8')
            if not choice in (u'1', u'2', u'3'):
                print u'Enter number: 1, 2 or 3'
            else:
                index_command = int(choice) - 1
                list_command[index_command]()

    def _get_message(self):
        print u'Получаю ваши сообщения, пожалуйста подождите...'
        messages = self.lib_vk.message_get()
        print u'Операция выполнена...\n'
        count_content = len(messages[u'message_content'])
        print u'Сообщения({0}):'.format(len(messages[u'message']))
        print u'\tКоличество непрочитанных сообщений: {0}'.format(messages[u'count_unread'])
        print u'\tКоличество сообщений с медиа-контентом: {0}'.format(count_content)
        if count_content != 0:
            choice = raw_input(u'\nХотите скачать медиа-контент сообщений?(y/n)')
        else:
            print u'У вас нет недавно полученного медиа-контента. Извиняй!!!\n\tПопробуй сделать что-нибудь другое;)'
        if choice in u'y':
            UserQuery.download_content(messages[u'message_content'][0][u'attachments'])

    @staticmethod
    def download_content(content):
        dir_download = u'C:\\Users\\Grigory\\Downloads\\'
        list_files = []
        print u'\n...Загрузка контента...'
        print u'\tКоличество медиа-файлов в сообщении: {0}'.format(len(content))
        for media_file in content:
            document = media_file.get(u'doc')
            if document != None:
                url = document.get(u'url')
                name_file = document.get(u'title')
                list_files.append(dir_download + name_file)
                if url != None:
                    print u'\n\tНачинаю загрузку файла: {0}'.format(name_file)
                    r = requests.get(url)
                    file_load = open(dir_download + name_file, 'wb')
                    file_load.write(r.content)
                    file_load.close()
                    print u'\tЗагрузка завершена...'
        for file_doc in list_files:
            try:
                JpegDecode.decrypt_message(file_doc)
            except DecryptError as msg:
                print msg


    def _send_message(self):
        count = 0
        for photo in self.photo_user.photos_user:
            count += 1
            print (str(count) + '.').decode('utf8') + photo.decode('utf8')
        choice = raw_input(u'Enter photo to send: ').decode('utf8')
        index = int(choice) - 1
        photo_send = self.photo_user.photos_user[index]
        message_encrypt = raw_input(u'Enter message encryption JPEG: ').decode('utf8')
        path_file_encrypt = JpegDecode(photo_send, message_encrypt).decode_jpeg()
        print u'List Your Friends:'
        count = 0
        for friend in self.lib_vk.friends:
            count += 1
            print str(count) + '.' + friend['first_name'] + ' ' + friend['last_name']
        choice = raw_input(u'Enter friend to send message: ').decode('utf8')
        index = int(choice) - 1
        uid = self.lib_vk.friends[index]['uid']
        message_to_send = raw_input(u"Введите сообщение к контенту")
        self.lib_vk.message_send(uid, path_file_encrypt, message_to_send)

    @staticmethod
    def _test_correct_email(email):
        if not u'@' in email:
            raise EmailError(u'Error type email address. Example: example@mail.ru')
        if not u'.' in email:
            raise EmailError(u'Error type email address. Example: example@mail.ru')


if __name__ == '__main__':
    menu = UserQuery()
    menu.user_menu()
    raw_input()
    pass
