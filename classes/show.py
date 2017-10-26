from psychopy import visual, event, core
import time
import random

from classes.check_exit import check_exit
from classes.show_info import show_info


def draw_fixation(win, fixation, config, part_id=None, beh=None, triggers_list=None):
    fixation_show_time = random.uniform(config['Fixation_show_time'][0], config['Fixation_show_time'][1])
    fixation.setAutoDraw(True)
    win.flip()
    time.sleep(fixation_show_time)
    fixation.setAutoDraw(False)
    check_exit(part_id=part_id, beh=beh, triggers_list=triggers_list)
    win.flip()


# TODO: triggers
def show(win, screen_res, experiment, config, part_id, port_eeg, trigger_no, triggers_list, frame_time=1/60.):
    beh = []
    fixation = visual.TextStim(win, color='black', text='+', height=2 * config['Text_size'])
    clock = core.Clock()

    for block in experiment:
        if block['type'] == 'break':
            show_info(win=win, file_name=block['file_name'], text_size=config['Text_size'],
                      screen_width=screen_res['width'])
            continue

        for trial in block['trials']:
            draw_fixation(win, fixation, config, part_id, beh, triggers_list)

            # draw cue
            cue_show_time = random.uniform(config['Cue_show_time'][0], config['Cue_show_time'][1])
            trial['cue']['stimulus'].setAutoDraw(True)
            win.callOnFlip(clock.reset)
            event.clearEvents()
            win.flip()
            # ------ trigger ------
            while clock.getTime() < cue_show_time - frame_time:
                check_exit(part_id=part_id, beh=beh, triggers_list=triggers_list)
                win.flip()
            # print cue_show_time-clock.getTime()
            trial['cue']['stimulus'].setAutoDraw(False)
            win.flip()

            # draw target
            target_show_time = random.uniform(config['Target_show_time'][0], config['Target_show_time'][1])
            trial['target']['stimulus'].setAutoDraw(True)
            win.callOnFlip(clock.reset)
            event.clearEvents()
            win.flip()
            # ------ trigger ------
            while clock.getTime() < target_show_time - frame_time:
                key = event.getKeys(keyList=config['Keys'])
                if key:
                    reaction_time = clock.getTime()
                    # ------ trigger ------
                    response = key[0]
                    break

                check_exit(part_id=part_id, beh=beh, triggers_list=triggers_list)
                win.flip()
            # print target_show_time-clock.getTime()
            trial['target']['stimulus'].setAutoDraw(False)
            win.flip()

            # empty screen
            empty_screen_show_time = random.uniform(config['Empty_screen_show_time'][0],
                                                    config['Empty_screen_show_time'][1])
            while clock.getTime() < empty_screen_show_time:
                check_exit(part_id=part_id, beh=beh, triggers_list=triggers_list)
                win.flip()

            # draw feedback
            # TODO: feedback
            # TODO: save beh

    return beh, triggers_list
