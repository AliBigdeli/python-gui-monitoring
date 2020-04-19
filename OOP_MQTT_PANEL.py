#importing libraries
from tkinter import *
import tk_tools
from datetime import datetime
import threading,time,random,sys,pip,os ,schedule
import paho.mqtt.client as mqtt
from random import choice
from string import ascii_uppercase,digits
#print("ClientID-{}".format(''.join(choice(ascii_uppercase + digits) for i in range(8))))

global threads
threads = []
stop_threads = False
on_cancel = False

def clickTest():
    print ("Click!")

def popupmsg(msg):
    popup = Tk()
    popup.wm_title("Alert")
    popup.geometry('230x160')
    NORM_FONT = ("Helvetica", 10)
    label = Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()



def show_info():
    popupmsg('''this program has been written by:
    Ali Bigdeli Known as BlackFox
    bigdeli.ali3@gmail.com
    www.icc-aria.ir''')   


def exit_all(): 
    print("exit")
    try:        
        client.disconnect()                         
    except:
        pass
    finally:
        app.quit()



class App(Tk):
    def __init__(self):
        Tk.__init__(self)        
        self.title("Server Monitoring")
        menuBar = MenuBar(self)
        #optionBar = OptionBar(self)        
        bottomFrame = BottomFrame(self)
        credentialFrame = CredentialFrame(self)
        monitorFrame = MonitorFrame(self)        
        elementsFrame = ElementsFrame(self)
        self.config(menu=menuBar)        
        #optionBar.pack( side = TOP,anchor=W)        
        bottomFrame.pack( side = BOTTOM ,pady=10)
        credentialFrame.pack( side = TOP,anchor=W,pady=10)        
        monitorFrame.pack(side = TOP,anchor=W,pady=10)        
        elementsFrame.pack(side = TOP,anchor=W,pady=10)

class MenuBar(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)
        
        #building menu bar for file
        fileMenu = Menu(self, tearoff=False)
        self.add_cascade(label="File", menu=fileMenu)        
        fileMenu.add_command(label="Settings")
        fileMenu.add_command(label="Exit", command=exit_all)        
        #building menu bar for about and register
        aboutMenu = Menu(self, tearoff=False)
        self.add_cascade(label="About", menu=aboutMenu)        
        aboutMenu.add_command(label="register", command=clickTest)
        aboutMenu.add_command(label="Info", command=show_info)

    
        
        

