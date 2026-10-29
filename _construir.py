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

def menu(actual, app=None):
    # «Entrar» lleva a la app de cada producto: en la página de Dos Décimas, a Dos Décimas; en el resto, a Plantilla de Repaso
    items = [("/plantilla-repaso/", "Plantilla de Repaso", "opc"), ("/#contacto", "Contacto", ""), (app or APP, "Entrar", "entrar")]
    actual_attr = ' aria-current="page"'   # fuera del f-string: así funciona también con Python anterior al 3.12
    links = "".join(f'<a href="{h}" class="{c}"{actual_attr if h == actual else ""}>{t}</a>' for h, t, c in items)
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
  <details class="card"><summary><b>¿Podemos probarla con nuestro temario?</b></summary><p class="muted" style="margin-top:10px">Durante el mes gratis practicáis con preguntas de vuestros temas sacadas del BOE, revisadas por vuestros profesores. Si os quedáis, preparamos las de vuestro propio temario.</p></details>
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

# ---------------------------------------------------------------- Dos Décimas: Plantilla de Repaso para opositores particulares (lista de espera)
# Fuera del menú a propósito: de momento se llega solo por enlace directo.
# La lista de espera guarda en la tabla «lista_espera» del Supabase de producción (ver _sql/lista_espera.sql).
# Mientras LISTA_ABIERTA sea False, el botón solo dice cuándo abre y la página no envía nada a ningún sitio.
# Para abrirla: aplicar antes el SQL en Supabase, poner True, ejecutar este guion y publicar.
LISTA_ABIERTA = False
SUPABASE_URL = "https://lolqvimwnlikytbsnvsn.supabase.co"
SUPABASE_CLAVE = "sb_publishable_JHbrAd6FUpp-js3O44kCjg_J6qPVFoL"   # clave pública por diseño (la misma de la app); la protección la pone el RLS
FECHAS_EXAMEN = [("2027", "En 2027"), ("mas_adelante", "Más adelante"), ("no_lo_se", "No lo sé")]
OK_LISTA = "Apuntado. Te avisamos por email cuando abra Dos Décimas, con los 45 temas listos."

def lista_js():
    if not LISTA_ABIERTA:
        return '''<script>
(function(){var f=document.getElementById("lista");if(!f)return;
  f.addEventListener("submit",function(e){e.preventDefault()});
})();
</script>'''
    return f'''<script>
(function(){{var f=document.getElementById("lista");if(!f)return;
  var b=f.querySelector("button[type=submit]"),m=document.getElementById("listaMsg"),t=b.textContent;
  var aviso=function(txt,ok){{m.textContent=txt;m.className="aviso "+(ok?"ok":"mal");m.hidden=false}};
  f.addEventListener("submit",function(e){{e.preventDefault();
    if(f.web.value){{aviso({OK_LISTA!r},true);return}}   // campo trampa: solo lo rellenan los robots
    if(!f.reportValidity())return;
    b.disabled=true;b.textContent="Enviando…";
    fetch("{SUPABASE_URL}/rest/v1/lista_espera",{{method:"POST",
      headers:{{"apikey":"{SUPABASE_CLAVE}","Content-Type":"application/json","Prefer":"return=minimal"}},
      body:JSON.stringify({{email:f.email.value.trim().toLowerCase(),fecha_examen:f.fecha.value,consentimiento:f.acepto.checked}})
    }}).then(function(r){{
      // 409 = ese email ya estaba apuntado: se contesta igual, para no desvelar quién está en la lista
      if(r.ok||r.status===409){{f.reset();aviso({OK_LISTA!r},true)}}
      else aviso("No se ha podido guardar. Prueba otra vez o escríbenos a {CORREO}.",false);
    }}).catch(function(){{aviso("No hay conexión. Prueba otra vez en un momento.",false)}})
    .then(function(){{b.disabled=false;b.textContent=t}});
  }});
}})();
</script>'''

