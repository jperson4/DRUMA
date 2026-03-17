import sounddevice as sd
import numpy as np

duration = 2
freq = 440
t = np.linspace(0, duration, int(44100 * duration))
tone = np.sin(2 * np.pi * freq * t).astype(np.float32)
sd.play(tone, samplerate=44100)
sd.wait()