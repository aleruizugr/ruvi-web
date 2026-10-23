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
    items = [("/plantilla-repaso/", "Plantilla de Repaso", "opc"), ("/#contacto", "Contacto", ""), (APP, "Entrar", "entrar")]
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
(function(){{var b=document.getElementById("demoBtn"),c=document.getElementById("demoBox"),x=document.getElementById("demoCerrar");if(!b||!c)return;
  var vs=c.querySelectorAll("video"),cual=function(){{return matchMedia("(max-width:820px)").matches?vs[1]:vs[0]}};
  var abrir=function(){{c.hidden=false;b.setAttribute("aria-expanded","true");b.textContent="Ocultar la demo";c.scrollIntoView({{behavior:"smooth",block:"start"}});var p=cual().play();if(p&&p.catch)p.catch(function(){{}})}};
  var cerrar=function(){{vs.forEach(function(v){{v.pause();try{{v.currentTime=0}}catch(e){{}}}});c.hidden=true;b.setAttribute("aria-expanded","false");b.textContent="Ver la demo en un minuto →";document.getElementById("hero").scrollIntoView({{behavior:"smooth",block:"start"}})}};
  b.addEventListener("click",function(){{c.hidden?abrir():cerrar()}});
  x.addEventListener("click",cerrar);
  // al terminar, deja a la vista el botón para quitar el vídeo
  vs.forEach(function(v){{v.addEventListener("ended",function(){{x.classList.add("fin");x.scrollIntoView({{behavior:"smooth",block:"center"}});x.focus({{preventScroll:true}})}});v.addEventListener("play",function(){{x.classList.remove("fin")}})}});
}})();
</script>
</body></html>'''

TELEFONO = "669 767 570"
WHATSAPP = "34669767570"
from urllib.parse import quote
ASUNTO = "Plantilla de Repaso para nuestra academia"
CUERPO = ("Hola:\n\nNos interesa Plantilla de Repaso y nos gustaría verla con los temas de nuestra academia.\n\n"
          "Academia: \nCiudad: \nNúmero de alumnos: \nTeléfono de contacto: \n"
          "Mejor día y hora para la videollamada: \n\nGracias.")
WA_TEXTO = "Hola, os escribo desde ruvilab.es. Me interesa Plantilla de Repaso y me gustaría verla con los temas de mi academia."

def correo_bloque():
    mailto = f"mailto:{CORREO}?subject={quote(ASUNTO)}&body={quote(CUERPO)}"
    wa = f"https://wa.me/{WHATSAPP}?text={quote(WA_TEXTO)}"
    return f'''<div class="btns">
    <a class="btn p" href="{mailto}">Escribir un correo</a>
    <a class="btn wa" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
  </div>
  <p class="muted">{CORREO} · <span style="white-space:nowrap">{TELEFONO}</span></p>'''

def con_version(html_txt):
    # añade ?v=<huella> a las imágenes de /img/, para que el navegador no muestre una versión vieja
    import re as _re
    def f(m):
        ruta = R / m.group(2).lstrip("/")
        h = hashlib.md5(ruta.read_bytes()).hexdigest()[:8] if ruta.exists() else "0"
        return f'{m.group(1)}="{m.group(2)}?v={h}"'
    return _re.sub(r'(src|poster)="(/(?:img|video)/[^"?]+)"', f, html_txt)

def escribir(ruta, contenido):
    contenido = con_version(contenido)
    p = R / ruta.strip("/") / "index.html" if ruta != "/" else R / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(contenido, encoding="utf-8")
    print("escrito", p.relative_to(R))

# ---------------------------------------------------------------- Inicio
escribir("/", cabeza("Ruvï · Herramientas para preparar oposiciones",
  "Ruvï crea herramientas para academias de oposiciones. Primer producto: Plantilla de Repaso, tests tipo examen para Policía Nacional y cualquier oposición tipo test.", "/")
+ menu("/") + f'''
<main>
<section><div class="in dos" id="hero">
  <div class="stack">
    <h1>Herramientas para <mark>preparar oposiciones</mark></h1>
    <p class="lead">Nuestro primer producto: Plantilla de Repaso, tests tipo examen para academias. Nació para Policía Nacional y se adapta a cualquier oposición con examen tipo test.</p>
    <div class="btns"><a class="btn p" href="/plantilla-repaso/">Ver Plantilla de Repaso</a></div>
    <p style="font-size:.95rem;margin:0"><button class="enlace-demo" type="button" id="demoBtn" aria-expanded="false" aria-controls="demoBox">Ver la demo en un minuto →</button></p>
  </div>
  <div style="display:flex;justify-content:center"><div class="movil"><img src="/img/app-pregunta.png" alt="Una pregunta tipo test de Plantilla de Repaso en el móvil, con tres opciones, el cronómetro y los botones Dudo y Dejar en blanco" width="390" height="700"></div></div>
</div>
<div class="in" id="demoBox" hidden>
  <div class="video">
    <video class="v-ancho" controls playsinline preload="none" poster="/img/demo-horizontal.jpg" width="1280" height="720" aria-label="Demo de Plantilla de Repaso en vídeo horizontal"><source src="/video/demo-horizontal.mp4" type="video/mp4"></video>
    <video class="v-movil" controls playsinline preload="none" poster="/img/demo-vertical.jpg" width="720" height="1280" aria-label="Demo de Plantilla de Repaso en vídeo vertical"><source src="/video/demo-vertical.mp4" type="video/mp4"></video>
  </div>
  <div class="demo-pie"><button class="demo-cerrar" type="button" id="demoCerrar">Cerrar vídeo</button></div>
</div></section>

