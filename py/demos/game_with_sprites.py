import quokka, framebuf, random, pyb
SMILEY = """
111110000011111
111001111100111
110111111111011
101111111111101
101111111111101
011001111100110
011001111100110
011111111111110
011111111111110
011011111110110
101101111101101
101110000011101
110111000111011
111001111100111
111110000011111
"""
BADDIE = """
000111111111000
100011111110001
110001111100011
111000111000111
111100010001111
111110000011111
111111000111111
111110000011111
111100010001111
111000111000111
110001111100011
100011111110001
000111111111000
"""
WIDTH = 128
HEIGHT = 64

move_x = False
def move(timer):
    global move_x
    move_x = True

def draw_sprite(sprite):
    piclist = sprite.split()
    width = len(piclist[0])
    height = len(piclist)
    buf = bytearray(width*height)
    fb = framebuf.FrameBuffer(buf, width, height, framebuf.MONO_VLSB)
    #FrameBuffer.pixel(x, y[, c])
    y=0
    for line in piclist:
        x=0
        for char in line:
            fb.pixel(x,y,int(char))
            x+=1
        y+=1
    return fb,width,height
hero, hero_width, hero_height = draw_sprite(SMILEY)
baddie, baddie_width, baddie_height = draw_sprite(BADDIE)

hero_x = hero_width//2
hero_y = hero_height//2

baddie_x = random.randint(0,(WIDTH-baddie_width))
baddie_y = random.randint(0,(HEIGHT-baddie_height))

timer = pyb.Timer(4)
timer.init(freq=0.25)
timer.callback(move)

quokka.display.fill(1)
quokka.display.blit(hero,hero_x,hero_y)
quokka.display.blit(baddie,baddie_x,baddie_y)
quokka.display.show()

score = 0
def collide():
    return baddie_x <= hero_x <= baddie_x+baddie_width and baddie_y <= hero_y <= baddie_y+baddie_height or \
            baddie_x <= hero_x+hero_width <= baddie_x+baddie_width and baddie_y <= hero_y+hero_height <= baddie_y+baddie_height
while True:
    if move_x:
        baddie_x = random.randint(0,(WIDTH-baddie_width))
        baddie_y = random.randint(0,(HEIGHT-baddie_height))
        move_x=False
    if quokka.buttons.a.was_pressed(): #A button
        hero_x -= hero_width//2
    if quokka.buttons.b.was_pressed(): #B button
        hero_x += hero_width//2
    if quokka.buttons.c.was_pressed(): #C button
        hero_y -= hero_height//2
    if quokka.buttons.d.was_pressed(): #D button
        hero_y += hero_height//2
    #collision detect
    #if x of good is between x_bad and x_bad + width or x + width is between x bad and x bad + width
    if collide():
        #collision
        score+=1
        move_x=True
        timer.init(freq=0.25)
        print(score)
    
    quokka.display.fill(1)
    quokka.display.blit(hero,hero_x,hero_y)
    quokka.display.blit(baddie,baddie_x,baddie_y)
    quokka.display.show()
