#define trigPin2 5
#define echoPin2 6
#define trigPin1 11
#define echoPin1 12
#define led 13
int flag=0;

void setup() {
  Serial.begin (9600);
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  pinMode(led, OUTPUT);
}

void loop() {
  long duration1, duration2, distance1, distance2;
 // digitalWrite(trigPin, LOW);  // Added this line
 // delayMicroseconds(2); // Added this line
  digitalWrite(trigPin1, HIGH);
//  delayMicroseconds(1000); - Removed this line
  delayMicroseconds(10); // Added this line
  digitalWrite(trigPin1, LOW);
  duration1 = pulseIn(echoPin1, HIGH);
  
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);
  duration2 = pulseIn(echoPin2, HIGH);
  
  distance1 = (duration1/2) / 29.1;
  distance2 = (duration2/2) / 29.1;

  Serial.print(distance1);
  Serial.print(" ");
  Serial.print(distance2);
  Serial.print(" ");
  Serial.print(flag);
  Serial.print("\n");
  delay(10);
  if ( (distance1 <= 20) && (distance2 > 20) )  {
    flag = 1;  
    digitalWrite(led,LOW);
  }
  else if ( (distance1 <= 20) && (distance2 <= 20) && (flag==1) ) {  // This is where the LED On/Off happens
    digitalWrite(led,HIGH); // When the Red condition is met, the Green LED should turn off
  }
  else {
    flag = 0;
    digitalWrite(led,LOW);
  }
}
