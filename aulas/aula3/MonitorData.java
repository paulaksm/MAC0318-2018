import lejos.nxt.*;
import lejos.robotics.navigation.DifferentialPilot;
import java.lang.Thread;	
	
public class MonitorData {
	public static class RobotMonitor extends Thread {	
		private int delay;
		UltrasonicSensor sonar;
		
		public RobotMonitor(int d, UltrasonicSensor sonar) {
			this.setDaemon(true);
			this.delay = d;
			this.sonar = sonar;
		}	

		public void run() { 	
			while(true) {	
				LCD.clear();
				LCD.drawString("MotorA ="+Motor.A.getTachoCount(), 0 , 0);
				LCD.drawString("MotorC ="+Motor.C.getTachoCount(), 0 , 1);
				LCD.drawString("Sonar ="+sonar.getDistance(), 0 , 2);
	
				try { this.sleep(delay); }
				catch (Exception e) { }
			} // end while	
		} // end run	
	} // end class	

	public static void main(String [] args) throws Exception {
		UltrasonicSensor sonic = new UltrasonicSensor(SensorPort.S1);
		DifferentialPilot pilot = new DifferentialPilot(5.6f, 11.2f, Motor.C, Motor.A);
		RobotMonitor rm = new RobotMonitor(400, sonic);	
	
		pilot.arcForward(30);	
		rm.start(); // inicia thread	
	
		while(sonic.getDistance() >= 30) {	
			Thread.sleep(200);	
		}
	}
}	
