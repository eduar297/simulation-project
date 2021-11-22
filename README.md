# Proyecto de simulación basado en Eventos Discretos

### Eduardo Moreira González C-411

#### Problema 4

###### Happy Computing

Happy Computing es un taller de reparaciones electrónicas se realizan las
siguientes actividades (el precio de cada servicio se muestra entre paréntesis):

1. Reparación por garantı́a (Gratis)
2. Reparación fuera de garantı́a ($350)
3. Cambio de equipo ($500)
4. Venta de equipos reparados ($750)

Se conoce además que el taller cuenta con 3 tipos de empleados: Vendedor, Técnico y Técnico Especializado.
Para su funcionamiento, cuando un cliente llega al taller, es atendido por un vendedor y en caso de que el servicio que requiera sea una Reparación (sea de tipo 1 o 2) el cliente debe ser atendido por un técnico (especializado o no). Además en caso de que el cliente quiera un cambio de equipo este debe ser aten- dido por un técnico especializado. Si todos los empleados que pueden atender al cliente están ocupados, entonces se establece una cola para sus servicios. Un técnico especializado sólo realizará Reparaciones si no hay ningún cliente que desee un cambio de equipo en la cola. Se conoce que los clientes arriban al local con un intervalo de tiempo que distribuye poisson con λ = 20 minuts y que el tipo de servicios que requieren pueden ser descrito mediante la tabla de probabilidades:

| Tipo de servicio | Probabilidad |
| ---------------- | ------------ |
| 1                | 0.45         |
| 2                | 0.25         |
| 3                | 0.1          |
| 4                | 0.2          |

Además se conoce que un técnico tarda un tiempo que distribuye exponecial con λ = 20 minutos, en realizar una Reparación Cualquiera. Un técnico especializdo tarda un tiempo que distribuye exponencial con λ = 15 minutos para realizar un cambio de equipos y la vendedora puede atender cualquier servicio en un tiempo que distribuye normal (N(5 min, 2mins)). El dueño del lugar desea realizar una simulación de la ganancia que tendrı́a en una jornada laboral si tuviera 2 vendedores, 3 técnicos y 1 técnico especializado.

###### Explicación

El modelo de simulación de eventos discretos desarrollado para resolver el
problema fue el de tener 6 servidores en paralelo, de la siguiente manera:

Tenemos un servidor por cada obrero que oferta cada servicio, o sea, 2 server para vendedores, 3 para técnicos y 1 para el técnico especializado.

La idea es que al llegar un cliente este elige que servivio usar y si puede ser atendido lo hace, sino se encola hasta que llegue su turno y en cada interacion se guarda el tiempo total, los tiempos de llegada y salida, estos ultimos de cada cliente que sale de cada uno de los servicios ofertados. 

Vamos por pasos:

Tenemos un metodo **simular()** que lo que hace es madar a inicializar todas las variables descritas en el **script.py**, luego se analiza dentro de un ciclo que en un inicio seria infinito a menos que se mande a detener intencionalmente. En cada iteracion preguntamos si llega un cliente y si lo hace, se maneja con la funcion **evento_de_arribo()**, en otro caso vemos si el cliente sale del servicio del vendedor 1 o 2 (**evento_de_salida_vendedor_1(), evento_de_salida_vendedor_2()**) respectivamente, sino analizamos si lo mismo con alguno de los 3 tecnicos (**evento_de_salida_tecnico_1(), evento_de_salida_tecnico_2, (), evento_de_salida_tecnico_3**), y de igual forma si sale de un especialista (**evento_de_salida_especialista()**). Sinó es alguno de estos casos es porque el taller cerró y por tanto no pueden entrar mas clientes, pero si se deben analizar los que se encuentran aun siendo atendidos o en las colas. Para esto tenemos los metodos: **evento_de_cierre_vendedor_1(), evento_de_cierre_vendedor_2(), evento_de_cierre_especialista(), evento_de_cierre_tecnico_1(), evento_de_cierre_tecnico_2(), evento_de_cierre_tecnico_3()**

La idea de cada uno de estos metodos es la misma que la dada en conferencia para 2 servers en paralelo solo que ahora tendriamos 6. Al leer el codigo por la forma en que estan nombradas las variables y los metodos y la forma en que se llaman y algunos comentarios se puede entender el funcionamiento de nuestra simulacion correctamente. Algo agregado extra a lo dado en conferencia es un diccionario para guardar la ganancia que aporta cada cliente, asi al final de la simulacion nos movemos por todos los elementos de dicho y su sumatoria seria la ganancia total de la tienda en un horario de x horas, que por defecto es 8h*60min, o sea, un horario laboral, dado que la sumulacion se baso en minutos.

Algo de lo que nos podemos percatar en la simulacion y en los datos dados como tal es que la mayoria de los clientes usan el servicio 1, aportando 0 ganacias a la tienda.

Tambien luego de varias corridas podemos ver que en promedio la gancia es de $6765.55 aproximadamente.

Podemos ver que el especialista recibe pocas visitas al igual que los vendedores mientras que los tecnicos tienen mas actividad, en especial si es gratis :laughing:

