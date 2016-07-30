# machinelol

Primero configure los path de los datos en los siguientes scripts, segun donde ubique la carpeta /Data/ incluida con este paquete:

Django\recomendation\_getChampionIdList.py in getChampionIds, line 6
Django\recomendation\_getChampionsDataFromIdArray.py in main, line 21
Django\recomendation\utilites.py in -, line 18

Una vez configurado los path ya puede ejecutar el algoritmo de recomendacion en su equipo.
Esto es estrictamente necesario para el correcto funcionamiento.

!!!
La base de datos viene vacia por defecto.
Es necesaria cargarla con por lo menos 1000 datos antes de correr la recomendación.

1. Abrir CMD y ubicarse en /Django
2. Ejecutar 'python manage.py poblate_db 10133 1000'
3. La base de datos queda cargada con 1000 datos para el clustering, incluido 10133.
!!!

Como usar:
	* Abrir CMD y ubicarse en /Django
	* Tiene dos opciones para ejecutar la recomendacion:

	A. Ejecutar desde shell
		1. Elegir Id de sujeto de prueba (Ej. 21685) (Elija del contenido de Data/PlayerSummary/las)
		2. Asegurese que esté el sujeto de prueba en la base de datos ejecutando (en /Django):
			python manage.py poblate_db <sujeto-id> 10
		3. Ejecute el sistema de recomendaciones y vea resultado en el shell:
			python manage.py recommend_command <sujeto-id>


	B. Ejecutar desde pagina
		1. Elegir Nick sujeto de prueba (Ej. Vicho)
		2. Encender servidor Django:
			python manage.py runserver
		3. Ir a 127.0.0.1:8000 e ingresar Nick (Vicho). (Como region debe poner 'las')
		4. Esperar a obtener resultados.


	En ambos casos se utilizan scripts identicos, son dos formas de recibir la respuesta.

Cualquier duda envíe un correo a vicenteoyanedel@gmail.com
Podemos coordinar una prueba o lo puedo ayudar a solucionar algun problema.
