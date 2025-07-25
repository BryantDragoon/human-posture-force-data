
/* Codigo para lectura de multiples sensores usando multiplexores, a traves de una conexion Bluetooth */

//Bibliotecas
#include "BluetoothSerial.h"
#include <string.h>

//Configuracion conexion
BluetoothSerial SerialBT;
const char Nombredisp[] = "SistemaFSR"; //Nombre dispositivo
char dataRX[10]; 

//Entradas
const byte Mux1SIG = 13; //Pin de lectura en multiplexor 1
const byte Mux1S0 = 27; //S0 - Pines de conmutacion estados MUX 1
const byte Mux1S1 = 26; //S1
const byte Mux1S2 = 25; //S2
const byte Mux1S3 = 33; //S3
const byte Mux2SIG = 4; //Pin de lectura en multiplexor 2
const byte Mux2S0 = 16; //S0 - Pines de conmutacion estados MUX 2
const byte Mux2S1 = 17; //S1
const byte Mux2S2 = 18; //S2
const byte Mux2S3 = 19; //S3

//Variables
char Data[5]; //Lectura en un solo sensor
boolean estado = false; //Estado inicial para lecturas de sensores
const int NumSensores = 16; //Numero de sensores en una sola plantilla
char DataTX[3+8*NumSensores+2*NumSensores-1]; //Arreglo con lectura de todos los sensores


void setup() { //Configuracion en placa
  pinMode(Mux1SIG, INPUT);
  pinMode(Mux1S0, OUTPUT);
  pinMode(Mux1S1, OUTPUT);
  pinMode(Mux1S2, OUTPUT);
  pinMode(Mux1S3, OUTPUT);
  pinMode(Mux2SIG, INPUT);
  pinMode(Mux2S0, OUTPUT);
  pinMode(Mux2S1, OUTPUT);
  pinMode(Mux2S2, OUTPUT);
  pinMode(Mux2S3, OUTPUT);
  pinMode(2, OUTPUT); //Pin con led
  SerialBT.begin(Nombredisp);
}


void loop() { //Programa principal
  serialEvent();

  if (strcmp(dataRX, "a") == 0) {
    estado = true;
    strcpy(dataRX, "\0");   
    digitalWrite(2, HIGH);  
  }
  else if (strcmp(dataRX, "s") == 0) {
    estado = false;
    strcpy(dataRX, "\0");
    digitalWrite(2, LOW); 
  }

  if (estado == true) { //Comienza ciclo
    strcpy (DataTX,"<");
    for (byte i = 0; i < NumSensores; i++){ //Lecturas de los sensores
      ConfMux1(i);
      sprintf(Data, "%d", analogRead(Mux1SIG)); //Lectura en primer multiplexor
      strcat(DataTX, Data); 
      strcat(DataTX, ","); //Siguiente lectura
      ConfMux2(i);
      sprintf(Data, "%d", analogRead(Mux2SIG)); //Lectura de segundo multiplexor  
      strcat(DataTX, Data);
      if (i+1 < NumSensores)
        strcat(DataTX, ",");     
    }
    strcat(DataTX, ">");
    SerialBT.println(DataTX);
    delay(50);  
  } 
}


void serialEvent(){ //Lee cadenas de entrada con marca de inicio y final  
  char IniMarc = '<';
  char FinMarc = '>';
  char simb;  
  char continua = 'n';
  byte caracter = 0;

  while(SerialBT.available() && continua != 't'){  
    simb = SerialBT.read();

    if (continua == 's'){
      if (simb != FinMarc && caracter < 9){
        dataRX[caracter] = simb; 
        caracter++;   
      }
      else{
        dataRX[caracter] = '\0';
        continua = 't';   
      }
    }
    else if (simb == IniMarc){
      continua = 's';
    }      
  }
}

void ConfMux1(byte canal){ //Conmuta canal en MUX 1
  digitalWrite(Mux1S0, bitRead(canal, 0));
  digitalWrite(Mux1S1, bitRead(canal, 1));
  digitalWrite(Mux1S2, bitRead(canal, 2));
  digitalWrite(Mux1S3, bitRead(canal, 3));
}

void ConfMux2(byte canal){ //Conmuta canal en MUX 2
  digitalWrite(Mux2S0, bitRead(canal, 0));
  digitalWrite(Mux2S1, bitRead(canal, 1));
  digitalWrite(Mux2S2, bitRead(canal, 2));
  digitalWrite(Mux2S3, bitRead(canal, 3));
}
