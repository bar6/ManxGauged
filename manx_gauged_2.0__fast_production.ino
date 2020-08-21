#include <stdio.h>
#include <LiquidCrystal.h>


#define DELA 500   // Long delay.
#define DSHORT 250 // Short delay.
const int ledPin = 13;

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

// initialize the library with the numbers of the interface pins
//LiquidCrystal lcd(12, 11, 5, 4, 9, 8);


//prepopulate temp array
int index_air_array = 0;
int air_temp_temp = 0;
volatile unsigned char air_temp_array[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}; //50 long

//prepopulate fuel level array
int index_fuellevel_array = 0;
int fuellevel_temp_temp = 0;
volatile unsigned int fuellevel_temp_array[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}; //50 long

//prepopulate oil temperature array
int index_oiltemperature_array = 0;
int oiltemperature_temp_temp = 0;
volatile float oiltemperature_temp_array[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}; //50 long


//prepopulate tachometer array
int index_tachometer_array = 0;
volatile unsigned int tachometer_array[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}; //50 long



void setup() {
  // initialize digital pins
  pinMode(11, INPUT); //oil light
  pinMode(10, OUTPUT); //Suicide Relay
  pinMode(6, INPUT); //key on/off detection
  pinMode(7, INPUT); //tachometer
  pinMode(2, INPUT); //left wheel
  pinMode(3, INPUT); //right wheel
  pinMode(5, INPUT); //left turn  //uncomment for production mode (no 16x2 LCD)
  pinMode(4, INPUT); //right turn //uncomment for production mode (no 16x2 LCD)
  pinMode(9, INPUT); //high beam  //uncomment for production mode (no 16x2 LCD)
  pinMode(8, INPUT); //alternator //uncomment for production mode (no 16x2 LCD)

  // set up the LCD's number of columns and rows:
  //lcd.begin(16, 2);
  digitalWrite(10, 1); //Pin 10 is suicide relay pin  //remember 0 is on and 1 is off for relay

  Serial.begin(57600); 
  inputString.reserve(200);
  
  attachInterrupt(digitalPinToInterrupt(2), ISRleftwheel, RISING);
  attachInterrupt(digitalPinToInterrupt(3), ISRrightwheel, RISING);
  

  //Wait 1 seconds before turning suicide relay pin on
  delay(1000);
  digitalWrite(10, 0); //Pin 10 is suicide relay pin  //remember 0 is on and 1 is off for relay

  air_temp_temp = (5.0 * analogRead(0) * 100.0) / 1024;
  for(index_air_array = 0;index_air_array < 50; index_air_array++){
    air_temp_array[index_air_array] = air_temp_temp;
  }
  index_air_array = 0;

  //read fuel level and populate array
    fuellevel_temp_temp = analogRead(1);
  for(index_fuellevel_array = 0;index_fuellevel_array < 50; index_fuellevel_array++){
    fuellevel_temp_array[index_fuellevel_array] = fuellevel_temp_temp;
  }
  index_air_array = 0;
}

//HyperTerminal SPI Definitions:
#define XTAL 7373000L
#define BAUD 115200L

//Motor Rotate Definitions
  
#define FREQ 10000L //To interrupt timer 0 every 100 microseconds ((1/10000Hz)=100 us)
#define TIMER0_RELOAD_VALUE (65536L-((XTAL)/(2*FREQ))) //Reload Value (calculated using datasheet formula)
#define CLK 11111111L
#define TIMER_2_RELOAD (0x10000L-(CLK/(32L*BAUD)))

//define external pins to read idiot lights, and turn signals
#define oil_light_pin 11

//#define suicide_pin 10
#define key_onoff_pin 6
#define left_turn_light_pin 5     //uncomment for production mode (no 16x2 LCD)
#define right_turn_light_pin 4    //uncomment for production mode (no 16x2 LCD)
#define high_beam_light_pin 9     //uncomment for production mode (no 16x2 LCD)
#define alternator_light_pin 8    //uncomment for production mode (no 16x2 LCD)


volatile unsigned char lefttractionLOST = 0;
volatile unsigned char righttractionLOST = 0;

//wheel speed
#define wheelleftpin 8 //input
#define wheelrightpin 9 //input
volatile unsigned int overflow0count = 0;
volatile unsigned int overflow1count = 0;

//Tachometer
#define tach_pin 7 //input

//wheel dimensions
//float wheelcircumference = 0.0023141; //in km
float wheelcircumference = 0.0014379; //in km

