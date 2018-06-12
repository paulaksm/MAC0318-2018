import lejos.nxt.*;

class Wonder {
	public static void main (String[] args){
		int rotation = 282;
		boolean inverse = false;
		// note que nesse código o sensor está na porta 1
		UltrasonicSensor ultra = new UltrasonicSensor(SensorPort.S4);
		TouchSensor touch = new TouchSensor(SensorPort.S1);
		
		while (true) {
			if (ultra.getDistance() < 40 || touch.isPressed()) {

				Motor.B.setSpeed(200);
				Motor.C.setSpeed(200);

				if (inverse) {
					Motor.B.rotate(360, true);
					Motor.C.rotate(360, false);
				} else {
					Motor.B.rotate(-360, true);
					Motor.C.rotate(-360, false);
				}

				if (Math.random() < 0.5) {
					Motor.B.rotate(-rotation, true);
					Motor.C.rotate(rotation, false);
				} else {
					Motor.B.rotate(rotation, true);
					Motor.C.rotate(-rotation, false);
				}

				if (Math.random() < 0.5)
					inverse = !inverse;

			} else {
				Motor.B.setSpeed((float) Math.random()*400);
				Motor.B.setSpeed((float) Math.random()*400);
				if (!inverse) {
					Motor.B.forward();
					Motor.C.forward();
				} else {
					Motor.B.backward();
					Motor.C.backward();
				}
			}
		
		}
	}
}
