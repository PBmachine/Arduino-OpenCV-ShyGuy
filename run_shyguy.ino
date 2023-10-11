//https://forum.arduino.cc/t/serial-input-basics-updated/382007/2

const byte numChars = 16;
char receivedChars[numChars];
char tempChars[numChars]; 
int msgInt = 0; 
char msgChars[numChars] = {0};
bool newData = false;


//states = [hiding,waiting,dancing]
int state = 1;
int motion = 0;
int control_pin = 5; 
int led = 6;

unsigned long motortimer;
unsigned long timershimmy;

int motorperiod = 6; 
bool motorOn = false;

void setup()
{
  //start serial communication at Baud rate of 9600
  Serial.begin(9600);
  pinMode(control_pin, OUTPUT);
  pinMode(led, OUTPUT);
  digitalWrite(led, HIGH);
}

void loop() {
    recvWithStartEndMarkers();
    if (newData == true){
      strcpy(tempChars, receivedChars);
      parseMessage();
      newData = false;
    }
    runGuy();
}

void runMotor(){
  int ondelay = 1000*map(motion,0,100,0.1,motorperiod);
  int offdelay = (motorperiod*1000 -ondelay)+100;

  if(motorOn){
    if ((millis()-motortimer)>= ondelay){
      motorOn = false;
      motortimer = millis();
    }
    digitalWrite(control_pin,HIGH);
  }
  else{
    if ((millis()-motortimer)>= offdelay){
      motorOn = true;
      motortimer = millis();
      digitalWrite(control_pin,HIGH);
    }
    digitalWrite(control_pin,LOW);

  }
    
}

void runGuy(){
  switch(state)
  {
    case 0:
    //hiding
      motion = 0; 
      digitalWrite(control_pin, LOW);
      break;
    case 1:
      runMotor();
      break;
    case 2:
      runMotor();
      break;
  }
}


void executeMessage(int new_int,char new_char){
  bool newValues = false;
  int new_state;
  switch(new_char){
    case 'D':
      new_state = 2;
      break;
    case 'H':
      new_state = 0;
      break;
      case 'W':
      new_state = 1;
      break;
  }
  if (new_state != state){
    state = new_state;
  }
  if (new_int != motion){
    motion = new_int;
  }
}

void parseMessage()
{
char *msgNdx; // pointer index for parsing input message into tokens
msgNdx = strtok(tempChars, ":,"); //split on : , 
strcpy(msgChars, msgNdx); //store first part of message as char
msgChars[0] &= 0xDF;
msgChars[1] &= 0xDF; //make chars uppercase
msgNdx = strtok(NULL, ":,"); //continue tokenizing message
msgInt = atoi(msgNdx); //store next part of message as int
executeMessage(msgInt,msgChars[0]);
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