//Speed variables
volatile unsigned int RPM = 999;
volatile float speedleft = 0.0;
volatile float speedright = 0.0;
volatile float tachometer = 0.0;
volatile unsigned char truncspeedleft = 0;
volatile unsigned char trunctachometer = 0;
volatile unsigned char truncspeedright = 0;
volatile unsigned int avgleftspeed = 0;
volatile unsigned int avgrightspeed = 0;
volatile unsigned int avg_air_temp = 0;
volatile unsigned long avg_fuellevel_temp = 0;
volatile float avg_oiltemperature_temp = 0;
volatile unsigned long avg_tachometer = 0;


volatile unsigned char speedleftarray[] = {0,0,0,0,0,0,0,0,0,0}; //9 long
volatile unsigned char speedrightarray[] = {0,0,0,0,0,0,0,0,0,0}; //9 long


//timestamps
volatile unsigned long timestamp_start_left;
volatile unsigned long timestamp_end_left;
volatile unsigned long timestamp_start_right;
volatile unsigned long timestamp_end_right;
volatile unsigned long timestamp_start_right_previous;
volatile unsigned long timestamp_end_right_previous;
volatile unsigned long timestamp_start_left_previous;
volatile unsigned long timestamp_end_left_previous;

//Serial Variables
String speed_left_serial = "";
String speed_right_serial = "";

//Variables sent to Raspberry pi
volatile int air_temp_raw = 0;
volatile int air_temp = 0;
volatile int fuellevel_temp = 0;
volatile int enginetemperature = 194;
volatile int alternator_light = 1;
volatile int oil_light = 1;
volatile int high_beam_light = 0;
volatile int left_turn_light = 1;
volatile int right_turn_light = 1;
volatile unsigned long odometer = 0;
volatile unsigned long tripometer = 0;
volatile int pi_on = 1; //1 = on, 0 = off
volatile int boot_override = 0;

volatile unsigned long ambient_air_resistance = 0;

//unsigned char number7segCONVERT[] = {0b11000000, 0b11111001, 0b10100100, 0b10110000, 0b10011001, 0b10010010, 0b10000010, 0b11111000, 0b10000000, 0b10011000}; //HGFEDCBA Common  Anode
unsigned char number7segCONVERT[] = {0b00111111, 0b00000110, 0b01011011, 0b01001111, 0b01100110, 0b01101101, 0b01111101, 0b00000111, 0b01111111, 0b01100111}; //HGFEDCBA Common  Cathode


//UI Variables
unsigned short int i = 0;         
signed  int platform[2]={0,0};
volatile short int cursor = 0;    //cursor index
volatile short int valueINDEX = 6;

//PWM Iterupt Variables
volatile unsigned char pwmcount;
volatile unsigned char redPWM1;
volatile unsigned char redPWM2;
volatile unsigned char bluePWM1;
volatile unsigned char bluePWM2;
char redSPEED[2] = {0, 40};
char blueSPEED[2] = {0, 25};
char redMODE[2] = {0,0};  // 0,0 = stop; 0,1 = positive; 1,0 = negative
char blueMODE[2] = {0,0};   // 0,0 = stop; 0,1 = positive; 1,0 = negative
char possibleINPUTS[] = {-45,-35,-25,-15,-10,-5,0,5,10,15,25,35,45};
int UIbuffer = 0;



//putcharlcd Function Variable, to differentiate between LCD and SPI display 
unsigned short int ToLCD = 1;




