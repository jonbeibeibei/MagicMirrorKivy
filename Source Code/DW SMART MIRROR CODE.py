from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
import cv2
import threading
from datetime import date
import calendar
import time
import sys;
reload(sys);
sys.setdefaultencoding("utf8")
Config.set('graphics','fullscreen','0')
Config.write()


#-----------------------------------------------------------------------------------------------------
#--WEBCRAWLER CODE SEGMENT----------------------------------------------------------------------------


import requests
from bs4 import BeautifulSoup

#input whatever string you wish to search events for below
keyword= "science"
url= "https://www.eventbrite.sg/d/singapore--singapore/"+str(keyword)+"/?mode=search"
r=requests.get(url)
soup = BeautifulSoup(r.content,"html.parser")

# soup2 = soup.prettify().encode('UTF-8')

eventHeader = soup.find_all("h4",{"class":"list-card__title"})
eventTime = soup.find_all("time",{"class":"list-card__date"})

#List of events
eHeaderlist = []
for item in eventHeader:
	eHeaderlist += [str(item.text.strip())]        


#List for date and time
eTimelist = []
eTimelist1 = []

for item in eventTime:
	eTimelist += [str(item.text.strip())]
for i in eTimelist:
    j=i.replace('\n','---')
    k=j.replace(' ','')
    eTimelist1+=[k]
   
#Dict w events as keys and dates/time as one value
Dict={}
for i in range(len(eHeaderlist)):
    Dict[eHeaderlist[i]] = eTimelist1[i]

       




#------------------------------------------------------------------------------------------------------------------
#---VARIABLES USED-------------------------------------------------------------------------------------------------
a = "Today"
timenow = time.asctime()
teamnames = "Charles Wong \n Aravind S.K \n Loh Wei Quan \n Tan Jia Hui \n Jonathan Bei"
weathernow = "Sunny"
deadline1 = "Lab Report"
deadline1data = "The report requires a total of 5 pages, documenting \n your lab work and analysis"
deadline2 = "Math Hmwk"
deadline2data = "To be submitted by 5PM on Monday"
deadline3 = "Bio Flip"
deadline3data = "Complete on Sunday night by 12PM"
week=["Mon","Tue","Wed","Thu","Fri"]

#Variables for Calendar events
calendar1 = str(week[0])
calendar2 = str(week[1])
calendar3 = str(week[2])
calendardata1 = "You have Systems World \n at [b]0800[/b]HRS"

#Shortening event text
event1long = eHeaderlist[0]
event1 = str(eHeaderlist[0][:25]) + "..."
event1data1 = eTimelist1[0]
event2long = eHeaderlist[1]
event2 = str(eHeaderlist[1][:25]) + "..."
event2data1 = eTimelist1[1]
event3long = eHeaderlist[2]
event3 = str(eHeaderlist[2][:25] + "...")
event3data1 = eTimelist1[2]
name = "Jon Bei."
hello = "[i]Hello[/i]"

