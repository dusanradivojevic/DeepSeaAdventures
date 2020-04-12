from playsound import playsound
import wave
import contextlib
import threading


class SoundPlayer:
    def __init__(self, file, loop=False):
        self.file = file
        self.duration = self.get_duration()
        self.looping = loop
        self.active = True

    def stop(self):
        self.active = False

    def play(self):
        if not self.active:
            return

        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

        if self.looping:
            loop_thread = threading.Timer(self.duration, self.play)
            loop_thread.daemon = True
            loop_thread.start()

    def get_duration(self):
        with contextlib.closing(wave.open(self.file, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration

    def run(self):
        playsound(self.file, True)

