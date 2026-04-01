# -*- coding: utf-8 -*-
# AddOn for studio recorder
# adds braille support and a few additional keystrokes
# to ease the use of SR.
# Copyright 2026 Marco Steinebach <studio@windyradio.de>

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

# addonHandler.initTranslation()

# for making the single letter scripts work when the script key is pressed two times.
gbTaskTimer = None

class AppModule(appModuleHandler.AppModule):
  scriptCategory = "Studio Recorder"
  oldShowBrailleMessages = config.conf["braille"]["showMessages"]
  
  # helper functions
  def inMainWindow(self, obj):
  # returns True, if focus is in the main window
    if (obj.windowClassName == "ComRecWV" or
        obj.windowClassName == "AfxFrameOrView140s"):
      return True
    else:
      return False
      
  def displayInfos(self, obj):
  # displays the needed infos on the braille display.
    focusObject = api.getFocusObject()
    # any document open?
    if focusObject.windowClassName == "MDIClient":
      speech.speakMessage (_("No documents open"))
      return
    # are we in the main window of studio recorder?
    if not self.inMainWindow(focusObject):
      return
    # does event apply to status bar?
    if obj.windowClassName != "msctls_statusbar32":
      return
    text = ""
    # event fires for each child of the status bar
    for i in obj.parent.children:
      text = text + i.name + " "
    text = text.strip()
    # cosmetic
    # Translators: shown when status is set to stopped.
    text = text.replace ("Stopped", _("s"))
    # Translators: shown when status is set to playing.
    text = text.replace ("Playing", _("p"))
    # Translators: shown when status is set to recording (over).
    text = text.replace ("Recording (over)", _("rec over"))
    # Translators: shown when status is set to recording (insert).
    text = text.replace ("Recording (insert)", _("rec ins"))
    if text.find ("sl") == -1:
      text = text + " --"
    else:
      text = text.replace(" sl", "")
    # add currently open dokument
    title = api.getForegroundObject().name
    title = title[title.find("-")+2:]
    braille.handler.message (text + " " + title)

  def sendKeySequence(self, gesture, keys, msg):
  # sends the given key sequence, one key after the other.
  # if focus is not in main window, e.g. a dialog,
  # the key that triggered the script is send
  # and nothing is spoken.
    if not self.inMainWindow(api.getFocusObject()):
      gesture.send()
      return
    # if control is included in the script key,
    # just send a single control.
    # This is necessary, if control is part of the script key,
    # the rest of the key sequence won't work.
    keyboardHandler.KeyboardInputGesture.fromName("control").send()
    for key in keys:
      keyboardHandler.KeyboardInputGesture.fromName(key).send()
    speech.speakMessage (msg)

  # events
  def event_gainFocus(self, obj, nextHandler):
    if (self.inMainWindow (obj) or
        obj.windowClassName == "MDIClient"): # no document open
      # we are in the main window
      if config.conf["braille"]["showMessages"] != braille.ShowMessages.SHOW_INDEFINITELY:
        config.conf["braille"]["showMessages"] = braille.ShowMessages.SHOW_INDEFINITELY
      self.displayInfos(api.getStatusBar ().children[0])
    nextHandler()   
    
  def event_loseFocus(self, obj, nextHandler):
    if (self.inMainWindow (obj) or
        obj.windowClassName == "MDIClient"): # no document open
      # we are in the main window
      if config.conf["braille"]["showMessages"] != self.oldShowBrailleMessages:
        config.conf["braille"]["showMessages"] = self.oldShowBrailleMessages
    nextHandler()   
      
  def event_nameChange(self, obj, nextHandler):
  # occures whenever the value of status bar changes.
    self.displayInfos(obj)
    nextHandler()

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

  @script(
    description=_("entfernen"),
    gesture="kb:delete"
  )
  def script_pressDelete(self, gesture):
    gesture.send()
    speech.speakMessage (_("deleted."))

  # silencing cursor movement
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
  

