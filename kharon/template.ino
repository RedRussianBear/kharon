//Imports


//Global declarations
int channel, messageLen;

//Hardware pin allocations


//Functions


void setup(){
    Serial.begin(9600);

    //Setup
}

void loop(){

    //No Input


    if(Serial.available() >= 2){
        channel = Serial.read() << 8;
        channel += Serial.read();

        messageLen = Serial.read() << 8;
        messageLen += Serial.read();

        switch(channel){
            //InputCases


        }

    }

}