# NVDA AddOn for "Studio Recorder"

Author:  
Marco Steinebach <studio@windyradio.de>

## What is "Studio Recorder"?

"Studio Recorder", developed by the american printing house (APH), is an App to record and manipulate audio.
More about this program including the download can be found [here](https://www.aph.org/product/studio-recorder-software-digital-download/)
The users manual can be viewed [here](https://tech.aph.org/sr_doc.htm).

## what does this addOn offer?

This addOn adds braille support as well as some additional keystrokes to ease the use of "Studio Recorder".

## braille support

If you have a braille display, the content of the status bar is displayed on the brailledisplay while you are in the main window of "Studio Recorder".
This makes it possible to see the current time while audio is played back
and/or while you record new audio.
So you can always keep track of your position within the audio material.

The addOn displays all elements you have configured to be displayed in the status bar.
In Studio Recorder's settings (CTRL+t) go to the TAB "Status Bar".
Here you can tell "Studio Recorder" which elements you want to see on the status bar.

We recommend to check the following Items:

- background progress
- Message/status
- current time
- total time
- selection length

and to uncheck all other items.

## additional keyboard shortcuts

If one of the single letter key strokes listed below is also a 
Studio Recorder command, just press it twice to perform the action which 
was originally designed for "Studio Recorder".

The following shortcuts are added through the addOn.

- CTRL+Delete:  
    delete all audio to the beginning
- ALT+Delete:  
    Delete all audio to the end
- j:  
    set start of selection.  
    The normal key to do this in "Studio Recorder" is the left bracket,
    but this key can't be used on non-english keyboards.
- k:  
    set end of selection.
- shift+j:  
    select to beginning.
- shift+k:  
    select to end.
- ctrl+j:  
    go to start of selection.
- ctrl+k:  
    go to end of selection.
- i:  
    fade in.  
    Marks all audio to the beginning and performs a fade in.
- o:  
    fade out.  
    Marks all audio to the end and performs a fade out.
- n:  
    normalize all audio  
    Marks all audio and performs a normalize.

All keystrokes can be changed in NVDA's gestures dialog.  
If you want to have Studio Recorder's original behaviour back for a keystroke,
just delete it from the gestures dialog under "Studio Recorder".

The arrow keys do not speak if pressed, to avoid
unwanted speech output while navigating the document.

## contact

If you want to get in touch with me you can use
[GitHub](https://github.com/MooSteinebach/StudioRecorder)
or send an email to
<studio@windyradio.de>

## change log

### V26.02

Fix: Some keystrokes did'nt work as expected
