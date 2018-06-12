import java.io.*;
import lejos.nxt.*;
import lejos.nxt.comm.*;
import lejos.robotics.navigation.DifferentialPilot;

public class RemoteCarDP { 
    public static DataOutputStream dataOut; 
    public static DataInputStream dataIn;
    public static USBConnection USBLink;
    public static int speed = 200, turnSpeed = 100, speedBuffer, speedControl;
    public static int commandValue,transmitReceived, lastCommand = 0;
    public static DifferentialPilot dp;
    //public static UltrasonicSensor sonar;
   
    public static void main(String [] args) throws Exception {
        connect();
        dp = new DifferentialPilot(5.6f, 11.2f, Motor.C, Motor.A, false);
        //sonar = new UltrasonicSensor(SensorPort.S1);
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
                dp.forward();
                break;
            case 1: // right
                dp.rotateRight();
                break;
            case 2: // left
                dp.rotateLeft();
                break;
            case 3: // backward
                dp.backward();
                break;
            case 4: // sonar read
                int val = Motor.A.getTachoCount();
                //int val = sonar.getDistance();
                dataOut.writeInt(val);
                dataOut.flush();
                break;
           default:
                dp.stop();
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
