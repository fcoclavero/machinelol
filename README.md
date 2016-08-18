# machinelol

El paquete contiene:

	* /Data: Carpeta con datos necesarios para el funcionamiento.
	* /Django: Framework y base de datos.

Primero configure los path de los datos en los siguientes scripts, segun donde ubique la carpeta /Data incluida con este paquete:
Ej: C:/users/vicho/bin/Data

[ Perdon por esto :( ]

Django\recomendation\_getChampionIdList.py in getChampionIds, line 6
Django\recomendation\_getChampionsDataFromIdArray.py in main, line 21
Django\recomendation\utilites.py in -, line 18
Django\recomendation\management\commands\poblate_db.py, line 19
Django\recomendation\management\commands\recommend_command.py, line 14
Django\recomendation\management\commands\_getChampionIdList.py in getChampionIds, line 6
Django\recomendation\management\commands\_getChampionsDataFromIdArray.py in main, line 21

Una vez configurado los path ya puede ejecutar el algoritmo de recomendacion en su equipo.
Esto es estrictamente necesario para el correcto funcionamiento.

!!!

La base de datos (db.sqlite3) viene con 1000 datos aproximadamente.

!!!

Como usar:

	* Abrir CMD y ubicarse en /Django
	* Tiene dos opciones para ejecutar la recomendacion:

	(Ver video YouTube)
	A. Ejecutar desde shell
		1. Elegir Id de sujeto de prueba (Ej. 21685) (Elija del contenido de Data/PlayerSummary/las) (Si aparece Processing User repetidamente, usar otra id)
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

Cualquier duda envíe un correo a vicenteoyanedel@gmail.com o fcoclavero32@gmail.com.
Podemos coordinar una prueba o lo puedo ayudar a solucionar algun problema.

-----------------------------------------------------------------------------------------------------------

Problemas:
	1. Al usar populate_db me sale muchas veces Processing user <id>: El user <id> no tiene estadisticas de ranked por lo que es rechazado.
		Probar con otra id

	2. Al ejecutar recomendación me aparece un cluster vacío:
	El usuario fue tomado como out-lier o ruido. Es necesario correr la recomendacion nuevamente.
	Si sigue apareciendo vacío probar cargando más datos en la BD corriendo:
		a. Abrir CMD y ubicarse en /Django
		b. Ejecutar 'python manage.py poblate_db 21685 600'

	3. Hay problema con la base de datos: Ver archivo EN CASO DE DB ERROR.txt en este mismo dir.
