/* Dos Décimas · aviso de cookies y píxel de Meta (26-11-2026)
   - Sin el número del píxel (PIXEL vacío) no hace NADA: ni aviso ni carga.
   - El píxel solo se carga si la persona pulsa «Aceptar». Si rechaza o no contesta, no se carga nada de Meta.
   - La elección se guarda en este aparato y se puede cambiar con cualquier enlace que lleve data-cookies.
   - Eventos que manda (solo con permiso): PageView, TestTerminado, FormularioEmpezado, InitiateCheckout (pulsa tarifas),
     Lead + CompleteRegistration (alta de la semana gratis). Nunca manda el email ni el nombre. */
(function(){
  var PIXEL="1168015229207719";   // ← número del píxel «Dos Décimas · web ruvilab.es» (Administrador de eventos de Meta)
  var CLAVE="dd-cookies-v1";
  var h=location.hostname,local=/^(localhost|127\.0\.0\.1|192\.168\.)/.test(h);
  if(local){var pp=/[?&]pixelprueba=(\d{6,20})/.exec(location.search);if(pp)PIXEL=pp[1]}
  if(!PIXEL)return;
  if(!local&&h!=="ruvilab.es"&&h!=="www.ruvilab.es")return;

  var cola=[],activo=false;
  var MAPA={quiz_terminado:["c","TestTerminado"],test_terminado:["c","TestTerminado"],form_empezado:["c","FormularioEmpezado"],clic_tarifa:["s","InitiateCheckout"],form_enviado:["s","Lead","CompleteRegistration"]};
  function manda(ev){var m=MAPA[ev];if(!m||!window.fbq)return;for(var i=1;i<m.length;i++){m[0]==="s"?fbq("track",m[i]):fbq("trackCustom",m[i])}}
  // Engancha el contador propio de la web: cada evento que ya contamos también va al píxel (si hay permiso)
  var orig=window.ddCuenta;
  window.ddCuenta=function(ev){try{orig&&orig(ev)}catch(e){}if(activo)manda(ev);else cola.push(ev)};

  function leer(){try{return localStorage.getItem(CLAVE)}catch(e){return null}}
  function guardar(v){try{localStorage.setItem(CLAVE,v)}catch(e){}}
  function cargar(){if(activo)return;activo=true;
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version="2.0";n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,"script","https://connect.facebook.net/en_US/fbevents.js");
    fbq("init",PIXEL);fbq("track","PageView");
    cola.splice(0).forEach(manda);
  }

  // Aviso como el de cualquier web: barra abajo a todo lo ancho, «Rechazar», «Configurar» y «Aceptar» (mismo tamaño)
  var css=".dd-ck{position:fixed;left:0;right:0;bottom:0;z-index:9999;background:var(--papel-0,#FFFCF8);color:var(--tinta,#1A1614);border-top:1px solid var(--raya,#D9D2CA);box-shadow:0 -6px 24px var(--sombra-c,rgba(26,22,20,.16));font:400 .9rem/1.45 var(--ft,system-ui,sans-serif)}"+
    ".dd-ck-in{max-width:1120px;margin:0 auto;padding:14px 16px;display:flex;gap:12px 24px;align-items:center;flex-wrap:wrap}"+
    ".dd-ck-t{flex:1 1 420px;margin:0}.dd-ck-t b{display:block;margin-bottom:2px;font-size:.95rem}.dd-ck a{color:var(--cobre-t,#8C5233)}"+
    ".dd-ck-b{display:flex;gap:8px;flex:0 1 auto;flex-wrap:wrap}"+
    ".dd-ck button{min-height:42px;padding:0 18px;border-radius:8px;border:1px solid var(--tinta,#1A1614);background:transparent;color:var(--tinta,#1A1614);font:700 .9rem var(--ft,system-ui,sans-serif);cursor:pointer;transition:background-color .15s}"+
    ".dd-ck button:hover{background:var(--papel-2,#ECE7E1)}.dd-ck button:focus-visible{outline:3px solid var(--cobre-t,#8C5233);outline-offset:2px}"+
    ".dd-ck-conf{flex:1 1 100%;border-top:1px solid var(--raya,#D9D2CA);padding-top:10px;display:grid;gap:8px}.dd-ck-conf[hidden]{display:none}"+
    ".dd-ck-conf label{display:flex;gap:10px;align-items:flex-start}.dd-ck-conf input{width:18px;height:18px;margin-top:2px;accent-color:var(--cobre-t,#8C5233)}"+
    "@media (max-width:560px){.dd-ck-b{flex:1 1 100%}.dd-ck-b button{flex:1 1 0;padding:0 8px}}"+
    "@media (prefers-reduced-motion:reduce){.dd-ck button{transition:none}}";
  function aviso(){
    if(document.querySelector(".dd-ck"))return;
    if(!document.getElementById("dd-ck-css")){var st=document.createElement("style");st.id="dd-ck-css";st.textContent=css;document.head.appendChild(st)}
    var d=document.createElement("div");d.className="dd-ck";d.setAttribute("role","region");d.setAttribute("aria-label","Aviso de cookies");
    d.innerHTML="<div class=\"dd-ck-in\"><p class=\"dd-ck-t\"><b>Esta web usa cookies</b>Usamos cookies propias, necesarias para que la web funcione, y, si las aceptas, cookies de terceros (Meta) para medir nuestros anuncios y mostrarte publicidad relacionada. Puedes aceptarlas, rechazarlas o configurarlas. <a href=\"/privacidad/#cookies\">Más información</a></p>"+
      "<div class=\"dd-ck-b\"><button type=\"button\" class=\"no\">Rechazar</button><button type=\"button\" class=\"cf\" aria-expanded=\"false\">Configurar</button><button type=\"button\" class=\"si\">Aceptar</button></div>"+
      "<div class=\"dd-ck-conf\" hidden><label><input type=\"checkbox\" checked disabled> <span><b>Necesarias</b>: guardan tu elección sobre las cookies. Siempre activas.</span></label>"+
      "<label><input type=\"checkbox\" class=\"pub\"> <span><b>Publicidad (Meta)</b>: miden qué anuncios de Facebook e Instagram te han traído.</span></label>"+
      "<div><button type=\"button\" class=\"gd\">Guardar mi elección</button></div></div></div>";
    var cerrar=function(si){guardar(si?"si":"no");d.remove();if(si)cargar();else cola.length=0};
    d.querySelector(".si").onclick=function(){cerrar(true)};
    d.querySelector(".no").onclick=function(){cerrar(false)};
    d.querySelector(".cf").onclick=function(){var c=d.querySelector(".dd-ck-conf");c.hidden=!c.hidden;this.setAttribute("aria-expanded",String(!c.hidden))};
    d.querySelector(".gd").onclick=function(){cerrar(d.querySelector(".pub").checked)};
    document.body.appendChild(d);
  }
  document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("[data-cookies]");if(!a)return;e.preventDefault();
    if(activo){guardar("no");location.reload();return}   // quitar el permiso: se guarda «no» y se recarga sin píxel
    aviso()});
  var v=leer();
  if(v==="si")cargar();
  else if(v!=="no"){document.readyState==="loading"?document.addEventListener("DOMContentLoaded",aviso):aviso()}
})();
