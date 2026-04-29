# NVDA AddOn für den "Studio Recorder"

Author:  
Marco Steinebach <studio@windyradio.de>

## Was ist "Studio Recorder"?

"Studio Recorder", entwickelt von american printing house (APH), 
ist ein Programm zum Aufnehmen und Bearbeiten von Audio.
Mehr zu diesem Programm, inklusive des Download-Links, 
gibt es, auf englisch, [hier](https://www.aph.org/product/studio-recorder-software-digital-download/)
Das Nutzerhandbuch, in englischer Sprache, können Sie 
[hier](https://tech.aph.org/sr_doc.htm)
ansehen.

## was bietet dieses addOn?

Dieses addOn fügt Braille-Unterstützung hinzu,
sowie einige zusätzliche Tastenkombinationen, um die tägliche Arbeit mit
"Studio Recorder" zu vereinfachen.

## Braille-Unterstützung

Wenn Sie eine Braillezeile besitzen, wird alles,
was auf der Statuszeile angezeigt wird,
fortlaufend auf der Braillezeile dargestellt,
während Sie sich im Hauptfenster von "Studio Recorder" befinden.

Dies ermöglicht es, z.B. die aktuelle Zeit sofort nachzuvollziehen,
während Audio abgespielt wird oder Sie eine Aufnahme machen.

Das addOn zeigt genau das auf der Braillezeile an,
was in den Einstellungen von "Studio Recorder"
zur Anzeige für die Statuszeile ausgewählt wurde.

Öffnen Sie "Studio Recorder".  
aktivieren Sie die Einstellungen mit STRG+t.  
wechseln Sie auf die Registerkarte "Status bar" und wählen die Elemente aus,
die auf der Braillezeile angezeigt werden sollen.

Wir empfehlen, die folgenden Elemente zu aktivieren:

- background progress (Hintergrundaktivität)
- Message/status (Ereignisse und aktueller Status)
- current time (aktuelle zeit)
- total time (Gesamtzeit)
- selection length (Länge der Auswahl)

und alle anderen Einträge abzuwählen.

## zusätzliche Tastenkombinationen

Anmerkung zu den Tastenkombinationen, welche nur aus
einem Buchstaben bestehen, z.B. j.
Wenn eine dieser Tastenkombinationen auch von "Studio Recorder"
benutzt wird, drücken Sie die Taste zwei mal schnell,
um die Funktion auszuführen, die vom "Studio Recorder" selbst
bereitgestellt wurde.

Die folgenden Tastenkombinationen werden vom addOn bereitgestellt:

- STRG+ENTF:  
    Löscht alles von der aktuellen Cursorposition bis zum Anfang.
- ALT+ENTF:  
    Löscht alles von der aktuellen Cursorposition bis zum Ende.
- j:  
    Anfang der Auswahl setzen.  
    Für diese Funktion verwendet "Studio Recorder" standardmäßig die 
    eckigen Klammern. Diese sind auf einer
    Deutschen Tastatur aber nicht ohne Weiteres zugänglich.
- k:  
    Ende der Auswahl setzen.
- Umschalt+j:  
    bis zum Anfang auswählen.
- Umschalt+k:  
    bis zum Ende auswählen.
- STRG+j:  
    zum Anfang der Auswahl gehen.
- STRG+k:  
    zum Ende der Auswahl gehen.
- i:  
    Einblenden.  
    Markiert alles von der aktuellen Position
    bis zum Anfang und führt danach das Einblenden aus.
- o:  
    Ausblenden.  
    Markiert alles von der aktuellen Position
    bis zum Ende und führt danach das Ausblenden aus.
- n:  
    normalisieren.  
    Markiert das gesamte Dokument und führt die
    Normalisierung aus.

Alle Tastenkombinationen können im NVDA-Dialog
Tastenbefehle geändert werden.
Wenn Sie eine der Funktionen, die das addOn bereitstellt
nicht nutzen, sondern die Funktion nutzen möchten,
die von "Studio Recorder" bereitgestellt wird,
löschen Sie die entsprechende Tastenkombination
in diesem Dialog.

Wenn Sie sich mit den Pfeiltasten bewegen, 
erfolgt keine Sprachausgabe, um
ungewollte Ausgaben während der Navigation im Dokument zu vermeiden.

## Kontakt

Wenn Sie mich erreichen wollen können Sie dies über
[GitHub](https://github.com/MooSteinebach/StudioRecorder)
tun oder mir eine Email an
<studio@windyradio.de>
senden.

## Versionsgeschichte

### V26.03

- Bereit für NVDA 2026!

- ob ein offenes Dokument gespeichert werden muss, wird jetzt angesagt.

- wenn Studio Recorder im modus "gestoppt" ist, wird auf der Braillezeile ein Leerzeichen dargestellt.

- navigierte man mit strg+tab oder strg+Umschalt+tab durch die offenen Dokumente, wurden diese nicht angesagt.


### V26.02

Fix: einige Tastenkombinationen funktionierten nicht wie erwartet.
