#!/usr/bin/python2
# script to change Skype mood status to Clementine now playing.
#
# This is a modified version of mood.py

import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject
import sys

global bus
global clem
global iface

def mood(text=""):
    try:
        proxy = bus.get_object('com.Skype.API', '/com/Skype')
        proxy.Invoke('NAME skype_clementine.py')
        proxy.Invoke('PROTOCOL 2')

        command = 'SET PROFILE MOOD_TEXT %s' % text

        return proxy.Invoke(command)
    except:
        print "Could not contact Skype client"

def PrintInfo():
    info = iface.GetMetadata()
    mood('Now listening: %s - %s - %s' % (info['artist'], info['album'], info['title']))

def TrackChange(track):
    PrintInfo()

def StatusChange(status):
    if status[0] == 1 or status[0] == 2:
        mood("")
    elif status[0] == 0:
        PrintInfo()

DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
clem = bus.get_object('org.mpris.clementine', '/Player')
clem.connect_to_signal("TrackChange", TrackChange, dbus_interface="org.freedesktop.MediaPlayer") 
clem.connect_to_signal("StatusChange", StatusChange, dbus_interface="org.freedesktop.MediaPlayer") 
iface = dbus.Interface(clem, dbus_interface='org.freedesktop.MediaPlayer')

loop = gobject.MainLoop()

loop.run()
