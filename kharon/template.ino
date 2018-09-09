//Imports
//IMPORTS

//Global declarations
unsigned int channel, messageLen;
int ledPin = 13;
byte message[128];
//GLOBALS


//Functions
//FUNCTIONS

void setup(){
    Serial.begin(9600);
    pinMode(ledPin, OUTPUT);

    //Setup
    //SETUP
}

void loop(){

    //No Input


    if(Serial.available() >= 2){
        delay(500);
        channel = Serial.read();
        channel += Serial.read() << 8;

        messageLen = Serial.read();
        messageLen += Serial.read() << 8;

        int i;
        for(i = 0; i < messageLen; i++)
            message[i] = Serial.read();



        switch(channel){
            //Input Cases
            //CASES

            default:
                digitalWrite(ledPin, HIGH);
                delay(1000);
                digitalWrite(ledPin, LOW);
                delay(1000);
                break;
        }
    }

}