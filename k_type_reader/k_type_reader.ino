#include <Wire.h>
#include <Adafruit_ADS1015.h>

#define AREF 4.096           // set to AREF, typically board voltage like 3.3 or 5.0
#define ADC_RESOLUTION 16  // set to ADC bit resolution, 10 is default
 
Adafruit_ADS1115 ads1115;

float reading1, reading2, reading3, reading4, voltage1, voltage2, voltage3, voltage4, temperature1, temperature2, temperature3, temperature4;

float get_voltage(int raw_adc) {
  return raw_adc * 0.125/1000; 
  //return raw_adc * (AREF / (pow(2, ADC_RESOLUTION)-1));  
}

float get_temperature(float voltage) {
  return (voltage - 1.25) / 0.005;
}

void setup(void)
{
  Serial.begin(9600);
  Serial.println("Hello!");
  
  Serial.println("Getting single-ended readings from AIN0..3");
  ads1115.setGain(GAIN_ONE);     // 1x gain   +/- 4.096V  1 bit = 0.125mV
  //Serial.println("ADC Range: +/- 6.144V (1 bit = 3mV)");
  ads1115.begin();
}
 
void loop(void)
{
  //int16_t adc0, adc1, adc2, adc3;
 
  reading1 = ads1115.readADC_SingleEnded(0);
  reading2 = ads1115.readADC_SingleEnded(1);
  reading3 = ads1115.readADC_SingleEnded(2);
  reading4 = ads1115.readADC_SingleEnded(3);

  voltage1 = get_voltage(reading1);
  voltage2 = get_voltage(reading2);
  voltage3 = get_voltage(reading3);
  voltage4 = get_voltage(reading4);

  temperature1 = get_temperature(voltage1);
  temperature2 = get_temperature(voltage2);
  temperature3 = get_temperature(voltage3);
  temperature4 = get_temperature(voltage4);
  
  //Serial.print("ktype1: "); Serial.println(temperature1);
  //Serial.print("ktype2: "); Serial.println(temperature2);
  //Serial.print("ktype3: "); Serial.println(temperature3);
  //Serial.print("ktype4: "); Serial.println(temperature4);
  Serial.print((String)temperature1 + "," + (String)temperature2 + "," + (String)temperature3 + "," + (String)temperature4 + ",");
  Serial.println(" ");
  
  delay(1000);
}