#---------------------------------------------------------------------------------------------
#---FONT INITIALISATION-----------------------------------------------------------------------
LabelBase.register(

        name = "Lato",
        fn_regular = "/home/pi/Desktop/fonts/Lato-Light.ttf",
        fn_bold= "/home/pi/Desktop/fonts/Lato-Medium.ttf",
        fn_italic= "/home/pi/Desktop/fonts/Lato-Hairline.ttf",
        #"fn_bolditalic: "data/fonts/RobotoCondensed-Italic.ttf"

)
LabelBase.register(

        name = "Latotime",
        fn_regular = "/home/pi/Desktop/fonts/Lato-Hairline.ttf",
        #fn_bold= "/home/pi/Desktop/fonts/Lato-Bold.ttf",
        #fn_italic= "/home/pi/Desktop/fonts/Lato-Hairline.ttf",
        #"fn_bolditalic: "data/fonts/RobotoCondensed-Italic.ttf"

)
#------------------------------------------------------------------------------------------------
#---FACE-DETECTION-CLASS-------------------------------------------------------------------------           
class FaceDetection(Screen):
   
    def __init__(self,**kwargs):
        Screen.__init__(self,**kwargs)
        layout = FloatLayout(size=(766,1366))
        self.initialising = Label(text = 'Initializing', size_hint =(.1,.01), pos_hint = {'x':.9, 'y':0.02})
        initialisingani = Animation(color = (1,1,1,0.1) , d=0.5, t='in_out_quad') + Animation(color = (1,1,1,1), d=0.5, t='in_out_quad')
        initialisingani.repeat = True
        initialisingani.start(self.initialising)
        self.add_widget(self.initialising)
        self.add_widget(layout)

    # Executing multithreading in kivy the moment screen is displayed    
    def on_enter(self):
        t = threading.Thread(target= self.facedetect)
        t.start()

    # Method for detecting face    
    def facedetect(self):
        # Creating a face cascade    
        cascPath = sys.argv[1]                         
        faceCascade = cv2.CascadeClassifier(cascPath)   

        # Sets video source to the webcam
        video_capture = cv2.VideoCapture(0)     
       
        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()   

            # Binarize the image/frame        
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

            # Searching for the face 
            faces = faceCascade.detectMultiScale(          
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )
            # Once face is detected, release video capture and exit the loop    
            if len(faces) != 0:
                video_capture.release()
                cv2.destroyAllWindows()
                print 'detected'
                break
        
        # Change screen to our main interface
        Clock.schedule_once(self.changeToUI)
        
    def changeToUI(self,values):
       self.manager.current = 'UI'
               
       
#---------------------------------------------------------------------------------------------
#--CLOCK WIDGET CLASS-------------------------------------------------------------------------
class BasicClock(Label):

    def update(self, *args):
        self.text = time.strftime("%I.%M.%S %p", time.localtime())
        
        # self.size = (.25,.25)

class BasicDate(Label):
    def update(self, *args):
        self.text = time.strftime("%d %b %Y", time.gmtime())

class BasicDay(Label):
    def update(self, *args):
        self.text = str("It's "+ str(calendar.day_name[date.today().weekday()]))

#---------------------------------------------------------------------------------------------
#--MAIN-CLASS-START--------------------------------------------------------------------------------

class MirrorApp(Screen):
    
    def __init__(self, **kwargs):
        Screen.__init__(self,**kwargs)
#---------------------------------------------------------------------------------------------
#---INITIALISE-LAYOUT-------------------------------------------------------------------------

        layout = FloatLayout(size=(1080,1920))

#---------------------------------------------------------------------------------------------
#--Date Widget Top Left-----------------------------------------------------------------------

        self.weatherback = Image(source = '/home/pi/Desktop/MAGIC/rectanglenew.png',size_hint =(.4,.05),
                                 pos_hint = {'x':.005, 'y':.93}, allow_stretch = True, keep_ratio = False)
        layout.add_widget(self.weatherback)

        clock1 = BasicClock()
        clock1.size_hint = (.25,.25)
        clock1.pos_hint = {'x':.080, 'y':.83}
        Clock.schedule_interval(clock1.update, 1)
        clock1.font_name = 'Latotime'
        clock1.font_size = 70
        layout.add_widget(clock1)

        
        clock2 = BasicDate()
        clock2.size_hint = (.05,.05)
        clock2.pos_hint = {'x':.05, 'y':.88}
        Clock.schedule_interval(clock2.update, 1)
        clock2.font_name = 'Lato'
        clock2.font_size = 23
        layout.add_widget(clock2)

        clock3 = BasicDay()
        clock3.size_hint = (.05,.05)
        clock3.pos_hint = {'x':.05, 'y':.86}
        Clock.schedule_interval(clock3.update, 1)
        clock3.font_name = 'Lato'
        clock3.font_size = 23
        layout.add_widget(clock3)