void loop()
{
  unsigned char indexleft = 0;
  unsigned char indexright = 0;
  unsigned char indextach = 0;
  char pidata[6];
  int frompi;
  int topi;
  byte incoming;

  //new wheel speed variables
  float speed;
  float timeinterval;
  float rpmwheel;

  float oiltemp_resistance;
  
  int leftwheel_check4stale_index = 0;
  int rightwheel_check4stale_index = 0;
  

  //initLCD();
  settimers();

  
  
  redPWM1 = 1;
  redPWM2 = 1;
  bluePWM1 = 1;
  bluePWM2 = 1;
  
  //init interrupts
  //ET1 = 1; //enable timer 1 interrupt 
  //ET0 = 1; //enable timer 0 interrupt
  //EA = 1; //enable global interrupts
  
  overflow0count = 0;
  overflow1count = 0;
  
  

  
  //TR0 = 0;
  //InitSerialPort();
  //ToLCD = 0;
  
  //printf_tiny("Current Platform Angles:\nRed = %d\nBlue =%d\n\nEnter Desired Platform Angle:\n0 = -45\n1 = -35\n2 = -25\n3 = -15\n4 = -10\n5 = -5\n6 = 0\n7 = 5\n8 = 10\n9 = 15\n10 = 25\n11 = 35\n12 = 45\n\nRed, Blue:\n", platform[0], platform[1]); 
  while (1)
  { 
    ToLCD = 0;


    //check for idiot lights and turn signals
    if (digitalRead(oil_light_pin) == 0){
      oil_light = 1;
    }else{
      oil_light = 0;}

    if (digitalRead(alternator_light_pin) == 0){
      alternator_light = 1;}
    else{
      alternator_light = 0;}
      
    if (digitalRead(high_beam_light_pin) == 1){
      high_beam_light = 1;}
    else{
      high_beam_light = 0;}

    if (digitalRead(left_turn_light_pin) == 1){
      left_turn_light = 1;}
    else{
      left_turn_light = 0;}

    if (digitalRead(right_turn_light_pin) == 1){
      right_turn_light = 1;}
    else{
      right_turn_light = 0;}
     


    if (digitalRead(key_onoff_pin) == 0){
      pi_on = 0;
    }
    else
      pi_on = 1;


      //delete this. Keeps pi on without looking at key on/ogg pin
       //pi_on = 1;
      
    

    
   //Serial.write("character");
    //button codes
    //P3_0 = wheelleftpin;
    
    //RPM = getfreqRED();

    


    tachometer = gettachometer(); //pin 7

    
    //new calculate wheel speed left 
    timeinterval = (timestamp_end_left-timestamp_start_left)/1000000.0;
    rpmwheel = 60.0/(timeinterval*16.0); //original
    //lcd.setCursor(0,1);
    //lcd.print(timeinterval);
    //lcd.print("     ");
    speed = rpmwheel*wheelcircumference*(60.0); //in km/h
    truncspeedleft = speed;

    //new calculate wheel speed right
    timeinterval = (timestamp_end_right-timestamp_start_right)/1000000.0;
    rpmwheel = 60.0/(timeinterval*16.0); //original
    //lcd.setCursor(0,1);
    //lcd.print(timeinterval);
    //lcd.print("     ");
    speed = rpmwheel*wheelcircumference*(60.0); //in km/h
    truncspeedright = speed;

    //check for no wheelspeed (see if micros has changes for 20 checks)
    if(timestamp_start_left_previous == timestamp_start_left && timestamp_end_left_previous == timestamp_end_left)
      leftwheel_check4stale_index = leftwheel_check4stale_index + 1;
    else
      leftwheel_check4stale_index = 0;
    //lcd.setCursor(0,1);
    //lcd.print("  ");
    //lcd.setCursor(0,1);
    //lcd.print(rightwheel_check4stale_index);

    if(timestamp_start_right_previous == timestamp_start_right && timestamp_end_right_previous == timestamp_end_right)
      rightwheel_check4stale_index = rightwheel_check4stale_index + 1;
    else
      rightwheel_check4stale_index = 0;

   if(leftwheel_check4stale_index > 80){
      leftwheel_check4stale_index = 88; //just to make sure it doesnt increment over 255 since its a char
      truncspeedleft = 0;
   }
   if(rightwheel_check4stale_index > 80){
      rightwheel_check4stale_index = 88; //just to make sure it doesnt increment over 255 since its a char
      truncspeedright = 0;
   }
   
    timestamp_start_left_previous = timestamp_start_left;
    timestamp_end_left_previous = timestamp_end_left;
    timestamp_start_right_previous = timestamp_start_right;
    timestamp_end_right_previous = timestamp_end_right;

    
    
    //since speed is shacky, try averaging
    //Left Speed averaging
    if (indexleft > 9)
      indexleft = 0;
    speedleftarray[indexleft] = truncspeedleft;
    //average speedleftarray
    avgleftspeed = (speedleftarray[0]+speedleftarray[1]+speedleftarray[2]+speedleftarray[3]+speedleftarray[4]+speedleftarray[5]+speedleftarray[6]+speedleftarray[7]+speedleftarray[8]+speedleftarray[9])/10;
    indexleft++;
    
    //Right Speed averaging
    if (indexright > 9)
      indexright = 0;
    speedrightarray[indexright] = truncspeedright;
    //average speedleftarray
    avgrightspeed = (speedrightarray[0]+speedrightarray[1]+speedrightarray[2]+speedrightarray[3]+speedrightarray[4]+speedrightarray[5]+speedrightarray[6]+speedrightarray[7]+speedrightarray[8]+speedrightarray[9])/10;
    indexright++;
    
   /* //find faster spped and display om 7 seg (incase senser breaks)
    if(avgrightspeed > avgleftspeed)
      displaySPEED7seg(avgrightspeed);
    else
      displaySPEED7seg(avgleftspeed);
    //displaySPEED7seg(truncspeedleft);*/

      
      
      
    //ToLCD = 1;
    //display();

    //this is the old way fro bough temp sensors from digikey
    //calculate air temp
    //air_temp_raw = analogRead(0);
    //air_temp = (5.0 * analogRead(0) * 100.0) / 1024;

    //Ford Temperature Sesnor
    //resistor in voltage divider = 98200 ohms
    ambient_air_resistance = ((1023.0*98200.0)/analogRead(8))-98200.0;
    air_temp=-21.62*log(ambient_air_resistance)+247.96;
    //ambient_air_temperature_f = (ambient_air_temperature_c*(9.0/5.0)) + 32.0

    //Average Air Temperature
    if (index_air_array > 49)
      index_air_array = 0;
    
    air_temp_array[index_air_array] = air_temp;
    
    avg_air_temp = (air_temp_array[0]+air_temp_array[1]+air_temp_array[2]+air_temp_array[3]+air_temp_array[4]+air_temp_array[5]+air_temp_array[6]+air_temp_array[7]+air_temp_array[8]+air_temp_array[9]+air_temp_array[10]+air_temp_array[11]+air_temp_array[12]+air_temp_array[13]+air_temp_array[14]+air_temp_array[15]+air_temp_array[16]+air_temp_array[17]+air_temp_array[18]+air_temp_array[19]+air_temp_array[20]+air_temp_array[21]+air_temp_array[22]+air_temp_array[23]+air_temp_array[24]+air_temp_array[25]+air_temp_array[26]+air_temp_array[27]+air_temp_array[28]+air_temp_array[29]+air_temp_array[30]+air_temp_array[31]+air_temp_array[32]+air_temp_array[33]+air_temp_array[34]+air_temp_array[35]+air_temp_array[36]+air_temp_array[37]+air_temp_array[38]+air_temp_array[39]+air_temp_array[40]+air_temp_array[41]+air_temp_array[42]+air_temp_array[43]+air_temp_array[44]+air_temp_array[45]+air_temp_array[46]+air_temp_array[47]+air_temp_array[48]+air_temp_array[49])/50;
   index_air_array = index_air_array+1;
   
    //Average Fuellevel
    if (index_fuellevel_array > 49)
      index_fuellevel_array = 0;
    
    fuellevel_temp_array[index_fuellevel_array] = analogRead(1);
    
    avg_fuellevel_temp = (fuellevel_temp_array[0]+fuellevel_temp_array[1]+fuellevel_temp_array[2]+fuellevel_temp_array[3]+fuellevel_temp_array[4]+fuellevel_temp_array[5]+fuellevel_temp_array[6]+fuellevel_temp_array[7]+fuellevel_temp_array[8]+fuellevel_temp_array[9]+fuellevel_temp_array[10]+fuellevel_temp_array[11]+fuellevel_temp_array[12]+fuellevel_temp_array[13]+fuellevel_temp_array[14]+fuellevel_temp_array[15]+fuellevel_temp_array[16]+fuellevel_temp_array[17]+fuellevel_temp_array[18]+fuellevel_temp_array[19]+fuellevel_temp_array[20]+fuellevel_temp_array[21]+fuellevel_temp_array[22]+fuellevel_temp_array[23]+fuellevel_temp_array[24]+fuellevel_temp_array[25]+fuellevel_temp_array[26]+fuellevel_temp_array[27]+fuellevel_temp_array[28]+fuellevel_temp_array[29]+fuellevel_temp_array[30]+fuellevel_temp_array[31]+fuellevel_temp_array[32]+fuellevel_temp_array[33]+fuellevel_temp_array[34]+fuellevel_temp_array[35]+fuellevel_temp_array[36]+fuellevel_temp_array[37]+fuellevel_temp_array[38]+fuellevel_temp_array[39]+fuellevel_temp_array[40]+fuellevel_temp_array[41]+fuellevel_temp_array[42]+fuellevel_temp_array[43]+fuellevel_temp_array[44]+fuellevel_temp_array[45]+fuellevel_temp_array[46]+fuellevel_temp_array[47]+fuellevel_temp_array[48]+fuellevel_temp_array[49])/50;
   index_fuellevel_array = index_fuellevel_array+1;

   //Calculate and Average oiltemperature
    if (index_oiltemperature_array > 49)
      index_oiltemperature_array = 0;

     oiltemp_resistance = (146.4*((analogRead(2)/1023.0)*5.0))/(5-((analogRead(2)/1023.0)*5.0)); //find the voltage from
    
    oiltemperature_temp_array[index_oiltemperature_array] = oiltemp_resistance;
    
    avg_oiltemperature_temp = (oiltemperature_temp_array[0]+oiltemperature_temp_array[1]+oiltemperature_temp_array[2]+oiltemperature_temp_array[3]+oiltemperature_temp_array[4]+oiltemperature_temp_array[5]+oiltemperature_temp_array[6]+oiltemperature_temp_array[7]+oiltemperature_temp_array[8]+oiltemperature_temp_array[9]+oiltemperature_temp_array[10]+oiltemperature_temp_array[11]+oiltemperature_temp_array[12]+oiltemperature_temp_array[13]+oiltemperature_temp_array[14]+oiltemperature_temp_array[15]+oiltemperature_temp_array[16]+oiltemperature_temp_array[17]+oiltemperature_temp_array[18]+oiltemperature_temp_array[19]+oiltemperature_temp_array[20]+oiltemperature_temp_array[21]+oiltemperature_temp_array[22]+oiltemperature_temp_array[23]+oiltemperature_temp_array[24]+oiltemperature_temp_array[25]+oiltemperature_temp_array[26]+oiltemperature_temp_array[27]+oiltemperature_temp_array[28]+oiltemperature_temp_array[29]+oiltemperature_temp_array[30]+oiltemperature_temp_array[31]+oiltemperature_temp_array[32]+oiltemperature_temp_array[33]+oiltemperature_temp_array[34]+oiltemperature_temp_array[35]+oiltemperature_temp_array[36]+oiltemperature_temp_array[37]+oiltemperature_temp_array[38]+oiltemperature_temp_array[39]+oiltemperature_temp_array[40]+oiltemperature_temp_array[41]+oiltemperature_temp_array[42]+oiltemperature_temp_array[43]+oiltemperature_temp_array[44]+oiltemperature_temp_array[45]+oiltemperature_temp_array[46]+oiltemperature_temp_array[47]+oiltemperature_temp_array[48]+oiltemperature_temp_array[49])/50;
   index_oiltemperature_array = index_oiltemperature_array+1;

  //Average Tachometer
    if (index_tachometer_array > 9)
      index_tachometer_array = 0;
    
    tachometer_array[index_tachometer_array] = tachometer;
    
    //backup way too slow...lol avg_tachometer = (tachometer_array[0]+tachometer_array[1]+tachometer_array[2]+tachometer_array[3]+tachometer_array[4]+tachometer_array[5]+tachometer_array[6]+tachometer_array[7]+tachometer_array[8]+tachometer_array[9]+tachometer_array[10]+tachometer_array[11]+tachometer_array[12]+tachometer_array[13]+tachometer_array[14]+tachometer_array[15]+tachometer_array[16]+tachometer_array[17]+tachometer_array[18]+tachometer_array[19]+tachometer_array[20]+tachometer_array[21]+tachometer_array[22]+tachometer_array[23]+tachometer_array[24]+tachometer_array[25]+tachometer_array[26]+tachometer_array[27]+tachometer_array[28]+tachometer_array[29]+tachometer_array[30]+tachometer_array[31]+tachometer_array[32]+tachometer_array[33]+tachometer_array[34]+tachometer_array[35]+tachometer_array[36]+tachometer_array[37]+tachometer_array[38]+tachometer_array[39]+tachometer_array[40]+tachometer_array[41]+tachometer_array[42]+tachometer_array[43]+tachometer_array[44]+tachometer_array[45]+tachometer_array[46]+tachometer_array[47]+tachometer_array[48]+tachometer_array[49])/50;
    avg_tachometer = (tachometer_array[0]+tachometer_array[1]+tachometer_array[2]+tachometer_array[3]+tachometer_array[4]+tachometer_array[5]+tachometer_array[6]+tachometer_array[7]+tachometer_array[8]+tachometer_array[9])/10;
 
   index_tachometer_array = index_tachometer_array+1;



    //write to serial
    serialEvent(); //call the function
    // print the string when a newline arrives:
    if (stringComplete) {

        if (inputString == "odometer"  ){
            stringComplete = false;
            while(stringComplete == false){
              serialEvent();
              delay(200);
              //Serial.println(inputString);
            }
            //Serial.println("after while loop");
            //Serial.println(inputString); //delete for pi
            //Serial.println("im the best!!!"); //delete for pi
            //Serial.println("im the best!!!");
            //Serial.println("im the best!!!");
            //Serial.println("\n\n\n\n\n\n"); //delete for pi

            odometer = inputString.toInt();
            //lcd.setCursor(3,1);
            //lcd.print("odo:");
            //lcd.print(odometer);
            //Serial.println(odometer); //delete for pi
            Serial.println("odoupdated");
            Serial.println(odometer);
            boot_override = 0;
            //stringComplete = false;
            //inputString = "done";

        
        }
        else if (inputString == "shutdown"  && pi_on == 0 && boot_override == 0){
            stringComplete = false;
            delay(200);
            if(pi_on == 1)
              Serial.println("stopsd");
            else
              Serial.println("confirm");
              boot_override = 1;
              suicide_arduino();
        }
        else{
      
      speed_left_serial = String(avgleftspeed);
      speed_right_serial = String(avgrightspeed);
      //Serial.println(inputString);
      Serial.println("datastart");
      Serial.println(speed_left_serial);
      Serial.println(speed_right_serial);
      Serial.println(avg_air_temp);
      Serial.println(enginetemperature);
      Serial.println(oil_light);
      Serial.println(alternator_light);
      Serial.println(high_beam_light);
      Serial.println(left_turn_light);
      Serial.println(right_turn_light);
      Serial.println(odometer);
      Serial.println(pi_on);
       Serial.println(avg_fuellevel_temp);
       Serial.println(avg_oiltemperature_temp);
       Serial.println(avg_tachometer);
      Serial.println("dataend");
        }
    // clear the string:
    inputString = "";
    stringComplete = false;
        
  } 
    //end write to serial
    //lcd.setCursor(0,0);
    //lcd.print("L:");
    //lcd.print(truncspeedleft);
    //lcd.print("   ");
    //lcd.print("R:");
    //lcd.print(truncspeedright);
    //lcd.print("   ");

    //lcd.setCursor(3,1);
    //lcd.print("air:");
    //lcd.print("   ");
    // lcd.setCursor(7,1);
    //lcd.print(avg_air_temp);
    //lcd.print(air_temp);
    //lcd.setCursor(5,1);
    //lcd.print("       ");
    //lcd.setCursor(5,1);
    //lcd.print(odometer);
    

   /* lcd.setCursor(0,1);
    lcd.print("Temp:");
    lcd.print(air_temp);
    lcd.print("     "); */
    
    //wait100ms; //try this
/*
    //adjust the platform to desired angle
    getPLAT();
    rotateMOTORS();
    
    //check for user input
    ToLCD=0;
    if(RI)
    {
      scanf("%d", &valueINDEX);
      platform[0] = possibleINPUTS[valueINDEX];
      
      scanf("%d", &valueINDEX);
      platform[1] = possibleINPUTS[valueINDEX];
    printf_tiny("Current Platform Angles:\nRed = %d\nBlue =%d\n\nEnter Desired Platform Angle:\n0 = -45\n1 = -35\n2 = -25\n3 = -15\n4 = -10\n5 = -5\n6 = 0\n7 = 5\n8 = 10\n9 = 15\n10 = 25\n11 = 35\n12 = 45\n\nRed, Blue:\n", platform[0], platform[1]); 

    }
    */
  }
}

