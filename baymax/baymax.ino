/*
Designed by The Psychedelic Psychiatrist
Robo-Tech 2023 @ GT
*/

#define bitRead(value, bit) (((value) >> (bit)) & 0b01)
#define opCode(value) (((value) >> (6)))

int[] servoPins   = {0, 1, 2, 3, 4, 5}
int[] fAidPins    = {0, 0, 0, 0, 0, 0}

uint8_t command   = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  if(Serial.available() > 0) {
    command = Serial.read();
    switch (opCode(command)))
    {
    case 1:
      /* Medicine */
      for (int i = 0; i < 6; i++) {
        analogWrite(servoPins[i], bitRead(command, i) * 255);
      }
      break;
    case 2:
      /* First Aid */
      for (int i = 0; i < 6; i++) {
        analogWrite(fAidPins[i], bitRead(command, i) * 255);
      }
      break;
    case 3:
      /* Workout */
      break;
    default:
      /* Default State */
      for (int i = 0; i < 7; i++) {
        analogWrite(servoPins[i], 0);
      }
      break;
    }
  }
}