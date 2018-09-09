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

        Serial.println(channel);
        Serial.println(messageLen);

        Serial.readBytes((char*)&message, messageLen);

        Serial.println((char *)message)



        switch(channel){
            //Input Cases
            //CASES

        }
    }

}