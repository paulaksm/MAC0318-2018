import lejos.nxt.Motor;
import java.io.*;
import lejos.nxt.comm.*;
import lejos.util.Delay;
import lejos.nxt.LCD;

public class ConsoleTest {
    public static DataOutputStream dataOut;
    public static DataInputStream dataIn;
    public static NXTConnection Link;

    public static int speed = 200, turnSpeed = 125, speedBuffer, speedControl;
    public static int commandValue,transmitReceived, lastCommand = 0;

    public static void main(String [] args) throws Exception {
        connect();

        while(true){
            if (dataIn.available() > 0){
                byte x = dataIn.readByte();
                if(checkCommand((int)x)) {
                    disconnect();
                    break;
                }
            }
        }
    }
 
    public static boolean checkCommand(int data) {
        System.out.println(data);
        switch (data) {
            case 0x64:
                return true;
            case 0x1: // forward
                Motor.A.setSpeed(speed);
                Motor.C.setSpeed(speed);
                Motor.A.forward(); 
                Motor.C.forward();
                break;
            case 0x2: // forward
                Motor.A.setSpeed(speed);
                Motor.C.setSpeed(speed);
                Motor.A.backward(); 
                Motor.C.backward();
                break;
            case 0x3: // forward
                Motor.A.setSpeed(speed);
                Motor.C.setSpeed(speed);
                Motor.A.forward(); 
                Motor.C.backward();
                break;
            case 0x4: // forward
                Motor.A.setSpeed(speed);
                Motor.C.setSpeed(speed);
                Motor.A.backward(); 
                Motor.C.forward();
                break;
           default:
                Motor.A.stop(true); 
                Motor.C.stop();
        }
        return false;
    }

    public static void connect() {  
        System.out.println("Listening..");
        Link = Bluetooth.waitForConnection(0, NXTConnection.RAW);
        dataOut = Link.openDataOutputStream();
        dataIn = Link.openDataInputStream();

    }

    public static void disconnect() throws java.io.IOException {  
        System.out.println("Closing...");
        dataOut.close();
        dataIn.close();
        USB.usbReset();
        System.exit(0);
    }
}
