unsigned short EMGsig;           // Store the EMG signal value
unsigned short EMGRawsig;        // Store the EMG raw signal value

void setup() {
 Serial.begin(9600); // Starting the communication with the computer
 EMGsig = 0;
 EMGRawsig = 0;
}

void loop() {
 EMGsig = analogRead(A0); // Read the analog values of the rectified+integrated EMG signal (0–1023)
 EMGRawsig = analogRead(A1); // Read the analog values of the raw EMG signal (0–1023)
 // print to srial the values
 Serial.print(EMGsig);
 Serial.print(",");
 Serial.println(EMGRawsig);
 
 delay(10);  // 1 second (1000ms) delay to not cause it to move as frantically. But this can be adjusted as you like.
}
