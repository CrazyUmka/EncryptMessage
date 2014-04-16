# Steganography Engine VK.com (Alpha version)
###### Разработка

## №1. Установка зависимостей 
### Установка на Windows

```bash
# Установить git
http://git-scm.com/downloads

# Запустить git_bash в директории для проекта и выполнить:
git clone https://github.com/CrazyUmka/EncryptMessage.git
cd EncryptMessage

# Установить зависимости python(не обращайте внимание на ошибки)
pip install -r requirements.txt

# Установить Python-Extensions(PyCrypto) для Windows
http://www.voidspace.org.uk/python/modules.shtml#pycrypto 
```

### Установка на Ubuntu

```bash
#**Предварительно**, проверьте установлен ли данный пакет: python-dev
sudo apt-get update
sudo apt-get install python-dev

# Скачайте репозиторий
git clone https://github.com/CrazyUmka/EncryptMessage.git
cd EncryptMessage

# Создайте virtualenv
virtualenv --system-site-packages EnvMessage

# Активируйте virtualenv
source ./EnvMessage/bin/activate

# Установите зависимости python
pip install -r requirements.txt
```

## №2. Работа с программой
После выполнения *пункта 1* можно приступить к работе. На данный момент используется **консольный интерфейс**.
Для запуска используйте команду в git-bash:

```bash
python core.py
```

После запуска следуйте инструкциям.

# Примечание:
**Обязательно** присылайте найденные ошибки на issue tracker