<section id="nosotros" style="padding-top:0"><div class="in stack" style="max-width:760px">
  <h2>Quiénes somos</h2>
  <p class="lead">Soy Alejandro, opositor a Policía Nacional. Creé Plantilla de Repaso al echar en falta tests que se parecieran de verdad al examen. Junto a mi socio, miembro de las Fuerzas y Cuerpos de Seguridad del Estado que también pasó por la oposición, fundamos Ruvï.</p>
</div></section>

<section class="banda" id="contacto"><div class="in stack" style="max-width:760px">
  <h2>¿Tienes una academia?</h2>
  <p class="lead">Te enseñamos la app con tus temas en 15 minutos. El primer mes es gratis.</p>
  {correo_bloque()}
</div></section>
</main>''' + PIE)

# ---------------------------------------------------------------- Plantilla de Repaso
escribir("/plantilla-repaso/", cabeza("Plantilla de Repaso · Tu temario, convertido en examen",
  "Tests tipo examen para tu academia, de Policía Nacional o cualquier oposición tipo test: preguntas de tus temas, revisadas por tus profesores, con corrección con la ley.", "/plantilla-repaso/")
+ menu("/plantilla-repaso/") + f'''
<main>
<section><div class="in dos" id="hero">
  <div class="stack">
    <h1>Tu temario, <mark>convertido en examen</mark></h1>
    <p class="lead">Hacemos las preguntas de vuestros temas. Vuestros alumnos practican en una app, como el día del examen.</p>
    <p class="muted">Nació para Policía Nacional. Se adapta a cualquier oposición con examen tipo test.</p>
    <div class="btns"><a class="btn p" href="#contacto">Pruébala con tus temas</a></div>
    <p class="muted" style="font-size:.95rem">Primer mes gratis. Sin permanencia.</p>
  </div>
  <div style="display:flex;justify-content:center"><div class="movil"><img src="/img/app-inicio.png" alt="Pantalla de inicio del alumno: aviso de fallos por repasar, su última nota, preguntas hechas, y la elección de tema, número de preguntas y corrección para empezar un test" width="390" height="844"></div></div>
</div></section>

<section class="banda"><div class="in dos inv">
  <div style="display:flex;justify-content:center"><div class="movil"><img src="/img/app-resultado.png" alt="Resultado de un test: un 7 sobre 10, aciertos, errores y preguntas en blanco, la cuenta como en el examen y cuántos puntos le ha sumado arriesgar en las preguntas que dudaba" width="390" height="748"></div></div>
  <div class="stack">
    <h2>Como el examen real</h2>
    <ul class="lista">
      <li>Tres opciones, −0,5 por fallo y cronómetro</li>
      <li>Cada fallo, corregido con el artículo de la ley</li>
      <li>«Dudo»: saber si compensa arriesgar</li>
      <li>Cuaderno con los fallos para repasar</li>
      <li>En el móvil o el ordenador, sin instalar nada</li>
    </ul>
  </div>
</div></section>

<section><div class="in stack">
  <h2>Cómo funciona</h2>
  <div class="grid3">
    <div class="card stack" style="gap:8px"><span class="num">1</span><h3>Elegís los temas</h3><p class="muted">Preguntas del BOE o de vuestro temario, que es solo vuestro.</p></div>
    <div class="card stack" style="gap:8px"><span class="num">2</span><h3>Vuestros profesores las revisan</h3><p class="muted">Ninguna llega a los alumnos sin su visto bueno.</p></div>
    <div class="card stack" style="gap:8px"><span class="num">3</span><h3>Los alumnos practican</h3><p class="muted">Les damos de alta con su email y empiezan.</p></div>
  </div>
</div></section>

<section style="padding-top:0"><div class="in grid2" style="align-items:start">
  <div class="stack"><h2>Tres packs</h2><p class="lead">Precio según el número de alumnos.</p><div class="btns"><a class="btn s" href="#contacto">Pide las tarifas</a></div></div>
  <div class="card stack" style="gap:12px">
    <p><b>Tests</b> <span class="muted">· tests, corrección y cuaderno</span></p>
    <p><b>Plus</b> <span class="muted">· + plan semanal y preguntas más falladas</span></p>
    <p><b>Completo</b> <span class="muted">· + ranking y pruebas físicas</span></p>
  </div>
</div></section>

<section style="padding-top:0"><div class="in stack" style="max-width:820px">
  <h2>Preguntas frecuentes</h2>
  <details class="card"><summary><b>¿Sirve para otras oposiciones?</b></summary><p class="muted" style="margin-top:10px">Sí. Adaptamos el temario, el número de opciones, la penalización y el tiempo al examen de cada oposición tipo test.</p></details>
  <details class="card"><summary><b>¿Qué datos se guardan de los alumnos?</b></summary><p class="muted" style="margin-top:10px">Nombre, email y progreso, en la Unión Europea. Cada academia solo ve los suyos y firmamos un contrato de protección de datos.</p></details>
  <details class="card"><summary><b>¿Y si una pregunta tiene un error?</b></summary><p class="muted" style="margin-top:10px">Los alumnos avisan desde la propia pregunta y la corregimos para todos.</p></details>
  <details class="card"><summary><b>¿Nuestro temario se usa para otras academias?</b></summary><p class="muted" style="margin-top:10px">No. El temario y sus preguntas son solo vuestros.</p></details>
</div></section>

<section class="banda" id="contacto"><div class="in stack" style="max-width:760px">
  <h2>Pruébala un mes gratis</h2>
  <p class="lead">Te la enseñamos con tus temas en una videollamada de 15 minutos.</p>
  {correo_bloque()}
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
