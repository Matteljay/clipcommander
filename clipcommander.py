#!/usr/bin/env python3
# -*- mode: python -*-
#
# ClipCommander - Clipboard selection monitor YouTube-dl GUI front-end
# Copyright (C) 2018 Matteljay-at-pm-dot-me
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Donate if you find this app useful, educational or you like to motivate more projects like this.
#
# XMR:  4B6YQvbL9jqY3r1cD3ZvrDgGrRpKvifuLVb5cQnYZtapWUNovde7K5rc1LVGw3HhmTiijX21zHKSqjQtwxesBEe6FhufRGS
# DASH: XnMLmmisNAyDMT3Sr1rhpfAPfkMjDyUiwJ
# NANO: xrb_3yztgrd4exg16r6dwxwc64fasdipi81aoe8yindsin7o31trqsgqanfi9fym
# ETH:  0x7C64707BD877f9cFBf0B304baf200cB1BB197354
# BTC:  14VZcizduTvUTesw4T9yAHZ7GjDDmXZmVs
#

# IMPORTS
# Kivy cross platform graphical user interface
from kivy import __version__ as KIVY_VERSION
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
#from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch') # right mouse behave like left button
Config.set('graphics', 'position', 'custom')
Config.set('graphics','left', 100)
Config.set('graphics','top', 0)
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '360')
Config.set('graphics', 'window_state', 'hidden') # start hidden
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock
# Regex string manipulation
import re
# System
from subprocess import Popen, PIPE
import os, sys
import shutil
from pathlib import Path
from argparse import ArgumentParser
import socket # Linux single instance check
import psutil

name = 'clipcommander'
version = '2018.12.11'
def_defaultcfg = {
    'startmodus': 'normal',
    'showbar': '1',
    'welcome_msg': 'Ready! Select a YouTube video link (example: https://www.youtube.com/watch?v=-O5kNPlUV7w)',
    'reflags': 'IGNORECASE',
    'storewin': '0',
    'storewindata' : '',
    'btn1_text': 'Download best video',
    'btn1_patt': '(https://www\.youtube\.com/watch\?v=[\w-]{11})',
    'btn1_cmd': 'xterm -e youtube-dl $1',
    'btn2_text': 'Download average mp4 video',
    'btn2_patt': '(https://www\.youtube\.com/watch\?v=[\w-]{11})',
    'btn2_cmd': 'xterm -e youtube-dl -f18 $1',
    'btn3_text': 'Download best audio',
    'btn3_patt': '(https://www\.youtube\.com/watch\?v=[\w-]{11})',
    'btn3_cmd': 'xterm -e youtube-dl -fbestaudio $1',
}
def_jsondata = '''[
    { "type": "options", "title": "Window startup mode", "desc": "Visibility and daemonizing, select text !showyourself to override",
    "section": "settings", "key": "startmodus", "options": ["normal", "hidden", "hidden_runfirst"] },
    { "type": "bool", "title": "Show edit bar", "desc": "When hidden, press F1 to access this menu",
    "section": "settings", "key": "showbar" },
    { "type": "string", "title": "Welcome message", "desc": "Message to show at startup",
    "section": "settings", "key": "welcome_msg" },
    { "type": "string", "title": "Python regex flags", "desc": "See docs.python.org could be: MULTILINE|DOTALL",
    "section": "settings", "key": "reflags" },
    { "type": "bool", "title": "Store window pos & size", "desc": "Usage: 1: toggle OFF 2: move and drag window 3: toggle ON",
    "section": "settings", "key": "storewin" },
    { "type": "title", "title": "Release version: ''' + version + ''' - Matteljay" }
    ]'''
