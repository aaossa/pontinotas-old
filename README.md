# PontiNotas :sunglasses:
Aplicación simple con base funcional en Python 3.4 y disponible en Heroku que permite la creación de un pdf correspondiente a la Ficha Académica Acumulada entregada por la Pontificia Universidad Católica de Chile.

La aplicación se encuentra [**disponible en Heroku**](http://pontinotas.herokuapp.com).

## Módulos, librerías y otros
**Python**: Flask, requests, html2text.
**Javascript**: pdfmake.

## Pendiente
* Podrían haber datos que falten, que no se encuentran disponibles en la página de la que se extraen los datos de los cursos. Por ejemplo, como soy alumno de pregrado, no sé como se ve la página para los alumnos de posgrado, ya que podrían haber tablas que no hagan "match" con ninguno de los filtros del código que extrae la información.
* Desplgear ventanas de errores correctas. Por ejemplo, al colocar una clave incorrecta o un usuario no válido se obtiene un error 500. Lo ideal sería desplegar una ventana informando de la invalidez de esas credenciales e invitar a probar nuevamente.
* API. Solamente con fines de aprendizaje. Dificilmente tendrá un uso práctico alguna vez, como esta página :joy:

Cualquier error/duda/comentario envía un mail a: **aaossa@uc.cl**. Si tienes una cuenta de GitHub abre una issue.

######IMPORTANTE: NO OFICIAL
*He usado este pequeño proyecto para aprender javascript y comprender más y mejores usos de flask. Además de aplicar lo que he ido aprendiendo dentro del marco javascript + css + html.*
