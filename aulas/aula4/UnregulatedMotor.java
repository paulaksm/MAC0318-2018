import lejos.nxt.Button;
import lejos.nxt.LightSensor;
import lejos.nxt.MotorPort;
import lejos.nxt.NXTMotor;
import lejos.nxt.SensorPort;

public class UnregulatedMotor {

  static LightSensor light;
  static NXTMotor mA;
  static NXTMotor mC;

  public static void main(String args[]) 
  {
    light = new LightSensor(SensorPort.S4);
    mA = new NXTMotor(MotorPort.A);
    mC = new NXTMotor(MotorPort.C);
    Button.waitForAnyPress();

    while (light.getLightValue() < 50){
      mA.setPower(50);
      mC.setPower(50);
      //mA.setPower(-50);
      //mC.setPower(-50);
    }
    mA.stop();
    mC.stop();
  } 
}