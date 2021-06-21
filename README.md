# Web-Scrapping
> Nadia González Fernández C412
>
> Luis Alejandro Lara Rojas

## Cómo correr el sistema

Nuestro sistema distribuido tiene 3 tipos de nodos:


- **Chord**: nodo base de sistema distribuido. Este es el encargado del manejo y almacenamiento de la información.
- **Server**: encargado de recibir las peticiones del usuario e interactuar con el chord para obtener la página correspondiente.
- **Scrapper**: encargado de buscar las páginas requeridos.

Para correr nuestro proyecto se debe correr en consola dentro de la carpeta Web-Scrapping/src:

````
python3 create_chord_node.py ip_no port_no
````

Este comando crea el primer nodo chord del sistema y recibe el número de ip y puerto por donde este nodo va a escuchar. Para el correcto funcionamiento del sistema se debe crear al menos un nodo chord antes de crear otro tipo de nodo.

Todo nodo, excepto el primer nodo chord creado, al iniciarse recibe como parámetros: ip y puerto por el que escucha e ip y puerto de cualquier otro nodo en el sistema:

Para crear un nodo scrapper:
```
python3 create_scrapper_node.py ip_no port_no other_node_ip other_node_port
```

Para crear un nodo server:
```
python3 create_server_node.py ip_no port_no other_node_ip other_node_port
```

Una vez creado el nodo, podrá introducir en la consola la url deseada y, luego de realizada a busqueda, se mostrará en pantalla el código html de la página.

Para el correcto funcionamiento de los pedidos al sistema deben correr a la vez al menos un nodo de cada tipo.

### Mensajes en consola

En consola se muestran el mensaje que indica cuando el nodo está escuchando:
```
Listening from port 8880...
```
En este caso indica que el nodo espera mensajes por el puerto 8880.

En la consola se imprimen los mensajes que llegan y salen del nodo:

Cada mensaje tiene cierta estructura que sigue el protocolo utilizado. Cada mensaje consta de un encabezado (`Action`) y un cuerpo (`Body`). 
El  encabezado indica la acción a realizar y el cuerpo los parámetros.
```
Received message:
Action: get-succ-node
Body:
Successor node found: 14
Replied message:
Action: ret-succ-node
Body: localhost%8883%14
```

En este ejemplo se recibe un mensaje que indica obtener el sucesor del nodo y se retorna el mensaje con el ip, el puerto y el id del sucesor (`ip=localhost, port=8883, id=14`). Estos 3 parámetros se empaquetan en el cuerpo del mensaje separados por el caracter "%".

El siguente mensaje indica que el nodo está estabilizando sus referencias

```
Stabilizing...
Checking successor...
Fixing fingers...
```

## Funcionamiento general del sistema

El sistema distribuido está basado en el protocolo y algoritmo de Chord.

El sistema está compuesto por 3 tipos de nodos: server, scrapper y chord. 

Al inicializar un nodo de tipo server o scrapper, se le asocia a cada uno un nodo chord al cual le harán los pedidos necesarios. El sistema garantiza que todo nodo tenga siempre un nodo chord asociado. En caso de que el nodo sea de tipo chord, su nodo chord afiliado será el mismo. 

> Nota: para el correcto funcionamiento del sistema siempre tiene que existir al menos un nodo chord funcionando.

Todo nodo chord tiene una lista donde guarda referencias a nodos scrapper para poder buscar las páginas que no estén guardadas en el sistema. Si la lista se queda vacía, el nodo pedirá a su predecesor un nodo scrapper. Si este último no tiene ninguna referencia a un scrapper también este hará el mismo pedido a su predecesor y así sucesivamente. De no encontrarse ninguna referencia en el sistema se lanzará una excepción.

Cuando a un nodo server le llega el pedido de una url, este pide a su nodo chord asociado el código html de esa página. El nodo chord busca en el sitema si la página está guardada. De ser así, este simplemente manda la información encontrada. De lo contrario, este pide a algún nodo scrapper buscar la información. Este último realiza la búsqueda en profundidad 3 del sitio y luego manda al nodo chord los códigos html de las páginas encontradas.


Todos los mensajes que se envían  entre los nodos del sistema tienen un tiempo de espera de 3 mínutos. Esto implica que al enviar un mensaje, se espera durante ese tiempo la respuesta, luego se asume error de conexión.

## Implementación

El proyecto utiliza sockets zmq para la comunicación de los nodos. 

En Web-scrapping/src/node.py está la clase `Node`, donde se define un nodo genérico padre del cual heredan todos los nodos. 

### Nodo Chord

El nodo chord está implementado en Web-Scrapping/src/node/chord.py. Allí se crea una clase `ChordNode`. Esta implementa el algoritmo de chord y almacena las páginas buscadas. 

Para mantener consistencia en el sistema, el nodo mantiene una lista con los 5 próximos sucesores. Esta se actualiza constantemente en el background. Esto se usa en caso de fallas en el sistema para estabilizarlo. 

### Nodo Server 

El nodo server es el encargado de recibir las peticiones del cliente y hacer los pedidos pertinentes al nodo chord

### Nodo Scrapper

El nodo scrapper hace búsquedas con profundidad 3 de los sitios pedidos. Para ello se utiliza la clase `WebNode` donde se almacenan los links y htmls encontrados. En esta clase se utilizan expresiones regulares y la biblioteca BeautifulSoup.

## Ejemplo

Para inicializar el primer nodo chord del sistema:
```
python3 create_chord_node.py localhost 8880
```

Se imprime en consola:
```
Id:  8

Stabilizing...
Checking successor...
Fixing fingers...

Received message:
Action: get-pred-node
Body:
Replied message:
Action: ret-pred-node
Body: localhost%8880%8

Listening from port 8880...
```

Para inizializar un nodo scrapper:
```
python3 create_scrapper_node.py localhost 8882 localhost 8880
```
Se mostrará en consola:
```
Listening from port 8882...
```

Para inizializar un nodo server:
```
python3 create_server_node.py localhost 8884 localhost 8882
```
Se mostrará en consola:
```
Listening from port 8884...
```
```
Enter url:
```
Esto indica que ya puede introducir la url del sitio que se quiere hacer scrap.
