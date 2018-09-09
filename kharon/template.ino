//Imports
//IMPORTS

//Global declarations
byte message[128];
//GLOBALS


struct Gen {
  unsigned int channel;
  unsigned int messageLen;
  } general;

//Functions
//FUNCTIONS

void setup(){
    Serial.begin(9600);

    //Setup
    //SETUP
}

void loop(){

    //No Input


    if(Serial.available() >= 4){
        delay(500);
        Serial.readBytes((char*)&general, 4);

        unsigned int channel = general.channel;
        unsigned int messageLen = general.messageLen;

        Serial.readBytes((char*)&message, messageLen);

        switch(channel){
            //Input Cases
            //CASES

        }

    }

}