float gettachometer(void){
  float speed;
  float engineRPM;
  float timeinterval;
  float MachineCycles_timeinterval;
  float rpmwheel;
  float timeonerotation;
  int testing = 1337; //testing
  int long timer1count = 0;
  unsigned long timestamp_start;
  unsigned long timestamp_end;
  float timeinterval2;
  
  
  overflow0count = 0;
  overflow1count = 0;

  trunctachometer = 0;
  
  
  //start setmefree timer
  //TR0 = 1;
  TCNT2 = 0;
  overflow0count = 0;
  
  while(!digitalRead(tach_pin) && overflow0count < 25); //waiting for rising edge   -- put back
  while(digitalRead(tach_pin) && overflow0count < 25);  //waiting for falling edge   --  put back
  //lcd.setCursor(0,0);
  //lcd.print(overflow0count);
  //lcd.print("");
  
  //start calculating time interval
  //TR1 = 1; //timer 1 on
  TCNT1H = 0;
  TCNT1 = 0;
  overflow1count = 0;
  timestamp_start = micros();
  
  
  //turn timer 0 off
  //TR0 = 0;
  
  //start time interval calculation and check if over-flowed
  if(overflow0count > 24){
  
  //P3_0 = keyUP; //testing
  
  //testing = overflow0count; //testing 
  
  //overflow0count = 0;
  //TH0 = 0;
  //TL0 = 0;
  TCNT2 = 0;
  
  //TR1 = 0; //timer 1 off
  
  
  speed = 0.0;
  truncspeedleft = speed;
  
  RPM = 0;
  return 0.0;
  
  }
  else{ //continue calculated speed (wheel is probably turning )
  overflow0count = 0;
  //TH0 = 0;
  //TL0 = 0;
  //TR0 = 1; //timer 0 on
  TCNT2 = 0;
  
  
  
  //while(wheelleftpin && overflow0count < 4); //waiting for falling edge
  
  while(!digitalRead(tach_pin) && overflow0count < 25); //waiting for rising edge of time interval
  while(digitalRead(tach_pin) &&  overflow0count < 25); //waiting for falling edge of time interval

  timer1count = TCNT1;
  timestamp_end = micros();
  //TR1 = 0; //timer 1 off
  //TR0 = 0; //timer 0 off

  //calcualte time interval
  MachineCycles_timeinterval = timer1count + 65535.0*overflow1count;
  //timeinterval = (1.0/16000000.0)*MachineCycles_timeinterval;
  timeinterval = (timestamp_end-timestamp_start)/1000000.0;
  
  timeonerotation = timeinterval*2.0; //x2 since 2 sparks per rotation
  rpmwheel = 60.0/(timeinterval*2.0); //original
  
  //speed = rpmwheel;
  speed = 60.0/(timeinterval*2.0); //this is actually enginee rpm
  //timeinterval2 = (timestamp_end-timestamp_start)/1000000.0;
  //lcd.setCursor(0,1);
  //lcd.print("Tach:");
  //lcd.print(timeinterval2);
  //lcd.print("    ");
  //speed = rpmwheel*wheelcircumference*(60.0); //in km/h
  //truncspeedleft = speed;
  
  //check for overflow has stopped count
  if(overflow0count > 24){
  
  
    //overflow0count = 0;
    //TH0 = 0;
    //TL0 = 0;
    TCNT2 = 0;
    
    RPM = 0;
    speed = 0.0;
    trunctachometer = speed;
    return 0.0;
  }
  
 // P3_0 = keyUP; //testing
  
  //turn off SetMeFree timer
  //TR0 = 0; //timer 0 off
  overflow0count = 0;
  //TH0 = 0;
  //TL0 = 0;
  TCNT2 = 0;
  
  
  //calcualte time interval
  /*MachineCycles_timeinterval = ((TH1*256.0 + TL1*1.0) + 65535.0*overflow1count);
  timeinterval = (1.0/3686500.0)*MachineCycles_timeinterval;
  
  timeonerotation = timeinterval*6.0;
  rpmwheel = 60.0/(timeinterval*6.0); //original
  
  RPM = rpmwheel;

  
  speed = rpmwheel*wheelcircumference*(60.0); //in km/h
  truncspeedleft = speed; */
  truncspeedleft = speed;// /1000;  //divide by 1000 hack job to make it look right (its not)
  //lcd.setCursor(0,1);
  //lcd.print("Speed:");
  //lcd.print(speed);
  trunctachometer = speed;
  return speed;
    
  }
  
}
  
float getwheelspeedright(void){
  float speed;
  float timeinterval;
  float MachineCycles_timeinterval;
  float rpmwheel;
  float timeonerotation;
  int testing = 1337; //testing
  int long timer1count = 0;
  unsigned long timestamp_start;
  unsigned long timestamp_end;
  float timeinterval2;
  
  
  overflow0count = 0;
  overflow1count = 0;
  
  
  //start setmefree timer
  //TR0 = 1;
  TCNT2 = 0;
  overflow0count = 0;
  
  while(!digitalRead(wheelrightpin) && overflow0count < 10); //waiting for rising edge   -- put back
  while(digitalRead(wheelrightpin) && overflow0count < 10);  //waiting for falling edge   --  put back
 
  
  
  //start calculating time interval
  //TR1 = 1; //timer 1 on
  TCNT1H = 0;
  TCNT1 = 0;
  overflow1count = 0;
  timestamp_start = micros();
  
  
  //turn timer 0 off
  //TR0 = 0;
  
  //start time interval calculation and check if over-flowed
  if(overflow0count > 59){
  
  overflow0count = 0;
  //TH0 = 0;
  //TL0 = 0;
  TCNT2 = 0;
  
  //TR1 = 0; //timer 1 off
  
  
  speed = 0.0;
  truncspeedright = speed;
  
  RPM = 0;
  return 0.0;
  
  }
  else{ //continue calculated speed (wheel is probably turning )
  overflow0count = 0;
  //TH0 = 0;
  //TL0 = 0;
  //TR0 = 1; //timer 0 on
  TCNT2 = 0;

  
  while(!digitalRead(wheelrightpin) && overflow0count < 60); //waiting for rising edge of time interval
  while(digitalRead(wheelrightpin) &&  overflow0count < 60); //waiting for falling edge of time interval

  timer1count = TCNT1;
  timestamp_end = micros();
  //TR1 = 0; //timer 1 off
  //TR0 = 0; //timer 0 off

  //calcualte time interval
  MachineCycles_timeinterval = timer1count + 65535.0*overflow1count;
  //timeinterval = (1.0/16000000.0)*MachineCycles_timeinterval;
  timeinterval = (timestamp_end-timestamp_start)/1000000.0;
  
  timeonerotation = timeinterval*6.0;
  rpmwheel = 60.0/(timeinterval*6.0); //original
  
  RPM = rpmwheel;
  
  timeinterval2 = (timestamp_end-timestamp_start)/1000000.0;
  //lcd.setCursor(0,1);
  //lcd.print(timeinterval2);
  //lcd.print("     ");
  speed = rpmwheel*wheelcircumference*(60.0); //in km/h
  truncspeedright = speed;
  
  //check for overflow has stopped count
  if(overflow0count > 59){
  
  
    overflow0count = 0;
    //TH0 = 0;
    //TL0 = 0;
    TCNT2 = 0;
    
    RPM = 0;
    speed = 0.0;
    truncspeedright = speed;
    return 0.0;
  }
  
 // P3_0 = keyUP; //testing
  
  //turn off SetMeFree timer
  //TR0 = 0; //timer 0 off
  overflow0count = 0;
  //TH0 = 0;
  //TL0 = 0;
  TCNT2 = 0;

  truncspeedright = speed;// /1000;  //divide by 1000 hack job to make it look right (its not)

  return speed;
    
  }
  
}

ISR(TIMER1_OVF_vect) //interrupt overflow timer 0
{
  

  overflow1count = overflow0count + 1;
  //TF0 = 0; //may not need to reset the overflow bit
  //TOIE1 = 0;
  

}

ISR(TIMER2_OVF_vect) //interrupt overflow timer 1 (speed)
{
  
  overflow0count ++;
  //TF1 = 0; //may not need to reset the overflow bit
  //TOIE2 = 0;
  

}





//---------------------------------START CAPACITOR FUNCTIONS-----------------------------





void settimers(void)
{
  // initialize Timer1
  noInterrupts(); // disable all interrupts
  TCCR1A = 0;
  TCCR1B = B00000101;;
  
  //TCNT1 = 34286; // preload timer 65536-16MHz/256/2Hz
  //TCCR1B |= (1 &lt;&lt; CS12); // 256 prescaler
  TIMSK1 |= (1 << TOIE1);   // enable timer overflow interrupt
  TCNT1 = 0;   // preload timer
 
  interrupts(); // enable all interrupts

    // initialize Timer2
  noInterrupts(); // disable all interrupts
  TCCR2A = 0;
  TCCR2B = B0000101;;
  
  //TCNT1 = 34286; // preload timer 65536-16MHz/256/2Hz
  //TCCR1B |= (1 &lt;&lt; CS12); // 256 prescaler
  TIMSK2 |= (1 << TOIE2);   // enable timer overflow interrupt
  interrupts(); // enable all interrupts

  //Init Arduino Interupts
  sei();

  return;
}

