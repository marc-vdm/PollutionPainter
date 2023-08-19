
#include <Adafruit_DotStar.h>
// Because conditional #includes don't work w/Arduino sketches...
#include <SPI.h>

#define NUMPIXELS 240
#define DATAPIN    11
#define CLOCKPIN   13
Adafruit_DotStar strip(NUMPIXELS, DATAPIN, CLOCKPIN, DOTSTAR_BRG);

unsigned int cutoff = 250;
unsigned int brightness = 20;
unsigned int wait = 10;
unsigned int fade = 5000;
unsigned int currentBrightness;
int state = 0;

//String inputString = "";
//boolean stringComplete;
unsigned long lastUpdate;
unsigned long startTime;

const byte numChars = 32;
char receivedChars[numChars];
bool newData = false;

void setup() {
  // put your setup code here, to run once:
  strip.begin();
  strip.show();
  strip.setBrightness(brightness);
  Serial.begin(9600);
  //inputString.reserve(200);
  // tell the PC we are ready
  //Serial.println("<Arduino is ready>");
}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}


void loop() {
//  while (Serial.available()) {
//    // get the new byte:
//    char inChar = (char)Serial.read();
//    // add it to the inputString:
//    inputString += inChar;
//    // if the incoming character is a newline, set a flag so the main loop can
//    // do something about it:
//    if (inChar == '\n') {
//      stringComplete = true;
//    }
    // get the new string:
    //inputString = Serial.readStringUntil('\n');
    //stringComplete = true;
//
//    
//  }
  recvWithStartEndMarkers();
  if (newData) {
    //Serial.println(receivedChars);
    String inputString(receivedChars);
    Serial.print(inputString);
    if (inputString.startsWith("cutoff ") && inputString.length() == 10) {
      cutoff = constrain(inputString.substring(7).toInt(),0, 255);
//      Serial.print("cutoff ");
//      Serial.println(cutoff, DEC);
    } else if (inputString.startsWith("brightness ") && inputString.length() == 14) {
      brightness = constrain(inputString.substring(11).toInt(), 0, 255);
      strip.setBrightness(brightness);
//      Serial.print("brightness ");
//      Serial.println(brightness, DEC);
    } else if (inputString.startsWith("wait ") && inputString.length() == 8) {
      wait = inputString.substring(5).toInt();
//      Serial.print("wait ");
//      Serial.println(wait, DEC);
    } else if (inputString.startsWith("fade ") && inputString.length() == 9) {
      fade = inputString.substring(5).toInt();
//      Serial.print("fade ");
//      Serial.println(fade, DEC);
    } else if (inputString.startsWith("start")) {
      state = 1;
      startTime = millis();
//      Serial.println("starting");
    } else if (inputString.startsWith("stop")) {
      state = 3;
      startTime = millis();
//      Serial.println("stopping");
    }
    //inputString = "";
    //stringComplete = false;
    newData = false;
  }

  if (millis() - lastUpdate > wait) {
    // put your main code here, to run repeatedly:
    switch (state) {
      case 0:
        for (int i = 0; i < strip.numPixels(); i++) {
          strip.setPixelColor(i, strip.Color(0, 0, 0));
        }
        break;
      case 1:
        if (millis() - startTime < fade) {
          for (int i = 0; i < strip.numPixels(); i++) {
            if (cutoff < random(256)) {
              strip.setPixelColor(i, strip.Color(255, 255, 255));
            } else {
              strip.setPixelColor(i, strip.Color(0, 0, 0));
            }
          }
          currentBrightness = map(millis() - startTime, 0, fade, 0, brightness);
          strip.setBrightness(map(millis() - startTime, 0, fade, 0, brightness));
        } else {
          for (int i = 0; i < strip.numPixels(); i++) {
            if (cutoff < random(256)) {
              strip.setPixelColor(i, strip.Color(255, 255, 255));
            } else {
              strip.setPixelColor(i, strip.Color(0, 0, 0));
            }
          }
          strip.setBrightness(brightness);
          currentBrightness = brightness;
          state = 2;
        }
        break;
      case 2:
        for (int i = 0; i < strip.numPixels(); i++) {
          if (cutoff < random(256)) {
            strip.setPixelColor(i, strip.Color(255, 255, 255));
          } else {
            strip.setPixelColor(i, strip.Color(0, 0, 0));
          }
        }
        break;
      case 3:
        if (millis() - startTime < fade) {
          for (int i = 0; i < strip.numPixels(); i++) {
            if (cutoff < random(256)) {
              strip.setPixelColor(i, strip.Color(255, 255, 255));
            } else {
              strip.setPixelColor(i, strip.Color(0, 0, 0));
            }
          }
          strip.setBrightness(map(millis() - startTime, 0, fade, currentBrightness, 0));
        } else {
          for (int i = 0; i < strip.numPixels(); i++) {
            strip.setPixelColor(i, strip.Color(0, 0, 0));
          }
          strip.setBrightness(0);
          state = 0;
        }
        break;
    }
    strip.show();
    lastUpdate = millis();
  }
}

//void serialEvent() {
//  while (Serial.available()) {
//    // get the new byte:
//    char inChar = (char)Serial.read();
//    // add it to the inputString:
//    inputString += inChar;
//    // if the incoming character is a newline, set a flag so the main loop can
//    // do something about it:
//    if (inChar == '\n') {
//      stringComplete = true;
//    }
//  }
//}