def lista_form():
    opciones = "".join(f'<label class="opcion"><input type="radio" name="fecha" value="{v}" required> {t}</label>' for v, t in FECHAS_EXAMEN)
    boton = ('<button class="btn p" type="submit">Apuntarme a la lista</button>' if LISTA_ABIERTA
             else '<button class="btn p" type="submit" disabled aria-describedby="listaCerrada">Abrimos la lista el 2 de noviembre</button>')
    cerrada = '' if LISTA_ABIERTA else '<p class="muted" id="listaCerrada" style="font-size:.95rem">Todavía no guardamos nada: el formulario se activa el 2 de noviembre.</p>'
    return f'''<form class="card stack form" id="lista" novalidate>
    <label class="campo"><b>Tu email</b>
      <input type="email" name="email" required maxlength="254" autocomplete="email" inputmode="email" placeholder="tu@email.com"></label>
    <fieldset class="campo"><legend><b>¿Cuándo te examinas?</b></legend><div class="opciones">{opciones}</div></fieldset>
    <label class="trampa" aria-hidden="true">No rellenar <input type="text" name="web" tabindex="-1" autocomplete="off"></label>
    <label class="casilla"><input type="checkbox" name="acepto" required>
      <span>He leído la <a href="/privacidad/#lista-espera">política de privacidad</a> y acepto que Ruvï guarde mi email para avisarme cuando abra Dos Décimas.</span></label>
    <div class="btns">{boton}</div>
    {cerrada}
    <p id="listaMsg" class="aviso" role="status" hidden></p>
  </form>'''

# Avance del temario: cambiar TEMAS_LISTOS cada vez que se publique un tema nuevo (van en orden, del 1 al 45).
TEMAS_LISTOS = 26
BLOQUES_TEMARIO = [("Ciencias Jurídicas", 1, 26), ("Ciencias Sociales", 27, 37), ("Técnico-Científicas", 38, 45)]

def avance_temas():
    filas = ""
    for nombre, a, b in BLOQUES_TEMARIO:
        total, listos = b - a + 1, max(0, min(TEMAS_LISTOS, b) - a + 1)
        filas += f'''<div class="bloque">
      <div class="bloque-cab"><b>{nombre}</b><span class="muted">temas {a}-{b} · <span class="num-p">{listos}/{total}</span></span></div>
      <div class="barra" role="img" aria-label="{nombre}: {listos} de {total} temas disponibles"><i style="width:{round(listos / total * 100)}%"></i></div>
    </div>'''
    return filas

# ---------- Venta de Dos Décimas ----------
# Tarifas (IVA incluido) y su enlace de pago de Stripe.
# Enlaces de pago REALES de Stripe (modo activo, creados el 29-10-2026): cobran dinero de verdad.
DD_CORREO = "dosdecimas@ruvilab.es"
DD_APP = "https://dosdecimas.ruvilab.es"
TARIFA_FUNDADOR = dict(nombre="Fundador", precio="7,99 €", periodo="al mes", plazas=30,
  enlace="https://buy.stripe.com/3cIcN7bck9DibmO7Vx04801")
TARIFAS_DD = [
  dict(nombre="Mensual", precio="10,99 €", periodo="al mes", al_mes=None, ahorro=None,
       enlace="https://buy.stripe.com/cNi28tbckbLq9eGfnZ04800", nota="Se renueva cada mes. Sin permanencia."),
  dict(nombre="Trimestre", precio="29,99 €", periodo="cada 3 meses", al_mes="9,99 €", ahorro="−9 %",
       enlace="https://buy.stripe.com/aFafZjfsA4iY9eG0t504802", nota="Se renueva cada 3 meses. Sin permanencia."),
  dict(nombre="Semestre", precio="54,99 €", periodo="cada 6 meses", al_mes="9,17 €", ahorro="−17 %",
       enlace="https://buy.stripe.com/28E14peowdTy2QicbN04804", nota="Se renueva cada 6 meses. Sin permanencia."),
  dict(nombre="Curso completo", precio="89,99 €", periodo="pago único", al_mes="7,50 €", ahorro="−32 %", destacada=True,
       enlace="https://buy.stripe.com/28E9AV2FO16McqS1x904803", nota="Hasta el 31 de octubre de 2027. No se renueva."),
]
if any("/test_" in t["enlace"] for t in TARIFAS_DD + [TARIFA_FUNDADOR]):
    print("AVISO: la página de Dos Décimas lleva enlaces de pago de PRUEBA de Stripe. Cámbialos por los de modo activo antes de publicar.")