class OptionBar(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        #buidling options
        Label(self, text="Options : ").pack(side=LEFT,anchor=W,padx=5)
        global img_show 
        img_show = IntVar()
        Checkbutton(self, text="No images", variable=img_show).pack(side=LEFT,anchor=W)
        global slt_mode 
        slt_mode = IntVar()        
        Checkbutton(self, text="Silent mode", variable=slt_mode).pack(side=LEFT,anchor=W)
        global man_log 
        man_log = IntVar()
        Checkbutton(self, text="Manual login", variable=man_log).pack(side=LEFT,anchor=W)
        global RAS
        RAS = IntVar()
        Checkbutton(self, text="Raspberry", variable=RAS).pack(side=LEFT,anchor=W)



class BottomFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        global state
        state = StringVar()
        state.set("not connected to server")        
        global state_field
        state_field = Label(self, textvariable = state)        
        state_field.config(foreground="red")        
        state_field.pack(side = TOP)
        
        curstate = Label(self, text="version 0.1.ALPHA")
        curstate.pack(side=BOTTOM)

class CredentialFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Label(self, text="Address/IP server:").grid(row=0, column=0,padx=5,sticky=W)    
        global Server
        Server = Entry(self,width=20)            
        #Server.insert(0,"broker.hivemq.com")
        Server.insert(0,"5.238.103.219")
        Server.grid(row=0, column=1,padx=5,sticky=W)
        global Port
        Label(self, text="Port:").grid(row=0, column=2,padx=5,sticky=W)    
        Port = Entry(self,width=4)
        Port.insert(0,"1883")
        Port.grid(row=0, column=3,padx=5,sticky=W)
        global Client_ID
        Label(self, text="Client ID:").grid(row=0, column=4,padx=5,sticky=W)    
        Client_ID = Entry(self,width=13)            
        Client_ID.insert(0,"ClientID-{}".format(''.join(choice(ascii_uppercase + digits) for i in range(8))))
        Client_ID.grid(row=0, column=5,padx=5,sticky=W)    
        global Live_time
        Label(self, text="Live time:").grid(row=0, column=6,padx=5,sticky=W)    
        Live_time = Entry(self,width=3)            
        Live_time.insert(0,"60")
        Live_time.grid(row=0, column=7,padx=5,sticky=W)
        Button(self, text='Login', command=self.Start_MQTT).grid(row=1, column=0, sticky=W,padx=5)        
    
        '''
        Label(self, text="Username:").grid(row=1, column=0,padx=5,sticky=W)    
        server = Entry(self,width=13)            
        #Host.insert(0,"127.0.0.1")
        server.grid(row=1, column=1,padx=5,sticky=W)
        Label(self, text="Password:").grid(row=1, column=2,padx=5,sticky=W)    
        server = Entry(self,width=13)            
        #Host.insert(0,"127.0.0.1")
        server.grid(row=1, column=3,padx=5,sticky=W)
        '''
    def Start_MQTT(self):                
            #module_checkup()    
            log_t = threading.Thread(target=Start_MQTT_t)
            threads.append(log_t)
            #log_t.daemon = True
            log_t.start()

def Start_MQTT_t():
    global client    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.username_pw_set(username="guest",password="12345678")
    #client.connect(chosen_server, 1883,60)    
    #print(Server.get())
    #print(Port.get())
    #print(Client_ID.get())
    #print(Live_time.get())
    port = Port.get()
    lt = Live_time.get()
    try:
        client.connect(Server.get(),int(port),int(lt))                
    except:
        global state
        global state_field    
        state.set("Something went wrong, check your entries")             
        state_field.config(foreground="orange")
        return False
    try:
        global topic_list
        topic_list=["server/temp","server/humidity","server/motion","server/fire","server/air","server/voltage","server/door","server/smoke"]
        for topics in topic_list:
            client.subscribe(topics)
    except:
        return False
    client.loop_forever()
    
        

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: "+str(rc))
    global state
    global state_field
    if (rc == 0):        
        state.set("Connection accepted, logged in successfully")             
        state_field.config(foreground="green")
    elif (rc == 1):        
        state.set("Connection refused, unacceptable protocol version")             
        state_field.config(foreground="red")
    elif (rc == 2):        
        state.set("Connection refused, identifier rejected")             
        state_field.config(foreground="red")
    elif (rc == 3):
        state.set("Connection refused, server unavailable")             
        state_field.config(foreground="red")
    elif (rc == 4):
        state.set("Connection refused, bad user name or password")             
        state_field.config(foreground="red")
    elif (rc == 5):
        state.set("Connection refused, not authorized")             
        state_field.config(foreground="red")

# The callback for when a PUBLISH message is received from the server base on subscribed Topic
def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))
    if message.topic in topic_list:
        #print("it was in list")
        action(message.topic,str(message.payload))

