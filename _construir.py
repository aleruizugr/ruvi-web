# Genera las páginas de la web a partir de las piezas comunes (cabecera y pie).
# Uso: python3 _construir.py   (el guion bajo hace que GitHub Pages no publique este archivo)
import pathlib, html, hashlib
R = pathlib.Path(__file__).parent
VERSION = hashlib.md5((pathlib.Path(__file__).parent / "ruvi.css").read_bytes()).hexdigest()[:8]   # cambia sola cuando cambian los estilos, para que el navegador no use una copia vieja
APP = "https://plantilla-repaso.netlify.app"   # botón «Entrar»: cambiar aquí si la app cambia de dirección
CORREO = "hola@ruvilab.es"

def cabeza(titulo, desc, ruta, noindex=False):
    return f'''<!doctype html>
<html lang="es"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{titulo}</title>
<meta name="description" content="{html.escape(desc)}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://ruvilab.es{ruta}">
<meta property="og:image" content="https://ruvilab.es/img/ruvi-og.jpg">
<meta property="og:locale" content="es_ES">
<link rel="icon" type="image/png" href="/img/favicon.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preload" href="/fuentes/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/ruvi.css?v={VERSION}">
</head><body>'''

def menu(actual):
    items = [("/#proyectos", "Proyectos", "opc"), ("/plantilla-repaso/", "Plantilla de Repaso", ""), ("/#contacto", "Contacto", "")]
    links = "".join(f'<a href="{h}" class="{c}"{" aria-current=\"page\"" if h == actual else ""}>{t}</a>' for h, t, c in items)
    return f'''<header class="top"><div class="in">
<a class="marca" href="/" aria-label="Ruvï, inicio"><img src="/img/ruvi-monograma.png" alt="" width="40" height="40"><b>RUVÏ</b></a>
<nav class="menu" aria-label="Menú">{links}</nav>
</div></header>'''

PIE = f'''<footer class="pie"><div class="in">
<span>© 2026 Ruvï · <a href="mailto:{CORREO}">{CORREO}</a></span>
<nav aria-label="Legal"><a href="/aviso-legal/">Aviso legal</a><a href="/privacidad/">Privacidad y cookies</a></nav>
</div></footer>
<script>
document.querySelectorAll("[data-copiar]").forEach(function(b){{b.addEventListener("click",function(){{
  var t=b.getAttribute("data-copiar"),ok=function(){{b.textContent="Copiado";setTimeout(function(){{b.textContent="Copiar"}},1800)}};
  if(navigator.clipboard)navigator.clipboard.writeText(t).then(ok,function(){{}});}})}});
</script>
</body></html>'''

TELEFONO = "669 767 570"
WHATSAPP = "34669767570"
from urllib.parse import quote
ASUNTO = "Demo de Plantilla de Repaso"
CUERPO = ("Hola:\n\nQueremos ver una demo de Plantilla de Repaso.\n\n"
          "Academia: \nCiudad: \nNúmero de alumnos: \nTeléfono de contacto: \n"
          "Mejor día y hora para la videollamada: \n\nGracias.")
WA_TEXTO = "Hola, os escribo desde ruvilab.es. Me gustaría ver una demo de Plantilla de Repaso para mi academia."

def correo_bloque():
    mailto = f"mailto:{CORREO}?subject={quote(ASUNTO)}&body={quote(CUERPO)}"
    wa = f"https://wa.me/{WHATSAPP}?text={quote(WA_TEXTO)}"
    return f'''<div class="btns">
    <a class="btn p" href="{mailto}">Escribir un correo</a>
    <a class="btn wa" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
  </div>
  <div class="correo"><code>{CORREO}</code><button class="copiar" type="button" data-copiar="{CORREO}">Copiar</button></div>
  <p class="muted" style="font-size:.95rem">O llámanos o escríbenos al <b style="white-space:nowrap">{TELEFONO}</b>.</p>'''

