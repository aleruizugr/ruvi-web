# Genera las páginas de la web a partir de las piezas comunes (cabecera y pie).
# Uso: python3 _construir.py   (el guion bajo hace que GitHub Pages no publique este archivo)
import pathlib, html, hashlib
from urllib.parse import quote
R = pathlib.Path(__file__).parent
VERSION = hashlib.md5((pathlib.Path(__file__).parent / "ruvi.css").read_bytes()).hexdigest()[:8]   # cambia sola cuando cambian los estilos, para que el navegador no use una copia vieja
APP = "https://plantilla-repaso.netlify.app"   # botón «Entrar»: cambiar aquí si la app cambia de dirección
CORREO = "hola@ruvilab.es"

def cabeza(titulo, desc, ruta, noindex=False, icono="ruvi"):
    # icono="dosdecimas": las páginas de Dos Décimas llevan su propio icono en la pestaña y en la pantalla de inicio
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
<link rel="icon" type="image/png" href="/img/{'dosdecimas-favicon' if icono == 'dosdecimas' else 'favicon'}.png">
<link rel="apple-touch-icon" href="/img/{'dosdecimas-apple-touch-icon' if icono == 'dosdecimas' else 'apple-touch-icon'}.png">
<link rel="preload" href="/fuentes/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/ruvi.css?v={VERSION}">
</head><body>'''

def menu(actual, app=None):
    # «Entrar» lleva a la app de cada producto: en la página de Dos Décimas, a Dos Décimas; en el resto, a Plantilla de Repaso
    # Dos Décimas sin «opc»: se ve también en el móvil, que es donde más miran los opositores
    items = [("/plantilla-repaso/", "Plantilla de Repaso", "opc"), ("/dos-decimas/", "Dos Décimas", ""), ("/#contacto", "Contacto", ""), (app or APP, "Entrar", "entrar")]
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
(function(){{
  // Demos plegables: cada botón con data-demo="x" abre o cierra el bloque id="demo-x" (con su vídeo horizontal y vertical)
  var cual=function(c){{var vs=c.querySelectorAll("video");return matchMedia("(max-width:820px)").matches?vs[1]:vs[0]}};
  var parar=function(c){{c.querySelectorAll("video").forEach(function(v){{v.pause();try{{v.currentTime=0}}catch(e){{}}}})}};
  var cerrar=function(c){{parar(c);c.hidden=true;document.querySelectorAll('[data-demo="'+c.id.slice(5)+'"]').forEach(function(b){{b.setAttribute("aria-expanded","false")}})}};
  var abrir=function(c){{document.querySelectorAll(".demo").forEach(function(o){{if(o!==c&&!o.hidden)cerrar(o)}});c.hidden=false;
    document.querySelectorAll('[data-demo="'+c.id.slice(5)+'"]').forEach(function(b){{b.setAttribute("aria-expanded","true")}});
    c.scrollIntoView({{behavior:"smooth",block:"start"}});var p=cual(c).play();if(p&&p.catch)p.catch(function(){{}})}};
  document.querySelectorAll("[data-demo]").forEach(function(b){{var c=document.getElementById("demo-"+b.dataset.demo);if(!c)return;
    b.addEventListener("click",function(){{c.hidden?abrir(c):cerrar(c)}})}});
  document.querySelectorAll(".demo").forEach(function(c){{var x=c.querySelector(".demo-cerrar");
    x.addEventListener("click",function(){{cerrar(c);var t=document.querySelector('.producto[data-de="'+c.id.slice(5)+'"]');if(t)t.scrollIntoView({{behavior:"smooth",block:"start"}})}});
    // al terminar, deja a la vista el botón para quitar el vídeo
    c.querySelectorAll("video").forEach(function(v){{v.addEventListener("ended",function(){{x.classList.add("fin");x.scrollIntoView({{behavior:"smooth",block:"center"}});x.focus({{preventScroll:true}})}});v.addEventListener("play",function(){{x.classList.remove("fin")}})}})}});
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
  "Ruvï crea herramientas para preparar oposiciones: Plantilla de Repaso, tests tipo examen para academias, y Dos Décimas, tests de Policía Nacional para opositores por libre.", "/")
+ menu("/") + f'''
<main>
<section><div class="in stack" id="hero">
  <h1>Herramientas para <mark>preparar oposiciones</mark></h1>
  <p class="lead" style="max-width:640px">Tests tipo examen para Policía Nacional, hechos por opositores. Dos productos: uno para academias y otro para quien prepara la oposición por su cuenta.</p>
