#include <Adafruit_LiquidCrystal.h>
#include <Servo.h>
#include <Keypad.h>

//declara váriaveis globais
int j, cofre;
int Tilt = 13;
int Estado;
int pos = 0;
//configura o servo /*fechadura*/
Servo servo_9;

//Configura o sensor de distancia ultrasónico
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

/*os leds são os primeiros 4 digitos
do lcd para verificar o código*/




void setup()
{
  int i;
  pinMode( 2, OUTPUT );/*configura porta do buzzer*/
  pinMode(Tilt, INPUT);/*configura a porta do tilt*/
  j = 0;/*j é a váriavel usada para confirmar os numeros*/
  
  lcd_1.begin(16, 2);/*configura os espaços do lcd*/
  
  Serial.begin(9600);/*configura serial*/
  
  lcd_1.setCursor(0, 0);/*mete o cursor do lcd a 0*/
  
  lcd_1.setBacklight(1);/*liga o lcd*/
  
  lcd_1.print("initializing");/*testa o lcd*/
  
  lcd_1.setCursor(0, 1);/*troca de linha*/
  
  lcd_1.print("setup...");/*testa o lcd*/
  
  for( i = 0; i<4; i++ )
  	leds[i] = 0;/*configura as 4 primeiros digitos do lcd*/
  
  lcd_1.clear(); /*limpa o lcd*/
  
  codigo();
  
  
  //servo_9.attach(11, 500, 2500);/*configura o servo*/
  servo_9.attach(9, 500, 2500);
  
  for (pos = 0; pos <= 90; pos += 1) 
  {
    servo_9.write(pos);
  }/*testa o servo*/
}



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
