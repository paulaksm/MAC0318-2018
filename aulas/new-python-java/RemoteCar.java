import java.io.*;
import lejos.nxt.*;
import lejos.nxt.comm.*;

public class RemoteCar { 
    public static DataOutputStream dataOut; 
    public static DataInputStream dataIn;
    public static USBConnection USBLink;
    public static int speed = 200, turnSpeed = 100, speedBuffer, speedControl;
    public static int commandValue,transmitReceived, lastCommand = 0;
   
    public static void main(String [] args) throws Exception {
        connect();
        while(true){
            if (dataIn.available() > 0){
                int x = dataIn.readInt();
                if(checkCommand(x)) {
                    disconnect();
                    break;
                }
            }
        }
    }
 
    public static boolean checkCommand(int data) throws Exception {
        System.out.println(data);
        switch (data) {
            case 99:
                return true;
            case 0: // forward
                Motor.A.setSpeed(speed);
                Motor.C.setSpeed(speed);
                Motor.A.forward(); 
                Motor.C.forward();
                break;
            case 1: // right
                Motor.A.setSpeed(turnSpeed);
                Motor.C.setSpeed(turnSpeed);
                Motor.A.backward(); 
                Motor.C.forward();
                break;
            case 2: // left
                Motor.A.setSpeed(turnSpeed);
                Motor.C.setSpeed(turnSpeed);
                Motor.A.forward(); 
                Motor.C.backward();
                break;
            case 3: // backward
                Motor.A.setSpeed(speed);
                Motor.C.setSpeed(speed);
                Motor.A.backward(); 
                Motor.C.backward();
                break;
            case 4: // sonar read
                int val = Motor.A.getTachoCount();
                //int val = sonar.getDistance();
                dataOut.writeInt(val);
                dataOut.flush();
                break;
            case 6: // greetings
                String s = "Remote Controlled Car Project";
                dataOut.writeBytes(s);
                dataOut.flush();
                break;
           default:
                Motor.A.stop(true); 
                Motor.C.stop();
        }
        return false;
    }

    public static void connect() {  
        System.out.println("Listening..");
        USBLink = USB.waitForConnection(0, NXTConnection.RAW);
        dataOut = USBLink.openDataOutputStream();
        dataIn = USBLink.openDataInputStream();

    }

    public static void disconnect() throws java.io.IOException {  
        System.out.println("Closing...");
        dataOut.close();
        dataIn.close();
        USB.usbReset();
        System.exit(0);
    }
}