#---------------------------------------------------------------------------------------------
#---Weather Widget Top Right------------------------------------------------------------------


        self.weathericon = Image(source = '/home/pi/Desktop/MAGIC/Cloud.zip', anim_delay = 0.09, size_hint = (.25,.25),
                                 pos_hint = {'x':.81, 'y':.83},allow_stretch = True)
        

        #animation1 = Animation(size_hint = (.2,.2), d=5, t='in_out_quad')
        #animation1.start(self.weathericon)
        layout.add_widget(self.weathericon)

        
        self.weather = Label(text = "Mostly sunny with \n afternoon showers", size_hint = (.1,.05), pos_hint = {'x':.75, 'y':.925},
                             markup = True,font_name = 'Lato', font_size = 20, color = (0,0,0,0))
        animationweather = Animation(color = (1,1,1,1), font_size=20, d=2, t='in_out_quad' )
        animationweather.start(self.weather)
        layout.add_widget(self.weather)



#---------------------------------------------------------------------------------------------
#---Deadlines Widget Bottom Right-------------------------------------------------------------

        self.deadlineslabel = Label(text="[b]Deadlines: [/b] ", size_hint = (.1,.1), pos_hint = {'x':.06, 'y':.18},
                                    markup = True,font_name = 'Lato', font_size = 30, color = (0,0,0,0))
        animationdeadlines = Animation(color = (1,1,1,1), font_size=30, d=1, t='in_out_quad' )
        animationdeadlines.start(self.deadlineslabel)
        layout.add_widget(self.deadlineslabel)

        self.deadlines = Button(text = deadline1, size_hint = (.4,.05), pos_hint = {'x':.02, 'y':.14},
                                font_name = 'Lato', background_color = (1,1,1,0.3), color = (0,0,0,0))
        animationdeadlines1 = Animation(color = (1,1,1,1), font_size=25, d=2, t='in_out_quad' )
        animationdeadlines1.start(self.deadlines)
        layout.add_widget(self.deadlines)
        self.deadlines.bind(on_press=MirrorApp.pop1)

        self.deadlinesnote = Image(source = "/home/pi/Desktop/MAGIC/red!.png", color = (1,0,0,1),
                                   size_hint = (.03,.03), pos_hint = {'x':.083,'y':.153})
        
        animationnotif = Animation(color = (1,0,0,0.1), d = 1, t = 'in_out_quad'    ) + Animation(color = (1,0,0,1), d = .5,
                                                                                              t = 'in_out_quad')
        animationnotif.repeat = True
        animationnotif.start(self.deadlinesnote)
        layout.add_widget(self.deadlinesnote)

        self.deadlines2 = Button(text = deadline2, size_hint = (.4,.05), pos_hint = {'x':.02, 'y':.09},
                                 font_name = 'Lato',background_color = (1,1,1,0.3), color = (0,0,0,0))
        animationdeadlines2 = Animation(color = (1,1,1,1), font_size=25, d=3, t='in_out_quad' )
        animationdeadlines2.start(self.deadlines2)
        layout.add_widget(self.deadlines2)
        self.deadlines2.bind(on_press=MirrorApp.pop2)

        
        self.deadlinesnote2 = Image(source = "/home/pi/Desktop/MAGIC/amber!.png",
                                   size_hint = (.03,.03), pos_hint = {'x':.083,'y':.1})
        layout.add_widget(self.deadlinesnote2)


        self.deadlines3 = Button(text = deadline3, size_hint = (.4,.05), pos_hint = {'x':.02, 'y':.04},
                                 font_name = 'Lato',background_color = (1,1,1,0.3), color = (0,0,0,0))
        animationdeadlines3 = Animation(color = (1,1,1,1), font_size=25, d=4, t='in_out_quad' )
        animationdeadlines3.start(self.deadlines3)
        layout.add_widget(self.deadlines3)
        self.deadlines3.bind(on_press=MirrorApp.pop3)

        
        self.deadlinesnote3 = Image(source = "/home/pi/Desktop/MAGIC/green!.png",
                                   size_hint = (.03,.03), pos_hint = {'x':.083,'y':.05})
        layout.add_widget(self.deadlinesnote3)

