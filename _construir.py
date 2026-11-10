# Genera las páginas de la web a partir de las piezas comunes (cabecera y pie).
# Uso: python3 _construir.py   (el guion bajo hace que GitHub Pages no publique este archivo)
import pathlib, html, hashlib
from urllib.parse import quote
R = pathlib.Path(__file__).parent
APP = "https://plantilla-repaso.netlify.app"   # botón «Entrar»: cambiar aquí si la app cambia de dirección
CORREO = "hola@ruvilab.es"
DD_CORREO = "dosdecimas@ruvilab.es"
DD_APP = "https://dosdecimas.ruvilab.es"

ENTRADAS_JS = """<script>
(function(){
  var ents=document.querySelectorAll(".ent"),ver=function(e){e.classList.add("visto")};
  if("IntersectionObserver" in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){ver(e.target);io.unobserve(e.target)}})},{rootMargin:"0px 0px -10% 0px"});ents.forEach(function(e){io.observe(e)})}
  else ents.forEach(ver);
  setTimeout(function(){ents.forEach(ver)},1500);
})();
</script>"""

# Contador de visitas de Dos Décimas, anónimo: suma 1 a un número por día, página, acción y procedencia
# (función apuntar_web() de la migración 026 de plantilla-repaso). No usa cookies, no guarda nada en el aparato
# y no manda ningún dato de la persona: solo «instagram», «tiktok», «google»… según de dónde llega.
# Solo cuenta en ruvilab.es (no en local). La clave es la pública de siempre.
CUENTA_JS = """<script>
(function(){
  var U="__URL__/rest/v1/rpc/apuntar_web",K="__CLAVE__",h=location.hostname;
  var pag=/test-gratis/.test(location.pathname)?"test-gratis":/gracias/.test(location.pathname)?"gracias":"dos-decimas";
  var ua=navigator.userAgent||"",r="";try{r=document.referrer?new URL(document.referrer).hostname:""}catch(e){}
  var o=/Instagram/i.test(ua)||/instagram\\./.test(r)?"instagram":/musical_ly|TikTok|Bytedance/i.test(ua)||/tiktok\\./.test(r)?"tiktok":/FBAN|FBAV/.test(ua)||/facebook\\.|(^|\\.)fb\\./.test(r)?"facebook":/google\\./.test(r)?"google":/(^|\\.)ruvilab\\.es$/.test(r)?"interno":r?"otro":"directo";
  window.ddCuenta=function(ev){
    if(h!=="ruvilab.es"&&h!=="www.ruvilab.es")return;
    try{fetch(U,{method:"POST",headers:{"apikey":K,"Authorization":"Bearer "+K,"Content-Type":"application/json"},body:JSON.stringify({pagina:pag,evento:ev,origen:o}),keepalive:true}).catch(function(){})}catch(e){}
  };
  ddCuenta("visita");
  document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a[href]");if(!a)return;var f=a.getAttribute("href");
    if(/buy\\.stripe\\.com/.test(f))ddCuenta("clic_tarifa");else if(/#prueba$/.test(f))ddCuenta("clic_prueba");else if(/test-gratis/.test(f)&&pag!=="test-gratis")ddCuenta("clic_test")});
})();
</script>"""

def pie(marca="ruvi", *scripts):
    # el pie es un cierre: el nombre de la marca a todo el ancho
    if marca == "dd":
        nombre, linea = "Dos Décimas", f'Tests de Policía Nacional, Escala Básica · Un proyecto de <a href="/">Ruvï</a> · <a href="mailto:{DD_CORREO}">{DD_CORREO}</a>'
        extra = f'<a href="{DD_APP}">Entrar en la app</a>'
    else:
        nombre, linea = "Ruvï", f'Herramientas para preparar oposiciones · <a href="mailto:{CORREO}">{CORREO}</a>'
        extra = '<a href="/plantilla-repaso/">Plantilla de Repaso</a><a href="/dos-decimas/">Dos Décimas</a>'
    return f'''<footer class="pie"><div class="in">
<p class="grande" translate="no">{nombre}</p>
<div class="fila"><span>{linea}</span>
<nav aria-label="Legal">{extra}<a href="/aviso-legal/">Aviso legal</a><a href="/privacidad/">Privacidad</a></nav></div>
</div></footer>
''' + (CUENTA_JS.replace("__URL__", SUPABASE_URL).replace("__CLAVE__", SUPABASE_CLAVE) if marca == "dd" else "") + "".join(scripts) + ENTRADAS_JS + "\n</body></html>"

TELEFONO = "669 767 570"
WHATSAPP = "34669767570"
ASUNTO = "Plantilla de Repaso para nuestra academia"
CUERPO = ("Hola:\n\nNos interesa Plantilla de Repaso y nos gustaría verla con los temas de nuestra academia.\n\n"
          "Academia: \nCiudad: \nNúmero de alumnos: \nTeléfono de contacto: \n"
          "Mejor día y hora para la videollamada: \n\nGracias.")
WA_TEXTO = "Hola, os escribo desde ruvilab.es. Me interesa Plantilla de Repaso y me gustaría verla con los temas de mi academia."

def contacto(titulo, texto):
    mailto = f"mailto:{CORREO}?subject={quote(ASUNTO)}&body={quote(CUERPO)}"
    wa = f"https://wa.me/{WHATSAPP}?text={quote(WA_TEXTO)}"
    return f'''<section class="sec campo-oscuro contacto" id="contacto"><div class="in">
  <div class="ent"><h2>{titulo}</h2><p class="lead">{texto}</p></div>
  <div class="ent">
    <div class="btns"><a class="btn btn-p" href="{mailto}">Escribir un correo</a><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">WhatsApp</a></div>
    <p class="datos suave">{CORREO} · <span style="white-space:nowrap">{TELEFONO}</span></p>
  </div>
</div></section>'''

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
# La portada de Ruvï y la de Plantilla de Repaso se escriben al final, con el panel (cabeza_panel).

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

