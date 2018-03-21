import lejos.robotics.navigation.DifferentialPilot;
import lejos.nxt.UltrasonicSensor;
import lejos.nxt.TouchSensor;
import lejos.nxt.SensorPort;
import lejos.nxt.Button;
import lejos.nxt.Motor;

public class Ultrasonic {
  public static void main(String[] args) {
    UltrasonicSensor sonic = new UltrasonicSensor(SensorPort.S4);
    TouchSensor touch = new TouchSensor(SensorPort.S1);
    DifferentialPilot pilot = new DifferentialPilot(5.6f, 11.2f, Motor.B, Motor.C, false); //in cm
    while (!touch.isPressed()) {
      if (sonic.getDistance() > 30) {
        pilot.forward();
      } else {
        pilot.stop();
      }
    }
  }
}