</div></section>

<section style="padding-top:0"><div class="in productos">
  <article class="card producto" data-de="plantilla">
    <button class="miniatura" type="button" data-demo="plantilla" aria-expanded="false" aria-controls="demo-plantilla" aria-label="Ver la demo de Plantilla de Repaso"><img src="/img/demo-horizontal.jpg" alt="" width="1280" height="720" loading="lazy"><span class="play" aria-hidden="true">▶</span></button>
    <span class="eb">Para academias</span>
    <h2>Plantilla de Repaso</h2>
    <p class="muted">Tu temario convertido en tests tipo examen para tus alumnos, con las preguntas revisadas por tus profesores y corregidas con la ley.</p>
    <div class="btns"><a class="btn p" href="/plantilla-repaso/">Ver Plantilla de Repaso</a><button class="btn s" type="button" data-demo="plantilla" aria-expanded="false" aria-controls="demo-plantilla">▶ Demo · 1 min</button></div>
  </article>
  <article class="card producto" data-de="dosdecimas">
    <button class="miniatura" type="button" data-demo="dosdecimas" aria-expanded="false" aria-controls="demo-dosdecimas" aria-label="Ver el vídeo de Dos Décimas"><img src="/img/dosdecimas-horizontal.jpg" alt="" width="1920" height="1080" loading="lazy"><span class="play" aria-hidden="true">▶</span></button>
    <span class="eb">Para opositores</span>
    <h2>Dos Décimas</h2>
    <p class="muted">Para quien prepara Policía Nacional por su cuenta: tests de los 45 temas comprobados con el BOE vigente, exámenes oficiales y simulacros. Desde 7,99 € al mes.</p>
    <div class="btns"><a class="btn p" href="/dos-decimas/">Ver Dos Décimas</a><button class="btn s" type="button" data-demo="dosdecimas" aria-expanded="false" aria-controls="demo-dosdecimas">▶ Vídeo · 40 s</button></div>
  </article>
</div>
<div class="in demo" id="demo-plantilla" hidden>
  <div class="video">
    <video class="v-ancho" controls playsinline preload="none" poster="/img/demo-horizontal.jpg" width="1280" height="720" aria-label="Demo de Plantilla de Repaso en vídeo horizontal"><source src="/video/demo-horizontal.mp4" type="video/mp4"></video>
    <video class="v-movil" controls playsinline preload="none" poster="/img/demo-vertical.jpg" width="720" height="1280" aria-label="Demo de Plantilla de Repaso en vídeo vertical"><source src="/video/demo-vertical.mp4" type="video/mp4"></video>
  </div>
  <div class="demo-pie"><button class="demo-cerrar" type="button">Cerrar vídeo</button></div>
</div>
<div class="in demo" id="demo-dosdecimas" hidden>
  <div class="video">
    <video class="v-ancho" controls playsinline preload="none" poster="/img/dosdecimas-horizontal.jpg" width="1280" height="720" aria-label="Demo de Dos Décimas en vídeo horizontal"><source src="/video/dosdecimas-horizontal.mp4" type="video/mp4"></video>
    <video class="v-movil" controls playsinline preload="none" poster="/img/dosdecimas-vertical.jpg" width="720" height="1280" aria-label="Demo de Dos Décimas en vídeo vertical"><source src="/video/dosdecimas-vertical.mp4" type="video/mp4"></video>
  </div>
  <div class="demo-pie"><button class="demo-cerrar" type="button">Cerrar vídeo</button></div>
</div>
</section>

<section id="nosotros" style="padding-top:0"><div class="in stack" style="max-width:760px">
  <h2>Quiénes somos</h2>
  <p class="lead">Soy Alejandro, opositor a Policía Nacional. Creé Plantilla de Repaso al echar en falta tests que se parecieran de verdad al examen, y después Dos Décimas para quien se prepara por su cuenta. Junto a mi socio, miembro de las Fuerzas y Cuerpos de Seguridad del Estado que también pasó por la oposición, fundamos Ruvï.</p>
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