# Semana gratis: el formulario llama a pedir_prueba() en el Supabase de producción (migración 016 de plantilla-repaso),
# que da el alta al momento a los emails nuevos. El formulario es dd_form(); sale en la página de Dos Décimas y al acabar
# el test gratis (origen "web" o "test", para saber de dónde llegan). Clave pública por diseño: solo puede llamar a esa función.
# Va en <script> normal (no f-string): se pega tal cual en las dos páginas.
PRUEBA_JS = ("""<script>
(function(){
  var URL="__URL__/rest/v1/rpc/pedir_prueba",CLAVE="__CLAVE__",APPDD="__APP__",CORREO="__CORREO__";
  window.activarPrueba=function(f){if(!f||f.dataset.listo)return;f.dataset.listo=1;
    var b=f.querySelector("button[type=submit]"),m=f.querySelector(".aviso"),t=b.textContent;
    var aviso=function(html,ok){m.innerHTML=html;m.className="aviso "+(ok?"ok":"mal");m.hidden=false;m.focus&&m.setAttribute("tabindex","-1");m.focus()};
    f.addEventListener("submit",function(e){e.preventDefault();
      if(f.web.value)return;   // campo trampa: solo lo rellenan los robots
      if(!f.reportValidity())return;
      var correo=f.email.value.trim().toLowerCase(),nombre=f.nombre?f.nombre.value.trim().replace(/\\s+/g," "):"";
      b.disabled=true;b.textContent="Enviando…";
      fetch(URL,{method:"POST",headers:{"apikey":CLAVE,"Authorization":"Bearer "+CLAVE,"Content-Type":"application/json"},
        body:JSON.stringify({correo:correo,origen:f.dataset.origen,nombre:nombre||null,como:f.como&&f.como.value||null})   // como: «¿Dónde nos viste?» (migración 020)
      }).then(function(r){return r.ok?r.json():Promise.reject(r.status)}).then(function(d){
        var esc=correo.replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]});
        // función bienvenida-dos-decimas: manda la bienvenida si de verdad acaba de recibir el alta o, si se ha
        // quedado en espera, avisa al dueño para que la dé a mano (migración 027)
        var avisar=function(){try{fetch(URL.replace("/rest/v1/rpc/pedir_prueba","/functions/v1/bienvenida-dos-decimas"),{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({correo:correo}),keepalive:true}).catch(function(){})}catch(e){}};
        avisar();
        if(d&&d.estado==="en_espera"){aviso("<b>Recibido.</b> Te damos de alta en unas horas y te escribimos a <b>"+esc+"</b>.",true);return}
        window.ddCuenta&&ddCuenta("form_enviado");
        Array.prototype.forEach.call(f.children,function(c){if(c!==m)c.style.display="none"});   // deja solo el aviso (con display: el CSS de .campo y .btns gana a hidden)
        var nomEsc=nombre.split(" ")[0].replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]});
        aviso("<b>¡Hecho"+(nomEsc?", "+nomEsc:"")+"! Tienes 7 días gratis.</b><br>Te acabamos de mandar un correo a <b>"+esc+"</b>. Ábrelo, pulsa el botón y elige tu contraseña: ya estás dentro.<br><span class=\\"muted\\" style=\\"font-size:.9rem\\">¿No te llega en un par de minutos? Mira en spam o <a href=\\""+APPDD+"/?primera\\">entra por aquí</a> con «Primera vez».</span><br><span class=\\"muted\\" style=\\"font-size:.9rem\\">¿Ya la habías probado antes? Escríbenos a "+CORREO+".</span>",true);
      }).catch(function(s){aviso(s===400?"Ese email no parece válido. Revísalo y prueba otra vez.":"No se ha podido enviar. Prueba otra vez o escríbenos a "+CORREO+".",false)})
      .then(function(){b.disabled=false;b.textContent=t});
    });
  };
  document.querySelectorAll(".prueba-form").forEach(activarPrueba);
})();
</script>""").replace("__URL__", SUPABASE_URL).replace("__CLAVE__", SUPABASE_CLAVE).replace("__APP__", DD_APP).replace("__CORREO__", DD_CORREO)

FAQ_DD = [
  ("¿Puedo probarla antes de pagar?", "Sí: 7 días gratis, sin tarjeta. Deja tu email en «Pruébala 7 días gratis» y normalmente entras al momento."),
  ("¿Cómo entro después de pagar?", f"Entra en {DD_APP.replace('https://', '')}, pulsa «Primera vez» y escribe el mismo email con el que has pagado. Te llega un correo para crear tu contraseña y ya está."),
  ("¿Están actualizadas a la ley vigente?", "Sí: cada pregunta se comprueba con la ley vigente del BOE antes de publicarse. Si una ley cambia o ves un error, avisas desde la propia pregunta y la corregimos para todos."),
  ("¿Qué cubre y qué no?", "Cubre la prueba de conocimientos: tests de los 45 temas de la Escala Básica, 12 exámenes oficiales desde 2015 y un simulacro cada fin de semana. También te ayuda con las físicas, con el baremo oficial. No es un temario para estudiar desde cero: es para practicar lo que estudias. Tampoco incluye psicotécnicos ni la entrevista."),
  ("¿Funciona en el móvil?", "Sí. Se abre en el navegador del móvil o del ordenador y puedes añadirla a la pantalla de inicio como una app, sin pasar por ninguna tienda."),
  ("¿Puedo darme de baja cuando quiera?", "Sí, sin permanencia. Mantienes el acceso hasta el final de lo que ya pagaste. El curso completo es un pago único y no se renueva."),
  ("¿Y si no me convence?", f"Tienes 14 días para desistir y te devolvemos todo, aunque ya la hayas usado. Basta con escribir a {DD_CORREO}."),
]

# ---------- Dos Décimas: página de venta (ruvilab.es/dos-decimas/) ----------
# Cabecera y pie de Dos Décimas (marca="dd"), campos oscuros para los momentos fuertes
# y, como pieza viva, la calculadora de décimas (tu nota → cuántas preguntas te faltaron para el 7,05).
DD_CORTE = "7,05"

def dd_form(origen, boton="Pruébala 7 días gratis"):
    return f'''<form class="alta-form prueba-form" data-origen="{origen}" novalidate>
    <label class="campo campo-nombre"><b>Tu nombre</b>
      <input type="text" name="nombre" required maxlength="40" autocomplete="given-name" autocapitalize="words" placeholder="Cómo te llamas"></label>
    <label class="campo"><b>Tu email</b>
      <input type="email" name="email" required maxlength="254" autocomplete="email" inputmode="email" spellcheck="false" placeholder="tu@email.com"></label>
    <label class="campo campo-como"><b>¿Dónde nos viste? <span class="opcional">(opcional)</span></b>
      <select name="como"><option value="">Elige una opción</option><option value="instagram">Instagram</option><option value="tiktok">TikTok</option><option value="companero">Me lo pasó un compañero</option><option value="grupo">En un grupo de opositores</option><option value="creador">Un creador de contenido</option><option value="google">Google</option><option value="otro">Otro</option></select></label>
    <label class="trampa" aria-hidden="true">No rellenar <input type="text" name="web" tabindex="-1" autocomplete="off"></label>
    <div class="btns"><button class="btn btn-p" type="submit">{boton}</button></div>
    <p class="nota">7 días con todo, sin tarjeta. Usamos tu nombre y tu email solo para darte acceso y mandarte cómo entrar, como dice la <a href="{DD_APP}/privacidad.html">política de privacidad</a>.</p>
    <div class="aviso" role="status" hidden></div>
  </form>'''