def tarifas_dd():
    tarjetas = "".join(f"""<div class="card tarifa{' dest' if t.get('destacada') else ''}">
      <div class="tarifa-cab"><h3>{t['nombre']}</h3>{f'<span class="chip">{t["ahorro"]}</span>' if t['ahorro'] else ''}</div>
      <p class="precio"><span class="num">{t['precio']}</span> {t['periodo']}</p>
      <p class="muted">{f"Sale a {t['al_mes']} al mes. " if t['al_mes'] else ''}{t['nota']}</p>
      <a class="btn {'p' if t.get('destacada') else 's'}" href="{t['enlace']}" rel="noopener">Elegir {t['nombre'].lower()}</a>
    </div>""" for t in TARIFAS_DD)
    f = TARIFA_FUNDADOR
    return f"""<div class="card fundador">
    <div class="stack" style="gap:8px">
      <span class="eb">Precio fundador · solo {f['plazas']} plazas</span>
      <p class="precio"><span class="num">{f['precio']}</span> {f['periodo']}, para siempre mientras sigas suscrito</p>
      <p class="muted">Después, 10,99 € al mes. Si te das de baja y vuelves, pagas el precio de entonces.</p>
    </div>
    <a class="btn p" href="{f['enlace']}" rel="noopener">Quiero el precio fundador</a>
  </div>
  <div class="tarifas">{tarjetas}</div>"""

FAQ_DD = [
  ("¿Cómo entro después de pagar?", f"Entra en {DD_APP.replace('https://', '')}, pulsa «Primera vez» y escribe el mismo email con el que has pagado. Te llega un correo para crear tu contraseña y ya está."),
  ("¿Están actualizadas a la ley vigente?", "Sí: cada pregunta se comprueba con la ley vigente del BOE antes de publicarse. Si una ley cambia o ves un error, avisas desde la propia pregunta y la corregimos para todos."),
  ("¿Funciona en el móvil?", "Sí. Se abre en el navegador del móvil o del ordenador y puedes añadirla a la pantalla de inicio como una app, sin pasar por ninguna tienda."),
  ("¿Puedo darme de baja cuando quiera?", "Sí, sin permanencia. Mantienes el acceso hasta el final de lo que ya pagaste. El curso completo es un pago único y no se renueva."),
  ("¿Y si no me convence?", f"Tienes 14 días para desistir y te devolvemos todo, aunque ya la hayas usado. Basta con escribir a {DD_CORREO}."),
]
FAQ_DD_HTML = "".join(f'<details class="card"><summary><b>{q}</b></summary><p class="muted" style="margin-top:10px">{r}</p></details>' for q, r in FAQ_DD)