void serialEvent() {
        char inChar;
        stringComplete == false;
        if(Serial.available())
          inputString = "";
        while (Serial.available() && stringComplete == false) {   //while (Serial.available() && stringComplete == false) {
          // get the new byte:
          inChar = (char)Serial.read();
          // add it to the inputString:
          //inputString += inChar;
          // if the incoming character is a newline, set a flag
          // so the main loop can do something about it:
          if (inChar == '\n') {
            stringComplete = true;
          }
          else
          inputString += inChar;
        }
       
}


void ISRleftwheel(void){
  timestamp_start_left = timestamp_end_left;
  timestamp_end_left = micros();
  
}

void ISRrightwheel(void){
  timestamp_start_right = timestamp_end_right;
  timestamp_end_right = micros();
  odometer = odometer + 1;
}

void suicide_arduino(void){
  //wait 12 seconds for pi to shutdown (takes 8seconds but give it some extra
    //lcd.setCursor(3,1);
    //lcd.print("Wait2Die");

  delay(1000);
  Serial.println("confirm"); //send confirm again just incase the pi missed it
  delay(1000);
  Serial.println("confirm"); //send confirm again just incase the pi missed it
  delay(1000);
  Serial.println("confirm"); //send confirm again just incase the pi missed it
  delay(1000);
  Serial.println("confirm"); //send confirm again just incase the pi missed it
  delay(16000);
  digitalWrite(10, 1);  //remember 0 is on and 1 is off for relay
  //check to make sure key is still off
  delay(1000);
  if (digitalRead(key_onoff_pin) == 1)
    //restart pi, since key is turned back on
    digitalWrite(10, 0);//remember 0 is on and 1 is off for relay
    delay(5000); //wait 5 seconds for pi to start booting then go back to loop
    inputString = "nothing";
    return;
    



}