def dd_tarifas():
    tarjetas = ""
    for t in TARIFAS_DD:
        dest = t.get("destacada")
        sale = f"Sale a {t['al_mes']} al mes" if t["al_mes"] else ""
        if sale and t["ahorro"]: sale += f' (<span class="ahorro">{t["ahorro"]}</span>)'
        if sale: sale += ". "
        tarjetas += f"""<div class="tarifa{' dest' if dest else ''}">
      <h3>{t['nombre']}</h3>
      <p class="precio">{t['precio']} <small>{t['periodo']}</small></p>
      <p class="peq{'' if dest else ' suave'}">{sale}{t['nota']}</p>
      <a class="btn {'btn-p' if dest else 'btn-s'}" href="{t['enlace']}" rel="noopener">Elegir {t['nombre'].lower()}</a>
    </div>"""
    f = TARIFA_FUNDADOR
    return f"""<div class="fundador">
    <div><p class="precio">{f['precio']} <small>{f['periodo']}</small></p>
      <p>Precio fundador, solo para las {f['plazas']} primeras personas, para siempre mientras sigas suscrito.</p>
      <p class="suave peq">Después, 10,99 € al mes. Si te das de baja y vuelves, pagas el precio de entonces.</p></div>
    <a class="btn btn-p" href="{f['enlace']}" rel="noopener">Quiero el precio fundador</a>
  </div>
  <div class="tarifas">{tarjetas}</div>"""

_MAS = '<svg class="mas" viewBox="0 0 18 18" aria-hidden="true"><path d="M9 2v14M2 9h14" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="square"/></svg>'
FAQ_DD_HTML = "".join(f'<details><summary>{q}{_MAS}</summary><p>{r}</p></details>' for q, r in FAQ_DD)



# La página de venta de Dos Décimas (el panel de tablillas) se escribe más abajo.


# ---------- Dos Décimas: test gratis «¿Llegarías al 7,05?» ----------
# 20 preguntas reales de la promoción 43 (las múltiplos de 5 del modelo A, sin elegir a mano). Sin registro:
# todo ocurre en el navegador y no se guarda ni se envía nada.
import json as _json
_TG = _json.dumps(_json.loads((R / "_fuentes" / "test-gratis.json").read_text(encoding="utf-8")), ensure_ascii=False).replace("</", "<\\/")

# Cabecera de las páginas con el mundo del panel (panel.css): Ruvï, Plantilla de Repaso y Dos Décimas.
# Cada página es de una marca: «ruvi» (inicio, Plantilla de Repaso, legales) o «dd» (Dos Décimas).
def _huella(ruta):
    return hashlib.md5((R / ruta.lstrip("/")).read_bytes()).hexdigest()[:8]

def cabeza_panel(titulo, desc, ruta, marca="dd", og=None, noindex=False, actual=""):
    dd = marca == "dd"
    og = og or ("dosdecimas-og.jpg" if dd else "ruvi-og.jpg")
    icono = "dosdecimas-" if dd else ""
    if dd:
        cab = f'''<a class="marca" href="/dos-decimas/" aria-label="Dos Décimas, inicio"><img src="/img/dosdecimas-logo.png" alt="" width="34" height="34"><span class="nombre">Dos Décimas</span></a>
<nav aria-label="Menú"><a class="opc" href="/dos-decimas/#como">Cómo funciona</a><a href="/dos-decimas/#planes">Tarifas</a><a class="opc" href="/dos-decimas/test-gratis/">Test gratis</a><a class="btn-ruvi" href="/" title="Ir a la web de Ruvï"><img src="/img/ruvi-monograma.png" alt="" width="22" height="22">Ruvï</a><a class="btn btn-s" href="{DD_APP}">Entrar</a></nav>'''
    else:
        # en el móvil «Plantilla de Repaso» se acorta a «Plantilla» para que quepa con el logo
        enlaces = [("/plantilla-repaso/", 'Plantilla<span class="larga"> de Repaso</span>', ""), ("/dos-decimas/", "Dos Décimas", ""), ("/#contacto", "Contacto", "opc")]
        marcado = ' aria-current="page"'
        clase = lambda c: f' class="{c}"' if c else ""
        links = "".join(f'<a{clase(c)} href="{h}"{marcado if h == actual else ""}>{t}</a>' for h, t, c in enlaces)
        cab = f'''<a class="marca" href="/" aria-label="Ruvï, inicio"><img src="/img/ruvi-monograma.png" alt="" width="34" height="34"><span class="nombre">Ruvï</span></a>
<nav aria-label="Menú">{links}<a class="btn btn-s" href="{APP}">Entrar</a></nav>'''
    return f'''<!doctype html>
<html lang="es"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{titulo}</title>
<meta name="description" content="{html.escape(desc)}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<meta name="theme-color" content="#0A0A0A">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://ruvilab.es{ruta}">
<meta property="og:image" content="https://ruvilab.es/img/{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="es_ES">
<link rel="icon" type="image/png" href="/img/{icono}favicon.png">
<link rel="apple-touch-icon" href="/img/{icono}apple-touch-icon.png">
<link rel="preload" href="/fuentes/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/panel.css?v={_huella("panel.css")}">
<script>document.documentElement.classList.add("js")</script>
</head><body>
<header class="cab"><div class="in">
{cab}
</div></header>'''

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
    clearInterval(reloj);if(!resultado.hecho){resultado.hecho=1;window.ddCuenta&&ddCuenta("test_terminado")}var A=0,E=0,B=0;res.forEach(function(r,k){if(r===null)B++;else if(r===P[k].a)A++;else E++});
    var nota=(A-E/2)*10/P.length,dif=CORTE-nota;
    var tit=nota>=CORTE?"Con esta nota superarías el corte de 2026":dif<=1?"Te quedarías a "+coma(dif)+" del corte":"Te faltarían "+coma(dif)+" puntos para el corte";
    var txt=nota>=CORTE?"Buena señal, pero 20 preguntas son solo una muestra. Compruébalo con un examen entero.":dif<=1?"Así se pierden las plazas: por décimas. Mira en qué fallas para que no te pase.":"Aún hay margen, y saber dónde fallas es lo primero para recortarlo.";
    caja.textContent="";
    var np=el("p","tg-nota");np.setAttribute("aria-label","Tu nota: "+coma(nota));coma(nota).split("").forEach(function(ch){var c=el("span",ch===","?"coma":null,ch);c.setAttribute("aria-hidden","true");np.appendChild(c)});caja.appendChild(np);caja.appendChild(el("p","muted","Corte de la promoción 43: 7,05 · "+A+" aciertos, "+E+" fallos y "+B+" en blanco"));
    caja.appendChild(el("h2",null,tit));caja.appendChild(el("p","lead",txt));
    // la semana gratis, aquí mismo: el formulario viene en un <template> de la página y se copia al resultado
    var tpl=$("tg-plantilla");if(tpl&&window.activarPrueba){var pf=tpl.content.firstElementChild.cloneNode(true);caja.appendChild(el("h3",null,"Pruébala 7 días gratis"));caja.appendChild(el("p","muted","Deja tu email y normalmente entras al momento en Dos Décimas, con todos los tests, los exámenes oficiales y el simulacro."));caja.appendChild(pf);activarPrueba(pf)}
    var bt=el("div","btns");
    var w=el("a","btn s","Reta a un compañero");w.href="https://wa.me/?text="+encodeURIComponent("He sacado un "+coma(nota)+" en este test con preguntas reales del examen de Policía Nacional de 2026. ¿Tú llegarías al 7,05? https://ruvilab.es/dos-decimas/test-gratis/");w.target="_blank";w.rel="noopener";bt.appendChild(w);caja.appendChild(bt);
    var mal=P.map(function(q,k){return{q:q,r:res[k]}}).filter(function(x){return x.r!==x.q.a});
    if(mal.length){caja.appendChild(el("h3","tg-rev","Lo que has fallado o dejado en blanco"));mal.forEach(function(x){var c=el("div","tg-mal");c.appendChild(el("p","tg-mq",x.q.q));if(x.r!==null)c.appendChild(el("p","tg-no","Tu respuesta: "+"abc"[x.r]+") "+x.q.o[x.r]));c.appendChild(el("p","tg-si","Correcta: "+"abc"[x.q.a]+") "+x.q.o[x.q.a]));caja.appendChild(c)});
      caja.appendChild(el("p","muted","En la app, cada corrección trae además el porqué y lo que dice la ley."))}
    caja.scrollIntoView({block:"start"});
  }
  $("tg-go").onclick=function(){window.ddCuenta&&ddCuenta("test_empezado");fin=Date.now()+SEG*1000;reloj=setInterval(tiempo,1000);pregunta()};
})();
</script>""".replace("__PREGUNTAS__", _TG)
escribir("/dos-decimas/test-gratis/", cabeza_panel("¿Llegarías al 7,05? · Test gratis de Policía Nacional",
  "20 preguntas reales del examen de Policía Nacional de 2026, sin registro. Compara tu nota con el corte de 7,05.", "/dos-decimas/test-gratis/", og="dosdecimas-test-og.jpg")
+ """
<main>
<section class="tg"><div class="in"><div class="tg-in" id="tg">
  <h1>¿Llegarías al 7,05?</h1>
  <p class="sub">Ese fue el corte del examen de 2026. Comprueba cómo vas con 20 preguntas reales de ese examen, puntuadas igual: −0,5 por fallo y sin penalizar el blanco.</p>
  <ul class="lista"><li><b>10 minutos</b>, al ritmo del examen</li><li><b>Sin registro:</b> no pedimos datos ni guardamos tus respuestas</li><li>Al acabar, tu nota y las respuestas correctas de lo que falles</li></ul>
  <div class="btns"><button class="btn btn-p" type="button" id="tg-go">Empezar el test</button></div>
  <p class="peq suave">Preguntas 5, 10, 15… hasta la 100 del modelo A del examen del 26-09-2026, con las respuestas de la plantilla publicada. El resultado es orientativo: 20 preguntas son solo una muestra.</p>