def con_version(html_txt):
    # añade ?v=<huella> a las imágenes de /img/, para que el navegador no muestre una versión vieja
    import re as _re
    def f(m):
        ruta = R / m.group(1).lstrip("/")
        h = hashlib.md5(ruta.read_bytes()).hexdigest()[:8] if ruta.exists() else "0"
        return f'src="{m.group(1)}?v={h}"'
    return _re.sub(r'src="(/img/[^"?]+)"', f, html_txt)

def escribir(ruta, contenido):
    contenido = con_version(contenido)
    p = R / ruta.strip("/") / "index.html" if ruta != "/" else R / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(contenido, encoding="utf-8")
    print("escrito", p.relative_to(R))

# ---------------------------------------------------------------- Inicio
escribir("/", cabeza("Ruvï · Herramientas para preparar oposiciones",
  "Ruvï crea herramientas digitales para academias de oposiciones. Nuestro primer proyecto: Plantilla de Repaso, tests de Policía Nacional para los alumnos de tu academia.", "/")
+ menu("/") + f'''
<main>
<section><div class="in dos" id="hero">
  <div class="stack">
    <span class="eb">Ruvï</span>
    <h1>Herramientas digitales para <mark>preparar oposiciones</mark></h1>
    <p class="lead">Hacemos el trabajo pesado para que las academias se centren en enseñar y sus alumnos en aprobar.</p>
    <p class="lead">Preguntas hechas por opositores, con el formato y el nivel de los exámenes oficiales de la División.</p>
    <div class="btns"><a class="btn p" href="/plantilla-repaso/">Conoce Plantilla de Repaso</a><a class="btn s" href="#contacto">Hablemos</a></div>
  </div>
  <div style="display:flex;justify-content:center"><div class="movil"><img src="/img/app-pregunta.png" alt="Una pregunta tipo test de Plantilla de Repaso en el móvil, con tres opciones y el cronómetro" width="390" height="696"></div></div>
</div></section>

<section id="proyectos" style="padding-top:0"><div class="in stack">
  <span class="eb">Proyectos</span>
  <h2>Lo que hacemos</h2>
  <a class="card proy" href="/plantilla-repaso/" style="text-decoration:none;color:inherit">
    <div class="stack" style="gap:12px">
      <span class="eb" style="color:var(--muted)">Para academias de Policía Nacional</span>
      <h3 style="font-size:1.7rem">Plantilla de Repaso</h3>
      <p class="lema" style="font-size:1.15rem">Tu temario, convertido en examen.</p>
      <p class="muted">Tests tipo examen de vuestros temas, listos para vuestros alumnos en una app. Preparamos las preguntas a partir del BOE o de vuestro temario, vuestros profesores las revisan y los alumnos practican con corrección al momento.</p>
      <span style="color:var(--accent);font-weight:700">Ver el proyecto →</span>
    </div>
    <img src="/img/ruvi-monograma.png" alt="" width="96" height="96" style="width:96px;height:96px" class="opc-img">
  </a>
</div></section>

<section class="banda" id="nosotros"><div class="in grid2" style="align-items:start">
  <div class="stack"><span class="eb">Quiénes somos</span><h2>Dos socios, una marca</h2><img src="/img/ruvi-logo-oscuro.png" alt="Logotipo de Ruvï" width="600" height="418" style="width:220px;height:auto;margin-top:12px"></div>
  <div class="stack">
    <p>Ruvï es la marca con la que dos socios lanzamos nuestros proyectos. Empezamos por lo que conocemos desde dentro: preparar una oposición.</p>
    <p class="muted">Plantilla de Repaso nació de opositar a Policía Nacional y de echar en falta tests que se parecieran de verdad al examen: tres opciones, penalización por fallo, cronómetro y la ley a mano para entender cada error.</p>
  </div>
</div></section>

<section id="contacto"><div class="in stack" style="max-width:760px;margin-inline:auto;text-align:left">
  <span class="eb">Contacto</span>
  <h2>¿Tienes una academia? Te enseñamos la app en 15 minutos</h2>
  <p class="lead">Escríbenos y te proponemos una videollamada corta para verla con tus propios temas. El primer mes es gratis.</p>
  {correo_bloque()}
</div></section>
</main>''' + PIE)

