import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from time import sleep
import os
from pydub.silence import split_on_silence


class VideoToText:
    def __init__(self):
        # initializing the speech recognition
        self.audio_initializer = sr.Recognizer()
        self.videopath = input("Enter the video path from your laptop, pc.....::").replace('"', '')
        self.name = input("Name the audio file for use::").replace(" ", "")
        # self.text = input("Name the text file you will be getting the text in::")

    def video_to_text(self):  

        def video_to_audio():
            try:
                clip = mp.VideoFileClip(f"{self.videopath}")
                print(
                    "Converting video file to audio for processing..... To auto be deleted....")  # bug, reminder to delete file
                clip.audio.write_audiofile(f"curses.mp3")
            except OSError:
                print("Invalid file path, file not found.")
                exit()
            print("Preparing to render to text......")
            sleep(5)

            def audio_to_text():  # method that converts audio to text by splitting them into files in a folder and picking them for work
                final_text = ""
                mp3_file = f"{self.name}.mp3"
                wav_file_convert = AudioSegment.from_mp3(mp3_file)
                wav_file_convert.export(f"{self.name}", format="wav")
                sounds = AudioSegment.from_wav(f"{self.name}.wav")
                chunks = split_on_silence(sounds, min_silence_len=500, keep_silence=500,
                                          silence_thresh=sounds.dBFS - 14)
                # creating a new directory for the audio chunks from where i will take them for processing
                folder_name = input(
                    "Enter a folder name... It must be different for every time you run this program....")
                if not os.path.isdir(folder_name):
                    os.mkdir(folder_name)
                else:
                    print("Enter a different folder name as this already exists.")
                    exit()
                for i, audio_chunk in enumerate(chunks, start=1):
                    chunk_filename = os.path.join(folder_name, f"chunk{i}.mp3")
                    audio_chunk.export(chunk_filename, format="mp3")
                    with sr.AudioFile(chunk_filename) as sourcer:
                        audio_listened = self.audio_initializer.record(sourcer)
                        try:
                            textt = self.audio_initializer.recognize_google(audio_listened)
                        except sr.UnknownValueError as error:
                            print(f"Error {error}")
                        else:
                            final_text += textt
                print(final_text)

            return audio_to_text()

        return video_to_audio()


def proccesses():
    user = VideoToText()

    return user.video_to_text()


print(proccesses())
