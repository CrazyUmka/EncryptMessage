__author__ = 'Grigory'
#coding:UTF-8
import os
from Crypto.Cipher import AES
import base64


class DecryptError(Exception):
    pass


class Encryptions(object):

    @staticmethod
    def decrypt_message(image):
        index = image.rfind('\\') + 1
        if image == -1:
            name_file = image
        else:
            name_file = image[index:]
        file_load = open(image, 'rb')
        data_file = file_load.read().decode('cp866')
        file_load.close()
        index = data_file.rfind(u'_') + 1
        if index == 1:
            raise DecryptError(u'Файд не возможно расшифровать, проверьте его целостность!')
        size_file = int(data_file [index : ])
        message = data_file [size_file : index - 1]
        message_decrypt = Encryptions.run_aes(name_file, message, u'Decode')
        print u'Расшифрованно новое сообщение:\n\t' + message_decrypt

    @staticmethod
    def run_aes(key, text=u'', type_aes=u'Encode'):
        block_size = 32
        padding = u'{'
        Pad = lambda s: s + (block_size - len(s) % block_size) * padding
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(Pad(s)))
        DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(padding)
        magic_uni = u'magic_great_dead_or_alive'
        if len(key) < 32:
            ostatok = 32 - len(key)
            temp_str = magic_uni[:ostatok]
            for i in temp_str:
                key += i
        secret = key
        chiper = AES.new(secret)
        if type_aes in u'Encode':
            return EncodeAES(chiper, text)
        else:
            return DecodeAES(chiper, text)


class JpegDecode(Encryptions):

    def __init__(self, image=u'17014.jpg', message=u'Privet lol, kak dela?'):
        self.image_shifr = image
        self.message_shifr = message

    def decode_jpeg(self):
        file_image = open(self.image_shifr, 'rb')
        size = str(os.path.getsize(self.image_shifr))
        data_image = file_image.read().decode('cp866')
        file_image.close()
        # dir_file = self.image_shifr[: self.image_shifr.rfind(u'\\') + 1]
        name_rec_file = self.image_shifr[self.image_shifr.rfind(u'\\') + 1: self.image_shifr.rfind(u'.')]
        name_rec_file += u'_last.jpg'
        message = JpegDecode.run_aes(name_rec_file, self.message_shifr)
        data_image += message + u'_' + size.decode('utf8')
        file_rec = open(name_rec_file, 'wb')
        file_rec.write(data_image.encode('cp866'))
        file_rec.close()
        print u'End Decode Successful'
        return name_rec_file


class Mp3Decode(Encryptions):

    def __init__(self, mp3_file, message):
        self.file_decode = mp3_file
        self.message = message

    def decode_mp3(self):
        file_mp3 = open(self.file_decode, 'rb')
        size_file = os.path.getsize(self.file_decode)
        data = file_mp3.read()
        file_mp3.close()
        data += self.message + u'_' + size_file
        name_rec_file = self.file_decode[self.file_decode.rfind(u'\\') + 1: self.file_decode.rfind(u'.') - 1]
        name_rec_file += u'last.jpg'
        file_rec = open(name_rec_file, 'wb').write(data)
        file_rec.close()


if __name__ in '__main__':
    PicDecoder = JpegDecode()