col_white = [1, 1, 1, 1]
col_good = [0.1, 0.5, 0.1, 1]
col_bad = [0.5, 0.1, 0.1, 1]
col_proximate = [0.3, 0.3, 0.5, 1]
# Global screen placeholders
Builder.load_string('''
<MainWidget>:
    statuslabel: id_statuslabel
    lab_hidden: id_lab_hidden
    delarea: id_delarea
    mainbox: id_mainbox
    plusbtn: id_plusbtn
    mybar: id_mybar
    rootbox: id_rootbox
    editbtn: id_editbtn
    BoxLayout:
        id: id_rootbox
        canvas:
            Color:
                rgba: 0.9, 0.9, 0.9, 1
            Rectangle:
                pos: self.pos
                size: self.size
        padding: 0
        spacing: 0
        orientation: 'vertical'
        BoxLayout:
            id: id_mainbox
            padding: 8
            spacing: 2
            orientation: 'vertical'
            Label:
                id: id_statuslabel
                font_size: 20
                size_hint: 1, 1.3
                text_size: self.width, None
                halign: 'center'
                text: ''
        BoxLayout:
            id: id_mybar
            canvas:
                Color:
                    rgba: 0.84, 0.84, 0.84, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            size: self.width, 30
            size_hint: 1, None
            padding: 0
            spacing: 0
            orientation: 'horizontal'
            Label:
                size: 100, 30
                size_hint: None, None
                id: id_lab_hidden
                text: ''
                font_size: 16
                halign: 'left'
                text_size: self.width, None
                padding_x: 8
            Widget:
            Label:
                size: 100, 30
                size_hint: None, None
                id: id_delarea
                text: '[delete]'
                font_size: 20
            Button:
                size: 30, 30
                size_hint: None, None
                background_normal: ''
                background_color: 0.84, 0.84, 0.84, 1
                on_press: app.btn_plusbtn()
                id: id_plusbtn
                text: '+'
                font_size: 20
            ToggleButton:
                id: id_editbtn
                size: 30, 30
                size_hint: None, None
                background_normal: ''
                background_color: 0.84, 0.84, 0.84, 1
                on_press: app.btn_toggle_edit()
                text: 'e'
                font_size: 20
            Button:
                size: 30, 30
                size_hint: None, None
                background_normal: ''
                background_color: 0.84, 0.84, 0.84, 1
                on_press: app.open_settings()
                text: '\u00B7\u00B7\u00B7'
                font_size: 20
<ButtonEditor>:
    on_enter: app.w_input_enter()
    t_name: id_t_name
    t_patt: id_t_patt
    t_cmd: id_t_cmd
    simmsg: id_simmsg
    BoxLayout:
        canvas:
            Color:
                rgba: 0.9, 0.9, 0.9, 1
            Rectangle:
                pos: self.pos
                size: self.size
        padding: 8
        spacing: 2
        orientation: 'vertical'
        BoxLayout:
            padding: 8
            spacing: 2
            orientation: 'vertical'
            Label:
                id: id_simmsg
                font_size: 20
                text: ''
            Label:
                color: 0, 0, 0, 1
                font_size: 20
                text: 'Button name:'
            TextInput:
                unfocus_on_touch: False
                id: id_t_name
                text: ''
                multiline: False
                font_size: 20
                write_tab: False
                on_text_validate: app.btn_ok()
                text_validate_unfocus: False
            Label:
                color: 0, 0, 0, 1
                font_size: 20
                text: 'Clipboard Python-regex pattern:'
            TextInput:
                unfocus_on_touch: False
                id: id_t_patt
                text: ''
                multiline: False
                font_size: 20
                write_tab: False
                on_text_validate: app.btn_ok()
                text_validate_unfocus: False
            Label:
                color: 0, 0, 0, 1
                font_size: 20
                text: 'Command reference to pattern ($1 $2..):'
            TextInput:
                unfocus_on_touch: False
                id: id_t_cmd
                text: ''
                multiline: False
                font_size: 20
                write_tab: False
                on_text_validate: app.btn_ok()
                text_validate_unfocus: False
        BoxLayout:
            size_hint: 1, 0.2
            Button:
                on_press: app.btn_ok()
                is_focusable: False
                text: 'OK'
                font_size: 20
            Button:
                on_press: root.manager.current = 'main'
                is_focusable: False
                text: 'CANCEL'
                font_size: 20
''')
class MainWidget(Screen): pass
w_main = MainWidget(name='main')
class ButtonEditor(Screen): pass
w_input = ButtonEditor(name='input')