# ---------------------------------------------------------------- Plantilla de Repaso
escribir("/plantilla-repaso/", cabeza("Plantilla de Repaso · Tu temario, convertido en examen",
  "Tests tipo examen de Policía Nacional para los alumnos de tu academia: preguntas del BOE o de tu temario, revisadas por tus profesores, con corrección y la ley en cada pregunta.", "/plantilla-repaso/")
+ menu("/plantilla-repaso/") + f'''
<main>
<section><div class="in dos" id="hero">
  <div class="stack">
    <span class="eb">Plantilla de Repaso · Policía Nacional</span>
    <p class="lema">Tu temario, convertido en examen.</p>
    <h1>Tests tipo examen para los alumnos de <mark>tu academia</mark></h1>
    <p class="lead">Preparamos las preguntas de vuestros temas, a partir del BOE o de vuestro propio temario, y vuestros alumnos practican en una app con corrección al momento. Vuestros profesores dedican el tiempo a dar clase, no a hacer tests.</p>
    <div class="btns"><a class="btn p" href="#contacto">Pide una demo</a><a class="btn s" href="{APP}">Entrar en la app</a></div>
    <p class="muted" style="font-size:.95rem">Primer mes gratis y sin permanencia.</p>
  </div>
  <div style="display:flex;justify-content:center"><div class="movil"><img src="/img/app-inicio.png" alt="Pantalla de inicio del alumno: su última nota, preguntas realizadas, fallos por repasar y botón para empezar un test" width="390" height="820"></div></div>
</div></section>

<section style="padding-top:0"><div class="in grid2">
  <div class="card stack"><span class="eb">El problema</span><h3>Hacer buenas preguntas lleva horas</h3><p class="muted">Cada tema necesita decenas de preguntas bien hechas, con opciones trampa creíbles y al día con la ley. Ese tiempo sale de las clases.</p></div>
  <div class="card stack"><span class="eb">La solución</span><h3>Os las damos hechas y en una app</h3><p class="muted">100 preguntas por tema, revisadas por vuestros profesores antes de llegar a los alumnos, y una app para practicar como el día del examen.</p></div>
</div></section>

<section class="banda"><div class="in dos inv">
  <div style="display:flex;justify-content:center"><div class="movil"><img src="/img/app-resultado.png" alt="Resultado de un test: la nota sobre 10, aciertos, errores y preguntas en blanco, y la cuenta de cómo se calcula" width="390" height="484"></div></div>
  <div class="stack">
    <span class="eb">Qué incluye</span>
    <h2>Practicar como en el examen y entender cada fallo</h2>
    <ul class="lista">
      <li>Tests por tema con tres opciones, −0,5 por fallo y cronómetro, como el examen real</li>
      <li>Corrección con el artículo literal de la ley en cada pregunta</li>
      <li>Botón «Dudo» para saber si compensa arriesgar</li>
      <li>Mi cuaderno: los fallos y las preguntas sin contestar de cada test, para repasarlos</li>
      <li>Plan semanal de la academia y las preguntas más falladas, según el pack</li>
      <li>Panel para que la academia dé de alta y de baja a sus alumnos</li>
      <li>Funciona en el móvil y en el ordenador, sin instalar nada</li>
    </ul>
  </div>
</div></section>

<section><div class="in stack">
  <span class="eb">Calidad</span>
  <h2>Preguntas que se parecen al examen</h2>
  <div class="grid3">
    <div class="card stack"><h3>De la ley o de vuestro temario</h3><p class="muted">Salen del texto vigente del BOE o del temario que nos paséis, que solo se usa para vuestra academia.</p></div>
    <div class="card stack"><h3>Revisadas por vuestros profesores</h3><p class="muted">Antes de cada entrega, el profesor recibe un PDF para marcar cada pregunta como Vale, Cambiar o Quitar.</p></div>
    <div class="card stack"><h3>Siempre al día</h3><p class="muted">Si cambia una ley, avisamos y corregimos las preguntas afectadas. Los alumnos pueden avisar de un error desde la propia pregunta.</p></div>
  </div>
</div></section>

<section style="padding-top:0"><div class="in stack">
  <span class="eb">Cómo funciona</span>
  <h2>En marcha en tres pasos</h2>
  <div class="grid3">
    <div class="card stack"><span class="eb" style="font-size:1.6rem;font-family:var(--f-num);letter-spacing:0">1</span><h3>Hablamos</h3><p class="muted">Una videollamada corta: vemos la app y elegís los temas para empezar.</p></div>
    <div class="card stack"><span class="eb" style="font-size:1.6rem;font-family:var(--f-num);letter-spacing:0">2</span><h3>Preparamos vuestro espacio</h3><p class="muted">Hacemos las preguntas, las revisáis y las cargamos en vuestra academia.</p></div>
    <div class="card stack"><span class="eb" style="font-size:1.6rem;font-family:var(--f-num);letter-spacing:0">3</span><h3>Vuestros alumnos entran</h3><p class="muted">Les damos de alta con su email y empiezan a practicar desde el móvil.</p></div>
  </div>
</div></section>

<section style="padding-top:0"><div class="in grid2" style="align-items:start">
  <div class="stack"><span class="eb">Packs</span><h2>Tests, Plus o Completo</h2><p class="lead">Una cuota mensual según el número de alumnos, con el precio por alumno a la vista. El primer mes es gratis y no hay permanencia.</p><div class="btns"><a class="btn p" href="#contacto">Pide las tarifas</a></div></div>
  <div class="card stack" style="gap:14px">
    <div><b>Tests</b><p class="muted">Tests tipo examen, corrección con la ley, «Dudo» y Mi cuaderno.</p></div>
    <div><b>Plus</b><p class="muted">Todo lo anterior, más el plan semanal de la academia y las preguntas más falladas de vuestro grupo.</p></div>
    <div><b>Completo</b><p class="muted">Todo lo anterior, más el ranking de la academia y las pruebas físicas con su evolución.</p></div>
  </div>
</div></section>

<section style="padding-top:0"><div class="in stack" style="max-width:820px">
  <span class="eb">Preguntas frecuentes</span>
  <h2>Lo que suelen preguntarnos</h2>
  <details class="card"><summary><b>¿Funciona en el móvil?</b></summary><p class="muted" style="margin-top:10px">Sí. Se abre desde el navegador del móvil o del ordenador y se puede añadir a la pantalla de inicio. No hay que descargar nada de ninguna tienda.</p></details>
  <details class="card"><summary><b>¿Qué datos se guardan de los alumnos?</b></summary><p class="muted" style="margin-top:10px">Su nombre, su email y su progreso en la app. La academia decide sobre esos datos y firmamos con ella un contrato de protección de datos. Están alojados en la Unión Europea y cada academia solo ve los suyos.</p></details>
  <details class="card"><summary><b>¿Y si una pregunta tiene un error?</b></summary><p class="muted" style="margin-top:10px">Cada pregunta tiene un botón para avisar. Lo revisamos y la corregimos para todos los alumnos.</p></details>
  <details class="card"><summary><b>¿Nuestro temario se usa para otras academias?</b></summary><p class="muted" style="margin-top:10px">No. Vuestro temario y las preguntas hechas con él son solo vuestros.</p></details>
</div></section>

<section class="banda" id="contacto"><div class="in stack" style="max-width:820px">
  <span class="eb">Prueba un mes gratis</span>
  <h2>Te enseñamos la app con tus propios temas</h2>
  <p class="muted" style="font-size:1.1rem">Escríbenos y te proponemos una videollamada de 15 minutos. Si ya sois clientes, entrad desde el botón «Entrar en la app».</p>
  {correo_bloque()}
  <div class="btns"><a class="btn s" href="{APP}">Entrar en la app</a></div>
</div></section>
</main>''' + PIE)

