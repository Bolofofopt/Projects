# ConAmbiente
### ***Code not available***
# Results
TO COME.

# Problem to Solve
![Local de instalação](https://github.com/Bolofofopt/Projects/assets/145719526/a1acc6f5-d666-431a-a724-99f6f9e14fb0)
In this technical locker network (4 lockers) there are a lot of variables such as temperature, humidity, pressure, intrusion, hydrogen, and whether everything is powered correctly that are not monitored, because of that the engineer is responsible for making sure everything is working cannot validate the correct functioning of the system without going in person, plus, if anything goes wrong he can't check it remotely.

This project solves that problem.


## Description
This project has the objective of controlling remotely the ambient of a technical locker network, it consists of controlling the Temperature, Humidity, Hydrogen, Pressure, UPS Status, power availability status & intrusion.

# BASIC OVERVIEW
![image](https://github.com/Bolofofopt/Projects/assets/145719526/0aaafd33-6b8b-493c-b998-7722c108914d)

In this basic Overview, we can see that the Lockers don't have cables between them, so I used **Wi-Fi** (mode AP [Access Point]) on the ESP32 so the main locker, that has access to an outside network with a Zabbix Dashboard, accesses the AP retrieves the data via a WebPage, such as 192.168.4.1/temp to retrieve the temperature, 192.168.4.1/humi to retrieve the humidity, and so on and on and sends it to the server with a Zabbix Dashboard.

The Wi-Fi SSID is hidden and the SSID and Password are saved in the NVS of the ESP32, so it's impossible to know the SSID or the Password via code.
To make that possible I used <Preferences.h> library:

The data saved using preferences is structured like this:

First, begin preferences

```cpp
  ssid = "MYSSID";
  preferences.begin("my-app", false);
  preferences.putUString("ssid", myssid);
  preferences.end();
  ESP.restart
```

To retreive:
```cpp
  preferences.begin("credentials", false);
 
  ssid = preferences.getString("ssid", ""); 
  password = preferences.getString("password", "");

```


## Material:
![image](https://github.com/Bolofofopt/Projects/assets/145719526/a83d0e6c-b4b6-439e-8125-49cf28909e42)


Switch

Ubuntu Server with **Zabbix**

PCBs

# Sending Data to Zabbix
via <ESP32ZabbixSender.h> library
It consisted of making a connection to the Zabbix host, clearing the item list adding the item I wanted to send, and checking if the item was sent correctly.

```cpp
ESP32ZabbixSender zSender;
zSender.Init(IPAddress({IPADDRESS}), {PORT}, {DEVICEnameONzabbix});
zSender.ClearItem(); // clear item list
zSender.AddItem("air.temp", sht3x.readTemperature); // add item such as air temperture
zSender.AddItem("air.hum", sht3x.readHumidity); // add item such as air humidity
if (zSender.Send() == EXIT_FAILURE){ // send packet
    // error handling
}
```

# Challenges
## Hydrogen Sensor
The principal challenges were the Hydrogen sensor, because of the way it works:
  The MQ-8 sensor (not the module) has a resistor inside that overheats (because it's powered 5v) and then it triggers another resistor that differs when there is the presence of Hydrogen.
![image](https://github.com/Bolofofopt/Projects/assets/145719526/7fed941b-467f-49df-b0c2-84ad026ec0eb)
![image](https://github.com/Bolofofopt/Projects/assets/145719526/865fafb1-5018-4fa9-aa36-45f77d1b2351)
![image](https://github.com/Bolofofopt/Projects/assets/145719526/7137e6d4-4299-47e9-a321-b86748789df3)
![image](https://github.com/Bolofofopt/Projects/assets/145719526/ddcd7bb2-1ea9-4fc0-a8a9-346f98c25801)



So to know if there a presence of Hydrogen I need to do a Voltage Divider so I know the variable resistor value, and to do the Voltage Divider I need to know the Vout of the circuit. To be more accurate I put a Capacitor of 10pF to the Vout value doesn't differ much from its true value.
Voltage Divider:

Ri = (( Vn * R2 ) / Vout ) – R2 

The circuit ends like this:


![image](https://github.com/Bolofofopt/Projects/assets/145719526/2e36d4c6-7d03-4287-9450-c6602016e6c0)

The Green cable is connected to the GPIO33 to read the Vout


## SNMP Board
The SNMP Board is used to connect to the UPS and to retrieve vital information about the status of the UPS.
The challenge was I needed to Develop everything including the SNMP Board when I did not have the UPS and when I started I didn't know anything about SNMP and SNMP Boards. Despite de challenge, I overcame it in no time and when I tested in the field everything worked like it should. The SNMP Board is only connected to the ESP32 and then via a web page, the data is shown.

An MIB is a Management Information Base used for managing the entities in a communication network. OID stands for Object Identifiers, they uniquely identify managed objects in an MIB hierarchy.

![image](https://github.com/Bolofofopt/Projects/assets/145719526/483ce9e9-0645-49ec-a0cc-6cf3ad721a1a)

To retreive the SNMP data via ESP32 I used <Arduino_SNMP_Manager.h> library.
Some of the code consisted of:

### SNMPManager
Inicializing the SNMP community string:
```cpp
SNMPManager snmpManager = SNMPManager("public");
```

### SNMPGet
Create and SNMPGet object to make SNMP GetRequest calls (SNMPv1 = 0, SNMPv2 = 1):
```cpp
SNMPGet snmpRequest = SNMPGet("public", 1);
```

### Handlers and Callbacks
```cpp
ValueCallback *callbackSysName;  // Blank Callback for each OID
void setup()
{
    IPAddress target(192, 168, 200, 187);
    callbackSysName = snmpManager.addStringHandler(target, ".1.3.6.1.2.1.1.5.0", &sysNameResponse);  // Callback for SysName for target host
}
```

Within the main program snmpManager.loop() needs to be called frequently to capture and parse incoming GetResponses. GetRequests can be sent as needed, though typically a significantly lower rate than the main loop.
```cpp
void loop()
{
    snmpManager.loop();  // Call frequently
    getSNMP();
}
void getSNMP()
{
  // Check to see if it is time to send an SNMP request.
  if ((timeLast + pollInterval) <= millis())
  {
    // Send SNMP Get request
    snmpRequest.addOIDPointer(callbackSysName);
    snmpRequest.setIP(WiFi.localIP()); //IP of the arduino
    snmpRequest.setUDP(&udp);
    snmpRequest.setRequestID(rand() % 5555);
    snmpRequest.sendTo(router);
    snmpRequest.clearOIDList();
    // Display response (first call might be empty)
    Serial.print("sysNameResponse: ");
    Serial.println(sysNameResponse);
    Serial.println("----------------------")
    timeLast = millis();
  }
}
```
Check https://github.com/shortbloke/Arduino_SNMP_Manager for the library.