PRUEBA_ASUNTO = quote("Quiero probar Dos Décimas 7 días gratis")
PRUEBA_CUERPO = quote("Hola, quiero probar Dos Décimas gratis una semana.\n\nEl email con el que quiero entrar es: ")

FAQ_DD = [
  ("¿Puedo probarla antes de pagar?", f"Sí: 7 días gratis, sin tarjeta. Escríbenos a {DD_CORREO} con el email con el que quieres entrar y te damos de alta."),
  ("¿Cómo entro después de pagar?", f"Entra en {DD_APP.replace('https://', '')}, pulsa «Primera vez» y escribe el mismo email con el que has pagado. Te llega un correo para crear tu contraseña y ya está."),
  ("¿Están actualizadas a la ley vigente?", "Sí: cada pregunta se comprueba con la ley vigente del BOE antes de publicarse. Si una ley cambia o ves un error, avisas desde la propia pregunta y la corregimos para todos."),
  ("¿Funciona en el móvil?", "Sí. Se abre en el navegador del móvil o del ordenador y puedes añadirla a la pantalla de inicio como una app, sin pasar por ninguna tienda."),
  ("¿Puedo darme de baja cuando quiera?", "Sí, sin permanencia. Mantienes el acceso hasta el final de lo que ya pagaste. El curso completo es un pago único y no se renueva."),
  ("¿Y si no me convence?", f"Tienes 14 días para desistir y te devolvemos todo, aunque ya la hayas usado. Basta con escribir a {DD_CORREO}."),
]
FAQ_DD_HTML = "".join(f'<details class="card"><summary><b>{q}</b></summary><p class="muted" style="margin-top:10px">{r}</p></details>' for q, r in FAQ_DD)