# ---------------------------------------------------------------- Aviso legal
TITULAR = "Alejandro Ruiz Barreda"
escribir("/aviso-legal/", cabeza("Aviso legal · Ruvï", "Datos del titular de ruvilab.es y condiciones de uso de la web.", "/aviso-legal/")
+ menu("") + f'''
<main><section><div class="in legal stack">
<span class="eb">Legal</span><h1 style="font-size:2.2rem">Aviso legal</h1>
<p class="muted">Última actualización: 22 de octubre de 2026</p>
<h2>Titular de la web</h2>
<p>En cumplimiento del artículo 10 de la Ley 34/2002, de servicios de la sociedad de la información (LSSI), el titular de ruvilab.es es <b>{TITULAR}</b>, con NIF 49236511C y domicilio en C/ Gustavo Adolfo Bécquer, 25, 21122 Huelva (España). Contacto: <a href="mailto:{CORREO}">{CORREO}</a>.</p>
<p>Ruvï es una marca comercial; Plantilla de Repaso es un producto de Ruvï.</p>
<h2>Uso de la web</h2>
<p>Esta web informa sobre los productos de Ruvï. Quien la visita se compromete a usarla de forma lícita y a no dañar su funcionamiento.</p>
<h2>Propiedad intelectual</h2>
<p>Los textos, el diseño, el logotipo y las imágenes de esta web pertenecen a su titular o se usan con permiso. No se pueden copiar ni reutilizar sin autorización. Las tipografías se usan bajo licencia SIL Open Font License.</p>
<h2>Enlaces</h2>
<p>Esta web enlaza a la aplicación Plantilla de Repaso, que tiene su propio <a href="{APP}/aviso-legal.html">aviso legal</a> y su propia <a href="{APP}/privacidad.html">política de privacidad</a>.</p>
<h2>Responsabilidad</h2>
<p>Procuramos que la información sea correcta y esté al día, pero puede contener errores o cambiar sin aviso. Los precios y condiciones que valen son los que se acuerdan por escrito con cada academia.</p>
<h2>Ley aplicable</h2>
<p>Se aplica la ley española.</p>
</div></section></main>''' + PIE)

