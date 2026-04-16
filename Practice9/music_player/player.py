import pygame

tracks=["pp2/Practice9/music_player/music/t1.mp3",
        "pp2/Practice9/music_player/music/t2.mp3"
]
current=0
def play():
    pygame.mixer.music.load(tracks[current])
    pygame.mixer.music.play()

def stop():
    pygame.mixer.music.stop()

def next_track():
    global current
    current=(current+1)%len(tracks)
    play()

def prev_track():
    global current
    current=(current-1)%len(tracks)
    play()