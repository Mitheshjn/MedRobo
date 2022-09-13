// Motor A connections
int enA = 10;
int in1 = 8;
int in2 = 9;
// Motor B connections
int enB = 11;
int in3 = 12;
int in4 = 13;
//add pin num for med disp motors
int m11 = 4;//CHANGE PIN NUM
int m12 = 5;
int m21 = 6;
int m22 = 7;
int m31 = A0;
int m32 = A1;
int m41 = A2;
int m42 = A3;
char t;
void setup() {
pinMode(enA, OUTPUT);
pinMode(enB, OUTPUT);
pinMode(in1, OUTPUT);
pinMode(in2, OUTPUT);
pinMode(in3, OUTPUT);
pinMode(in4, OUTPUT);

pinMode(m11, OUTPUT);
pinMode(m12, OUTPUT);
pinMode(m21, OUTPUT);
pinMode(m22, OUTPUT);
pinMode(m31, OUTPUT);
pinMode(m32, OUTPUT);
pinMode(m41, OUTPUT);
pinMode(m42, OUTPUT);

digitalWrite(in1, LOW);
digitalWrite(in2, LOW);
digitalWrite(in3, LOW);
digitalWrite(in4, LOW);

digitalWrite(m11, LOW);
digitalWrite(m12, LOW);
digitalWrite(m21, LOW);
digitalWrite(m22, LOW);
digitalWrite(m31, LOW);
digitalWrite(m32, LOW);
digitalWrite(m41, LOW);
digitalWrite(m42, LOW);

Serial.begin(9600);
}
void loop() {
  
if(Serial.available()){
  t = Serial.read();
  Serial.println(t);
}
if(t == 'F'){            //move forward(all motors rotate in forward direction)
  digitalWrite(in1,HIGH);
  digitalWrite(in2,LOW);
  digitalWrite(in3,LOW);
  digitalWrite(in4,HIGH);
  analogWrite(enA,240);
  analogWrite(enB,200);
}
else if(t == 'B'){      //move reverse (all motors rotate in reverse direction)
  digitalWrite(in1,LOW);
  digitalWrite(in2,HIGH);
  digitalWrite(in3,HIGH);
  digitalWrite(in4,LOW);
  analogWrite(enA,240);
  analogWrite(enB,240);
}
else if(t == 'L'){      //turn right 
  digitalWrite(in1,LOW);
  digitalWrite(in2,HIGH);
  digitalWrite(in3,LOW);
  digitalWrite(in4,HIGH);
  analogWrite(enA,250);
  analogWrite(enB,250);
}
else if(t == 'R'){      //turn left
  digitalWrite(in1,HIGH);
  digitalWrite(in2,LOW);
  digitalWrite(in3,HIGH);
  digitalWrite(in4,LOW);
  analogWrite(enA,250);
  analogWrite(enB,250);
}
else if(t == 'S'){      //STOP (all rover motors stop)
  digitalWrite(in1,LOW);
  digitalWrite(in2,LOW);
  digitalWrite(in3,LOW);
  digitalWrite(in4,LOW);
}
else if(t == 'M'){      //medicine 1
  digitalWrite(m11,LOW);
  digitalWrite(m12,LOW);
  digitalWrite(m21,LOW);
  digitalWrite(m22,HIGH);
  digitalWrite(m31,LOW);
  digitalWrite(m32,LOW);
  digitalWrite(m41,LOW);
  digitalWrite(m42,LOW);
}
else if(t == 'N'){      //medicine 2
  digitalWrite(m11,LOW);  
  digitalWrite(m12,HIGH);
  digitalWrite(m21,LOW);
  digitalWrite(m22,LOW);
  digitalWrite(m31,LOW);
  digitalWrite(m32,LOW);
  digitalWrite(m41,LOW);
  digitalWrite(m42,LOW);

}
else if(t == 'O'){      //medicine 3
  digitalWrite(m11,LOW);
  digitalWrite(m12,LOW);
  digitalWrite(m21,LOW);
  digitalWrite(m22,LOW);
  digitalWrite(m31,LOW);
  digitalWrite(m32,HIGH);
  digitalWrite(m41,LOW);
  digitalWrite(m42,LOW);
}
else if(t == 'P'){      //medicine 3
  digitalWrite(m11,LOW);
  digitalWrite(m12,LOW);
  digitalWrite(m21,LOW);
  digitalWrite(m22,LOW);
  digitalWrite(m31,LOW);
  digitalWrite(m32,LOW);
  digitalWrite(m41,HIGH);
  digitalWrite(m42,LOW);
}
else if(t == 'Q'){      //stop medicine motors
  digitalWrite(m11,LOW);
  digitalWrite(m12,LOW);
  digitalWrite(m21,LOW);
  digitalWrite(m22,LOW);
  digitalWrite(m31,LOW);
  digitalWrite(m32,LOW);
  digitalWrite(m41,LOW);
  digitalWrite(m42,LOW);
}
delay(100);
}
