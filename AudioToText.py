import speech_recognition as sr
from pydub import AudioSegment
import math
import os

r = sr.Recognizer()
path = './temp' #insert your audio folder
ext = ('.wav')

class SplitWavAudioMubin():
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '\\' + filename
        
        self.audio = AudioSegment.from_wav(self.filepath)
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(self.folder + '\\' + split_filename, format="wav")
        
    def multiple_split(self, min_per_split):
        splitDict = []
        total_mins = math.ceil(self.get_duration() / 60)
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i, i+min_per_split, split_fn)
            print(str(i) + ' Done')
            splitDict.append(split_fn)
            if i == total_mins - min_per_split:
                print('All splited successfully')
        return splitDict


def checkLength(file):
        audio = AudioSegment.from_wav(path + '/' + file)
        duration = audio.duration_seconds
        return duration

def buildDataSet():
    # Filter out the .wav audio files under the dir
    dataset = []
    for files in os.listdir(path):
        if files.endswith(ext):
            if(checkLength(files) <= 60):
                dataset.append(files)
            else:
                split_wav = SplitWavAudioMubin(path, files)
                # make a dictionary in multiple split then loop through that to add to dataset[]
                for files in split_wav.multiple_split(min_per_split=1):
                    dataset.append(files)
        else:
            continue
    return dataset

def recognizeWav(dataset):
    # Goes through the files in the built dataset
    for files in dataset:   
        # create a variable that will become the source (Make sure to have the path)
        temp = sr.AudioFile(path + '/' + files)
        with temp as source:
            audio=r.record(source)
        try:
            # Limitations: https://cloud.google.com/speech-to-text/quotas
            val = r.recognize_google(audio)
            # Add the newly created .wav to text variable to a document

            # this if statement was used for my personal data sample
            if ('[' in files):
                files = files[0:files.index('[')] + files[files.index(']')+1:]
            
            fileBreak = files.split('.')
            f = open("result.csv", "a")
            f.write(fileBreak[0] + ',' + fileBreak[1] + ','+ val + ',' + '\n')
            f.close()
        except:
            pass

def main():
    dataset = buildDataSet()
    recognizeWav(dataset)

if __name__ == '__main__':
    main()