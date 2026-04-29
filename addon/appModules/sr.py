# -*- coding: utf-8 -*-

"""
AddOn for studio recorder
adds braille support and a few additional keystrokes
to ease the use of SR.
Copyright 2026 Marco Steinebach <studio@windyradio.de>
V26.03:
- Ready for NVDA 2026!
- not speaks open document when changing with ctrl+tab and ctrl+shift+tab
- if documentwindow is not maximized, it's maximized automatically.
- Minor bug fixes!
V26.02:
used overlay classes, because some keystrokes did'nt work in other
than main window.
"""

import appModuleHandler
import addonHandler
import scriptHandler
from scriptHandler import script
import api
import braille
import keyboardHandler
import speech
import config
import wx
from NVDAObjects.IAccessible import IAccessible

addonHandler.initTranslation()

# for making the single letter scripts work when the script key is pressed two times.
gbTaskTimer = None

def brailleMessage (msg):
# sends a message to the braille display.
# not really good style, but working!
  oldShowBrailleMessages = config.conf["braille"]["showMessages"]
  config.conf["braille"]["showMessages"] = braille.ShowMessages.SHOW_INDEFINITELY
  braille.handler.message (msg)
  config.conf["braille"]["showMessages"] = oldShowBrailleMessages

def getOpenDocument(modified):
  obj = api.getForegroundObject ()
  if obj is None:
    return ""
  title = obj.name
  if title is None:
    return ""
  if title.find("[") == -1:
    # no brackets arround the title name, window is not maximized!
    keyboardHandler.KeyboardInputGesture.fromName("alt+-").send()
    keyboardHandler.KeyboardInputGesture.fromName("x").send()
  title = title[title.find("-")+2:] # cut off app name
  title = title.replace("[", "")
  title = title.replace("]","")
  if modified:
    title = title.replace ("*", _(" - modified"))
  return title

def displayInfos():
# displays the infos on the status bar on the braille display.
  # any document open?
  if api.getFocusObject().windowClassName == "MDIClient":
    speech.speakMessage (_("No documents open"))
    return
  obj = api.getStatusBar ()
  if obj == None:
    return
  obj = obj.children[0]
  if obj == None:
    return
  if obj.windowClassName != "msctls_statusbar32":
    return
  text = ""
  # event fires for each child of the status bar
  for i in obj.parent.children:
    text += i.name + " "
  text = text.strip()
  # cosmetic
  text = text.replace ("Stopped", " ")
  # Translators: shown when status is set to playing.
  text = text.replace ("Playing", _("p"))
  # Translators: shown when status is set to recording (over).
  text = text.replace ("Recording (over)", _("rec over"))
  # Translators: shown when status is set to recording (insert).
  text = text.replace ("Recording (insert)", _("rec ins"))
  if text.find ("sl") == -1:
    text += " --"
  else:
    text = text.replace(" sl ", "")
  brailleMessage (text + " " + getOpenDocument(False))

