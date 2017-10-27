from psychopy import visual, event, core
import random

from classes.check_exit import check_exit
from classes.show_info import show_info, show_text


# TODO: triggers
def show(win, screen_res, experiment, config, part_id, port_eeg, trigger_no, triggers_list, frame_time=1/60.):
    beh = []
    mean_rt = 0
    fixation = visual.TextStim(win, color='black', text='+', height=2 * config['Text_size'])
    clock = core.Clock()

    for block in experiment:

        if block['type'] == 'break':
            show_info(win=win, file_name=block['file_name'], text_size=config['Text_size'],
                      screen_width=screen_res['width'])
            continue

        if block['type'] == 'calibration':
            mean_rt = 0

        for trial in block['trials']:
            reaction_time = None
            response = None
            acc = 'negative'

            # draw fixation
            fixation_show_time = random.uniform(config['Fixation_show_time'][0], config['Fixation_show_time'][1])
            show_text(win, fixation, fixation_show_time, part_id, beh, triggers_list)

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

            # verify reaction
            if response and trial['type'] == 'go':
                if not (block['type'] == 'experiment' and reaction_time > mean_rt - mean_rt * block['cutoff']):
                    acc = 'positive'
            elif not response and trial['type'] != 'go':
                acc = 'positive'
            elif trial['type'] == 'go':
                reaction_time = target_show_time

            # calibration
            if block['type'] == 'calibration' and trial['type'] == 'go':
                mean_rt += reaction_time

            # feedback
            if block['type'] == 'experiment':
                # choose feedback type
                feedback_type = 'Feedback_{}_{}_'.format(trial['type'], acc)

                # draw feedback
                if config[feedback_type + 'show']:
                    feedback_text = config[feedback_type + 'text']
                    feedback_text = visual.TextStim(win, color='black', text=feedback_text,
                                                    height=2 * config['Text_size'])
                    feedback_show_time = random.uniform(config['Feedback_show_time'][0],
                                                        config['Feedback_show_time'][1])
                    show_text(win, feedback_text, feedback_show_time, part_id, beh, triggers_list)

            # TODO: save beh

        if block['type'] == 'calibration':
            mean_rt /= len([trial for trial in block['trials'] if trial['type'] == 'go'])

    return beh, triggers_list
