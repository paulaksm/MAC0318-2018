Iniciar primeiro o código no robô e depois o código do python3.

##### Códigos:
    - RemoteCar.java 	-- implementação do carrinho de controle remoto acessando diretamente os motores
    - RemoteCarDP.java 	-- implementação do carrinho de controle remoto usando as abstrações do DifferentialPilot
    - USBInterface.py	-- classe que estabelece os métodos de comunicação vis USB
    - car_controller.py -- controlador do carrinho com comandos de teclado

__Obs: executar código car_controller.py como sudo__

##### Comandos (car_controller.py):
```console
'q' 			-- encerrar programa
'up_arrow'		-- mover robô para frente
'down_arrow'	-- mover robô para trás
'left_arrow'	-- mover robô para a esquerda
'right_arrow'	-- mover robô para a direita
'space_bar'		-- retorna a leitura do tacômetro da roda A
```