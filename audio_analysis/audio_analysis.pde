final static float   NORMALIZATION_FACTOR=1;
final static float DECAY=0.7;
final static int MAX_SUM=135;


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
  
  sum=0;
  for (int i = 0; i < 200; i++) {
    sum+=spectrum[i];
  }
  sum*=1000;

  
   println(sum);
  sum= normalize(sum);
   println("===",sum);

  sum=map(sum, 0, 800, 1, 135);

  
  if (sum>MAX_SUM) sum=MAX_SUM;
  myPort.write(int(sum));
  graph(int(l),sum);
 
  
}


void graph(int l,float sum){
   line(0, width/4, sum, width/4);
  for (int i = 0; i < bands; i++) {
        line( i, height, i, height - spectrum[i]*height*8 );
  }
}
float normalize(float x) {
  //if (old<=0) return old=0;
  old+=(x-old)/NORMALIZATION_FACTOR;
  return old;
}
float normalize2(float x) {
  return old=x*NORMALIZATION_FACTOR+old*(1-NORMALIZATION_FACTOR);
}


float loasy_peak_detetctor(float x) {
  if(x>=old) old+=x*0.5;
  else  old=old*DECAY;
  return old;
}