import pygame
import time
from threading import Thread, Event

from img import *
from object import Ball, Key
from midi4 import createMIDIList, openOutport, openInport, playSong, playNote
from tkinter_def import open_file, midifileErrorMessage
from key_pos import DICT_RECT



FPC = 120
WIDTH_DISPLAY = 1240
HEIGHT_DISPLAY = 829


pygame.init()


win = pygame.display.set_mode((WIDTH_DISPLAY, HEIGHT_DISPLAY), pygame.NOFRAME)
clock = pygame.time.Clock()


SPEED = 3

home_page = True
play_page = False
watch_page = False
watch_tune_page = False

playing_playSong = False
file_chosen = False
file_midi = None

inport = openInport()
outport = openOutport()

balls_live_group = pygame.sprite.Group()
keys_group = pygame.sprite.Group()
keys_clicked_group = pygame.sprite.Group()

midi_msg_balls = []


running = True
while running:

    pos = None
    start_playSong = False

    win.blit(bg_img, (0,0))
    win.blit(close_img, (1120, 0))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

        if pos and close_rect.collidepoint(pos):
            if watch_tune_page:
                event_th.set()
            outport.close()
            inport.close()
            running = False

        if play_page and pos:
            for key_dict, rect in DICT_RECT.items():
                if rect.collidepoint(pos):
                    keys_clicked_group.empty()
                    key = Key(win, key_dict)
                    keys_clicked_group.add(key)
                    ball = Ball(win, x=key_dict)
                    balls_live_group.add(ball)
                    outport.send(playNote(key_dict))


        if home_page and pos and play_rect.collidepoint(pos):
            play_page = True
            home_page = False

        if home_page and pos and watch_rect.collidepoint(pos):
            watch_page = True
            home_page = False


        if not home_page and pos and back_rect.collidepoint(pos):
            if watch_page: 
                home_page, watch_page = True, False

            elif play_page:
                
                home_page, play_page = True, False
                keys_clicked_group.empty()
                balls_live_group.empty()


            elif watch_tune_page:
                watch_page, watch_tune_page = True, False
                file_chosen = False
                event_th.set()

        if watch_page and pos and choose_rect.collidepoint(pos):
            file_midi = open_file()
            if file_midi:
                file_chosen = True
                try:
                    notes = createMIDIList(file_midi)[0]
                    mid = createMIDIList(file_midi)[1]
                    notes_cop = notes[:]
                    balls_group = pygame.sprite.Group()
                except:
                    midifileErrorMessage()
                    file_chosen = False


        if file_midi and pos and playtune_rect.collidepoint(pos):
            watch_tune_page = True
            watch_page = False
            start_playSong = True


    if home_page:
        win.blit(play_img, (470, 300))
        win.blit(watch_img, (470, 470))


    if play_page:
        win.blit(play_bg, (0, 0))
        win.blit(pianobg, (0, 670))
        win.blit(piano_img, (23, 675))
        win.blit(close_img, (1120, 0))

        if not inport:
            inport = openInport()
        else:
            for msg in inport.iter_pending():
                outport.send(msg)
                ball_curr = msg.dict()
                if ball_curr['type'] == 'note_on':
                    ball = Ball(win, x=ball_curr['note'], time=ball_curr['time'], 
                                    velocity=ball_curr['velocity'], channel=ball_curr['channel'])
                    balls_live_group.add(ball)
                    key = Key(win, x=ball_curr['note'], time=time.time())
                    keys_group.add(key)
    

        
        for ball in balls_live_group:
            ball.update(SPEED, 'up')
        
        for key in keys_group:
            key.update()

        for keys in keys_clicked_group:
            keys.update()
        

    if watch_page:
        win.blit(choose_img, (100, 150)) 
        win.blit(choosetune_img, (400, 250))

        if file_chosen:
            win.blit(playtune_img, (400, 450))

    if watch_tune_page:
        win.blit(play_bg, (0, 0))
        win.blit(close_img, (1120, 0))



        if start_playSong:
            time_start = time.time()
            time_all = 0
            if not outport:
                outport = openOutport()
            event_th = Event()
            th = Thread(target=playSong, args=(event_th, mid, outport))
            th.start()

        for ball in balls_group:
            ball.update(SPEED)

        if notes_cop:
            
            if notes_cop[0]['time'] <= time.time() - time_start - time_all:
                ball_curr = notes_cop[0]
                if ball_curr['type'] == 'note_on':
                    ball = Ball(win, x=ball_curr['note'], time=ball_curr['time'], 
                                velocity=ball_curr['velocity'], channel=ball_curr['channel'])
                    balls_group.add(ball)
                time_all += ball_curr['time']
                notes_cop.pop(0)
        else:
            balls_group.empty()


    if not home_page:
        win.blit(back_imag, (1030, 0))

    clock.tick(FPC)
    pygame.display.update()

pygame.quit()