#---------------------------------------------------------------------------------------------
#---Events Widget Bottom Right----------------------------------------------------------------

        self.eventslabel = Label(text = "[b]Events:[/b]", size_hint = (.1,.1), pos_hint = {'x':.85, 'y':.18},
                                 markup = True,font_name = 'Lato', font_size = 30, color = (0,0,0,0))
        animationevents = Animation(color = (1,1,1,1), font_size=30, d=1, t='in_out_quad' )
        animationevents.start(self.eventslabel)
        layout.add_widget(self.eventslabel)

        self.events = Button(text=event1, size_hint = (.4,.05), pos_hint = {'x':.58, 'y':.14},
                             font_name = 'Lato',background_color = (1,1,1,0.3), color = (0,0,0,0))
        animationevents1 = Animation(color = (1,1,1,1), font_size=25, d=2, t='in_out_quad' )
        animationevents1.start(self.events)
        layout.add_widget(self.events)
        self.events.bind(on_press=MirrorApp.pop4)

        self.events2 = Button(text=event2, size_hint = (.4,.05), pos_hint = {'x':.58, 'y':.09},
                              font_name = 'Lato',background_color = (1,1,1,0.3), color = (0,0,0,0))
        animationevents2 = Animation(color = (1,1,1,1), font_size=25, d=3, t='in_out_quad' )
        animationevents2.start(self.events2)
        layout.add_widget(self.events2)
        self.events2.bind(on_press=MirrorApp.pop5)

        self.events3 = Button(text=event3, font_size = 35, size_hint = (.4,.05), pos_hint = {'x':.58, 'y':.04},
                              font_name = 'Lato',background_color = (1,1,1,0.3), color = (0,0,0,0) )
        layout.add_widget(self.events3)
        animationdeadlines3 = Animation(color = (1,1,1,1), font_size=25, d=4, t='in_out_quad' )
        animationdeadlines3.start(self.events3)
        self.events3.bind(on_press=MirrorApp.pop6)

#---------------------------------------------------------------------------------------------
#---Greeting Widget Centre--------------------------------------------------------------------

        self.greetinglabel = Label(text=hello, font_size = 130 ,size_hint = (.1,.1), pos_hint = {'x':.3, 'y':.6},
                                   font_name = 'Lato', color = (0,0,0,0), markup = True)
        animationgreet = Animation(color = (1,1,1,1), font_size=145, d=3, t='in_out_quad' )
        animationgreet.start(self.greetinglabel)
        layout.add_widget(self.greetinglabel)
        
        self.greeting = Label(text=name, font_size = 140, size_hint = (.1,.1), pos_hint = {'x':.55, 'y':.50},
                              color = (0,0,0,0), font_name = 'Lato', markup = True)
        animationname = Animation(color = (1,1,1,1), font_size=150, d=1, t='in_out_quad' ) + Animation(color = (1,1,1,1),
                                                                                                       font_size = 160, d = 1,
                                                                                                       t='in_out_quad')
        animationname.repeat = True
        animationname.start(self.greeting)
        layout.add_widget(self.greeting)


#---------------------------------------------------------------------------------------------
#---Calendar Center---------------------------------------------------------------------------
        self.calendarlabel = Image(source = "/home/pi/Desktop/MAGIC/cal.png", size_hint =(.07,.07), pos_hint = {'x':.91, 'y':.86},
                                   font_name = 'Lato', color = (0,0,0,0))
        animationcalendarlabel = Animation(color = (1,1,1,1), d = 8, t = 'in_out_quad')
        animationcalendarlabel.start(self.calendarlabel)
        layout.add_widget(self.calendarlabel)

        self.calendardata = Button(text = calendardata1, size_hint = (.1,.05), pos_hint = {'x':.73, 'y':.87},
                                  font_name = 'Lato', font_size = 20, color = (1,1,1,.3), background_color = (1,1,1,0),
                                   markup = True)
        self.calendarbutton = Button(size_hint = (.07,.07), pos_hint = {'x':.91, 'y':.86},
                                  font_size = 20, color = (1,1,1,.3), background_color = (1,1,1,0),
                                   markup = True)
        animationcalendardata = Animation(color = (1,1,1,1), d = 8.5, t = 'in_out_quad')
        animationcalendardata.start(self.calendardata)
        self.calendarbutton.bind(on_press = MirrorApp.popcal)
        layout.add_widget(self.calendardata)
        layout.add_widget(self.calendarbutton)
