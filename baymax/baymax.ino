#include <Servo.h>

/*
Designed by The Psychedelic Psychiatrist
Robo-Tech 2023 @ GT
*/

#define bitRead(value, bit) (((value) >> (bit)) & 0b01)
#define opCode(value) (((value) >> (6)))

#define DRAWER_DELAY 1000

Servo servos[] = {Servo(), Servo(), Servo(), Servo(), Servo(), Servo()};

int servoPins[] = {3, 5, 6, 9, 10, 11};
int servoControl[] = {0, 0, 0, 0, 0, 0};

uint8_t command = 0;

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);

  for (int i = 0; i < 6; i++)
  {
    servos[i].attach(servoPins[i]);
    servos[i].write(0);
  }
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  if (Serial.available() > 0)
  {
    command = Serial.read();

    switch (opCode(command))
    {
    case 1:
      /* Medicine */
      for (int i = 0; i < 6; i++)
      {
        if (bitRead(command, i) && !servoControl[i])
        {
          servoControl[i] = 1;
          servos[i].write(90);
          delay(10);
        }
        else if (!bitRead(command, i) && servoControl[i])
        {
          servoControl[i] = 0;
          servos[i].write(0);
          delay(10);
        }
      }
      break;
    case 2:
      /* First Aid */
      break;
    case 3:
      /* Workout */
      break;
    case 0:
      /* Reset State */
      if (command != 0)
        break;

      for (int i = 0; i < 6; i++)
      {
        if (servoControl[i])
        {
          servoControl[i] = 0;
          servos[i].write(0);
        }
        delay(10);
      }
      break;
    default:
      break;
    }
  }
  delay(10);
}