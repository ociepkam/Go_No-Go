import os
from psychopy import visual
import codecs
from os.path import join
import yaml

possible_images_format = ('bmp', 'jpg', 'png', 'gif')
possible_audio_format = ('mp3', 'au', 'mp2', 'wav', 'wma', 'ogg')


def load_config():
    try:
        with open(join("docs", "config.yaml")) as yaml_file:
            doc = yaml.load(yaml_file)
        return doc
    except:
        raise Exception("Can't load config file")


def load_data(win, folder_name, config, screen_res):
    """
    ladowanie tekstu, zdjec i dzwiekow
    :param screen_res:
    :param config:
    :param win: visual.Window z psychopy
    :param folder_name: nazwa folderu z ktorego beda ladowane pliki
    """

    names = [f for f in os.listdir(folder_name)]
    data = list()
    for name in names:
        path = os.path.join(folder_name, name)
        try:
            if name[-3:] == 'txt':
                with open(path, 'r') as text_file:
                    for line in text_file:
                        trigger_name = line.split(':')[0]
                        text = line.split(':')[1]
                        text = text.split('\n')[0]
                        word = visual.TextStim(win=win, antialias=True, font=u'Arial', text=text,
                                               height=config['Text_size'], wrapWidth=screen_res['width'],
                                               color=u'black', alignHoriz='center', alignVert='center')
                        data.append(('text', trigger_name, word))
            elif name[-3:] in possible_images_format:
                # image = visual.ImageStim(win, image=path, interpolate=True)
                # data.append(('image', name.split('.')[0], image))
                data.append(path)
            elif name[-3:] in possible_audio_format:
                data.append(('sound', name.split('.')[0], path))
            else:
                raise Exception('Error while loading a file ' + name)
        except:
            raise Exception('Error while loading a file ' + name)

    return data


def load_data_in_folders(win, folder_name, config, screen_res):
    """
    ladowanie tekstu, zdjec i dzwiekow
    :param screen_res:
    :param config:
    :param win: visual.Window z psychopy
    :param folder_name: nazwa folderu z ktorego beda ladowane pliki
    """

    folders = [f for f in os.listdir(folder_name)]
    data = list()
    for folder in folders:
        p = os.path.join(folder_name, folder)
        names = [f for f in os.listdir(p)]
        for name in names:
            path = os.path.join(folder_name, folder, name)
            try:
                if name[-3:] == 'txt':
                    with open(path, 'r') as text_file:
                        for line in text_file:
                            trigger_name = line.split(':')[0]
                            text = line.split(':')[1]
                            text = text.split('\n')[0]
                            word = visual.TextStim(win=win, antialias=True, font=u'Arial', text=text,
                                                   height=config['Text_size'], wrapWidth=screen_res['width'],
                                                   color=u'black', alignHoriz='center', alignVert='center')
                            data.append(('text', folder + '_' + trigger_name, word))
                elif name[-3:] in possible_images_format:
                    image = visual.ImageStim(win, image=path, interpolate=True)
                    data.append(('image', folder + '_' + name.split('.')[0], image))
                elif name[-3:] in possible_audio_format:
                    data.append(('sound', folder + '_' + name.split('.')[0], path))
                else:
                    raise Exception('Error while loading a file ' + name)
            except:
                raise Exception('Error while loading a file ' + name)
    return data


def load_data_names(folder_name):
    folders = [f for f in os.listdir(folder_name)]
    data = list()
    for folder in folders:
        p = os.path.join(folder_name, folder)
        names = [f for f in os.listdir(p)]
        for name in names:
            path = os.path.join(folder_name, name)
            try:
                if name[-3:] == 'txt':
                    with open(path, 'r') as text_file:
                        for line in text_file:
                            data.append(folder + '_' +line.split(':')[0])
                elif name[-3:] in possible_images_format:
                    data.append(folder + '_' +name.split('.')[0])
                elif name[-3:] in possible_audio_format:
                    data.append(folder + '_' +name.split('.')[0])
                else:
                    raise Exception('Error while loading a file ' + name)
            except:
                raise Exception('Error while loading a file ' + name)

    return data


def read_text_from_file(file_name, insert=''):
    """
    Method that read message from text file, and optionally add some
    dynamically generated info.
    :param file_name: Name of file to read
    :param insert: dynamically generated info
    :return: message
    """
    if not isinstance(file_name, str):
        raise TypeError('file_name must be a string')
    msg = list()
    with codecs.open(file_name, encoding='utf-8', mode='r') as data_file:
        for line in data_file:
            if not line.startswith('#'):  # if not commented line
                if line.startswith('<--insert-->'):
                    if insert:
                        msg.append(insert)
                else:
                    msg.append(line)
    return ''.join(msg)
