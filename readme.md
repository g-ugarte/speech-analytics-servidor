# Uso de Analizador.exe

# Composición de los archivos en la carpeta ```src```

## ```index.py```

Cuenta con los procedimientos necesarios para unir todas las funciones, el flujo es el siguiente:
1. Espera la opción de bandera
2. Descarga el archivo de la plataforma y verifica que se haya realizado la descarga
3. Procede a hacer los análisis
4. Subida a Base de Datos
5. Obtención de gráficos

## ```download```

Es una carpeta asociada a los módulos utilizados para automatizar las descargas de las páginas web, de tal manera que cumple una función similar a las consultas por archivos en base a una API.

### ```call.py```

Utiliza Selenium para acceder a la plataforma Genesys Cloud y realizar la descarga de llamadas. Cuenta con la clase **Descargar_Llamada** con los siguientes métodos.

- ```descargar(self, llamada_id)```: Accede a la página y procede a descargar una llamada, es necesario proveer el id.
- ```validar(self, llamada_id)```: Verifica que un archivo haya sido descargado, para cerrar la ventana del explorador dado el id de la llamada.

### ```chat.py```

Utiliza Selenium para acceder a la plataforma S1 Gateway y descargar los chats. Cuenta con la clase **Descargar_Reporte**.
- ```descargar(self, patron)```: Accede a la página y procede a descargar una llamada, puede descargar mensajes o reportes de conversaciones a partir de un patron especificado.
- ```validar(self)```: Verifica que el archivo excel haya sido descargado, para cerrar la ventana del explorador dado el id de la llamada.

## ```load```

Carpeta utilizado para la creación y carga de modelos de IA.

### ```maquina.py```

Utiliza un modelo de IA de clasificación basado en el procedimiento Maquina de Soporte Vectorial (SVM). Esta clase cuenta con los métodos:
- ```clasificar(self, df)```: Recibe un dataframe de excel de conversaciones de chats para obtener un vector donde cada fila se le asocia un producto que fue entrenado anteriormente.
- ```clasificar_texto(self, texto)```: Recibe una transcripción y puede obtener una predicción de producto.

### ```sentimientos.py```

Utiliza un modelo de IA para analizar textos y retornar los valores entre 0 a 1 para el análisis de sentimientos. Se retornan diccionarios de valores para su resultado positivo, negativo y neutral.

### ```transcripcion.py```

Realiza una carga de un modelo de IA de transcripción que hace una carga del modelo **Whisper V3 Large**. Se le provee una ruta de un mp3 en el método ```transcribir(self, ruta_audio)``` para obtener una lista de transcripciones con sus respectivas marcas de tiempo.

### ```vectorizadores.py```

Utiliza modelos de procesamiento de texto para crear modelos basados en palabras clave en cada documento que representa una conversación ya sea llamada o chat.

- ```Counter```: Esta clase corresponde a la carga de un procedimiento de vectorización. Esta clase puede obtener una lista de conversaciones y retorna la misma cantidad de vectores para cada palabra signficativa. Cada valor del vector corresponde a su frecuencia.
- ```TfIdf```: Esta clase corresponde a la carga de un procedimiento de vectorización. Esta clase puede obtener una lista de conversaciones y retorna la misma cantidad de vectores para cada palabra signficativa. Cada valor del vector corresponde a su frecuencia invertida por la cantidad de documentos que contienen aquella palabra.

## ```utils```

Carpeta con funciones utiles para utilizar en el archivo ```index.py```.

### ```database.py```

Funciones para obtener datos esenciales sobre alguna conversación postventa y subir resultados de los análisis.

- Análisis de conversación de Llamada y Chat: ```obtener_producto_asesor_grupo_IVR``` y ```obtener_producto_asesor_grupo_S1```.
- Subida de resultados de Llamada y Chat: ```subir_datos_IVR``` y ```subir_datos_S1```.

### ```fragmentar.py```

Función ```Fragmentar(ruta_audio, carpeta_salida, tiempo_fragmento)``` que recibe una ruta de archivo y una ruta de carpeta que recibirá los audios particionados.

### ```graficos.py```

Métodos para crear los siguientes gráficos:

- Nubes de palabras: ```graficos_palabras(diccionario, carpeta, ruta_salida)```
- Gráfico de barras de tiempos de espera/ muertos: ```grafico_barras_espera(espera_min, espera_max, espera_prom, caso_id, carpeta, ruta_salida)``` / ```grafico_barras_activo(tiempo_activo, tiempo_total, carpeta, ruta_salida)```
- Gráfico de barras de análisis de sentimientos:

### ```texto_clave.py```

Utilizar funciones para obtener tokens de texto ya sea utilizando los vectorizadores **Counter** y **TfIdf**.

### ```wait.py```

- ```obtener_tiempos(df)```: Obtener tiempos de diferencia entre mensajes
- ```tiempo_muerto(dfs)```: Obtener tiempos dado las marcas de tiempo de transcripción donde el cliente espera a la respuesta del asesor

# Requisitos **(NO MOVER LA CARPETA ```res``` POR NINGÚN MOTIVO, MOVER TODO EL DIRECTORIO)**

Es necesario definir bien los archivos ```res/descarga_chat.json```, ```res/descarga_llamada.json``` y ```res/rutas.json```.

**Nota**: Para algunos valores es necesario guiarse de ```edge://version/``` dentro de edge.

## ```res/descarga_chat.json```

### Decripción de parámetros

- user-data-dir: Ruta encontrada en  ```edge://version/```
- profile-directory: Ruta encontrada en ```edge://version/```
- msedgedriver: Ruta del webdriver de Edge, este debe ser compatible, puede descargarse de: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads
- downloads: Carpeta de decargas de Edge
- range: Cantidad de dias a tomar en cuenta (ej: "yesterday" y "last2weeks")

### Ejemplo de parámetros

```json
{
    "user-data-dir": "C:/Users/AppData/Local/Microsoft/Edge/User Data",
    "profile-directory": "Profile 3",
    "msedgedriver": "C:\\Users\\Documents\\Speech-Analytics\\Descargar\\msedgedriver.exe",
    "downloads": "C:/Users/Downloads/Speech-Analytics-Downloads",
    "range": "yesterday"
}
```

## ```res/descarga_llamada.json```

### Descripción de parámetros

- user_data_dir: Ruta encontrada en  ```edge://version/```
- profile_directory: Ruta encontrada en  ```edge://version/```
- edge_driver: Ruta del webdriver de Edge, este debe ser compatible, puede descargarse de: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads
- admin_tab_id: Parámetro tabId dentro del enlace de IVR (https://apps.mypurecloud.com/directory/#/analytics/interactions/29af59bb-657c-4bea-b2dc-51f884f14c7a/admin?tabId=346200bf-61d3-4c17-a54f-23370c6cf11d)
- download_directory: Directorio de descargas

### Ejemplo de parámetros

```json
{
    "user_data_dir": "C:/Users/bp3285/AppData/Local/Microsoft/Edge/User Data",
    "profile_directory": "Profile 3",
    "edge_driver": "C:\\Users\\bp3285\\Documents\\Speech-Analytics\\Descargar-Llamadas\\msedgedriver.exe",
    "admin_tab_id": "346200bf-61d3-4c17-a54f-23370c6cf11d",
    "download_directory": "C:/Users/bp3285/Downloads/Speech-Analytics-Downloads" 
}
```

## ```res/rutas.json```

### Descripción de parámetros

- export: Directorio donde se encuentran los modelos y ffmpeg
- fragmentos: Directorio que fragmenta los audios para su procesamiento
- salida: Direcotrio en el que se obtendrán los gráficos, transcripciones, mensajes, etc.

### Ejemplo de parámetros

```json
{
    "export": "C:/Users/bp3285/Documents/ejecutable/export",
    "fragmentos": "./fragmentos",
    "salida": "./salida"
}
```

# Funciones

## Descarga y análisis 

### Conversaciones de WhatsApp

```sh
.\analizador.exe --excel
```

### Conversaciones de Teléfono

```sh
.\analizador.exe --mp3={uuid-de-la-llamada}
```

## Análisis de archivos

### Conversaciones de WhatsApp

```sh
.\analizador.exe --ruta_excel={ruta-a-archivo-xlsx}
```

### Conversaciones de Teléfono

```sh
.\analizador.exe --ruta_llamada={ruta-a-llamada-mp3}
```
