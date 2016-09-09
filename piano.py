"""
 Piano
 Copyright (c) 2016 Seeed Technology Limited.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import os
import threading
import wave

import pyaudio

CHUNK_SIZE = 256
PIANO_PATH = os.path.dirname(os.path.realpath(__file__))


class Player:
    def __init__(self, pa):
        self.pa = pa
        self.event = threading.Event()
        self.wav = wave.open(os.path.join(PIANO_PATH, 'c1.wav'), 'rb')
        self.stream = self.pa.open(format=pyaudio.paInt16,
                                   channels=self.wav.getnchannels(),
                                   rate=self.wav.getframerate(),
                                   output=True,
                                   # start=False,
                                   # output_device_index=1,
                                   frames_per_buffer=CHUNK_SIZE,
                                   stream_callback=self._callback)

    def play(self, wav_file, block=False):
        self.wav = wave.open(wav_file, 'rb')
        if block:
            self.event.clear()
            self.event.wait()

    def close(self):
        self.stream.close()

    def _callback(self, in_data, frame_count, time_info, status):
        data = self.wav.readframes(frame_count)
        if self.wav.getnframes() == self.wav.tell():
            if data is None:
                data = ''
            data = data.ljust(frame_count * self.wav.getsampwidth() * self.wav.getnchannels(), '\x00')
            self.event.set()

        return data, pyaudio.paContinue


if __name__ == '__main__':
    pa = pyaudio.PyAudio()
    player = Player(pa)

    while True:
        line = raw_input()
        if line:
            args = line.split(' ')
            tune = os.path.join(PIANO_PATH, args[-1])
            if os.path.isfile(tune):
                print('Play %s' % args[-1])
                player.play(tune)

            if line == 'close':
                break

    player.close()
