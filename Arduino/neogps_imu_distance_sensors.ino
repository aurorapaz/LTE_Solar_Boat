#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <I2Cdev.h>
#include <MPU6050.h>
#include <Seeed_vl53l0x.h>
#include <Servo.h>
#include <math.h>

//MOTOR
float received_speed;

//RECEIVED_MESSAGES
String received_message;
bool all_messages_received; 

//GPS
SoftwareSerial gpsPort(5,6);
TinyGPSPlus gps;
float gps_speed = 0;
float gps_lat = 0;
float gps_lon = 0;
 
//IMU 9DOF
MPU6050 accelgyro;
I2Cdev   I2C_M;
float Axyz[3];
float pitch = 0;
float roll = 0;
 
//Time of flight Distance sensor
Seeed_vl53l0x VL53L0X;
VL53L0X_RangingMeasurementData_t RangingMeasurementData;
bool tof_error = false;
float heigth = 0;
 
void setup()
{
  Serial.begin(9600);
  while(!Serial);
   
  //Time of flight Distance sensor
  setupVL53L0X();
   
  //IMU 9DOF
  Wire.begin();
  accelgyro.initialize();
   
  //GPS
  gpsPort.begin(9600);
  //SERVO
   
   
}
 
void loop(){
  getGPSData();
  getIMUData();
  getDistanceData();

  print_sensors_data();
  
  delay(100);
  
}
 
void print_sensors_data(){
  
    //GPS
    Serial.flush();
    Serial.print("S ");
    Serial.print(gps_speed*1000.0/3600.0);
    Serial.print(" Lat ");
    Serial.print(gps_lat);
    Serial.print(" Long ");
    Serial.println(gps_lon);
    Serial.flush();
    //IMU
    Serial.print("P ");
    Serial.print(pitch);
    Serial.print(" R ");
    Serial.println(roll);
    Serial.flush();
    //TOF Distance
    Serial.print("H ");
    Serial.println(heigth);
        
}
 
 
void setupVL53L0X(){
  VL53L0X_Error Status = VL53L0X_ERROR_NONE;
  Status = VL53L0X.VL53L0X_common_init();
  if (VL53L0X_ERROR_NONE != Status) tof_error = true;
  else tof_error = false;
  
  VL53L0X.VL53L0X_high_speed_ranging_init();
  if (VL53L0X_ERROR_NONE != Status)tof_error = true; 
  else tof_error = false;
}
 
void getDistanceData(){
  VL53L0X_Error Status = VL53L0X_ERROR_NONE;
 
  memset(&RangingMeasurementData, 0, sizeof(VL53L0X_RangingMeasurementData_t));
  Status = VL53L0X.PerformSingleRangingMeasurement(&RangingMeasurementData);
  if (VL53L0X_ERROR_NONE == Status && RangingMeasurementData.RangeMilliMeter < 2000) tof_error = false;
  else tof_error = true;

  if(!tof_error) heigth = RangingMeasurementData.RangeMilliMeter/10;
  else heigth = -10000000.00;
    
}
 

void getGPSData(){
    while(gpsPort.available()){  
      gps.encode(gpsPort.read());
      if(gps.location.isUpdated()){
        gps_lat = gps.location.lat();
        gps_lon = gps.location.lng();
      }
      if(gps.speed.isUpdated()) gps_speed = gps.speed.kmph();        
    }      
}
 
void getIMUData(){ 
  getAccel_Data();
  setPitchRoll();   
}
 
void setPitchRoll(void) {
    pitch = asin(-Axyz[0])*180/M_PI;
    roll = asin(Axyz[1] / cos(pitch))*180/M_PI;
    
    if(isnan(pitch))pitch = -10000000.00;
    
    if(isnan(roll))roll = -10000000.00;    

}
 
void getAccel_Data(void) {
    int16_t ax, ay, az;
    accelgyro.getAcceleration(&ax, &ay, &az);
    Axyz[0] = (double) ax / 16384;
    Axyz[1] = (double) ay / 16384;
    Axyz[2] = (double) az / 16384;
}
