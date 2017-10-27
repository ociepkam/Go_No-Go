from psychopy import visual, event
import time
import os

from classes.load_data import read_text_from_file
from classes.check_exit import check_exit


def show_info(win, file_name, text_size, screen_width, insert=''):
    """
    Clear way to show info message into screen.
    :param win:
    :param file_name:
    :param screen_width:
    :param text_size:
    :param insert: extra text for read_text_from_file
    :return:
    """
    hello_msg = read_text_from_file(os.path.join('messages', file_name), insert=insert)
    hello_msg = visual.TextStim(win=win, antialias=True, font=u'Arial',
                                text=hello_msg, height=text_size,
                                wrapWidth=screen_width, color=u'black',
                                alignHoriz='center', alignVert='center')
    hello_msg.draw()
    win.flip()
    key = event.waitKeys(keyList=['f7', 'return', 'space'])
    if key == ['f7']:
        exit(0)
    win.flip()


def show_text(win, text, show_time, part_id=None, beh=None, triggers_list=None):
    text.setAutoDraw(True)
    win.flip()
    time.sleep(show_time)
    text.setAutoDraw(False)
    check_exit(part_id=part_id, beh=beh, triggers_list=triggers_list)
    win.flip()
