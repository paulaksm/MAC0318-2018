import lejos.nxt.Motor;
import lejos.nxt.comm.RConsole;
import lejos.util.Delay;
import lejos.nxt.LCD;

public class RConsoleTest {
    public static void main(String[] args) throws Exception {
        RConsole.openAny(0); //parameter int in milliseconds that when set to 0, waits forever.
        Motor.A.rotate(1440,true);
        while (Motor.A.isMoving()){
            RConsole.println(""+Motor.A.getTachoCount());
            LCD.drawInt(Motor.A.getTachoCount(),5,5); //print in remote console
            Delay.msDelay(200);
        } 
        RConsole.close(); //close connection
    }
}
