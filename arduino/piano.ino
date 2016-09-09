/*
   Please use Arduino IDE 1.6.8+ which has some useful new features

   Play sound
   Use capacitive touch sensors to trigger sound
*/

#include "respeaker.h"

// use sound files which are able to be found on SD card, new mp3/wav files can be added to SD card
const char *sound_map[] = {"c1.wav", "d1.wav", "e1.wav", "f1.wav", "g1.wav", "a1.wav", "b1.wav", "c2.wav"};

void setup() {
  respeaker.begin();
  respeaker.attach_touch_handler(touch_event);  // add touch event handler
}

void loop() {}

// id: 0 ~ 7 - touch sensor id; event: 1 - touch, 0 - release
void touch_event(uint8_t id, uint8_t event) {
  if (event) {
    respeaker.pixels().set_color(id + 2, Pixels::wheel(id * 30));
    respeaker.play(sound_map[id]);
  } else {
   respeaker.pixels().set_color(id + 2, 0);
  }
  respeaker.pixels().update();
}
