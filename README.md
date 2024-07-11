Repositorio del Trabajo de fin de grado de DAM, hecho por Jordi Casanova Solanes.

-Este repositorio encontrara todo el proyecto del CFGS de DAM.
-El proyecto consta en realizar una aplicación  para la gestión de música.


--------------------------------------------------------------------------------------------------------------------------------------


·Funcionalidades que puedes hacer en la aplicación:

  -Crear nuevo usuario
  -Subir canciones 
  -Buscar canciones que hayan sido subidas anteriormente a la app.
  -Borrar la cuenta del usuario
  -Crear, eliminar listas de reproducción
  -Poder controlar el sonido de la música, los botones de reproducción (pause,continue,stop)



--------------------------------------------------------------------------------------------------------------------------------------


·Tecnologias implementadas en este Proyecto:

  -Cliente: Para el apartado frontend, he utilizado el lenjuage de programación Python con la libreria PySide6 para la UI, 
  también utilize funciones y herramientas de PySide6 como QMultimedia para el apartado de la reproducción de canciones. (Como editor de codigo utilize VSCode)

  -Servidor: Para el apartado de Backend, utilizé el lenjuage de programación Java con su framework SpringBoot y como ORM utilizé Hibernate. El servidor consta en realizar una API, donde luego el cliente hara sus peticiones HTTP
  correspondientes, luego se guarda en la BD que en mi caso utilizé PostgreSQl, aunque no es lo mas apropiado para este tipo de proyectos, una forma mas escalable seria utilizar almacenamiento en la nube
  como Amazon S3 ... (Como editor de codigo utilize el IDE de SpringToolSuite4)


  --------------------------------------------------------------------------------------------------------------------------------------

  ·Como utilizar la app?

    -Primero clonar el repositorio con el siguiente comando:

    git clone https://github.com/Jordismt/MySong_TFG_Jordi.git

    -Una vez clonado, veras que hay 2 carpetas:
      -QT_MySong (Parte del cliente)
      -MySong(Servidor)

    "Hay que tener en cuenta crear una BD en local y poner el mismo puerto y nombre que utilizé la aplicación SpringBoot"



    -Para ejecutar el cliente, abre la carpeta QT_Mysong y ejecute el archivo inicio.py.
    -Para ejecutar el servidor, abre el proyecto SpringBoot y ejecute el main de la app, (PRIMERO HAZ LA BD QUE LA DEJARE SUBIDA TAMBIÉN EN EL REPOSITORIO)

  