#---------------------------------------------------------------------------------------------------
#---QUIT BUTTON-------------------------------------------------------------------------------------
        self.quit = Button(text = 'quit', size_hint = (0.04,0.04), pos_hint = {'x':.4, 'y':.02},
                           font_name = 'Lato', color = (0,0,0,0), background_color = (0,0,0,0))
        self.quit.bind(on_press = MirrorApp.quitapp)

        layout.add_widget(self.quit)

#-----------------------------------------------------------------------------------------------------
#---CREDITS BUTTON------------------------------------------------------------------------------------

        self.credits = Image(source = 'circle.png', size_hint = (.04,.04), pos_hint = {'x':.95, 'y':.005} )
        self.creditsbutton = Button(size_hint = (.04,.04), pos_hint = {'x':.95, 'y': .005}, background_color = (1,1,0,0))
        self.creditsbutton.bind(on_press = MirrorApp.popcredits)
        layout.add_widget(self.credits)
        layout.add_widget(self.creditsbutton)


#----------------------------------------------------------------------------------------------
#---RETURN LAYOUT------------------------------------------------------------------------------
        self.add_widget(layout)


#-------------------------------------------------------------------------------------------------
#---POPUPS CREATION-------------------------------------------------------------------------------
    #Creation of popup buttons will be defined below

    def pop1(self): #First deadline popup
        print 'popup called'
        pop1label = Label(text = deadline1data, font_name = 'Lato', color = (0,0,0,0), font_size = 28)
        animationpop1label = Animation(color = (1,1,1,1), d = 4, t = 'in_out_quad')
        animationpop1label.start(pop1label)
        popup = Popup(title=deadline1, content = pop1label, size_hint=(0.6,0.05),
                      title_font = 'Lato', separator_color = (1,1,1,0), title_color = (0,0,0,0), title_size = 30)
        animationpopup1 = Animation(title_color = (1,1,1,1), d=2, t='in_out_quad', size_hint = (.70,.40) )
        animationpopup1.start(popup)
        popup.open()


    def pop2(self): #Second deadline popup
        print 'popup2 called'
        pop2label = Label(text = deadline2data, font_name = 'Lato', color = (0,0,0,0), font_size = 28)
        animationpop2label = Animation(color = (1,1,1,1), d = 4, t = 'in_out_quad')
        animationpop2label.start(pop2label)
        popup = Popup(title=deadline2, content = pop2label,size_hint=(0.6,0.05),
                      title_font = 'Lato', separator_color = (1,1,1,0), title_color = (0,0,0,0), title_size = 30)
        animationpopup2 = Animation(title_color = (1,1,1,1), d=2, t='in_out_quad', size_hint = (.60,.40) )
        animationpopup2.start(popup)
        popup.open()

    def pop3(self): #Third deadline popup
        print 'popup3 called'
        pop3label = Label(text = deadline3data, font_name = 'Lato', color = (0,0,0,0), font_size = 28)
        animationpop3label = Animation(color = (1,1,1,1), d = 4, t = 'in_out_quad')
        animationpop3label.start(pop3label)
        popup = Popup(title=deadline3, content = pop3label,size_hint=(.6,.05),
                      title_font = 'Lato', separator_color = (1,1,1,0), title_color = (0,0,0,0), title_size = 30)
        animationpopup3 = Animation(title_color = (1,1,1,1), d=2, t='in_out_quad', size_hint = (.6,.4))
        animationpopup3.start(popup)
        popup.open()

    def pop4(self): #First Event popup
        print 'popup4 called'
        box1 = GridLayout() #create a grid layout that can contain multiple widgets to be added directly to popup
        box1.cols = 1
        box1.rows = 2
        box1label1 = Label(text = event1data1, font_name = 'Lato', color = (0,0,0,0), font_size = 28)
        box1.add_widget(box1label1)
        animationpop4label = Animation(color = (1,1,1,1), d = 4, t = 'in_out_quad')
        animationpop4label.start(box1label1)
        popup = Popup(title=event1long, content = box1 ,size_hint=(.6,.05),
                      title_size = 25, title_font = 'Lato', separator_color = (1,1,1,0),
                      title_color = (0,0,0,0))
        animationpopup4 = Animation(title_color = (1,1,1,1), d=2, t = 'in_out_quad', size_hint = (.6,.4))
        animationpopup4.start(popup)
        popup.open()

    def pop5(self): #First Event popup
        print 'popup5 called'
        box2 = GridLayout() #same as pop4
        box2.cols = 1
        box2.rows = 3
        box2label1 = Label(text = event2data1, font_name = 'Lato', color = (0,0,0,0), font_size = 28)
        box2.add_widget(box2label1)
        animationpop5label = Animation(color = (1,1,1,1), d = 4, t = 'in_out_quad')
        animationpop5label.start(box2label1)
        popup = Popup(title=event2long, content = box2 ,size_hint=(.6,.05),
                      title_size = 25, title_font = 'Lato', separator_color = (1,1,1,0),
                      title_color = (0,0,0,0))
        animationpopup5 = Animation(title_color = (1,1,1,1), d=2, t = 'in_out_quad', size_hint = (.6,.4))
        animationpopup5.start(popup)
        popup.open()

    def pop6(self): #First Event popup
        print 'popup6 called'
        box3 = GridLayout() #same as pop4
        box3.cols = 1
        box3.rows = 3
        box3label1 = Label(text = event3data1, font_name = 'Lato', color = (0,0,0,0), font_size = 28)
        box3.add_widget(box3label1)
        animationpop6label = Animation(color = (1,1,1,1), d = 4, t = 'in_out_quad')
        animationpop6label.start(box3label1)
        popup = Popup(title=event3long, content = box3,size_hint=(.6,.05),
                      title_size = 25, title_font = 'Lato', separator_color = (1,1,1,0),
                      title_color = (0,0,0,0))
        animationpopup6 = Animation(title_color = (1,1,1,1), d=2, t = 'in_out_quad', size_hint = (.6,.4))
        animationpopup6.start(popup)
        popup.open()

    def popcal(self):
        print 'popcal called'

        boxcalimage = Image(source = '/home/pi/Desktop/MAGIC/Timetable1.png')
        popup = Popup(title = 'Calendar', size_hint = (.6,.05), content = boxcalimage, title_color = (1,1,1,0),
                      separator_color = (1,1,1,0),title_size = 20)
        animationpopcal = Animation(title_color = (1,1,1,1), d=3, t = 'in_out_quad', size_hint = (.7,.35))
        animationpopcal.start(popup)
        popup.open()

    
    def popcredits(self): #First deadline popup
        print 'popcredits called'
        pop1label = Label(text = teamnames, font_name = 'Lato', color = (0,0,0,0), font_size = 40)
        animationpop1label = Animation(color = (1,1,1,1), d = 4, t = 'in_out_quad')
        animationpop1label.start(pop1label)
        popup = Popup(title="Team", content = pop1label
                      , size_hint=(0.6,0.05), multiline = True,
                      title_font = 'Lato', separator_color = (1,1,1,0), title_color = (0,0,0,0), title_size = 50)
        animationpopup1 = Animation(title_color = (1,1,1,1), d=2, t='in_out_quad', size_hint = (.60,.40) )
        animationpopup1.start(popup)
        popup.open()


    def quitapp(self):
        App.get_running_app().stop()

class MainApp(App):
    def build(self): 
        sm=ScreenManager(transition= FadeTransition())
        fd = FaceDetection(name = 'F')
        st = MirrorApp(name = 'UI')
        sm.add_widget(st)
        sm.add_widget(fd)
        sm.current = 'F'
        return sm

if __name__ == "__main__":
    MainApp().run()
