#!/usr/bin/python2
# script to change Skype mood status to Clementine now playing.
#
# This is a modified version of mood.py

import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject
import sys

def mood(text=""):
    global bus

    try:
        proxy = bus.get_object('com.Skype.API', '/com/Skype')
        proxy.Invoke('NAME skype_clementine.py')
        proxy.Invoke('PROTOCOL 2')

        command = 'SET PROFILE MOOD_TEXT %s' % text

        return proxy.Invoke(command)

    except:
            print "Could not contact Skype client"

def TrackChange(track):
    info = {'artist': str(track.get('artist')), 'title': str(track.get('title'))}
    mood('Clementine Playing: %s - %s' % (info['artist'], info['title']))

DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
proxy = bus.get_object('org.mpris.clementine', '/Player')
proxy.connect_to_signal("TrackChange", TrackChange, dbus_interface="org.freedesktop.MediaPlayer") 

loop = gobject.MainLoop()

loop.run()
