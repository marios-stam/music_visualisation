#include <FastLED.h>

#define LED_PIN     7
#define NUM_LEDS    250
#define MIDDLE   125
#define BRIGHTNESS  64
#define MIN_BRIGHT  60
#define MAX_BRIGHT  120
#define BRIGHTNESS_FADE 1
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

#define UPDATES_PER_SECOND 100




CRGBPalette16 currentPalette;
TBlendType    currentBlending;



void setup() {
    Serial.begin(115200);
    delay( 3000 ); // power-up safety delay
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    FastLED.setBrightness(  BRIGHTNESS );
    
    currentPalette = RainbowColors_p;
    currentBlending = LINEARBLEND;
    
    static uint8_t startIndex = 0;
    
    FillLEDsFromPaletteColors( startIndex,MIDDLE,NUM_LEDS);
    
    FastLED.show();
}

int vol,i;
void loop(){
  if(Serial.available()) vol=Serial.read();
  
  FillLEDsFromPaletteColors(0,MIDDLE,constrain(MIDDLE+vol,0,MIDDLE*2));
  for (i=MIDDLE+vol;i<NUM_LEDS;i++){
      leds[i] = CRGB::Black; 
  } 
  mirroring();
  //FastLED.setBrightness(set_Brightness(vol));
  FastLED.show();
}

void mirroring(){
  for(int i=1;i<MIDDLE;i++){
    leds[MIDDLE-i]=leds[MIDDLE+i];
  }
}

int set_Brightness(int x) {
  static int current = MIN_BRIGHT;

  if (x > current) {
    current = x;
    return x;
  }
  current -= BRIGHTNESS_FADE;
  if (current < MIN_BRIGHT ) current = MIN_BRIGHT ;
  if (current > MAX_BRIGHT ) current = MAX_BRIGHT ;

  return current;
}


void FillLEDsFromPaletteColors( uint8_t colorIndex,int start,int telos){
    uint8_t brightness =200;
    
    for( int i = start; i < telos; i++) {
        leds[i] = ColorFromPalette( currentPalette, colorIndex, brightness, currentBlending);
        colorIndex += 3;
    }
}



