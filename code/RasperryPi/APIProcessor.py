from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from openai import OpenAI
import pvporcupine
import pyaudio
import numpy as np
import soundfile as sf
import time
from google.cloud import speech
import os
from TCP_sender import TCP_sender
import threading
import numpy as np
from numpy.linalg import norm
from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import logging
import gc


class APIProcessor:
    def __init__(self):
        self.openai_key = None
        self.elevenlabs_key = None
        self.porcupine_key = None
        self.system_prompt = None
        self.google_key_path = None 
        self.encoder = VoiceEncoder()
        self.load_prompt()
        self.message_history = [{"role": "system", "content": self.system_prompt}] 
        self.get_API_keys()
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.google_key_path
        self.client_openai = OpenAI(api_key=self.openai_key)
        self.client_elevenlabs = ElevenLabs(api_key=self.elevenlabs_key)
        self.client_porcupine = pvporcupine.create(access_key=self.porcupine_key,keyword_paths=["Hey-Pi-car_en_raspberry-pi_v3_0_0.ppn"])
        self.client_cloud = speech.SpeechClient()
        self.pa = pyaudio.PyAudio()
        self.frame_length = self.client_porcupine.frame_length
        self.sample_rate = self.client_porcupine.sample_rate

    def load_prompt(self):
        with open("system_prompt.txt") as f:
            self.system_prompt = f.read()
        

    def get_API_keys(self):
        load_dotenv()  # .env dosyasını oku

        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        self.porcupine_key = os.getenv("PORCUPINE_API_KEY")
        self.google_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    def speech(self, text):
        audio = self.client_elevenlabs.text_to_speech.convert(
            text=text,
            voice_id="IuRRIAcbQK5AQk1XevPj",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

        play(audio)

    def getJSON(self, command):
        message = {"role":"user", "content": command}
        self.message_history.append(message)
        completion = self.client_openai.responses.create(
        model="gpt-4o-mini",
        input= self.message_history
        )
        assistant_message = {"role":"assistant", "content": completion.output_text}
        self.message_history.append(assistant_message)
        return completion.output_text
    
    def detect_wakeword(self,pa):
        print("🎧 Wake word dinleniyor...")
        threading.Thread(target=TCP_sender,args=("ses",), daemon=True).start()

        stream = pa.open(
            rate= self.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer= self.frame_length
        )

        try:
            while True:
                pcm = stream.read(self.frame_length, exception_on_overflow=False)
                pcm = np.frombuffer(pcm, dtype=np.int16)
                result = self.client_porcupine.process(pcm)
                if result >= 0:
                    print("✅ Wake word detected!")
                    #threading.Thread(target=TCP_sender,args=("ses",), daemon=True).start()
                    break
        finally:
            stream.stop_stream()
            stream.close()

    def record_command(self,pa, threshold=500, silence_duration=1):
        print("🎙️ Komut bekleniyor...")
        threading.Thread(target=TCP_sender,args=("wakeword",), daemon=True).start()

        stream = pa.open(
            rate=self.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.frame_length,
        )

        frames = []
        silent_chunks = 0

        # 3 saniye boyunca kayıt (sessizlik kontrolü olmadan)
        start_time = time.time()
        while time.time() - start_time < 1:
            audio = stream.read(self.frame_length, exception_on_overflow=False)
            frames.append(audio)

        print("⏳ 1 saniye tamamlandı, sessizlik algılanacak...")

        # Sonrasında sessizlik algılamaya başla
        while True:
            audio = stream.read(self.frame_length, exception_on_overflow=False)
            data = np.frombuffer(audio, dtype=np.int16)
            volume = np.abs(data).mean()
            frames.append(audio)

            if volume < threshold:
                silent_chunks += 1
            else:
                silent_chunks = 0

            if silent_chunks > (silence_duration * self.sample_rate / self.frame_length):
                print("🔇 Sessizlik algılandı, kayıt sonlandırılıyor.")
                break

        stream.stop_stream()
        stream.close()

        # WAV dosyası olarak kaydet
        audio_data = b''.join(frames)
        audio_np = np.frombuffer(audio_data, dtype=np.int16)
        filename = "command.wav"
        sf.write(filename, audio_np, samplerate=self.sample_rate, subtype='PCM_16')
        print("💾 Komut kaydedildi:", filename)
        return filename
    
    def transcribe_google(self,audio_path):
        print("🧠 Komut Google Speech-to-Text ile çözülüyor...")

        with open(audio_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.sample_rate,
            language_code="tr-TR"
        )

        response = self.client_cloud.recognize(config=config, audio=audio)

        if not response.results:
            return ""

        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript

        return transcript
    
    def recognize_cosine(self, wav_path, profiles, threshold=0.7):
        wav = preprocess_wav(wav_path)
        test_embed = self.encoder.embed_utterance(wav)

        similarities = {
            name: np.dot(profile, test_embed) / (norm(profile) * norm(test_embed))
            for name, profile in profiles.items()
        }

        best_match = max(similarities, key=similarities.get)
        best_score = similarities[best_match]

        if best_score < threshold:
            return None, best_score
        return best_match, best_score
    
    def recognize_person(self, db):
        embeddings = np.load("/home/monster/grup10/myenv/embeddings.npy")
        labels = np.load("/home/monster/grup10/myenv/labels.npy")
        profiles_npz = np.load("/home/monster/grup10/myenv/profiles.npz")
        profiles = {key: profiles_npz[key] for key in profiles_npz.files}
        person = db.read_document("kullanici_kimliklendirme")

        if(person.get("herkes") == True):
            return True
        
        best_match, best_score = self.recognize_cosine("/home/monster/grup10/myenv/command.wav", profiles, 0.70)
        print(f"Tanınan kişi: {best_match or 'Tanımsız'} (skor: {best_score:.2f})")
        if(person.get("secilen_alperen") == True and best_match == "secilen_alperen"):
            return True
        elif(person.get("secilen_fatih") == True and best_match == "secilen_fatih"):
            return True
        elif(person.get("secilen_efe") == True and best_match == "secilen_efe"):
            return True
        elif(person.get("secilen_yagiz") == True and best_match == "secilen_yagiz"):
            return True
        elif(person.get("secilen_yilmaz") == True and best_match == "secilen_yilmaz"):
            return True
        else:
            return False
        
    
    def speech_to_text(self, db):
        try:
            self.detect_wakeword(self.pa)
            audio_file = self.record_command(self.pa)
            is_recognize = self.recognize_person(db)
            komut = self.transcribe_google(audio_file)
            print("📢 Algılanan komut:", komut)
        except KeyboardInterrupt:
            print("\n⛔ Kullanıcı tarafından durduruldu.")
            
        return komut, is_recognize
        