//Imports
//IMPORTS

//Global declarations
int channel, messageLen;
byte message[128];
//GLOBALS


//Functions
//FUNCTIONS

void setup(){
    Serial.begin(9600);

    //Setup
    //SETUP
}

void loop(){

    //No Input


    if(Serial.available() >= 2){
        channel = Serial.read() << 8;
        channel += Serial.read();

        messageLen = Serial.read() << 8;
        messageLen += Serial.read();

        int i;
        for(i = 0; i < messageLen; i++)
            message[i] = Serial.read();



        switch(channel){
            //Input Cases
            //CASES

        }
    }

}