class ClipCommanderApp(App):
    cmdline_process = None
    scancmd = None
    bad_lockdown = None
    resource_rootpath = '' # examples: /path/to/data or /usr/local/share
    edit_modus = False
    confpath = '' # ini file
    firstrun = False
    usedbtn = None # differentiate pressing the '+' or selecting an existing button
    reflags = 0 # regex
    prevcliptext = None
    btnslocked = False
    startmodus = ''
    def btn_ok(self):
        # textbox input checks
        w_input.t_name.text = w_input.t_name.text.strip()
        w_input.t_patt.text = w_input.t_patt.text.strip()
        w_input.t_cmd.text = w_input.t_cmd.text.strip()
        for tbox in (w_input.t_name, w_input.t_patt, w_input.t_cmd):
            if not tbox.text:
                w_input.simmsg.color = col_bad
                w_input.simmsg.text = 'Empty input not allowed'
                tbox.focus = True
                return
        # regex checks on t_patt
        try:
            re.compile(w_input.t_patt.text)
        except re.error as msg:
            w_input.simmsg.color = col_bad
            w_input.simmsg.text = 'Regex: ' + str(msg)
            w_input.t_patt.focus = True
            return
        # command executable check here on t_cmd
        cmd = w_input.t_cmd.text.split(maxsplit=1)
        if shutil.which(cmd[0]) is None:
            w_input.simmsg.color = col_bad
            w_input.simmsg.text = 'Command not found!'
            w_input.t_cmd.focus = True
            return
        # add button
        if self.usedbtn: # clicked red button
            self.usedbtn.patt = w_input.t_patt.text
            self.usedbtn.cmd = w_input.t_cmd.text
        else: # pressed '+'
            # check if name already exists
            for btn in (w for w in w_main.mainbox.children if type(w) == type(Button())):
                if btn.text == w_input.t_name.text:
                    w_input.simmsg.color = col_bad
                    w_input.simmsg.text = 'Cannot add, name already exists!'
                    w_input.t_name.focus = True
                    return
            # add button widget
            self.add_a_new_button(w_input.t_name.text, w_input.t_patt.text, w_input.t_cmd.text)
        # write with correct ordering
        self.write_button_widgets_to_config()
        screenman.current = 'main'
    def w_input_enter(self):
        # Clear previous contents, initialize window with relevant data
        if self.usedbtn:
            w_input.t_name.text = self.usedbtn.text
            w_input.t_patt.text = self.usedbtn.patt
            w_input.t_cmd.text = self.usedbtn.cmd
            w_input.t_name.disabled = True
            w_input.t_patt.focus = True
            w_input.simmsg.color = col_good
            w_input.simmsg.text = 'Edit existing button'
        else:
            w_input.t_name.text = ''
            w_input.t_patt.text = ''
            w_input.t_cmd.text = ''
            w_input.t_name.disabled = False
            w_input.t_name.focus = True
            w_input.simmsg.color = col_good
            w_input.simmsg.text = 'Add a new button'
    def btn_plusbtn(self):
        self.usedbtn = None
        screenman.current = 'input'
    def btn_toggle_edit(self):
        if w_main.editbtn.state == 'down':
            self.edit_modus = True
            for btn in (w for w in w_main.mainbox.children if type(w) == type(Button())):
                hide_widget(btn, False) # make all visible
                btn.background_color = [2, 0, 0, 1]
                btn.disabled = True
            w_main.lab_hidden.text = 'Edit modus'
        else:
            self.edit_modus = False
            for btn in (w for w in w_main.mainbox.children if type(w) == type(Button())):
                btn.background_color = col_white
                btn.disabled = False
            # do complete rescan
            self.prevcliptext = None
            self.myclock(0)
        # Toggle showing 'add button' plus symbol
        hide_widget(w_main.plusbtn, not self.edit_modus)
    def swapbuttons(self, src, dest):
        tempdestpos = list(dest.pos) # copy tuple content, prevent pointer assignment
        dest.pos = src.pos
        src.pos = tempdestpos
    def touch_move_btn_DL(self, btn, touch):
        if not btn.grabbed:
            return
        # check if the mouse left the initial button area
        if not btn.collide_point(*touch.pos):
            btn.triedswap = True
        # check if dragging to another button
        for widget in w_main.mainbox.children:
            if type(widget) == type(Button()) and not widget == btn:
                if widget.collide_point(*touch.pos):
                    # yes, swap button content
                    self.swapbuttons(btn, widget)
                    return
        # check if dragging into delete area
        if w_main.delarea.collide_point(*touch.pos):
            w_main.delarea.color = col_proximate
        else:
            w_main.delarea.color = col_white
    def touch_down_btn_DL(self, btn, touch):
        if self.edit_modus and btn.collide_point(*touch.pos):
            btn.grabbed = True
            btn.triedswap = False
            hide_widget(w_main.delarea, False)
    def write_button_widgets_to_config(self):
        # re-index/order buttons
        poslist = [] # list of tuples containing all the info per button
        for btn in (w for w in w_main.mainbox.children if type(w) == type(Button())):
            poslist.append((btn.y, btn.text, btn.patt, btn.cmd))
        poslist.sort(key=lambda tup: tup[0], reverse=True) # sort by y-coordinate
        # clear all btns from config
        for setting in self.config['settings']:
            if setting[:3] == 'btn':
                del self.config['settings'][setting]
        # store new btn setup to config
        for i, tup in enumerate(poslist):
            btnN = 'btn' + str(i + 1)
            self.config['settings'].update({btnN + '_text': tup[1], btnN + '_patt': tup[2], btnN + '_cmd': tup[3]})
        self.config.write()
    def touch_up_btn_DL(self, btn, touch):
        if not btn.grabbed:
            return
        btn.grabbed = False
        # delete button
        if w_main.delarea.collide_point(*touch.pos):
            w_main.mainbox.remove_widget(btn)
        # hide delete button
        w_main.delarea.color = col_white
        hide_widget(w_main.delarea, True)
        # edit button
        if not btn.triedswap:
            self.usedbtn = btn
            screenman.current = 'input'
            return
        # write with correct ordering
        self.write_button_widgets_to_config()
    def press_btn_DL(self, btn):
        # spam control: alternative to Kivy's min_state_time button
        if self.btnslocked: return
        btn.background_color[1] = 2
        self.btnslocked = True
        def greenback(dt):
            self.btnslocked = False
            btn.background_color[1] = 1
            self.on_request_close(None)
        Clock.schedule_once(greenback, 0.5)
        #print('"{}" "{}" "{}"'.format(btn.text, btn.patt, btn.cmd)) # debug
        # replace into groups
        command = btn.cmd # complete_selection = btn.matchobj.group(0)
        for i, obj in enumerate(btn.matchobj.groups()):
            i += 1
            command = command.replace('$' + str(i), obj)
        # execute command detached
        print('[EXEC   ] ' + command)
        Popen(command.split())
    def myclock(self, dt):
        if self.edit_modus:
            return
        # get clipboard data
        p = Popen(self.scancmd, stdout=PIPE, stderr=PIPE)
        output, errors = p.communicate()
        cliptext = output.decode('utf-8')
        if cliptext == self.prevcliptext:
            return
        self.prevcliptext = cliptext
        #print('cliptext: "{}"'.format(cliptext)) # debug
        # match & grab clipboard text, see if button needs to be hidden
        lastmatch = None
        cnt = 0
        for btn in (w for w in w_main.mainbox.children if type(w) == type(Button())):
            btn.matchobj = re.match(btn.patt, cliptext, flags=self.reflags)
            if btn.matchobj:
                hide_widget(btn, False) # show button
                lastmatch = btn
            else:
                hide_widget(btn, True)
                cnt += 1
        w_main.lab_hidden.text = 'Hidden: ' + str(cnt)
        if lastmatch and self.startmodus == 'hidden_runfirst':
            self.press_btn_DL(lastmatch)
        elif lastmatch or cliptext == '!showyourself':
            self.fixed_window_show()
    def fixed_window_show(self):
        Window.show()
        # maximize() and restore() make no sense but seem to work to make show() work on older SDL2 window providers
        Window.maximize()
        Window.restore()
        Window.raise_window()
    def add_a_new_button(self, _text, patt, cmd):
        btn = Button(text=_text, font_size=20)
        btn.background_down = btn.background_normal
        btn.patt = patt
        btn.cmd = cmd
        btn.grabbed = False
        btn.bind(on_press=self.press_btn_DL, on_touch_down=self.touch_down_btn_DL, \
          on_touch_move=self.touch_move_btn_DL, on_touch_up=self.touch_up_btn_DL)
        w_main.mainbox.add_widget(btn)
        if self.edit_modus:
            btn.background_color = [2, 0, 0, 1]
            btn.disabled = True
        else:
            btn.background_color = col_white
            btn.disabled = False
        return btn
    def on_config_change(self, config, section, key, value):
        if config is not self.config or self.bad_lockdown:
            return # ignore config change of kivy itself
        if key == 'welcome_msg':
            w_main.statuslabel.text = value
        elif key == 'showbar':
            screenman.current = 'main'
            if value == '0':
                if self.edit_modus:
                    w_main.editbtn.state = 'normal'
                    self.btn_toggle_edit()
                hide_widget(w_main.mybar)
            else:
                hide_widget(w_main.mybar, False)
        elif key == 'reflags':
            self.reflags = 0
            flagslist = value.split('|')
            for flagstr in flagslist:
                if hasattr(re, flagstr):
                    self.reflags |= getattr(re, flagstr)
        elif key == 'startmodus':
            self.startmodus = value
        elif key == 'storewin':
            if value == '1':
                winstr = ' '.join(str(n) for n in [Window.left, Window.top, Window.size[0], Window.size[1]])
                config.set('settings', 'storewindata', winstr)
                config.write()
    def on_start(self):
        # Pre-run requirement tests
        if shutil.which('xclip'):
            self.scancmd = ['xclip', '-o']
        elif shutil.which('xsel'):
            self.scancmd = ['xsel', '-o']
        if not self.scancmd:
            self.bad_lockdown = 'Please install either "xclip" or "xsel" to use this app'
        if not shutil.which('youtube-dl'):
            self.bad_lockdown = 'Please install "youtube-dl" ("ffmpeg" is also recommended!)'
        # See if app can function
        cfg = self.config['settings']
        statuslabel = w_main.statuslabel
        if self.bad_lockdown:
            statuslabel.color = col_bad
            statuslabel.text = self.bad_lockdown
            # hide mybar
            Clock.schedule_once(lambda dt: hide_widget(w_main.mybar), 1) # doing this sooner seems defective
            self.fixed_window_show()
            return
        elif self.firstrun:
            statuslabel.color = col_good
            statuslabel.text = 'First time run, welcome! Wrote config {}\n Copy a YouTube video link into the clipboard'.format(self.confpath)
            self.firstrun = False
        else:
            statuslabel.color = col_good
            statuslabel.text = cfg['welcome_msg']
        # Add command buttons from config
        i = 1
        while True:
            btnN = 'btn' + str(i)
            newtext = self.config.getdefault('settings', btnN + '_text', '')
            if not newtext:
                break
            btn = self.add_a_new_button(newtext, cfg[btnN + '_patt'], cfg[btnN + '_cmd'])
            i += 1
        # Only show in edit modus
        hide_widget(w_main.plusbtn)
        hide_widget(w_main.delarea)
        # showbar
        if cfg['showbar'] == '0':
            Clock.schedule_once(lambda dt: hide_widget(w_main.mybar), 1) # doing this sooner seems defective
        # evaluate regex flags
        self.reflags = 0
        flagslist = cfg['reflags'].split('|')
        for flagstr in flagslist:
            if hasattr(re, flagstr):
                self.reflags |= getattr(re, flagstr)
        # Start responsive timer/scanner
        self.myclock(0)
        Clock.schedule_interval(self.myclock, 1)
    def get_application_config(self):
        self.confpath = super(type(self), self).get_application_config('~/.config/%(appname)s.ini')
        return self.confpath
    def build_config(self, config):
        self.confpath = self.get_application_config()
        if os.access(self.confpath, os.R_OK):
            config.setdefaults('settings', {}) # don't re-create buttons that may have been deleted
        else:
            self.firstrun = True
            config.setdefaults('settings', def_defaultcfg)
    def build_settings(self, settings):
        settings.add_json_panel('ClipCommander', self.config, data=def_jsondata)
    def on_request_close(self, args):
        if self.startmodus[:6] == 'hidden':
            if self.edit_modus:
                w_main.editbtn.state = 'normal'
                self.btn_toggle_edit()
            Window.hide()
            print('[HIDDEN ]')
            return True # daemon mode, impossible to close normally
    def build(self):
        # get icon and resource path
        app_path = Path(__file__).resolve()
        for tryroot in (str(app_path.parents[1]) + '/share', str(app_path.parents[0]) + '/data'):
            tryicon = tryroot + '/pixmaps/' + name + '.png'
            if os.access(tryicon, os.R_OK):
                self.icon = tryicon
                self.resource_rootpath = tryroot
                break
        else:
            print('WARNING: Could not find application resource files', file=sys.stderr)
        # storewin
        cfg = self.config['settings']
        if cfg['storewin'] == '1':
            coords = cfg['storewindata'].split()
            if len(coords) == 4:
                Window.left, Window.top = int(coords[0]), int(coords[1])
                Window.size = (int(coords[2]), int(coords[3]))
        # determine startmodus
        self.startmodus = cfg['startmodus']
        if self.startmodus[:6] == 'hidden':
            print('[HIDDEN ]')
        else:
            self.fixed_window_show()
        # wrap close request to handle startmodus
        Window.bind(on_request_close=self.on_request_close)
        return screenman

