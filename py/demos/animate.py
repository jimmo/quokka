import quokka

HEART = [
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,
0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,
0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,
0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,
0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,
0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,
0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,
0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,
0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,
0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

DIAMOND = [
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,
0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,
0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,
0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,
0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,
0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,
0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,
0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,
0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,
0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,
0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,
0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


def show_pic(fb, img=DIAMOND, colour = 1, start_x = 0, start_y = 0,  scale = 4, repeat = False ):
    #what happens to validate my inputs, what happens if start x and y are wrong, scale is too high etc?
    #need to deal with screen width and height to ensure I'm not writing to empty indexes.
    for i,cell in enumerate(img):
        #find the row
        x=i%16
        y=i//16
        #scale and update the fb
        if cell: 
            #test for being on screen
            fb.fill_rect(scale * x + start_x, scale*y + start_y, scale, scale, colour)
def animate(fb, fps = 5, img = HEART, colour = 1, start_x = 0, start_y = 0, scale = 4, repeat = False ):
    fb.fill((colour+1)%2)
    show_pic(fb, img = img, colour = colour, start_x = start_x, start_y = start_y, scale = scale, repeat = repeat)
    fb.show()
    quokka.sleep(1000//fps)
    fb.fill((colour+1)%2)
    show_pic(fb, img = img, colour = colour, 
        start_x = start_x + scale**2, start_y = start_y + scale**2, scale = scale//2, repeat = repeat)
    fb.show()
    quokka.sleep(1000//fps)

if __name__ == '__main__':
    fb = quokka.display
    while True:
        animate(fb)
        
    


