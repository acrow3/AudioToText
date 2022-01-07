# AudioToText
* This is a program written in Python3 used to split Audio Files of the .WAV file type into readable text.
* The recognizer of choice is the google recognizer, however this recognizer comes with some limitations
  * The primary one of conflict being the lenght the audio files are allowed to be
    * This was circumvented by breaking the audio into 1 minute segments (this can be adjusted to 2 mins if wanted)

* Python packages that you will need are:
  * AudioSegment from pydub
  * SpeechRecognition
  * math
  * os

* The final output will have the filename, file type and, the file text