escribir("/dos-decimas/", cabeza("Dos Décimas · Tests de Policía Nacional",
  "Dos Décimas: tests de Policía Nacional (Escala Básica) a nivel de examen, comprobados con la ley vigente del BOE. Hechos por un opositor que se quedó a dos décimas del corte.", "/dos-decimas/")
+ menu("/dos-decimas/", DD_APP) + f"""
<main>
<section><div class="in dos" id="hero">
  <div class="stack">
    <span class="eb">Dos Décimas · Policía Nacional, Escala Básica</span>
    <h1>Me quedé fuera por <mark>dos décimas</mark>. Que a ti no te pase.</h1>
    <p class="lead">Las plazas se deciden por décimas, y casi nunca se pierden por no estudiar: se pierden en un plazo, en un «NO» que no leíste o en una duda que arriesgaste. Dos Décimas te enseña dónde se te escapan las tuyas.</p>
    <div class="btns"><a class="btn p" href="#precio">Ver tarifas</a><a class="btn s" href="{DD_APP}">Ya tengo cuenta: entrar</a></div>
    <p class="muted" style="font-size:.95rem">Preguntas comprobadas con el BOE vigente por un opositor que se quedó a dos décimas del corte. Desde 7,99 € al mes, sin permanencia.</p>
  </div>
  <div style="display:flex;justify-content:center"><div class="movil"><img src="/img/app-pregunta.png" alt="Una pregunta tipo test en el móvil, con tres opciones, el cronómetro y los botones Dudo y Dejar en blanco" width="390" height="700"></div></div>
</div></section>

<section style="padding-top:0"><div class="in stack" style="max-width:960px">
  <h2>Dos Décimas en 30 segundos</h2>
  <div class="video">
    <video class="v-ancho" controls playsinline preload="none" poster="/img/dosdecimas-horizontal.jpg" width="1280" height="720" aria-label="Vídeo de Dos Décimas en horizontal: una nota de 6,95 frente a un corte de 7,05 y lo que hace la app para que no te pase"><source src="/video/dosdecimas-horizontal.mp4" type="video/mp4"></video>
    <video class="v-movil" controls playsinline preload="none" poster="/img/dosdecimas-vertical.jpg" width="720" height="1280" aria-label="Vídeo de Dos Décimas en vertical: una nota de 6,95 frente a un corte de 7,05 y lo que hace la app para que no te pase"><source src="/video/dosdecimas-vertical.mp4" type="video/mp4"></video>
  </div>
</div></section>

<section class="banda"><div class="in dos inv">
  <div style="display:flex;justify-content:center"><div class="movil"><img src="/img/app-resultado.png" alt="Resultado de un test: un 7 sobre 10, aciertos, errores y preguntas en blanco, la cuenta como en el examen y cuántos puntos le ha sumado arriesgar en las preguntas que dudaba" width="390" height="748"></div></div>
  <div class="stack">
    <span class="eb">Lo que hay dentro</span>
    <h2>Para no regalar ni una décima</h2>
    <ul class="lista">
      <li><span><b>Mis trampas.</b> Plazos, números, «podrá» o «deberá»… La app te dice en qué trampa caes más y te hace un test solo de esa.</span></li>
      <li><span><b>Repaso de 5 minutos.</b> Cada día, las preguntas que fallaste o dudaste, justo cuando toca repasarlas.</span></li>
      <li><span><b>Arriesgar o dejar en blanco.</b> Marca «Dudo» y verás si contestar cuando no estás seguro te suma o te resta.</span></li>
      <li><span><b>12 exámenes oficiales</b> desde 2015, con la nota de corte de cada promoción.</span></li>
      <li><span><b>Como el examen:</b> tres opciones, −0,5 por fallo y cronómetro. Y una corrección que te explica por qué.</span></li>
    </ul>
  </div>
</div></section>

<section><div class="in stack" style="max-width:860px">
  <span class="eb">Cada fin de semana</span>
  <h2>Un simulacro como el día del examen</h2>
  <p class="lead">100 preguntas, 50 minutos y un solo intento. El domingo ves tu nota, la media y la nota de corte de todos los que lo han hecho, y si has superado el corte.</p>
  <div class="grid3 datos">
    <div><span class="num">Vie 14:00</span><p class="muted">Abre el viernes</p></div>
    <div><span class="num">Dom 21:00</span><p class="muted">Cierra el domingo</p></div>
    <div><span class="num">1</span><p class="muted">intento, como el examen</p></div>
  </div>
</div></section>

<section style="padding-top:24px"><div class="in stack" style="max-width:860px">
  <span class="eb">Y también las físicas</span>
  <h2>Apunta tus marcas y mira tus puntos</h2>
  <p class="lead">Circuito, dominadas o suspensión y 1.000 metros, con el baremo oficial de hombres o de mujeres: tus puntos, si serías apto y cuánto te falta para el siguiente punto.</p>
</div></section>

<section class="banda" id="precio"><div class="in stack">
  <div class="stack" style="max-width:720px">
    <h2>Tarifas</h2>
    <p class="lead">Todas incluyen lo mismo. Sin permanencia y con IVA incluido.</p>
  </div>
  {tarifas_dd()}
  <p class="muted" style="font-size:.95rem">Pago seguro con Stripe: tus datos de tarjeta no llegan a nosotros. Tienes 14 días para desistir y te devolvemos todo.</p>
</div></section>

<section id="entrar"><div class="in stack">
  <h2>Empieza en tres pasos</h2>
  <ol class="pasos">
    <li class="card"><span class="paso">1</span><div><h3>Paga tu plan</h3><p class="muted">Con tarjeta, Apple Pay o Google Pay. Te llega el recibo por email.</p></div></li>
    <li class="card"><span class="paso">2</span><div><h3>Entra en la app</h3><p class="muted">Abre <a href="{DD_APP}"><b>{DD_APP.replace('https://', '')}</b></a>, pulsa <b>«Primera vez»</b> y escribe <b>el mismo email con el que has pagado</b>.</p></div></li>
    <li class="card"><span class="paso">3</span><div><h3>Confirma y crea tu contraseña</h3><p class="muted">Te llega un correo para confirmar que el email es tuyo: abre el enlace (o escribe el código que trae), elige tu contraseña y ya estás dentro.</p></div></li>
  </ol>
  <p class="muted" style="font-size:.95rem">¿No te llega el correo? Mira en spam o escríbenos a <a href="mailto:{DD_CORREO}">{DD_CORREO}</a>.</p>
</div></section>

<section id="faq"><div class="in stack" style="max-width:820px">
  <h2>Preguntas frecuentes</h2>
  {FAQ_DD_HTML}
</div></section>
</main>""" + PIE)

