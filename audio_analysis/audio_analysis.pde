final static int  NORMALIZATION_FACTOR=4 ;


import processing.sound.*;
import processing.serial.*;

Serial myPort;  // Create object from Serial class

FFT fft;
Amplitude amp;
AudioIn in;
int bands = 512;
float[] spectrum = new float[bands];
float  l;
void setup() {
  size(600, 360);
  background(255);

  String portName = Serial.list()[0]; //change the 0 to a 1 or 2 etc. to match your port
  myPort = new Serial(this, portName, 115200);

  // Create an Input stream which is routed into the Amplitude analyzer
  fft = new FFT(this, bands);
  amp = new Amplitude(this);

  in = new AudioIn(this, 0);
  // start the Audio Input
  in.start();


  // patch the AudioIn
  fft.input(in);
  amp.input(in);
}      
float old=0;
float l_max=0;
float sum;
void draw() { 
  background(255);
  fft.analyze(spectrum);
  l=amp.analyze();
  //l=map(l,0,0.3,0,100);

  //old_l+=(l-old_l)/5;

  sum=0;
  for (int i = 0; i < 200; i++) {
    sum+=spectrum[i];
  }

  sum=map(sum, 0, 0.4, 0, 100);
  sum=  normalize(sum, NORMALIZATION_FACTOR);
  println(sum);
  myPort.write(int(sum));
  line(0, width/4, l, width/4);
  for (int i = 0; i < bands; i++) {
    // The result of the FFT is normalized
    //draw the line for frequency band i scaling it up by 5 to get more amplitude. 

    line( i, height, i, height - spectrum[i]*height*8 );
  }
}

float normalize(float x, int factor) {
  old+=(x-old)/factor;
  return old;
}