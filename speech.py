from pydub import AudioSegment
import speech_recognition as sr


def mp3_to_wav(mp3_filename):
    """Convert mp3 to wav"""
    wav_filename = mp3_filename.replace(".mp3", ".wav")
    segment = AudioSegment.from_mp3(mp3_filename)
    sound = segment.set_channels(1).set_frame_rate(16000)
    garbage = len(sound) / 3.1
    sound = sound[+garbage:len(sound) - garbage]
    sound.export(wav_filename, format="wav")
    return wav_filename


def get_audio_text(mp3_filename):
    wav_filename = mp3_to_wav(mp3_filename)
    # Initialize a new recognizer with the audio in memory as source
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_filename) as source:
        audio = recognizer.record(source)  # read the entire audio file

    # recognize speech using Google Speech Recognition
    audio_output = None
    try:
        audio_output = recognizer.recognize_google(audio)
        print("Google Speech Recognition: " + audio_output)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return audio_output
