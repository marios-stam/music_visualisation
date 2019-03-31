#include <FastLED.h>

// How many leds in your strip?
#define NUM_LEDS 250

#define DATA_PIN 7
#define BRIGHTNESS  100

// Define the array of leds
CRGB leds[NUM_LEDS];

void setup() { 
       Serial.begin(115200);
      // Uncomment/edit one of the following lines for your leds arrangement.
       //FastLED.addLeds<WS2811, DATA_PIN, GRB>(leds, NUM_LEDS);
       FastLED.setBrightness( BRIGHTNESS );
      // FastLED.addLeds<WS2812, DATA_PIN, RGB>(leds, NUM_LEDS);
       FastLED.addLeds<WS2812B, DATA_PIN, RGB>(leds, NUM_LEDS);
      //FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
}
int volume,i,peak_pos=0;
void loop() { 
  // Turn the LED on, then pause
  if(Serial.available() > 0) {
    volume = Serial.read();
  }
  //volume=20;
  if(peak_pos<volume)peak_pos=volume;
  else peak_pos-=1;
  
  for(i=0;i<volume;i++){
       leds[i]=getColor(i);
  }
  for(i=volume;i<NUM_LEDS;i++){
       leds[i] = CRGB::Black;
  }
  leds[peak_pos]=CRGB::Purple;
    
  FastLED.show();
  
    }


CRGB getColor(int level ){
  if(level<50)   return CRGB::Yellow;
  else if(level<150) return CRGB::Red;
  else return CRGB::Green;
  }