class CustomMainWindow(IAccessible):
# will become active if user is in main window.
# most scripts are only useful, as long as focus is in main window.

  def sendKeySequence(self, gesture, keys, msg):
  # sends the given key sequence, one key after the other.
    # if the control-key is included in the script key,
    # just send a single control.
    # This is necessary, if control is part of the script key,
    # the rest of the key sequence won't work, e.g.: control+delete
    keyboardHandler.KeyboardInputGesture.fromName("control").send()
    for key in keys:
      keyboardHandler.KeyboardInputGesture.fromName(key).send()
    speech.speakMessage (msg)

  # events
  def event_gainFocus(self):
    speech.speakMessage (getOpenDocument (True))
    displayInfos()

  # scripts
  def doLater (self, gesture, keys, msg):
  # triggered if calling script key was pressed only once.
    global gbTaskTimer

    if gbTaskTimer is not None: # there was a script call before
      gbTaskTimer.Stop()
      gbTaskTimer = None
    if scriptHandler.getLastScriptRepeatCount() == 0:
      gbTaskTimer = wx.CallLater(250, self.sendKeySequence, gesture, keys, msg)
    else:
      gesture.send()

  @script(
    description=_("Deletes all audio to the beginning"),
    gesture="kb:control+delete"
  )
  def script_deleteToBeginning(self, gesture):
    self.sendKeySequence (gesture, [
      "alt+e", # open edit menu
      "b"], # delete to beginning
    _("Deleted to beginning!"))

  @script(
    description=_("Deletes all audio to the end"),
    gesture="kb:alt+delete"
  )
  def script_deleteToEnd(self, gesture):
    self.sendKeySequence (gesture, [
      "alt+e", # open edit menu
      "e"], # delete to end
    _("Deleted to end!"))

  @script(
    description=_("Mark start of selection"),
    gesture="kb:j"
  )
  def script_startOfSelection(self, gesture):
    self.doLater (gesture,
      ["alt+e", # open edit menu
       "s", # selection submenu
       "s"], # set start of selection
      _("set start of selection."))

  @script(
    description=_("Mark end of selection"),
    gesture="kb:k"
  )
  def script_endOfSelection(self, gesture):
    self.doLater (gesture,
      ["alt+e", # open edit menu
       "s", # selection submenu
       "e"], # set end of selection
      _("Set end of selection."))

  @script(
    description=_("Select to beginning"),
    gesture="kb:shift+j"
  )
  def script_selectToBeginning(self, gesture):
    self.doLater (gesture,
      ["alt+e", # open edit menu
       "s", # selection submenu
       "b"], # select to beginning
      _("selected to beginning."))

  @script(
    description=_("Select to end"),
    gesture="kb:shift+k"
  )
  def script_selectToEnd(self, gesture):
    self.doLater (gesture,
      ["alt+e", # open edit menu
       "s", # selection submenu
       "n"], # select to end
      _("Selected to end."))

  @script(
    description=_("Go to start of selection"),
    gesture="kb:control+j"
  )
  def script_goToStartOfSelection(self, gesture):
    self.doLater (gesture,
      ["alt+r", # open transport menu
       "c", # selection submenu
       "b"], # go to beginning of selection
      _("start of selection."))

  @script(
    description=_("Go to end of selection"),
    gesture="kb:control+k"
  )
  def script_goToEndOfSelection(self, gesture):
    self.doLater (gesture,
      ["alt+r", # open transport menu
       "c", # selection submenu
       "e"], # go to end of selection
      _("end of selection."))

  @script(
    description=_("fade in"),
    gesture="kb:i"
  )
  def script_fadeIn(self, gesture):
    self.doLater (gesture,
      ["alt+e", # open edit menu
       "s", # selection submenu
       "b", # select to beginning
       "alt+p", # open process menu
       "i"], # fade in
      _("faded in."))

  @script(
    description=_("fade out"),
    gesture="kb:o"
  )
  def script_fadeOut(self, gesture):
    self.doLater (gesture,
      ["alt+e", # open edit menu
       "s", # selection submenu
       "n", # select to end
       "alt+p", # open process menu
       "o"], # fade out
      _("faded out."))

  @script(
    description=_("normalize all audio"),
    gesture="kb:n"
  )
  def script_normalize(self, gesture):
    self.doLater (gesture,
      ["control+a", # mark all audio
       "alt+p", # open process menu
       "n", # normalize
       "enter"], # close the dialog
      _("normalized."))

  # silencing cursor movement
  @script(
    description=_("delete"),
    gesture="kb:delete"
  )
  def script_pressDelete(self, gesture):
    gesture.send()
    speech.speakMessage (_("deleted."))

  @script(
    description=_("do not speak while using arrow keys"),
    gestures=[
              "kb:leftarrow",
              "kb:rightarrow",
              "kb:alt+leftarrow",
              "kb:alt+rightarrow",
              "kb:control+leftarrow",
              "kb:control+rightarrow"
             ]
  )
  def script_pressArrowKey(self, gesture):
    gesture.send()

class CustomStatusBar(IAccessible):
  def event_nameChange(self):
  # occures whenever the value of status bar changes.
    displayInfos()
 
class AppModule(appModuleHandler.AppModule):
  scriptCategory = "Studio Recorder"

  def chooseNVDAObjectOverlayClasses(self, obj, clsList):
    if (obj.windowClassName == "ComRecWV" or
        obj.windowClassName == "AfxFrameOrView140s"):
      clsList.insert(0, CustomMainWindow)
    elif obj.windowClassName == "msctls_statusbar32":
      clsList.insert(0, CustomStatusBar)
    
