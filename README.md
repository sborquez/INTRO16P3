# INTRO 2016 (inf.utfsm.cl) - Problema 4

## Objetivos

Crear un bot lo suficientemente inteligente como para poder derrotar a un *botdummy* y desempeñarse lo mejor posible en contra de los bots de sus compañeros.

## Como jugar
El primer paso es montar el servidor contendio en **Sevidor/** usando:

_python servidor.py_

Nos entregara la ip y el puerto para conectarnos.

Segundo paso, conectar clientes. Ir a la carpeta **Cliente/**, ejecutar:

_python cliente_alumnos.py_ o _python cliente_dummy.py_

Aparecera un mensaje de "conectado" en su pantalla, esperando a que se conecten los demás jugadores.

Si todo va bien, al terminar la partida, un mesaje de "GAME OVER" aparecerá en su pantalla.

## Uso de Visualización

El servidor genera un registro escrito de la partida, para ver que sucedió utilizamos nuestro visualizador contendio en **Visualizacion/**.

_python main.py_

Toda partida que quiera ser reproducida debe dejarse en la carpeta logs.

Controles:
* Space bar: start / stop.
* Up/Down(durante reproducción): aumentar/reducir velocidad.
* Up/Down(durante resultados): subir/bajar.
* F: fullscreen.
* Esc: salir