# /opositores/ fue la primera dirección de Dos Décimas: se mantiene para que no se rompan los enlaces ya compartidos.
# GitHub Pages no hace redirecciones de servidor, así que se hace desde la propia página.
escribir("/opositores/", '''<!doctype html>
<html lang="es"><head>
<meta charset="utf-8">
<title>Dos Décimas · Ruvï</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="https://ruvilab.es/dos-decimas/">
<meta http-equiv="refresh" content="0; url=/dos-decimas/">
<script>location.replace("/dos-decimas/"+location.hash)</script>
</head><body>
<p>Esta página se ha movido a <a href="/dos-decimas/">ruvilab.es/dos-decimas</a>.</p>
</body></html>''')

# ---------------------------------------------------------------- Aviso legal
escribir("/aviso-legal/", cabeza("Aviso legal · Ruvï", "Contacto y condiciones de uso de la web de Ruvï.", "/aviso-legal/")
+ menu("") + f'''
<main><section><div class="in legal stack">
<span class="eb">Legal</span><h1 style="font-size:2.2rem">Aviso legal</h1>
<p class="muted">Última actualización: 24 de octubre de 2026</p>
<h2>Contacto</h2>
<p>Ruvï es una marca comercial; Plantilla de Repaso es un producto de Ruvï. Para cualquier consulta: <a href="mailto:{CORREO}">{CORREO}</a>.</p>
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
escribir("/privacidad/", cabeza("Privacidad y cookies · Ruvï", "Cómo trata Ruvï los datos de quien visita ruvilab.es, le escribe o se apunta a la lista de espera. Sin cookies ni analíticas.", "/privacidad/")
+ menu("") + f'''
<main><section><div class="in legal stack">
<span class="eb">Legal</span><h1 style="font-size:2.2rem">Privacidad y cookies</h1>
<p class="muted">Última actualización: 27 de octubre de 2026</p>
<p class="card"><b>En pocas palabras:</b> esta web no usa cookies, ni analíticas, ni publicidad. Solo tratamos tus datos si nos escribes, nos llamas o te apuntas a la lista de espera de Dos Décimas, y solo para eso.</p>
<h2>Responsable</h2>
<p>Ruvï. Contacto para privacidad: <a href="mailto:privacidad@ruvilab.es">privacidad@ruvilab.es</a>.</p>
<h2>Qué datos tratamos y para qué</h2>
<ul>
<li><b>Si nos escribes</b> a {CORREO}, por WhatsApp o nos llamas: tu nombre, tu email, el nombre de tu academia y lo que nos cuentes. Los usamos para contestarte y, si lo pides, para enseñarte la app y prepararte un presupuesto. Base legal: tu petición y las medidas previas a un contrato (artículo 6.1.b del RGPD).</li>
<li><b>Al visitar la web</b>: el proveedor que la aloja registra datos técnicos, como tu dirección IP y la hora, para servirla y por seguridad. No los usamos para nada más.</li>
</ul>
<h2 id="lista-espera">Lista de espera de Dos Décimas</h2>
<p>Dos Décimas es la versión de Plantilla de Repaso para opositores que preparan Policía Nacional por su cuenta. Si te apuntas a su lista de espera en <a href="/dos-decimas/">ruvilab.es/dos-decimas</a>:</p>
<ul>
<li><b>Qué guardamos:</b> tu email, cuándo te examinas (2027, más adelante o no lo sabes), la fecha en que te apuntas y que has aceptado esta política. Nada más: ni nombre, ni teléfono, ni cookies.</li>
<li><b>Para qué:</b> avisarte por email cuando abra Dos Décimas. Cuándo te examinas nos ayuda a preparar el lanzamiento. No te mandamos publicidad ni compartimos tu email con nadie.</li>
<li><b>Base legal:</b> tu consentimiento, al marcar la casilla (artículo 6.1.a del RGPD). Puedes retirarlo cuando quieras.</li>
<li><b>Dónde:</b> en una base de datos de Supabase, en la Unión Europea. Desde la web solo se puede añadir un email a la lista, no leerla.</li>
<li><b>Cuánto tiempo:</b> hasta que te des de baja o, como máximo, 12 meses después de apuntarte. Si al abrir el pago decides suscribirte, tus datos pasan a regirse por la <a href="{APP}/privacidad.html">política de privacidad de la app</a>.</li>
<li><b>Cómo darte de baja:</b> escribe a <a href="mailto:privacidad@ruvilab.es?subject=Baja%20de%20la%20lista%20de%20espera">privacidad@ruvilab.es</a> con el asunto «Baja» desde el email con el que te apuntaste, o contesta «Baja» a cualquiera de nuestros correos. Borramos tu email en un plazo máximo de un mes.</li>
</ul>
<h2>Cuánto tiempo</h2>
<p>Los correos se guardan mientras dure la conversación y, si llegas a ser cliente, mientras dure la relación y los plazos que exige la ley. Si no, los borramos como máximo un año después del último contacto.</p>
<h2>Quién más interviene</h2>
<div class="tw"><table>
<tr><th>Proveedor</th><th>Para qué</th><th>Dónde</th></tr>
<tr><td>GitHub (Microsoft)</td><td>Alojamiento de la web</td><td>Estados Unidos</td></tr>
<tr><td>Supabase</td><td>Base de datos de la lista de espera de Dos Décimas</td><td>Unión Europea</td></tr>
<tr><td>ImprovMX</td><td>Reenvío de los correos que nos mandas</td><td>Estados Unidos</td></tr>
<tr><td>Google (Gmail)</td><td>Buzón donde leemos y contestamos los correos</td><td>Unión Europea y Estados Unidos</td></tr>
<tr><td>WhatsApp (Meta)</td><td>Mensajes si nos escribes por WhatsApp</td><td>Unión Europea y Estados Unidos</td></tr>
</table></div>
<p>Las transferencias fuera de la Unión Europea se amparan en el Marco de Privacidad de Datos UE-EE. UU. o en las cláusulas contractuales tipo de la Comisión Europea. No vendemos ni cedemos tus datos a nadie.</p>
<h2>Tus derechos</h2>
<p>Puedes pedir acceder a tus datos, corregirlos, borrarlos, limitar su uso, oponerte o llevártelos escribiendo a <a href="mailto:privacidad@ruvilab.es">privacidad@ruvilab.es</a>. Si crees que no los respetamos, puedes reclamar ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es" rel="noopener">www.aepd.es</a>).</p>
<h2>Cookies</h2>
<p>Esta web no instala cookies ni usa herramientas de analítica o publicidad. Las letras y las imágenes se cargan desde la propia web, sin pedir nada a otros servicios. El formulario de la lista de espera solo se conecta con nuestra base de datos cuando lo envías, y tampoco usa cookies. Por eso no verás ningún aviso de cookies.</p>
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