# ---------------------------------------------------------------- Privacidad y cookies
escribir("/privacidad/", cabeza("Privacidad y cookies · Ruvï", "Cómo trata Ruvï los datos de quien visita ruvilab.es o le escribe. Sin cookies ni analíticas.", "/privacidad/")
+ menu("") + f'''
<main><section><div class="in legal stack">
<span class="eb">Legal</span><h1 style="font-size:2.2rem">Privacidad y cookies</h1>
<p class="muted">Última actualización: 22 de octubre de 2026</p>
<p class="card"><b>En pocas palabras:</b> esta web no usa cookies, ni analíticas, ni publicidad, y no tiene formularios. Solo tratamos tus datos si nos escribes o nos llamas, y solo para contestarte.</p>
<h2>Responsable</h2>
<p>{TITULAR}, NIF 49236511C, C/ Gustavo Adolfo Bécquer, 25, 21122 Huelva. Contacto para privacidad: <a href="mailto:privacidad@ruvilab.es">privacidad@ruvilab.es</a>.</p>
<h2>Qué datos tratamos y para qué</h2>
<ul>
<li><b>Si nos escribes</b> a {CORREO}, por WhatsApp o nos llamas: tu nombre, tu email, el nombre de tu academia y lo que nos cuentes. Los usamos para contestarte y, si lo pides, para enseñarte la app y prepararte un presupuesto. Base legal: tu petición y las medidas previas a un contrato (artículo 6.1.b del RGPD).</li>
<li><b>Al visitar la web</b>: el proveedor que la aloja registra datos técnicos, como tu dirección IP y la hora, para servirla y por seguridad. No los usamos para nada más.</li>
</ul>
<h2>Cuánto tiempo</h2>
<p>Los correos se guardan mientras dure la conversación y, si llegas a ser cliente, mientras dure la relación y los plazos que exige la ley. Si no, los borramos como máximo un año después del último contacto.</p>
<h2>Quién más interviene</h2>
<div class="tw"><table>
<tr><th>Proveedor</th><th>Para qué</th><th>Dónde</th></tr>
<tr><td>GitHub (Microsoft)</td><td>Alojamiento de la web</td><td>Estados Unidos</td></tr>
<tr><td>ImprovMX</td><td>Reenvío de los correos que nos mandas</td><td>Estados Unidos</td></tr>
<tr><td>Google (Gmail)</td><td>Buzón donde leemos y contestamos los correos</td><td>Unión Europea y Estados Unidos</td></tr>
<tr><td>WhatsApp (Meta)</td><td>Mensajes si nos escribes por WhatsApp</td><td>Unión Europea y Estados Unidos</td></tr>
</table></div>
<p>Las transferencias fuera de la Unión Europea se amparan en el Marco de Privacidad de Datos UE-EE. UU. o en las cláusulas contractuales tipo de la Comisión Europea. No vendemos ni cedemos tus datos a nadie.</p>
<h2>Tus derechos</h2>
<p>Puedes pedir acceder a tus datos, corregirlos, borrarlos, limitar su uso, oponerte o llevártelos escribiendo a <a href="mailto:privacidad@ruvilab.es">privacidad@ruvilab.es</a>. Si crees que no los respetamos, puedes reclamar ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es" rel="noopener">www.aepd.es</a>).</p>
<h2>Cookies</h2>
<p>Esta web no instala cookies ni usa herramientas de analítica o publicidad. Las letras y las imágenes se cargan desde la propia web, sin pedir nada a otros servicios. Por eso no verás ningún aviso de cookies.</p>
<h2>La app Plantilla de Repaso</h2>
<p>Los datos de los alumnos dentro de la app se rigen por su propia <a href="{APP}/privacidad.html">política de privacidad</a>.</p>
</div></section></main>''' + PIE)

