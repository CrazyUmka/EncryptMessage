__author__ = 'Grigory'
#coding:UTF-8
import vk_api
import requests
import getpass


class VKError(Exception):
    pass


class RequestError(VKError):
    pass


class VK(object):

    friends = None

    def __init__(self, email, password):
        try:
            self.api = vk_api.VkApi(email, password)
            del password
        except vk_api.authorization_error as error_msg:
            raise VKError(error_msg)

    def _photos_load_server(self, file_photos):
        print u'Start Upload Photo'
        url_upload = self.api.method('docs.getUploadServer')['upload_url']
        file_load = {'file': (file_photos[file_photos.rfind("\\")+1:], open(file_photos, 'rb'))}
        r = requests.post(url_upload, files=file_load)
        params = r.json()
        params['v'] = '5.14'
        result = self.api.method('docs.save', params)
        print u'Upload photo success!'
        id_photo_send = 'doc' + str(result[0]['owner_id']) + '_' + str(result[0]['id'])
        return id_photo_send

    def message_send(self, id_user, photo, message=u''):
        id_photo = self._photos_load_server(photo)
        payload = {'user_id': id_user,
                   'attachment': id_photo,
                   'message': message,
                   'v': '5.14'}
        result = self.api.method('messages.send', payload)
        print u'Message sending.'
        return result

    def message_get(self):
        print u'Check your unread message vk'
        payload = {'offset': '0',
                   'v': '5.14'}
        result = self.api.method('messages.get', payload)
        if result.get(u'items', u'None') == u'None':
            raise VKError(u'Body request empty: ' + result[u'error'])
        else:
            list_mes = {u'count_unread': 0, u'message_content': [], u'message': []}
            for message in result[u'items']:
                if message[u'read_state'] == 0:
                    list_mes[u'count_unread'] +=1
                if message.get(u'attachments') != None:
                    list_mes[u'message_content'].append(message)
                list_mes[u'message'].append(message)
            return list_mes

    def friends_get(self):
        friends = self.api.method('friends.get')['items']
        payload = {"user_ids": "",
                   "fields": 'photo_max_orig'}
        info_list = []
        for id_friend in friends:
            payload.update({"user_ids": id_friend})
            response = requests.get('https://api.vk.com/method/users.get', params=payload).json()
            if 'error' in response:
                raise RequestError(response['response']['error'])
            else:
                info_list.append(response['response'][0])
        self.friends = info_list
        return self.friends


if __name__ in '__main__':
    email = raw_input(u'Enter your email: ').decode('utf8')
    password = getpass.getpass()
    lib_vk = VK(email, password)
    lib_vk.message_get()