escribir("/dos-decimas/", cabeza("Dos Décimas · Tests de Policía Nacional",
  "Dos Décimas: tests de Policía Nacional (Escala Básica) a nivel de examen, comprobados con la ley vigente del BOE. Hechos por un opositor que se quedó a dos décimas del corte.", "/dos-decimas/", icono="dosdecimas")
+ menu("/dos-decimas/", DD_APP) + f"""
<main>
<section><div class="in dos" id="hero">
  <div class="stack">
    <img class="dd-logo" src="/img/dosdecimas-logo.png" alt="Dos Décimas" width="64" height="64">
    <span class="eb">Dos Décimas · Policía Nacional, Escala Básica</span>
    <h1>Me quedé fuera por <mark>dos décimas</mark>. Que a ti no te pase.</h1>
    <p class="lead">Las plazas se deciden por décimas, y casi nunca se pierden por no estudiar: se pierden en un plazo, en un «NO» que no leíste o en una duda que arriesgaste. Dos Décimas te enseña dónde se te escapan las tuyas.</p>
    <div class="btns"><a class="btn p" href="#prueba">Pruébala 7 días gratis</a><a class="btn s" href="{DD_APP}">Ya tengo cuenta: entrar</a></div>
    <p class="muted" style="font-size:.95rem">Preguntas comprobadas con el BOE vigente por un opositor que se quedó a dos décimas del corte.</p>
    <p style="font-size:.95rem"><a href="/dos-decimas/test-gratis/"><b>¿Llegarías al 7,05?</b> Haz el test gratis, sin registro →</a></p>
  </div>
  <div style="display:flex;justify-content:center"><div class="movil"><img src="/img/app-pregunta.png" alt="Una pregunta tipo test en el móvil, con tres opciones, el cronómetro y los botones Dudo y Dejar en blanco" width="390" height="700"></div></div>
</div></section>

<section style="padding-top:0"><div class="in stack" style="max-width:960px">
  <h2>Dos Décimas en 40 segundos</h2>
  <div class="video">
    <video class="v-ancho" controls playsinline preload="none" poster="/img/dosdecimas-horizontal.jpg" width="1280" height="720" aria-label="Vídeo de Dos Décimas en horizontal: una nota de 6,95 frente a un corte de 7,05 y lo que hace la app para que no te pase"><source src="/video/dosdecimas-horizontal.mp4" type="video/mp4"></video>
    <video class="v-movil" controls playsinline preload="none" poster="/img/dosdecimas-vertical.jpg" width="720" height="1280" aria-label="Vídeo de Dos Décimas en vertical: una nota de 6,95 frente a un corte de 7,05 y lo que hace la app para que no te pase"><source src="/video/dosdecimas-vertical.mp4" type="video/mp4"></video>
  </div>
</div></section>

<section class="banda"><div class="in dos inv">
  <div style="display:flex;justify-content:center"><div class="movil"><img src="/img/app-resultado.png" alt="Resultado de un test: un 7 sobre 10, aciertos, errores y preguntas en blanco, la cuenta como en el examen y cuántos puntos le ha sumado arriesgar en las preguntas que dudaba" width="390" height="748"></div></div>
  <div class="stack">
    <span class="eb">Mientras practicas</span>
    <h2>Cada pregunta te enseña algo</h2>
    <ul class="lista">
      <li><span>¿Se te escapan los «NO», «salvo» o «excepto»? <b>La lupa</b> te los resalta en el enunciado.</span></li>
      <li><span>¿No sabes por qué has fallado? <b>Cada corrección</b> trae la respuesta buena, el porqué y lo que dice el artículo de la ley.</span></li>
      <li><span>¿Arriesgar o dejar en blanco? Marca <b>«Dudo»</b> y la app te dice si contestar cuando no estás seguro te suma o te resta.</span></li>
      <li><span><b>Como el examen:</b> tres opciones, −0,5 por fallo y cronómetro.</span></li>
    </ul>
  </div>
</div></section>

<section><div class="in dos">
  <div class="stack">
    <span class="eb">Cuando repasas</span>
    <h2>Sabes qué tema llevas bien y cuál no</h2>
    <ul class="lista">
      <li><span>¿Qué tema llevas peor? <b>Cómo vas en cada tema</b> te los ordena del más flojo al más fuerte: por repasar, casi o bien. Tocas uno y lo practicas.</span></li>
      <li><span>¿Se te olvidan las que ya fallaste? <b>Tus fallos pendientes</b> vuelven hasta que las aciertes.</span></li>
      <li><span>¿Poco tiempo? <b>Repaso de 5 minutos</b> al día con lo que fallaste o dudaste, justo cuando toca repasarlo.</span></li>
      <li><span><b>Las más falladas:</b> las preguntas que más se fallan entre todos los opositores de Dos Décimas.</span></li>
    </ul>
  </div>
  <div style="display:flex;justify-content:center"><div class="movil"><img src="/img/app-temas.png" alt="Pantalla «Cómo vas en cada tema»: cada tema con su porcentaje de acierto y su barra en verde o amarillo, del más flojo al más fuerte" width="390" height="748" loading="lazy"></div></div>
</div></section>

<section class="banda"><div class="in dos inv">
  <div style="display:flex;justify-content:center"><div class="movil"><img src="/img/app-cuaderno.png" alt="Mi cuaderno: un test con su nota, 7 aciertos y 3 errores, y una pregunta fallada con la respuesta que se dio, la correcta y el porqué" width="390" height="748" loading="lazy"></div></div>
  <div class="stack">
    <span class="eb">Tus fallos, a la vista</span>
    <h2>Aprende de cada error</h2>
    <ul class="lista">
      <li><span><b>Mi cuaderno:</b> cada test que haces, con tu nota, lo que fallaste, la respuesta correcta y por qué. Y un botón para practicar solo esas.</span></li>
      <li><span>¿Fallas siempre en lo mismo? <b>Mis trampas</b> te dice en qué tipo caes más (plazos, números, quién es competente, «podrá» o «deberá»…) y te hace un test solo de esa.</span></li>
      <li><span>¿No lo sabías o no leíste bien? Al corregir, marcas <b>por qué fallaste</b> con un toque y ves qué es lo que más te pasa.</span></li>
      <li><span><b>12 exámenes oficiales</b> desde 2015, con la nota de corte de cada promoción: al acabar, sabes si habrías pasado.</span></li>
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

<section class="banda" id="prueba"><div class="in stack" style="max-width:860px">
  <span class="eb">Sin pagar nada</span>
  <h2>Pruébala 7 días gratis</h2>
  <p class="lead">Mándanos el email con el que quieres entrar y te damos acceso a todo durante una semana: tests, exámenes oficiales, simulacro, tus trampas y las físicas. Sin tarjeta y sin compromiso.</p>
  <div class="btns"><a class="btn p" href="mailto:{DD_CORREO}?subject={PRUEBA_ASUNTO}&amp;body={PRUEBA_CUERPO}">Quiero mi semana gratis</a></div>
  <p class="muted" style="font-size:.95rem">Te escribimos en cuanto te demos de alta. También puedes pedirlo comentando «ERROR» en cualquiera de nuestros vídeos de Instagram.</p>
</div></section>

<section id="precio"><div class="in stack">
  <details class="card plegable" id="planes">
    <summary><span><b>Ver planes y precios</b><span class="muted" style="display:block;font-size:.95rem;margin-top:4px">Todos incluyen lo mismo. Sin permanencia y con IVA incluido.</span></span></summary>
    <div class="stack" style="margin-top:20px">
      {tarifas_dd()}
      <p class="muted" style="font-size:.95rem">Pago seguro con Stripe: tus datos de tarjeta no llegan a nosotros. Tienes 14 días para desistir y te devolvemos todo.</p>
    </div>
  </details>
  <script>if(location.hash==="#precio"||location.hash==="#planes")document.getElementById("planes").open=true</script>
</div></section>

<section id="entrar"><div class="in stack">
  <h2>Empieza en tres pasos</h2>
  <ol class="pasos">
    <li class="card"><span class="paso">1</span><div><h3>Elige tu plan</h3><p class="muted">Cuando acabe tu semana gratis, o antes si quieres. Con tarjeta, Apple Pay o Google Pay. Te llega el recibo por email.</p></div></li>
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

# ---------- Dos Décimas: test gratis «¿Llegarías al 7,05?» ----------
# 20 preguntas reales de la promoción 43 (las múltiplos de 5 del modelo A, sin elegir a mano). Sin registro:
# todo ocurre en el navegador y no se guarda ni se envía nada.
import json as _json
_TG = _json.dumps(_json.loads((R / "_fuentes" / "test-gratis.json").read_text(encoding="utf-8")), ensure_ascii=False).replace("</", "<\\/")
_TG_JS = """<script>
(function(){
  var P=__PREGUNTAS__,CORTE=7.05,SEG=600,i=0,res=P.map(function(){return null}),fin=0,reloj=null;
  var $=function(id){return document.getElementById(id)},caja=$("tg");
  var coma=function(x){return x.toFixed(2).replace(".",",")};
  var el=function(tag,cls,txt){var e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e};
  function tiempo(){var s=Math.max(0,Math.round((fin-Date.now())/1000));var t=$("tg-t");if(t)t.textContent=Math.floor(s/60)+":"+String(s%60).padStart(2,"0");if(s<=0)resultado()}
  function pregunta(){
    caja.textContent="";var q=P[i];
    var cab=el("div","tg-cab");cab.appendChild(el("span","tg-n",(i+1)+" / "+P.length));var t=el("span","tg-n");t.id="tg-t";cab.appendChild(t);caja.appendChild(cab);
    var b=el("div","tg-barra");var bi=el("i");bi.style.width=(i/P.length*100)+"%";b.appendChild(bi);caja.appendChild(b);
    caja.appendChild(el("p","tg-q",q.q));
    q.o.forEach(function(o,k){var x=el("button","tg-op");x.type="button";x.appendChild(el("b",null,"abc"[k]));x.appendChild(el("span",null,o));x.onclick=function(){res[i]=k;sigue()};caja.appendChild(x)});
    var bl=el("button","btn s tg-bl","Dejar en blanco");bl.type="button";bl.onclick=function(){res[i]=null;sigue()};caja.appendChild(bl);
    tiempo();caja.scrollIntoView({block:"start"});
  }
  function sigue(){i++;i<P.length?pregunta():resultado()}
  function resultado(){
    clearInterval(reloj);var A=0,E=0,B=0;res.forEach(function(r,k){if(r===null)B++;else if(r===P[k].a)A++;else E++});
    var nota=(A-E/2)*10/P.length,dif=CORTE-nota;
    var tit=nota>=CORTE?"Con esta nota superarías el corte de 2026":dif<=1?"Te quedarías a "+coma(dif)+" del corte":"Te faltarían "+coma(dif)+" puntos para el corte";
    var txt=nota>=CORTE?"Buena señal, pero 20 preguntas son solo una muestra. Compruébalo con un examen entero.":dif<=1?"Así se pierden las plazas: por décimas. Mira en qué fallas para que no te pase.":"Aún hay margen, y saber dónde fallas es lo primero para recortarlo.";
    caja.textContent="";caja.appendChild(el("span","eb","Tu resultado"));
    caja.appendChild(el("p","tg-nota",coma(nota)));caja.appendChild(el("p","muted","Corte de la promoción 43: 7,05 · "+A+" aciertos, "+E+" fallos y "+B+" en blanco"));
    caja.appendChild(el("h2",null,tit));caja.appendChild(el("p","lead",txt));
    var bt=el("div","btns");var a=el("a","btn p","Pruébala 7 días gratis");a.href="/dos-decimas/#prueba";bt.appendChild(a);
    var w=el("a","btn s","Reta a un compañero");w.href="https://wa.me/?text="+encodeURIComponent("He sacado un "+coma(nota)+" en este test con preguntas reales del examen de Policía Nacional de 2026. ¿Tú llegarías al 7,05? https://ruvilab.es/dos-decimas/test-gratis/");w.target="_blank";w.rel="noopener";bt.appendChild(w);caja.appendChild(bt);
    var mal=P.map(function(q,k){return{q:q,r:res[k]}}).filter(function(x){return x.r!==x.q.a});
    if(mal.length){caja.appendChild(el("h3","tg-rev","Lo que has fallado o dejado en blanco"));mal.forEach(function(x){var c=el("div","tg-mal");c.appendChild(el("p","tg-mq",x.q.q));if(x.r!==null)c.appendChild(el("p","tg-no","Tu respuesta: "+"abc"[x.r]+") "+x.q.o[x.r]));c.appendChild(el("p","tg-si","Correcta: "+"abc"[x.q.a]+") "+x.q.o[x.q.a]));caja.appendChild(c)});
      caja.appendChild(el("p","muted","En la app, cada corrección trae además el porqué y lo que dice la ley."))}
    caja.scrollIntoView({block:"start"});
  }
  $("tg-go").onclick=function(){fin=Date.now()+SEG*1000;reloj=setInterval(tiempo,1000);pregunta()};
})();
</script>""".replace("__PREGUNTAS__", _TG)
escribir("/dos-decimas/test-gratis/", cabeza("¿Llegarías al 7,05? · Test gratis de Policía Nacional",
  "20 preguntas reales del examen de Policía Nacional de 2026, sin registro. Compara tu nota con el corte de 7,05.", "/dos-decimas/test-gratis/", icono="dosdecimas")
+ menu("/dos-decimas/", DD_APP) + """
<main>
<section><div class="in stack tg-in" id="tg">
  <img class="dd-logo" src="/img/dosdecimas-logo.png" alt="Dos Décimas" width="64" height="64">
  <span class="eb">Test gratis · Policía Nacional</span>
  <h1>¿Llegarías al <mark>7,05</mark>?</h1>
  <p class="lead">Ese fue el corte del examen de 2026. Comprueba cómo vas con 20 preguntas reales de ese examen, puntuadas igual: −0,5 por fallo y sin penalizar el blanco.</p>
  <ul class="lista"><li><span><b>10 minutos</b>, al ritmo del examen</span></li><li><span><b>Sin registro:</b> no pedimos datos ni guardamos tus respuestas</span></li><li><span>Al acabar, tu nota y las respuestas correctas de lo que falles</span></li></ul>
  <div class="btns"><button class="btn p" type="button" id="tg-go">Empezar el test</button></div>
  <p class="muted" style="font-size:.95rem">Preguntas 5, 10, 15… hasta la 100 del modelo A del examen del 26-09-2026, con las respuestas de la plantilla publicada. El resultado es orientativo: 20 preguntas son solo una muestra.</p>
</div></section>
</main>""" + PIE + _TG_JS)

# /opositores/ fue la primera dirección de Dos Décimas: se mantiene para que no se rompan los enlaces ya compartidos.
# GitHub Pages no hace redirecciones de servidor, así que se hace desde la propia página.
# ---------- Dos Décimas: página a la que vuelve Stripe después de pagar ----------
escribir("/dos-decimas/gracias/", cabeza("Pago completado · Dos Décimas",
  "Tu pago de Dos Décimas se ha completado. Entra en la app con el mismo email con el que has pagado.", "/dos-decimas/gracias/", noindex=True, icono="dosdecimas")
+ menu("/dos-decimas/", DD_APP) + f"""
<main>
<section><div class="in stack" style="max-width:720px">
  <img class="dd-logo" src="/img/dosdecimas-logo.png" alt="Dos Décimas" width="64" height="64">
  <span class="eb">Dos Décimas · pago completado</span>
  <h1>¡Ya estás dentro! <mark>Bienvenido</mark></h1>
  <p class="lead">Tu pago se ha completado. Stripe te enviará el recibo a tu email. Para entrar por primera vez:</p>
  <ol class="pasos" style="grid-template-columns:1fr">
    <li class="card"><span class="paso">1</span><div><h3>Pulsa «Entrar en Dos Décimas»</h3><p class="muted">Se abre la app en <b>{DD_APP.replace('https://', '')}</b>. Guárdala en favoritos o añádela a la pantalla de inicio del móvil.</p></div></li>
    <li class="card"><span class="paso">2</span><div><h3>Elige «Primera vez»</h3><p class="muted">Escribe <b>el mismo email con el que has pagado</b>.</p></div></li>
    <li class="card"><span class="paso">3</span><div><h3>Crea tu contraseña</h3><p class="muted">Te llega un correo con un enlace o un código. Ábrelo, elige tu contraseña y a por las décimas.</p></div></li>
  </ol>
  <div class="btns"><a class="btn p" href="{DD_APP}">Entrar en Dos Décimas</a></div>
  <p class="muted" style="font-size:.95rem">¿No te llega el correo? Mira en spam o escríbenos a <a href="mailto:{DD_CORREO}">{DD_CORREO}</a>.</p>
</div></section>
</main>""" + PIE)

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
escribir("/aviso-legal/", cabeza("Aviso legal · Ruvï", "Titular, contacto y condiciones de uso de la web de Ruvï.", "/aviso-legal/")
+ menu("") + f'''
<main><section><div class="in legal stack">
<span class="eb">Legal</span><h1 style="font-size:2.2rem">Aviso legal</h1>
<p class="muted">Última actualización: 31 de octubre de 2026</p>
<h2>Titular</h2>
<p>En cumplimiento del artículo 10 de la Ley 34/2002, de servicios de la sociedad de la información y de comercio electrónico, se informa de que esta web y la marca Ruvï, con sus productos Plantilla de Repaso y Dos Décimas, son de:</p>
<ul>
<li><b>Titular:</b> Alejandro Ruiz Barreda</li>
<li><b>NIF:</b> 49236511C</li>
<li><b>Domicilio:</b> C/ Gustavo Adolfo Bécquer, 25, 21122 Huelva</li>
<li><b>Email de contacto:</b> <a href="mailto:{CORREO}">{CORREO}</a></li>
</ul>
<h2>Uso de la web</h2>
<p>Esta web informa sobre los productos de Ruvï. Quien la visita se compromete a usarla de forma lícita y a no dañar su funcionamiento.</p>
<h2>Propiedad intelectual</h2>
<p>Los textos, el diseño, el logotipo y las imágenes de esta web pertenecen a su titular o se usan con permiso. No se pueden copiar ni reutilizar sin autorización. Las tipografías se usan bajo licencia SIL Open Font License.</p>
<h2>Enlaces</h2>
<p>Esta web enlaza a las aplicaciones Plantilla de Repaso, con su propio <a href="{APP}/aviso-legal.html">aviso legal</a> y su propia <a href="{APP}/privacidad.html">política de privacidad</a>, y Dos Décimas, también con su propio <a href="{DD_APP}/aviso-legal.html">aviso legal</a> y su propia <a href="{DD_APP}/privacidad.html">política de privacidad</a>.</p>
<h2>Responsabilidad</h2>
<p>Procuramos que la información sea correcta y esté al día, pero puede contener errores o cambiar sin aviso. En Plantilla de Repaso, los precios y condiciones que valen son los que se acuerdan por escrito con cada academia. En Dos Décimas, los que aparecen al contratar.</p>
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
<p>Alejandro Ruiz Barreda, titular de la marca Ruvï (más datos en el <a href="/aviso-legal/">aviso legal</a>). Contacto para privacidad: <a href="mailto:privacidad@ruvilab.es">privacidad@ruvilab.es</a>.</p>
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
