# main.py -- put your code here!
import quokka

def scroll(string, stringScale=2,
         charWidth=8,scWidth=128,
         charHeight=8,scHeight=64,
         startx = 5, starty = 5,
         textColour = 1):
    numchars=(scWidth-startx)//(charWidth*stringScale)
    
    while string:
        quokka.display.fill(1-textColour)
        quokka.display.text(string[:numchars], startx, starty, textColour, scale=stringScale)
        quokka.display.show()
        if len(string)>1:
            string = string[1:]
        else:
            string = ""
        quokka.sleep(200)
    quokka.display.fill(1-textColour)
            
    
scroll('Twas Brilig and the slivey toves did gyre and gimble in the wabe.')
