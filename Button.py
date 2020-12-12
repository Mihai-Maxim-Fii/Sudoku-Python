import pygame

class button():
    def __init__(self,color,x,y,w,h,txt=''):
        self.color=color
        self.x=x
        self.y=y
        self.width=w
        self.height=h
        self.text=txt
    def draw(self,win):
     pygame.draw.rect(win,pygame.Color("black"),pygame.Rect(self.x,self.y,self.width,self.height),2)
     pygame.draw.rect(win,self.color,pygame.Rect(self.x+2,self.y+2,self.width-2,self.height-2))

     if self.text!='':
         font=pygame.font.SysFont('none',30)
         text=font.render(self.text,1,(0,0,0))
         win.blit(text,(self.x+(self.width/2-text.get_width()/2),self.y+(self.height/2-text.get_height()/2)))

    def onButton(self,x,y):
        if x>self.x and x<self.x+self.width:
            if y>self.y and y<self.y+self.height:
                return True
        return False