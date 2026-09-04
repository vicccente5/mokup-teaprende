Para este proyecto (TeAcompañamos) se usó Claude como apoyo, principalmente porque el estudiante recién está aprendiendo Django y en varias partes escribía código que funcionaba pero no entendía del todo por qué. Se le pidió a la IA que explicara línea por línea archivos como models.py, forms.py y views.py, y también que explicara en simple los conceptos básicos de Django, para poder entender mejor la lógica del propio código.

También se usó para el CSS: se le mostraba a la IA lo que se quería lograr en pantallas como el dashboard o las tarjetas de módulos, y esta ayudaba a ordenar los colores con variables y a dejar los botones y bordes más consistentes. Los cambios se fueron probando en el navegador y ajustando según lo que hacía falta.

Cuando aparecían errores (por ejemplo al migrar la base de datos o validar el formulario de registro), se le pegaba el error a Claude para entender qué estaba pasando y así corregirlo, en vez de copiar una solución sin saber por qué funcionaba.

Los archivos Conceptos Básicos de Django.md y analisis_codigo.md, incluidos en la carpeta del proyecto, son justamente las notas generadas a partir de esas conversaciones, usadas para estudiar y poder explicar el proyecto.

El contenido sobre TEA, la estructura general y las decisiones del proyecto son trabajo propio del estudiante. La IA fue un apoyo para entender y ordenar código, no para hacer el trabajo.

Prompts utilizados
Explícame línea por línea qué hace mi models.py, forms.py y views.py.
Explícame en simple qué son los Models, Views, Templates y Forms en Django.
¿Cómo hago que el registro use el correo en vez de un username?
Me tira este error en Django, ¿qué significa y cómo lo soluciono?
Ayúdame a mejorar el CSS del dashboard, con colores y bordes más consistentes.
Puedes darme un código para el CSS sea mas bonito y agradable a la vista

