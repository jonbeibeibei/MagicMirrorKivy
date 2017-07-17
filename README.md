# MagicMirrorKivy
A Python implementation of a Magic Mirror, using Kivy, OpenCV and BeautifulSoup

![ScreenImage](https://github.com/jonbeibeibei/MagicMirrorKivy/blob/master/Infographic%20Poster%20/MirrorFront.png)
fig1. Sample Screen

## Problem
MagicMirrorKivy aims to aggregate data relevant to the user, and display it in an elegant and efficient manner. This is done through the use of: 

### Web Crawler
A web crawler that is designed to fetch personalized, relevant information. Preferences can be pre-set as an input string, which will be used to scour the web for relevant events that may be of interest. 

### Facial Detection 
OpenCV, an open source computer vision library built for object recognition is used. This enables the device to be able to recognize users as they step into view, relevant information that that specific user is then queried and displayed on screen. 

### Date/Time, Weather, Appointments
The most relevant and urgent information is displayed concisely at the top-right hand corner of the screen for easy viewing. 

### Welcome Message
To welcome the user, allowing the user to know that the displayed information is contextual and tailored to him/her. 

### Deadlines & Events
Assignment deadlines are ranked according to urgency, traffic light colours are used to represent the urgency. Events are pulled using the webcrawler, from various sources such as Facebook & Eventbrite. 