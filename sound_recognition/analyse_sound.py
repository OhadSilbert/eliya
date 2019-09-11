movie_file_path = r"C:\Users\Evi\Dropbox\Elia\WhatsApp Video 2019-09-10 at 17.32.07.mp4"
audio_fp = r"C:\Users\Evi\Dropbox\Elia\WhatsApp Video 2019-09-10 at 17.32.07 (online-audio-converter.com).wav"

# import speech_recognition as sr
# r = sr.Recognizer()
# with sr.AudioFile(audio_fp) as source:
#     audio = r.record(source)
import librosa
data, sampling_rate = librosa.load(audio_fp)
