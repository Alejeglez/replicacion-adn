# replicacion-adn
## Miriam Méndez Romero y Alejandro Jesús González Santana

En esta práctica se ha desarrollado un simulador de la replicación de ADN en python junto con una interfaz web. La secuencia de la que se partirá en la replicación puede ser generada aleatoriamente o leída desde un archivo fasta. Debido a la implementación de la replicación, se solicita que el tamaño mínimo de una cadena de ADN sea 11.

Para la implementación se ha desarrollado la clase ADN con distintos métodos. Cada método implementado hace alusión a un proceso de la replicación (como podrían ser la acción de la helicasa o de las ADN polimerasas). También se incluyen métodos para traducir entre ARN, ADN y bases complementarias. Los métodos más relevantes serían create() (que crea las dos hebras a replicar en nuestra clase de ADN), y start_replication() (que ejecuta las acciones de la replicación de forma iterativa).

El archivo fuera de la carpeta web realiza la replicación de ADN con una interfaz en línea de comandos, donde la diferencia con la web es que se ha incluido un input para que el usuario pueda leer lo que sucede en cada iteración y presionar una tecla para continuar. 
En la interfaz web hemos optado por hacer un resumen con las acciones principales de cada componente de la replicación. Estos resúmenes se han almacenado en un diccionario que es atributo de ADN, y que luego será accesible desde el servidor web. Para el desarrollo  de la interfaz web se ha utilizado la librería reflex. Para ejecutar el servidor web hay que ejecutar el comando reflex run sobre el directorio web.

Por último, la clase de ADN contiene el método validate_replication() que permite corroborar que la replicación se ha realizado con éxito.
