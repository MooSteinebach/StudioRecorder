# -*- coding: utf-8 -*-
# AddOn for studio recorder

import appModuleHandler
import api
import braille
import scriptHandler
from scriptHandler import script
import keyboardHandler
import speech
import config
import ui

class AppModule(appModuleHandler.AppModule):
  scriptCategory = "Studio recorder"
  oldShowBrailleMessages = config.conf["braille"]["showMessages"]
  
  # helper functions
  def displayInfos(self, obj):
  # displays the needed infos on the braille display.
    # any document open?
    focusObject = api.getFocusObject()
    if focusObject.windowClassName == "MDIClient":
      ui.message (_("No documents open"))
      return
    # are we in the main window of studio recorder?
    if (focusObject.windowClassName != "ComRecWV" and
        focusObject.windowClassName != "AfxFrameOrView140s"):
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
    text = text.replace ("Stopped", _("s"))
    text = text.replace ("Playing", _("p"))
    text = text.replace ("Recording (over)", _("rec over"))
    text = text.replace ("Recording (insert)", _("rec ins"))
    if text.find ("sl") == -1:
      text = text + " --"
    else:
      text = text.replace(" sl", "")
    # add currently open dokument
    title = api.getForegroundObject().name
    title = title[title.find("-")+2:]
    braille.handler.message (text + " " + title)

  def sendKeySequence(self, keys, alternativeKey):
    if api.getFocusObject().windowClassName != "ComRecWV":
      keyboardHandler.KeyboardInputGesture.fromName(alternativeKey).send()
      return False
    for key in keys:
      keyboardHandler.KeyboardInputGesture.fromName(key).send()
    return True
    
  # events
  def event_gainFocus(self, obj, nextHandler):
    if (obj.windowClassName == "ComRecWV" or # normal playback
        obj.windowClassName == "MDIClient" or # no document open
        obj.windowClassName == "AfxFrameOrView140s"): # recording 
      # we are in the main window
      if config.conf["braille"]["showMessages"] != braille.ShowMessages.SHOW_INDEFINITELY:
        config.conf["braille"]["showMessages"] = braille.ShowMessages.SHOW_INDEFINITELY
      self.displayInfos(api.getStatusBar ().children[0])
    nextHandler()   
    
  def event_loseFocus(self, obj, nextHandler):
    if (obj.windowClassName == "ComRecWV" or # normal playback
        obj.windowClassName == "MDIClient" or # no document open
        obj.windowClassName == "AfxFrameOrView140s"): # recording
      # we are in the main window
      if config.conf["braille"]["showMessages"] != self.oldShowBrailleMessages:
        config.conf["braille"]["showMessages"] = self.oldShowBrailleMessages
    nextHandler()   
      
  def event_nameChange(self, obj, nextHandler):
  # occures whenever the value of status bar changes.
    self.displayInfos(obj)
    nextHandler()
    
  # scripts
  @script(
    description=_("Deletes all audio to the beginning"),
    gesture="kb:control+delete"
  )
  def script_deleteToBeginning(self, gesture):
    self.sendKeySequence (["control", # to release control, because gesture includes control
      "alt+e", # open edit menu
      "b"], "") # delete to beginning
    speech.speakMessage (_("Deleted to beginning!"))

  @script(
    description=_("Deletes all audio to the end"),
    gesture="kb:alt+delete"
  )
  def script_deleteToEnd(self, gesture):
    self.sendKeySequence (["alt", # to release alt, because gesture includes alt
      "alt+e", # open edit menu
      "e"], "") # delete to end
    speech.speakMessage (_("Deleted to end!"))

  @script(
    description=_("Mark start of selection"),
    gesture="kb:g"
  )
  def script_startOfSelection(self, gesture):
    speech.speakMessage (str(scriptHandler.getLastScriptRepeatCount()))
    """
    if scriptHandler.getLastScriptRepeatCount() != 1:
      gesture.send()
      return
    if self.sendKeySequence (["alt+e", # open edit menu
        "s", # selection submenu
        "s"], # set start of selection
        "j"):
      speech.speakMessage (_("set start of selection."))
    """
    
  @script(
    description=_("Mark end of selection"),
    gesture="kb:k"
  )
  def script_endOfSelection(self, gesture):
    if scriptHandler.getLastScriptRepeatCount() != 0:
      gesture.send()
      return
    if self.sendKeySequence (["alt+e", # open edit menu
        "s", # selection submenu
        "e"], # set end of selection
        "k"):
      speech.speakMessage (_("Set end of selection."))

  @script(
    description=_("fade in"),
    gesture="kb:i"
  )
  def script_fadeIn(self, gesture):
    if scriptHandler.getLastScriptRepeatCount() != 0:
      gesture.send()
      return
    if self.sendKeySequence (["control", "alt+e", # open edit menu
        "s", # selection submenu
        "b", # select to beginning
        "alt+p", # open process menu
        "i"], # fade in
        "i"):
      speech.speakMessage (_("faded in."))

  @script(
    description=_("fade out"),
    gesture="kb:o"
  )
  def script_fadeOut(self, gesture):
    if scriptHandler.getLastScriptRepeatCount() != 0:
      gesture.send()
      return
    if self.sendKeySequence (["control", "alt+e", # open edit menu
        "s", # selection submenu
        "n", # select to end
        "alt+p", # open process menu
        "o"], # fade out
        "o"):
      speech.speakMessage (_("faded out."))

  @script(
    description=_("normalize all audio"),
    gesture="kb:n"
  )
  def script_normalize(self, gesture):
    if scriptHandler.getLastScriptRepeatCount() != 0:
      gesture.send()
      return
    if self.sendKeySequence (["control", 
        "control+a", # mark all audio
        "alt+p", # open process menu
        "n", # normalize
        "enter"], # close the dialog
        "n"):
      speech.speakMessage (_("normalized."))

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
  