def action(Topic,msg):    
    if (Topic == "server/temp"):                
        global temp_gauge 
        temp = list(msg.split("'"))
        temp = float(temp[1])                        
        temp_gauge.set_value(temp)
    
    if (Topic == "server/humidity"):        
        global humidity_gauge
        humidity = list(msg.split("'"))        
        humidity = float(humidity[1])                                
        humidity_gauge.set_value(humidity)
    if (Topic == "server/motion"):        
        motion = list(msg.split("'")) 
        motion_state.set(motion[1])  
        if motion[1]=="Normal":
            motion_state_field.config(foreground="green")
        else:
            motion_state_field.config(foreground="red")
    
    if (Topic == "server/smoke"):        
        smoke =  list(msg.split("'")) 
        smoke_state.set(smoke[1])
        if smoke[1]=="Normal":
            smoke_state_field.config(foreground="green")
        else:
            smoke_state_field.config(foreground="red")
    
    if (Topic == "server/fire"):        
        fire =  list(msg.split("'")) 
        fire_state.set(fire[1])
        if fire[1]=="Normal":
            fire_state_field.config(foreground="green")
        else:
            fire_state_field.config(foreground="red")

    if (Topic == "server/door"):        
        door =  list(msg.split("'")) 
        door_state.set(door[1])
        if door[1]=="Normal":
            door_state_field.config(foreground="green")
        else:
            door_state_field.config(foreground="red")
    
    if (Topic == "server/air"):
        global air_gauge
        air_v = list(msg.split("'"))        
        air_v = float(air_v[1])                                
        air_gauge.set_value(air_v)
        #air = str(message.payload)
    '''
    if (Topic == "server/voltage"):
        
        voltage = str(message.payload)
    
    '''
        
class MonitorFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        #Label(self, text="Username").grid(row=0, column=0,padx=5, sticky=W)                
        Label(self, text="دما").grid(row=0, column=0,padx=5)
        global temp_gauge
        temp_gauge= tk_tools.RotaryScale(self, max_value=50.0, unit='C')
        temp_gauge.grid(row=1,column=0)
        Label(self, text="رطوبت").grid(row=0, column=1,padx=5)
        global humidity_gauge
        humidity_gauge= tk_tools.RotaryScale(self, max_value=100.0, unit='%')
        humidity_gauge.grid(row=1,column=1)
        Label(self, text="ولتاژ").grid(row=0, column=2,padx=5)
        global voltage_gauge
        voltage_gauge= tk_tools.RotaryScale(self, max_value=100.0, unit='v')
        voltage_gauge.grid(row=1,column=2)
        Label(self, text="فشار هوا").grid(row=0, column=3,padx=5)
        global air_gauge
        air_gauge= tk_tools.RotaryScale(self, max_value=500.0, unit='')
        air_gauge.grid(row=1,column=3)

class ElementsFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        #Label(self, text="Username").grid(row=0, column=0,padx=5, sticky=W)                
        Label(self, text="وضعیت درب").grid(row=0, column=0,padx=5)
        global door_state
        door_state = StringVar()
        door_state.set("nothing yet")        
        global door_state_field
        door_state_field = Label(self, textvariable = door_state)        
        door_state_field.config(foreground="red")
        door_state_field.grid(row=0, column=1,padx=5)

        Label(self, text="وضعیت حضور").grid(row=0, column=2,padx=5)
        global motion_state
        motion_state = StringVar()
        motion_state.set("nothing yet")      
        global motion_state_field
        motion_state_field = Label(self, textvariable = motion_state)        
        motion_state_field.config(foreground="red")
        motion_state_field.grid(row=0, column=3,padx=5)

        Label(self, text="وضعیت آتش").grid(row=1, column=0,padx=5)
        global fire_state
        fire_state = StringVar()
        fire_state.set("nothing yet")      
        global fire_state_field
        fire_state_field = Label(self, textvariable = fire_state)
        fire_state_field.config(foreground="red")
        fire_state_field.grid(row=1, column=1,padx=5)

        Label(self, text="وضعیت دود").grid(row=1, column=2,padx=5)
        global smoke_state
        smoke_state = StringVar()
        smoke_state.set("nothing yet")      
        global smoke_state_field
        smoke_state_field = Label(self, textvariable = smoke_state)        
        smoke_state_field.config(foreground="red")
        smoke_state_field.grid(row=1, column=3,padx=5)
        
        
        

if __name__ == "__main__":
    app = App()
    app.resizable(width=False, height=False)
    app.geometry('600x400')
    app.protocol("WM_DELETE_WINDOW",exit_all)    
    app.mainloop() 
