unsigned short EMGsig;           // Store the EMG signal value
unsigned short esc;

void setup() {
 Serial.begin(9600); // Starting the communication with the computer
 esc = 0xFFFF;
 EMGsig = 0;
}

void loop() {
 //EMGsig = analogRead(A0); // Read the analog values of the rectified+integrated EMG signal (0–1023)
 EMGsig += 10;
 if (EMGsig > 1023)
  EMGsig = 0;  
 // print to srial the values
 Serial.write((byte*)&esc, 2);
 Serial.write((byte*)&EMGsig, 2);
 //Serial.println(EMGsig);
 
 delay(10);  // 1 second (1000ms) delay to not cause it to move as frantically. But this can be adjusted as you like.
}
