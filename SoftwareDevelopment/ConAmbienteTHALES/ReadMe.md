# ConAmbiente
### ***Code not available due to security reasons***
# Results
TO COME.


## Description
This Software Development project has the objective of controling remotetly the ambient of a technical locker network, it consists of controling the Temperature, Humidity, Hydrogen, Pressure, UPS Status and power availability status.
# BASIC OVERVIEW
![image](https://github.com/Bolofofopt/Projects/assets/145719526/0aaafd33-6b8b-493c-b998-7722c108914d)

In this basic Overview we can see that the Lockers don't have cables between them, so I used **Wi-Fi** (mode AP [Access Point]) on the ESP32 so the main locker that has access to an outside network with a Zabbix Dashboard accesses the AP. retreives the data via an Link, such as 192.168.4.1/temp to retreive the temperature, 192.168.4.1/humi to retreive the humidity, and so on an on.


## Material:
![image](https://github.com/Bolofofopt/Projects/assets/145719526/a83d0e6c-b4b6-439e-8125-49cf28909e42)


Switch

Ubuntu Server with **Zabbix Dashboard**

PCBs
# Challenges
## Hydrogen Sensor
The principal challenges were the Hydrogen sensor, because of the way it works:
  The MQ-8 sensor (not the module) has a resistor inside that overheats (because it's powered 5v) and then it triggers another resistor that differs when there is presence of Hydrogen.
![image](https://github.com/Bolofofopt/Projects/assets/145719526/7fed941b-467f-49df-b0c2-84ad026ec0eb)
![image](https://github.com/Bolofofopt/Projects/assets/145719526/865fafb1-5018-4fa9-aa36-45f77d1b2351)
![image](https://github.com/Bolofofopt/Projects/assets/145719526/7137e6d4-4299-47e9-a321-b86748789df3)
![image](https://github.com/Bolofofopt/Projects/assets/145719526/ddcd7bb2-1ea9-4fc0-a8a9-346f98c25801)



So to know if there is presence of Hydrogen I need to do a Voltage Divider so I know the variable resistor value, and to do the Voltage Divider I need to know the Vout of the circuit. To be more accurate I put a Capacitor of 10pF to the Vout value doesn't differ much from it's true value.
The circuit ends like this:


![image](https://github.com/Bolofofopt/Projects/assets/145719526/2e36d4c6-7d03-4287-9450-c6602016e6c0)
The Green cable is connected to the GPIO33 to read the Vout


## SNMP Board
The SNMP Board it's used to connect to the UPS and to retreive vital information about the status of the UPS.
The challenge was I needed to Develop everything included the SNMP Board when I dind't have the UPS and when I started I didn't know anything about SNMP and SNMP Boards. Put despite de challenge I overcome it in no time and when I tested in the field everything worked like it should.
