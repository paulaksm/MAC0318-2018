import lejos.nxt.LightSensor;
import lejos.nxt.Sound;
import lejos.util.Delay;
import lejos.nxt.LCD; 
import lejos.nxt.SensorPort;
import lejos.nxt.Button;

public class Light {
  public static void main(String[] args) {
    LCD.drawString("Sensor Optico", 0, 0); 
    LightSensor light = new LightSensor(SensorPort.S3);
    while (!Button.ENTER.isDown())  {
      int value = light.readValue();
      System.out.println(value);
      if (value > 10 && value < 40)
        Sound.playTone(200,500);
      else if (value > 50 && value < 80)
        Sound.playTone(500,500);
      Delay.msDelay(1000);
    }
  }
}
