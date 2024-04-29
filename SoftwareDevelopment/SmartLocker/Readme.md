<p align="center"><img width="40%" src="img/Arduino_Logo.png" /></p>

--------------------------------------------------------------------------------

This repository shows my project Smart Locker.

<br/>
# SmartLocker
### Skills improved:
      - Software Development 
      - Arduino IDE 
      - Programming language C

## Description:
The idea of this project consists in developing um device in the security and storage regime, it has several sensors and capable of communication with a database live data, for example if a sensor detects an unusual  behaviour, the Arduino communicaties with the Database and it transmits the data to a WebApp where the admins and users can check the status of their locker or door. The idea envolved to a locker network where an user consults a WebApp and chooses a locker that he pretends to use, the admins see every locker data on a Zabbix Dashboard and their logs and the users see the data of their locker on a WebApp.

# Code
First I imported the libraries and started global variables
```cpp
#include <Adafruit_LiquidCrystal.h>
#include <Servo.h>
#include <Keypad.h>

//declara váriaveis globais
int j, cofre;
int Tilt = 13;
int Estado;
int pos = 0;
//configura o servo
Servo servo_9;
```
Then I configured the ultrasonic distance sensor
```cpp
long readUltrasonicDistance(int triggerPin, int echoPin)
{
  pinMode(triggerPin, OUTPUT);  // Limpa o trigger
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  // Define o trigger para HIGH durante 10 microsegundos
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  pinMode(echoPin, INPUT);
  // Lê o echo pin, e retorna o tempo de viagem da onda de som em microsegundos
  return pulseIn(echoPin, HIGH);
}
```
Configuration of the 4x4 keyboard & LCD & passkey
```cpp
const byte qtdLinhas = 4; //configura o teclado 4x4
const byte qtdColunas = 4; 

char matriz_teclas[qtdLinhas][qtdColunas] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

byte PinosqtdLinhas[qtdLinhas] = {3, 4, 5, 6}; 
byte PinosqtdColunas[qtdColunas] = {8, 7, 10,11};
Keypad meuteclado = Keypad( makeKeymap(matriz_teclas), PinosqtdLinhas, PinosqtdColunas, qtdLinhas, qtdColunas); 
//configura o lcd
Adafruit_LiquidCrystal lcd_1(0);
//configura os *leds* 
char leds[4];

/*The leds are the first 4 digits of the passkey to check if they are valid*/
```
After the global configuration comes the setup() function:
```cpp
void setup()
{
  int i;
  pinMode( 2, OUTPUT );/*configures the buzzer*/
  pinMode(Tilt, INPUT);/*configures the tilt*/
  j = 0;/*j its the variable that i used to check the passkey*/
  
  lcd_1.begin(16, 2);/*configure the lcd spaces*/
  
  Serial.begin(9600);/*configura serial*/
  
  lcd_1.setCursor(0, 0);/*set cursor at 0*/
  
  lcd_1.setBacklight(1);/*turns on lcd*/
  
  lcd_1.print("initializing");/*tests lcd*/
  
  lcd_1.setCursor(0, 1);/*changes lines*/
  
  lcd_1.print("setup...");/*tests lcd*/
  
  for( i = 0; i<4; i++ )
  	leds[i] = 0;/*cconfigures the first 4 digits of the keyboard pressed keys*/
  
  lcd_1.clear(); /*cleans the lcd*/
  
  codigo();
  
  //servo_9.attach(11, 500, 2500);/*configure the servo*/
  servo_9.attach(9, 500, 2500);
  
  for (pos = 0; pos <= 90; pos += 1) 
  {
    servo_9.write(pos);
  }/*tests the servo*/
}
```
The code that resets the lcd and servo (closes the door)
```cpp
void reset() /*faz o reset do lcd e do servo*/
{
  int i;
  
  for( i = 0; i<4; i++ )
  	leds[i] = 0;
  
  j = 0;
  for (pos = 0; pos <= 90; pos += 1) 
    servo_9.write(pos);/*possivel problema de fechadura aqui*/
  
  codigo();
}
void codigo()
{
  
  lcd_1.clear(); //limpar o LCD
  
  loop();
  
}
```


Last but not least, the loop:
```cpp
void loop()
{
  int i;
  
  if(Estado == HIGH)/*possivel sensor a detetar erro*/
  {
  	lcd_1.setCursor(0, 0);
    lcd_1.print("Alerta");
  }
  if(digitalRead(Tilt) == HIGH)
  {
    tone( 2, 100, 200);
    lcd_1.print("ALERTA!");
  }
  
  /*verifica se alguma tecla foi pressionada*/
  char tecla_pressionada = meuteclado.getKey();
  
  /*verifica se o sensor deteta movimento para ligar o lcd*/
  if (0.01723 * readUltrasonicDistance(12, 12) <= 300) 
  {
      lcd_1.setBacklight(1); /*liga o lcd*/
  }
  
  else
  {
  	  lcd_1.setBacklight(0);/*desliga o lcd*/
    	reset();
  }
  
  
  if(tecla_pressionada && j<4) /*não deixa ultrapassar os 4 digitos*/
  {
    for( i = 0; i < 1; i++)
    {
          lcd_1.setCursor(j, 0);
      
          lcd_1.print("*"); /*esconde o código*/
      
      	  leds[j] = tecla_pressionada;
      
      	  j++;
    }
  }

  if(tecla_pressionada == '*') /*tecla do reset*/
  {
    reset();
  }
    
  if(tecla_pressionada == '#') /*tecla de verificação*/
  {
    if(leds[0] == '2' && leds[1] == '0' && leds[2] == '0' && leds[3] == '6')
    {
      lcd_1.setCursor(0, 0);
      
      lcd_1.print("Acertou!");
      
      tone( 2, 500, 200);
      for (pos = 0; pos <= 90; pos -= 1) /*abre a fechadura*/
      {
    	servo_9.write(pos);
  	  }
    }
    else
    {
      lcd_1.setCursor(0, 0); /*mete o cursor do lcd na posição 0*/
      
      lcd_1.print("Errou!"); /*lcd print errou*/
      
      tone( 2, 100, 200); /*o buzzer faz barulho*/
      
      
    }
  } 
}
```
# SmartLocker
![SmartlockerTinkercad](https://github.com/Bolofofopt/ProjetosC/assets/145719526/4159fff1-49a4-47f7-a156-37ceeada84da)



# Material:
|Teclado|4x4 |
|:-----|:---------------|
|LCD|16x2 |
|Servo|Motor |
|Sensor|Tilt |
|Sensor|Proximity |
|Alarm|Buzzer |

## TODO
This is a work in progress, it still misses the remote control of the lockers and the web system described in the 'Description'.
The upgrades include:
-        Changing the Arduino to a ESP32
-        Communication between the ESP32 and a server
-        Research of which software to use to receive the data an put it on a Web Page
-        Configuration of the SO and putting a local secure WebServer or a local secure Zabbix dashboard