</div></div></section>
</main>
""" + pie("dd", _TG_JS, PRUEBA_JS.replace("<script>", '<template id="tg-plantilla">' + dd_form("test") + "</template><script>", 1)))

# /opositores/ fue la primera dirección de Dos Décimas: se mantiene para que no se rompan los enlaces ya compartidos.
# GitHub Pages no hace redirecciones de servidor, así que se hace desde la propia página.
# ---------- Dos Décimas: página a la que vuelve Stripe después de pagar ----------
escribir("/dos-decimas/gracias/", cabeza_panel("Pago completado · Dos Décimas",
  "Tu pago de Dos Décimas se ha completado. Entra en la app con el mismo email con el que has pagado.", "/dos-decimas/gracias/", noindex=True)
+ f"""
<main>
<section class="texto-pag"><div class="in"><div>
  <h1>¡Ya estás dentro!</h1>
  <p class="lead">Tu pago se ha completado y Stripe te enviará el recibo a tu email. Para entrar por primera vez:</p>
  <ol class="lista-pasos">
    <li><h2>Pulsa «Entrar en Dos Décimas»</h2><p>Se abre la app en <b>{DD_APP.replace('https://', '')}</b>. Guárdala en favoritos o añádela a la pantalla de inicio del móvil.</p></li>
    <li><h2>Elige «Primera vez»</h2><p>Escribe <b>el mismo email con el que has pagado</b>.</p></li>
    <li><h2>Crea tu contraseña</h2><p>Te llega un correo con un enlace o un código. Ábrelo, elige tu contraseña y a por las décimas.</p></li>
  </ol>
  <a class="btn btn-p" href="{DD_APP}">Entrar en Dos Décimas</a>
  <p class="peq suave" style="margin-top:24px">¿No te llega el correo? Mira en spam o escríbenos a <a href="mailto:{DD_CORREO}">{DD_CORREO}</a>.</p>
