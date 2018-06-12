import lejos.nxt.Motor;
import java.io.*;
import lejos.nxt.comm.*;
import lejos.util.Delay;
import lejos.nxt.LCD;

public class ConsoleTest {
    public static DataOutputStream dataOut;
    public static DataInputStream dataIn;
    public static USBConnection USBLink;

    public static void main(String[] args) throws Exception {

        USBLink = USB.waitForConnection(0, NXTConnection.RAW);
        dataOut = USBLink.openDataOutputStream();
        dataIn = USBLink.openDataInputStream();
        // espera inicio da conexao
        while (dataIn.available() == 0);

        Motor.A.rotate(1440,true);
        while (Motor.A.isMoving()){

            //dataOut.writeBytes("Tacho_Count_Motor_A:"+Motor.A.getTachoCount());
            dataOut.writeBytes(""+Motor.A.getTachoCount());
            dataOut.flush();

            LCD.drawInt(Motor.A.getTachoCount(), 5, 5);
            Delay.msDelay(200);
        } 
        dataOut.close();
    }
}