# ---------------------------------------------------------------- 404
(R / "404.html").write_text(cabeza("Página no encontrada · Ruvï", "Esta página no existe.", "/404", noindex=True) + menu("") + '''
<main><section><div class="in stack" style="max-width:640px">
<span class="eb">Error 404</span><h1 style="font-size:2.4rem">Esta página no existe</h1>
<p class="lead">Puede que el enlace esté mal escrito o que la página se haya movido.</p>
<div class="btns"><a class="btn p" href="/">Ir al inicio</a></div>
</div></section></main>''' + PIE, encoding="utf-8")
print("escrito 404.html")

# ---------------------------------------------------------------- Tarifas (página aparte, solo para quien tenga el enlace)
t = (R / "_fuentes" / "tarifas.html").read_text(encoding="utf-8")
import re
t = re.sub(r'<link rel="preconnect"[^>]*>\s*', '', t)
t = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>', '<link rel="stylesheet" href="/fuentes/fuentes.css">', t)
t = t.replace('<meta name="claude:viewport-fit-sides" content="cover">', '')
t = re.sub(r'<img src="data:image/jpeg;base64,[^"]*" alt="Logo de Ruvï">', '<img src="/img/ruvi-monograma.png" alt="Logo de Ruvï" width="44" height="44">', t)
t = t.replace('.brand img{width:48px;height:48px;border-radius:50%;object-fit:cover;border:1px solid var(--line);box-shadow:0 4px 14px -8px var(--cobre-2);flex:none}', '.brand img{width:44px;height:44px;object-fit:contain;flex:none}')
t = t.replace('<div class="brand">', '<a class="brand" href="/" style="text-decoration:none;color:inherit">', 1)
t = t.replace('· Plantilla de Repaso</span></span></div>', '· Plantilla de Repaso</span></span></a>', 1)
t = t.replace('<span>Escríbenos: <b>hola@ruvilab.es</b></span>', '<span>Escríbenos: <b>hola@ruvilab.es</b> · <a href="/aviso-legal/" style="color:inherit">Aviso legal</a> · <a href="/privacidad/" style="color:inherit">Privacidad</a></span>')
assert 'base64' not in t and 'googleapis' not in t
t = ('<!doctype html>\n<html lang="es"><head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
     '<meta name="robots" content="noindex">\n<meta name="description" content="Tarifas de Plantilla de Repaso para academias, con calculadora de cuota.">\n'
     '<link rel="icon" type="image/png" href="/img/favicon.png">\n' + t.replace('</style>', 'body{margin:0}\n</style>\n</head><body>', 1) + '\n</body></html>')
escribir("/tarifas/", t)
