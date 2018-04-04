import lejos.nxt.Button;
import lejos.nxt.LightSensor;
import lejos.nxt.LCD;
import lejos.nxt.SensorPort;
import lejos.util.Delay;
 
public class CheckLine{
        public static void main(String [] args){
          LightSensor light = new LightSensor(SensorPort.S4);
          LCD.drawString("Teste sensor optico", 0, 0);
          Button.waitForAnyPress();
          LCD.clear();
          LCD.drawString("Preto", 0, 0); 
          LCD.drawInt(light.getLightValue(),  0, 4); 
          Button.waitForAnyPress();
          LCD.clear();
          LCD.drawString("Branco", 0, 0); 
          LCD.drawInt(light.getLightValue(), 0, 4); 
          Button.waitForAnyPress();
          LCD.clear();
        }
}