</div></div></section>
</main>
""" + pie("dd"))

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
escribir("/aviso-legal/", cabeza_panel("Aviso legal · Ruvï", "Titular, contacto y condiciones de uso de la web de Ruvï.", "/aviso-legal/", marca="ruvi")
+ f'''
<main><section class="texto-pag legal"><div class="in"><div>
<h1>Aviso legal</h1>
<p class="suave">Última actualización: 31 de octubre de 2026</p>
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
</div></div></section></main>''' + pie("ruvi"))

# ---------------------------------------------------------------- Privacidad y cookies
escribir("/privacidad/", cabeza_panel("Privacidad y cookies · Ruvï", "Cómo trata Ruvï los datos de quien visita ruvilab.es, le escribe o se apunta a la lista de espera. Sin cookies ni seguimiento.", "/privacidad/", marca="ruvi")
+ f'''
<main><section class="texto-pag legal"><div class="in"><div>
<h1>Privacidad y cookies</h1>
<p class="suave">Última actualización: 10 de noviembre de 2026</p>
<p class="resumen"><b>En pocas palabras:</b> esta web no usa cookies ni publicidad, y no te sigue: solo cuenta cuántas visitas hay, sin saber de quién son. Solo tratamos tus datos si nos escribes, nos llamas o pides la semana gratis de Dos Décimas, y solo para eso.</p>
<h2>Responsable</h2>
<p>Alejandro Ruiz Barreda, titular de la marca Ruvï (más datos en el <a href="/aviso-legal/">aviso legal</a>). Contacto para privacidad: <a href="mailto:privacidad@ruvilab.es">privacidad@ruvilab.es</a>.</p>
<h2>Qué datos tratamos y para qué</h2>
<ul>
<li><b>Si nos escribes</b> a {CORREO}, por WhatsApp o nos llamas: tu nombre, tu email, el nombre de tu academia y lo que nos cuentes. Los usamos para contestarte y, si lo pides, para enseñarte la app y prepararte un presupuesto. Base legal: tu petición y las medidas previas a un contrato (artículo 6.1.b del RGPD).</li>
<li><b>Si pides la semana gratis de Dos Décimas</b>: tu nombre y tu email, para darte acceso a la app durante 7 días, y de qué página lo pediste. Base legal: tu petición (artículo 6.1.b del RGPD). Para evitar abusos del formulario guardamos durante dos días una huella irreversible de la conexión desde la que se pide (no la dirección IP) y, si tu solicitud se queda en espera, tu nombre y tu email hasta darte el alta o, como máximo, 30 días. Base legal: nuestro interés legítimo en proteger el servicio (artículo 6.1.f). Además, para saber qué canales funcionan, guardamos tu respuesta a «¿Dónde nos viste?», si la contestas. Base legal: nuestro interés legítimo (artículo 6.1.f); no se usa para publicidad ni se cede a nadie. Desde ese momento tus datos se rigen por la <a href="{DD_APP}/privacidad.html">política de privacidad de Dos Décimas</a>.</li>
<li><b>Contador de visitas de Dos Décimas</b>: en las páginas de Dos Décimas sumamos 1 a un contador por día, página y acción (visita, test gratis empezado o terminado, formulario enviado, botón pulsado) y por procedencia general (Instagram, TikTok, Google, directo…). Es solo un número: no guarda tu dirección IP, no te identifica, no usa cookies ni deja nada en tu aparato. Lo usamos para saber qué páginas funcionan.</li>
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
<tr><td>Supabase</td><td>Base de datos de Dos Décimas (semana gratis, lista de espera y contador anónimo de visitas)</td><td>Unión Europea</td></tr>
<tr><td>ImprovMX</td><td>Reenvío de los correos que nos mandas</td><td>Estados Unidos</td></tr>
<tr><td>Google (Gmail)</td><td>Buzón donde leemos y contestamos los correos</td><td>Unión Europea y Estados Unidos</td></tr>
<tr><td>WhatsApp (Meta)</td><td>Mensajes si nos escribes por WhatsApp</td><td>Unión Europea y Estados Unidos</td></tr>
</table></div>
<p>Las transferencias fuera de la Unión Europea se amparan en el Marco de Privacidad de Datos UE-EE. UU. o en las cláusulas contractuales tipo de la Comisión Europea. No vendemos ni cedemos tus datos a nadie.</p>
<h2>Tus derechos</h2>
<p>Puedes pedir acceder a tus datos, corregirlos, borrarlos, limitar su uso, oponerte o llevártelos escribiendo a <a href="mailto:privacidad@ruvilab.es">privacidad@ruvilab.es</a>. Si crees que no los respetamos, puedes reclamar ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es" rel="noopener">www.aepd.es</a>).</p>
<h2>Cookies</h2>
<p>Esta web no instala cookies ni usa herramientas de analítica o publicidad de terceros. El contador de visitas de Dos Décimas es nuestro, anónimo y no guarda nada en tu aparato. Las letras y las imágenes se cargan desde la propia web, sin pedir nada a otros servicios. El formulario de la semana gratis solo se conecta con nuestra base de datos cuando lo envías, y tampoco usa cookies. Por eso no verás ningún aviso de cookies.</p>
<h2>La app Plantilla de Repaso</h2>
<p>Los datos de los alumnos dentro de la app se rigen por su propia <a href="{APP}/privacidad.html">política de privacidad</a>.</p>
</div></div></section></main>''' + pie("ruvi"))

# ---------------------------------------------------------------- 404
(R / "404.html").write_text(cabeza_panel("Página no encontrada · Ruvï", "Esta página no existe.", "/404", marca="ruvi", noindex=True) + '''
<main><section class="texto-pag"><div class="in"><div>
<h1>Esta página no existe</h1>
<p class="lead">Puede que el enlace esté mal escrito o que la página se haya movido.</p>
<div class="btns" style="margin-top:32px;display:flex;flex-wrap:wrap;gap:10px"><a class="btn btn-p" href="/">Ir al inicio</a><a class="btn btn-s" href="/dos-decimas/">Ver Dos Décimas</a></div>
</div></div></section></main>''' + pie("ruvi"), encoding="utf-8")
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

# ---------------------------------------------------------------- Dos Décimas (la portada con el móvil)
# Estilos en panel.css y móviles 3D en dd-movil.js (cabecera en cabeza_panel).
# _movil: uno o dos móviles; en pantallas, «dd» es la pantalla de resultado que dibuja dd-movil.js
# (la que se mueve con la barra de la nota) y lo demás son capturas de /img/.
def _movil(pantallas, alt, sin_js):
    doble = " doble" if len(pantallas) > 1 else ""
    datos = ",".join(p if p == "dd" else f"/img/{p}?v={_huella('/img/' + p)}" for p in pantallas)
    return f'<div class="movil{doble}" data-pantallas="{datos}" data-alt="{alt}"><div class="movil-dom">{sin_js}</div><div class="movil-3d"></div></div>'
_MOVIL_JS = f'<script src="/dd-movil.js?v={_huella("dd-movil.js")}" defer></script>'

VIAS = [
  ("pregunta", "Pregunta", "app-pregunta-dd.png", "La lupa te marca los «NO» y los «salvo». Si no lo tienes claro, pulsas «Dudo».",
   "Una pregunta tipo test en la app con la lupa activada: en el enunciado resalta «no», «ni» y «salvo»; debajo, tres opciones, el cronómetro y los botones Dudo y Dejar en blanco"),
  ("resultado", "Resultado", "app-resultado.png", "Tu nota con −0,5 por fallo y si arriesgar te ha sumado o restado.",
   "Resultado de un test: un 7 sobre 10, aciertos, errores y preguntas en blanco, y cuántos puntos le ha sumado arriesgar en las que dudaba"),
  ("cuaderno", "Mi cuaderno", "app-cuaderno.png", "Cada fallo con la respuesta buena, el porqué y el artículo, y un botón para repetir solo esas.",
   "Mi cuaderno: un test con su nota, 7 aciertos y 3 errores, y una pregunta fallada con la respuesta dada, la correcta y el porqué"),
  ("temas", "Temas", "app-temas.png", "Del tema más flojo al más fuerte. Tocas uno y lo practicas.",
   "Pantalla «Cómo vas en cada tema»: cada tema con su porcentaje de acierto y su barra, del más flojo al más fuerte"),
  ("fisicas", "Físicas", "app-fisicas.png", "Metes tus marcas de circuito, dominadas (o barra, si eres mujer) y 1.000 m. Te da los puntos de cada prueba con el baremo de la convocatoria, tu media y lo que te falta, y te dibuja cómo mejoras.",
   "Pantalla Físicas de la app: tu evolución de 5,00 a 8,00 de media en 63 días, un gráfico de barras con los puntos de antes y de ahora en circuito, dominadas y carrera, y cada prueba con lo que ha mejorado"),
]
def _vias(vias=None):
    vias = vias or VIAS
    botones = "".join(f'<li><button type="button" class="via" data-via="{k}" aria-pressed="{"true" if i == 0 else "false"}"><span class="n">{i + 1:02d}</span><span class="que">{n}</span><span class="para">{p}</span></button></li>' for i, (k, n, _, p, _a) in enumerate(vias))
    oculto = ' aria-hidden="true"'
    imgs = "".join(f'<img src="/img/{img}" data-via="{k}" data-alt="{a}" alt="{a if i == 0 else ""}"{"" if i == 0 else oculto} class="{"activa" if i == 0 else ""}" width="780" height="1496" loading="lazy">' for i, (k, _, img, _p, a) in enumerate(vias))
    return botones, imgs
_VIAS_BOTONES, _VIAS_IMGS = _vias()

def _tarifas_nueva():
    f = TARIFA_FUNDADOR
    filas = [f'''<li class="tarifa fundador"><span class="plan">Fundador</span><span class="precio">{f["precio"]}<small>{f["periodo"]}</small></span>
      <span class="det">Solo para las {f["plazas"]} primeras personas, para siempre mientras sigas suscrito. Después, 10,99 € al mes.</span>
      <a class="btn" href="{f["enlace"]}" rel="noopener">Quiero este precio</a></li>''']
    for t in TARIFAS_DD:
        sale = f'Sale a {t["al_mes"]} al mes (<b>{t["ahorro"]}</b>). ' if t["al_mes"] else ""
        clase = "tarifa dest" if t.get("destacada") else "tarifa"
        boton = "btn btn-p" if t.get("destacada") else "btn btn-s"
        filas.append(f'''<li class="{clase}"><span class="plan">{t["nombre"]}</span><span class="precio">{t["precio"]}<small>{t["periodo"]}</small></span>
      <span class="det">{sale}{t["nota"]}</span><a class="{boton}" href="{t["enlace"]}" rel="noopener">Elegir</a></li>''')
    return "".join(filas)

VIAS_JS = """<script>
(function(){
  // Vías: cada fila elige qué pantalla de la app se ve
  var bs=document.querySelectorAll(".via"),pant=document.querySelector(".pantalla");if(!bs.length||!pant)return;
  bs.forEach(function(b){b.addEventListener("click",function(){
    bs.forEach(function(o){o.setAttribute("aria-pressed",o===b)});
    pant.classList.add("cambia");setTimeout(function(){pant.classList.remove("cambia")},260);
    pant.querySelectorAll("img").forEach(function(i){var si=i.dataset.via===b.dataset.via;i.classList.toggle("activa",si);i.alt=si?i.dataset.alt:"";if(si){i.removeAttribute("aria-hidden");i.loading="eager"}else i.setAttribute("aria-hidden","true")});
    // en el móvil la pantalla queda encima de la lista: si no se ve, se sube hasta ella
    var r=pant.getBoundingClientRect();if(matchMedia("(max-width:900px)").matches&&(r.top<70||r.bottom>innerHeight))pant.scrollIntoView({block:"center",behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"});
  })});
})();
</script>"""

# Tarifas plegadas: se abren con el botón grande «Ver tarifas» (sin JavaScript se ven abiertas)
TARIFAS_JS = """<script>
(function(){
  var b=document.getElementById("ver-tarifas"),l=document.getElementById("lista-tarifas");if(!b||!l)return;
  l.classList.add("plegada");
  b.addEventListener("click",function(){
    var abrir=b.getAttribute("aria-expanded")!=="true";
    b.setAttribute("aria-expanded",abrir);b.querySelector(".vt-txt").textContent=abrir?"Ocultar tarifas":"Ver tarifas";
    l.classList.toggle("plegada",!abrir);
    if(abrir)setTimeout(function(){var r=l.getBoundingClientRect();if(r.bottom>innerHeight)scrollBy({top:Math.min(r.top-90,r.bottom-innerHeight+24),behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"})},380);
  });
})();
</script>"""

# vídeo de la portada: sin sonido hasta que se pide; si el sistema pide menos movimiento, no arranca solo
PV_JS = """<script>
(function(){var v=document.getElementById("pv"),b=document.getElementById("pv-sonido");if(!v)return;
if(window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches){v.removeAttribute("autoplay");v.pause();v.controls=true;}
if(b)b.addEventListener("click",function(){v.muted=!v.muted;if(!v.muted){v.currentTime=0;v.play();}b.setAttribute("aria-pressed",String(!v.muted));b.textContent=v.muted?"Activar sonido":"Quitar sonido";});
})();
</script>"""

# anclas de la página antigua (anuncios, mensajes, el test gratis) que ahora tienen otro nombre
ANCLAS_JS = """<script>
(function(){var m={"#precio":"#planes","#entrar":"#prueba","#decimas":"#empezar"};if(m[location.hash])location.replace(m[location.hash])})();
</script>"""

_cab_nueva = cabeza_panel("Dos Décimas · Tests de Policía Nacional",
  "Dos Décimas: tests de Policía Nacional (Escala Básica) a nivel de examen, comprobados con la ley vigente del BOE. Hechos por un opositor que se quedó a dos décimas del corte.", "/dos-decimas/")

escribir("/dos-decimas/", _cab_nueva + f"""
<main>
<section class="portada"><div class="in">
  <div class="cabeza con-video">
    <div class="cabeza-txt">
      <h1>Me quedé fuera por dos décimas.</h1>
    </div>
    <div class="portada-video">
      <video id="pv" autoplay muted loop playsinline preload="metadata" poster="/img/dosdecimas-presentacion.jpg" width="1920" height="1080" aria-label="Vídeo de Dos Décimas con todas las funciones de la app: tests por tema, lupa de negaciones, el porqué de cada fallo, repaso de 5 minutos, Mis trampas, el simulacro de fin de semana, El Atestado, los exámenes oficiales y las físicas"><source src="/video/dosdecimas-presentacion-movil.mp4" type="video/mp4" media="(max-width: 700px)"><source src="/video/dosdecimas-presentacion.mp4" type="video/mp4"></video>
      <button class="pv-sonido" id="pv-sonido" type="button" aria-pressed="false">Activar sonido</button>
    </div>
  </div>
  <div class="entrada">
    <div>
      <p class="sub">Saqué un 6,85 y el corte fue un {DD_CORTE}. Dos Décimas te enseña <b>dónde pierdes las tuyas</b>, para que a ti no te pase.</p>
      <p class="mas"><a class="enlace" href="/dos-decimas/test-gratis/">Haz el test gratis de 20 preguntas</a></p>
    </div>
    <div class="alta alta-cta" id="empezar">
      <p class="ac-tit">Pruébala <em>7 días gratis</em></p>
      <p class="ac-txt">Con todo incluido y sin tarjeta. Solo te pedimos tu nombre y tu email.</p>
      <a class="btn btn-p" href="#prueba">Empezar mis 7 días gratis</a>
    </div>
  </div>
</div></section>

<section class="sec vias" id="como"><div class="in">
  <div class="cabeza-sec ent"><h2 class="titulo gira">Dónde se van <em>tus décimas</em></h2><p class="gira">Un banco de preguntas te dice que has fallado. Dos Décimas te dice por qué y no te deja fallar lo mismo otra vez.</p></div>
  <div class="cuerpo">
    <div>
      <ul class="lista-vias">{_VIAS_BOTONES}</ul>
      <p class="ademas">Y además: <b>Mis trampas</b> (en qué tipo de pregunta caes), <b>repaso de 5 minutos</b> al día con tus fallos y <b>12 exámenes oficiales</b> desde 2015 con su corte.</p>
    </div>
    <div class="pantalla" aria-live="polite"><div class="vidrio">{_VIAS_IMGS}</div></div>
  </div>
</div></section>

<section class="sec simu"><div class="in">
  <div class="cabeza-sec ent"><h2 class="titulo gira">Un simulacro <em>cada fin de semana</em></h2><p class="gira">Como el día del examen: un intento y sin repetir.</p></div>
  <ul class="salidas ent">
    <li class="gira"><span class="hora"><span class="rotulo">VIE</span><span class="rotulo">14:00</span></span><span class="destino">Simulacro<small>100 preguntas y 50 minutos</small></span><span class="estado"><span class="rotulo cobre">Abre</span></span></li>
    <li class="gira"><span class="hora"><span class="rotulo">DOM</span><span class="rotulo">21:00</span></span><span class="destino">Tu nota, la media y el corte<small>Al cerrar ves si habrías pasado</small></span><span class="estado"><span class="rotulo">Cierra</span></span></li>
  </ul>
  <p class="nota-sim ent"><span class="gira">Cuando cierre, tienes en la app la corrección de tus fallos y de las que dejaste en blanco, con el porqué de cada una.</span></p>
</div></section>

<section class="sec" id="planes"><div class="in">
  <div class="cabeza-sec ent"><h2 class="titulo gira">Tarifas</h2><p class="gira">Todas incluyen lo mismo. Sin permanencia y con el IVA incluido.</p></div>
  <button type="button" class="ver-tarifas" id="ver-tarifas" aria-expanded="false" aria-controls="lista-tarifas"><span class="vt-txt">Ver tarifas</span><span class="vt-desde">Desde {TARIFA_FUNDADOR["precio"]} al mes</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 9l7 7 7-7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="square"/></svg></button>
  <div class="lista-tarifas" id="lista-tarifas"><div class="lt-in">
  <ul class="tarifas">{_tarifas_nueva()}</ul>
  <p class="pie-tarifas">Pago seguro con Stripe: tus datos de tarjeta no llegan a nosotros. Tienes 14 días para desistir y te devolvemos todo. Paga con el mismo email con el que pruebas la app.</p>
  </div></div>
</div></section>

<section class="sec cierre simu" id="prueba"><div class="in">
  <div class="cuerpo">
    <div class="ent">
      <h2 class="titulo gira">Pruébala <em>7 días gratis</em></h2>
      <ol class="pasos">
        <li><span>Deja tu nombre y tu email aquí.</span></li>
        <li><span>Te llega un correo: pulsa el botón.</span></li>
        <li><span>Elige tu contraseña. Ya estás dentro.</span></li>
      </ol>
    </div>
    <div>{dd_form("web", "Quiero mi semana gratis")}</div>
  </div>
</div></section>

<section class="sec faq" id="faq"><div class="in">
  <div class="cuerpo">
    <div class="ent"><h2 class="titulo gira">Preguntas</h2><p class="suave" style="margin-top:20px">¿Otra duda? Escribe a <a href="mailto:{DD_CORREO}">{DD_CORREO}</a>.</p></div>
    <div>{FAQ_DD_HTML}</div>
  </div>
</div></section>
</main>
""" + pie("dd", PRUEBA_JS, VIAS_JS, PV_JS, TARIFAS_JS, ANCLAS_JS))

# /dos-decimas/nueva/ fue la ruta de prueba: lleva a la de verdad
escribir("/dos-decimas/nueva/", '''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="robots" content="noindex"><link rel="canonical" href="https://ruvilab.es/dos-decimas/">
<title>Dos Décimas</title><script>location.replace("/dos-decimas/"+location.hash)</script></head>
<body><p><a href="/dos-decimas/">Ir a Dos Décimas</a></p></body></html>''')


# ---------------------------------------------------------------- Ruvï y Plantilla de Repaso, con el mismo móvil
_INICIO_PR = f'<img src="/img/app-inicio.png" alt="Pantalla de inicio de Plantilla de Repaso" width="780" height="1496">'

escribir("/", cabeza_panel("Ruvï · Herramientas para preparar oposiciones",
  "Ruvï crea herramientas para preparar oposiciones: Plantilla de Repaso, tests tipo examen para academias, y Dos Décimas, tests de Policía Nacional para opositores por libre.", "/", marca="ruvi", actual="/")
+ f'''
<main>
<section class="portada"><div class="in">
  <div class="cabeza">
    <div class="cabeza-txt">
      <h1>Herramientas para preparar oposiciones.</h1>
      <p class="sub">Ruvï hace herramientas para preparar Policía Nacional: <b>una para academias</b> y otra para quien se prepara por su cuenta. Con preguntas como las del examen, corregidas con la ley.</p>
      <div class="btns accesos"><a class="btn btn-s" href="/plantilla-repaso/">Tengo una academia</a><a class="btn btn-p" href="/dos-decimas/">Me preparo por mi cuenta</a></div>
    </div>
    {_movil(["app-inicio.png", "dd"], "Dos móviles: Plantilla de Repaso para academias y Dos Décimas para quien se prepara por su cuenta", _INICIO_PR)}
  </div>
</div></section>

<section class="sec"><div class="in">
  <div class="cabeza-sec ent"><h2 class="titulo gira">Una para cada <em>forma de prepararse</em></h2></div>
  <ul class="rutas">
    <li class="ruta ent"><span class="n gira">01</span><div class="gira"><span class="rotulo">Para academias</span><h3>Plantilla de Repaso</h3><p>Vuestro temario convertido en tests tipo examen para vuestros alumnos, con las preguntas revisadas por vuestros profesores y corregidas con la ley.</p></div>
      <div class="btns gira"><a class="btn btn-s" href="/plantilla-repaso/">Ver Plantilla de Repaso</a></div></li>
    <li class="ruta ent"><span class="n gira">02</span><div class="gira"><span class="rotulo cobre">Para opositores</span><h3>Dos Décimas</h3><p>Para quien prepara Policía Nacional por su cuenta: tests de los 45 temas comprobados con el BOE vigente, exámenes oficiales y simulacros. Desde 7,99 € al mes.</p></div>
      <div class="btns gira"><a class="btn btn-p" href="/dos-decimas/">Ver Dos Décimas</a><a class="btn btn-s" href="/dos-decimas/test-gratis/">Test gratis</a></div></li>
  </ul>
</div></section>

<section class="sec simu" id="nosotros"><div class="in">
  <div class="cuerpo-dos ent"><h2 class="titulo gira">Quiénes <em>somos</em></h2>
    <p class="grande-txt gira">Soy Alejandro, opositor a Policía Nacional. Creé Plantilla de Repaso al echar en falta tests que se parecieran de verdad al examen, y después Dos Décimas para quien se prepara por su cuenta. Junto a mi socio, miembro de las Fuerzas y Cuerpos de Seguridad del Estado que también pasó por la oposición, fundamos Ruvï.</p></div>
</div></section>

{contacto("¿Tienes una academia?", "Te enseñamos la app con tus temas en una videollamada de 15 minutos. El primer mes es gratis.")}
</main>
''' + pie("ruvi", _MOVIL_JS))

VIAS_PR = [
  ("inicio", "Inicio", "app-inicio.png", "El alumno ve sus fallos por repasar, su última nota y elige tema, número de preguntas y corrección.",
   "Pantalla de inicio del alumno: aviso de fallos por repasar, su última nota, preguntas hechas, y la elección de tema, número de preguntas y corrección"),
  ("pregunta", "Pregunta", "app-pregunta.png", "Tres opciones, −0,5 por fallo y cronómetro: las mismas reglas con las que se van a examinar.",
   "Una pregunta tipo test en la app, con tres opciones, el cronómetro y los botones Dudo y Dejar en blanco"),
  ("resultado", "Resultado", "app-resultado.png", "Su nota y si arriesgar en las que dudaba le ha sumado o restado.",
   "Resultado de un test: un 7 sobre 10, aciertos, errores y preguntas en blanco, y cuántos puntos le ha sumado arriesgar en las que dudaba"),
]
_PR_BOTONES, _PR_IMGS = _vias(VIAS_PR)
PACKS = [("Tests", "Tests tipo examen, corrección con la ley y cuaderno de fallos.", False),
         ("Plus", "Todo lo de Tests, más el plan semanal y las preguntas más falladas.", False),
         ("Completo", "Todo lo anterior, más el ranking de alumnos y las pruebas físicas.", True)]
_PACKS = "".join(f'<li class="tarifa pack{" dest" if d else ""}"><span class="plan">{n}</span><span class="det">{t}</span></li>' for n, t, d in PACKS)
FAQ_PR = [
  ("¿Sirve para otras oposiciones?", "Sí. Adaptamos el temario, el número de opciones, la penalización y el tiempo al examen de cada oposición tipo test."),
  ("¿Podemos probarla con nuestro temario?", "Durante el mes gratis practicáis con preguntas de vuestros temas sacadas del BOE, revisadas por vuestros profesores. Si os quedáis, preparamos las de vuestro propio temario."),
  ("¿Qué datos se guardan de los alumnos?", "Nombre, email y progreso, en la Unión Europea. Cada academia solo ve los suyos y firmamos un contrato de protección de datos."),
  ("¿Y si una pregunta tiene un error?", "Los alumnos avisan desde la propia pregunta y la corregimos para todos."),
  ("¿Nuestro temario se usa para otras academias?", "No. El temario y sus preguntas son solo vuestros."),
]
_FAQ_PR = "".join(f'<details><summary>{q}{_MAS}</summary><p>{r}</p></details>' for q, r in FAQ_PR)

escribir("/plantilla-repaso/", cabeza_panel("Plantilla de Repaso · Tu temario, convertido en examen",
  "Tests tipo examen para tu academia, de Policía Nacional o cualquier oposición tipo test: preguntas de tus temas, revisadas por tus profesores, con corrección con la ley.", "/plantilla-repaso/", marca="ruvi", og="plantilla-og.jpg", actual="/plantilla-repaso/")
+ f'''
<main>
<section class="portada"><div class="in">
  <div class="cabeza">
    <div class="cabeza-txt">
      <h1>Tu temario, convertido en examen.</h1>
      <p class="sub">Hacemos las preguntas de vuestros temas y vuestros alumnos practican en una app, como el día del examen. Nació para Policía Nacional y se adapta a <b>cualquier oposición tipo test</b>.</p>
      <div><div class="btns accesos"><a class="btn btn-p" href="#contacto">Pruébala con tus temas</a><a class="btn btn-s" href="#demo">Ver la demo · 1 min</a></div>
        <p class="suave" style="margin-top:14px">Primer mes gratis y sin permanencia.</p></div>
    </div>
    {_movil(["app-inicio.png"], "Pantalla de inicio de Plantilla de Repaso: los fallos por repasar, la última nota y el tema para practicar", _INICIO_PR)}
  </div>
</div></section>

<section class="sec vias" id="app"><div class="in">
  <div class="cabeza-sec ent"><h2 class="titulo gira">Como el <em>examen real</em></h2><p class="gira">Practican con las mismas reglas con las que se van a examinar, en el móvil o el ordenador y sin instalar nada.</p></div>
  <div class="cuerpo">
    <div>
      <ul class="lista-vias">{_PR_BOTONES}</ul>
      <p class="ademas">Y además: <b>cada fallo corregido con la ley</b> (la buena, el porqué y el artículo), <b>«Dudo»</b> para saber si arriesgar les suma y un <b>cuaderno de fallos</b> que les devuelve lo que fallaron hasta que lo aciertan.</p>
    </div>
    <div class="pantalla" aria-live="polite"><div class="vidrio">{_PR_IMGS}</div></div>
  </div>
</div></section>

<section class="sec simu video" id="demo"><div class="in">
  <div class="cabeza-sec ent"><h2 class="titulo gira">La demo, <em>en un minuto</em></h2></div>
  <video class="v-ancho" controls playsinline preload="none" poster="/img/demo-horizontal.jpg" width="1280" height="720" aria-label="Demo de Plantilla de Repaso en vídeo horizontal"><source src="/video/demo-horizontal.mp4" type="video/mp4"></video>
  <video class="v-movil" controls playsinline preload="none" poster="/img/demo-vertical.jpg" width="720" height="1280" aria-label="Demo de Plantilla de Repaso en vídeo vertical"><source src="/video/demo-vertical.mp4" type="video/mp4"></video>
</div></section>

<section class="sec" id="como"><div class="in">
  <div class="cabeza-sec ent"><h2 class="titulo gira">Cómo <em>funciona</em></h2></div>
  <ol class="lista-pasos tres">
    <li><h3>Elegís los temas</h3><p>Preguntas del BOE o de vuestro temario, que es solo vuestro.</p></li>
    <li><h3>Vuestros profesores las revisan</h3><p>Ninguna llega a los alumnos sin su visto bueno.</p></li>
    <li><h3>Los alumnos practican</h3><p>Les damos de alta con su email y empiezan.</p></li>
  </ol>
</div></section>

<section class="sec simu"><div class="in">
  <div class="cabeza-sec ent"><h2 class="titulo gira">Tres <em>packs</em></h2><p class="gira">El precio depende del número de alumnos.</p></div>
  <ul class="tarifas">{_PACKS}</ul>
  <div class="btns" style="margin-top:24px"><a class="btn btn-p" href="#contacto">Pide las tarifas</a></div>
</div></section>

<section class="sec faq"><div class="in">
  <div class="cuerpo">
    <div class="ent"><h2 class="titulo gira">Preguntas</h2></div>
    <div>{_FAQ_PR}</div>
  </div>
</div></section>

{contacto("Pruébala un mes gratis", "Te la enseñamos con tus temas en una videollamada de 15 minutos.")}
</main>
''' + pie("ruvi", VIAS_JS, _MOVIL_JS))


# ---------------------------------------------------------------- Mapa del sitio y robots (para Google)
# Solo las páginas públicas que queremos que salgan en buscadores.
_MAPA = ["/", "/dos-decimas/", "/dos-decimas/test-gratis/", "/plantilla-repaso/", "/aviso-legal/", "/privacidad/"]
(R / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
  + "".join(f"  <url><loc>https://ruvilab.es{u}</loc></url>\n" for u in _MAPA) + "</urlset>\n", encoding="utf-8")
(R / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /tarifas/\nDisallow: /dos-decimas/gracias/\n\nSitemap: https://ruvilab.es/sitemap.xml\n", encoding="utf-8")
print("escrito sitemap.xml y robots.txt")
