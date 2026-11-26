/* Dos Décimas · aviso de cookies y píxel de Meta (26-11-2026)
   - Sin el número del píxel (PIXEL vacío) no hace NADA: ni aviso ni carga.
   - El píxel solo se carga si la persona pulsa «Aceptar». Si rechaza o no contesta, no se carga nada de Meta.
   - La elección se guarda en este aparato y se puede cambiar con cualquier enlace que lleve data-cookies.
   - Eventos que manda (solo con permiso): PageView, TestTerminado, FormularioEmpezado, InitiateCheckout (pulsa tarifas),
     Lead + CompleteRegistration (alta de la semana gratis). Nunca manda el email ni el nombre. */
(function(){
  var PIXEL="";   // ← número del píxel «Dos Décimas · web ruvilab.es» (Administrador de eventos de Meta)
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

  var css=".dd-ck{position:fixed;left:12px;right:12px;bottom:12px;z-index:9999;max-width:560px;margin:0 auto;background:var(--noche,#0D0B0A);color:var(--crema,#F2EADF);border:1px solid var(--borde-n,#2B241F);border-radius:14px;padding:16px 16px 14px;box-shadow:0 10px 30px var(--sombra-f,rgba(0,0,0,.55));font:400 .95rem/1.45 var(--ft,system-ui,sans-serif)}"+
    ".dd-ck p{margin:0 0 12px}.dd-ck a{color:var(--cobre,#D9A276)}"+
    ".dd-ck .dd-ck-b{display:flex;gap:8px;flex-wrap:wrap}"+
    ".dd-ck button{flex:1 1 140px;min-height:44px;border-radius:10px;border:1px solid var(--cobre,#D9A276);font:700 .95rem var(--ft,system-ui,sans-serif);cursor:pointer;transition:transform .15s,background-color .15s}"+
    ".dd-ck .si{background:var(--cobre,#D9A276);color:var(--tinta,#1A1614)}.dd-ck .no{background:transparent;color:var(--crema,#F2EADF)}"+
    ".dd-ck button:active{transform:scale(.98)}.dd-ck button:focus-visible{outline:3px solid var(--cobre,#D9A276);outline-offset:2px}"+
    "@media (prefers-reduced-motion:reduce){.dd-ck button{transition:none}}";
  function aviso(){
    if(document.querySelector(".dd-ck"))return;
    if(!document.getElementById("dd-ck-css")){var st=document.createElement("style");st.id="dd-ck-css";st.textContent=css;document.head.appendChild(st)}
    var d=document.createElement("div");d.className="dd-ck";d.setAttribute("role","dialog");d.setAttribute("aria-label","Cookies");
    d.innerHTML="<p><b>¿Nos dejas medir los anuncios?</b> Con tu permiso usamos el píxel de Meta (cookies de Facebook e Instagram) para saber qué anuncios traen a opositores y no enseñártelos de más. Sin él, la web funciona igual. <a href=\"/privacidad/#cookies\">Más información</a></p>"+
      "<div class=\"dd-ck-b\"><button type=\"button\" class=\"no\">Rechazar</button><button type=\"button\" class=\"si\">Aceptar</button></div>";
    d.querySelector(".si").onclick=function(){guardar("si");d.remove();cargar()};
    d.querySelector(".no").onclick=function(){guardar("no");d.remove();cola.length=0};
    document.body.appendChild(d);
  }
  document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("[data-cookies]");if(!a)return;e.preventDefault();
    if(activo){guardar("no");location.reload();return}   // quitar el permiso: se guarda «no» y se recarga sin píxel
    aviso()});
  var v=leer();
  if(v==="si")cargar();
  else if(v!=="no"){document.readyState==="loading"?document.addEventListener("DOMContentLoaded",aviso):aviso()}
})();