#
########### NON-GUI Below
#

def hide_widget(wid, dohide=True):
    if hasattr(wid, 'saved_attrs'):
        if not dohide:
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
            del wid.saved_attrs
    elif dohide:
        wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

def fatal_err(line):
    print('ERROR: ' + line, file=sys.stderr)
    sys.exit(1)

def pymod_versioncheck(module_name, module_version, required_version):
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$','', v).split('.')]
    if normalize(module_version) < normalize(required_version):
        fatal_err('{} requires version {} (current version is {})'.format(module_name, required_version, module_version))
        sys.exit(1)
    else:
        print(':: {} version is: {}'.format(module_name, module_version))

#
##### Main program entry point (after reading all the functions above!)
#

if __name__ == '__main__':
    # linux-specific check for app single instance
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind('\0{}_lock'.format(name)) 
    except socket.error as err:
        error_code, error_string = err.args[0], err.args[1]
        print("Process already running ({}: {}). Exiting".format(error_code, error_string))
        sys.exit(0)
    # cross-platform check for app single instance, requires package 'tendo'
    #from tendo import singleton
    #me = singleton.SingleInstance()
    # check requirements
    pymod_versioncheck('kivy', KIVY_VERSION, '1.10.1')
    # Create the screen manager
    screenman = ScreenManager(transition=NoTransition())
    screenman.add_widget(w_main)
    screenman.add_widget(w_input)
    # Launch GUI
    ClipCommanderApp().run()

# End of file





