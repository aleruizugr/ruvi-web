/* Las portadas (Dos Décimas, Plantilla de Repaso y Ruvï): uno o dos móviles con pantallas de las apps.
   data-pantallas en .movil dice qué lleva cada móvil: «dd» es la pantalla de resultado de Dos Décimas,
   que se dibuja en un lienzo 2D y cambia con la barra de la nota; cualquier otra cosa es una captura (/img/…).
   Si hay WebGL y no se pide «reducir movimiento», los móviles se montan en 3D con Three.js. */
(function () {
  "use strict";
  var caja = document.querySelector(".movil");
  if (!caja) return;
  var CORTE = 7.05, barra = document.getElementById("nota"), verNota = document.getElementById("nota-ver"), salida = document.getElementById("salida");
  var quieto = matchMedia("(prefers-reduced-motion: reduce)").matches;

  var coma = function (x) { return x.toFixed(2).replace(".", ","); };
  var pl = function (k, a, b) { return k + " " + (k === 1 ? a : b); };

  // Aciertos, fallos y blancos de 100 preguntas que dan esa nota (−0,5 por fallo), partiendo de mi 75 · 13 · 12.
  function reparto(v) {
    var p = Math.round(v * 20), a = Math.min(75, Math.floor((100 + p) / 3));
    a = Math.max(a, Math.ceil(p / 2));
    var f = 2 * a - p;
    return { a: a, f: f, b: 100 - a - f };
  }
  function frase(v) {
    var d = Math.round((CORTE - v) * 100) / 100;
    if (d <= 0) return "Con un <b>" + coma(v) + "</b> habrías superado el corte de 2026. Ahora, a no perder ni una décima.";
    var ac = Math.ceil(d / 0.1 - 1e-9), bl = Math.ceil(d / 0.05 - 1e-9);
    return "Te faltan <b>" + coma(d) + "</b>: " + pl(ac, "acierto", "aciertos") + " más o " + pl(bl, "fallo", "fallos") + " dejados en blanco.";
  }

  // ---------- la pantalla (colores de la app) ----------
  var SW = 900, SH = Math.round(900 * 19.5 / 9), R = 120;
  var C = { fondo: "#F4F1EC", tarjeta: "#FFFFFF", linea: "#E6DFD6", tinta: "#2E2724", suave: "#6E625C", verde: "#1F9D5B", verdeT: "#16683D",
            pista: "#EFE7DF", rojo: "#B4232F", cobre: "#9A5B38", cobreT: "#F3E6DB", negro: "#0A0A0A" };
  var lienzo = document.createElement("canvas"); lienzo.width = SW; lienzo.height = SH;
  var x = lienzo.getContext("2d");
  var F = function (peso, px) { return peso + " " + px + 'px "Archivo", system-ui, sans-serif'; };

  function redondo(px, py, w, h, r) {
    x.beginPath(); x.moveTo(px + r, py); x.arcTo(px + w, py, px + w, py + h, r); x.arcTo(px + w, py + h, px, py + h, r);
    x.arcTo(px, py + h, px, py, r); x.arcTo(px, py, px + w, py, r); x.closePath();
  }
  // barra de estado e isla, encima de cualquier pantalla
  function barraEstado() {
    x.fillStyle = C.tinta; x.font = F(700, 38); x.textBaseline = "middle"; x.fillText("9:41", 92, 92);
    x.fillStyle = C.negro; redondo(SW / 2 - 135, 46, 270, 82, 41); x.fill();
    x.fillStyle = C.tinta; redondo(SW - 170, 78, 72, 30, 9); x.fill(); x.fillRect(SW - 94, 86, 6, 14);
  }
  // una captura de la app, a todo lo ancho y bajo la barra de estado
  function pintarCaptura(cv, im) {
    var guarda = x; x = cv.getContext("2d");
    x.clearRect(0, 0, SW, SH); x.save(); redondo(0, 0, SW, SH, R); x.clip();
    x.fillStyle = C.fondo; x.fillRect(0, 0, SW, SH);
    x.drawImage(im, 0, 140, SW, SW * im.naturalHeight / im.naturalWidth);
    x.fillStyle = C.fondo; x.fillRect(0, 0, SW, 140); barraEstado(); x.restore();
    x = guarda;
  }
  // v: nota que se ve (puede ir animándose); dentro: 0..1 para el paso a «dentro»
  function pintar(v, dentro) {
    var rp = reparto(v), d = Math.round((CORTE - v) * 100) / 100, ok = d <= 0;
    x.clearRect(0, 0, SW, SH);
    x.save(); redondo(0, 0, SW, SH, R); x.clip();
    x.fillStyle = C.fondo; x.fillRect(0, 0, SW, SH);
    barraEstado();
    // cabecera de la app
    x.textBaseline = "alphabetic";
    x.fillStyle = C.tinta; x.font = F(800, 46); x.fillText("Dos Décimas", 70, 236);
    x.fillStyle = C.suave; x.font = F(500, 34); x.fillText("Simulacro · 100 preguntas", 70, 286);
    // tarjeta
    var tx = 44, ty = 330, tw = SW - 88, th = SH - 330 - 70;
    x.fillStyle = C.tarjeta; redondo(tx, ty, tw, th, 52); x.fill();
    x.strokeStyle = C.linea; x.lineWidth = 3; x.stroke();
    x.fillStyle = C.suave; x.font = F(800, 30); x.fillText("RESULTADO", tx + 56, ty + 92);
    // anillo de la nota, con la marca del corte
    var cx = SW / 2, cy = ty + 420, ra = 230, gr = 44, a0 = -Math.PI / 2;
    x.lineCap = "butt"; x.lineWidth = gr;
    x.strokeStyle = C.pista; x.beginPath(); x.arc(cx, cy, ra, 0, Math.PI * 2); x.stroke();
    var col = ok ? C.verde : C.cobre;
    x.strokeStyle = col; x.beginPath(); x.arc(cx, cy, ra, a0, a0 + Math.PI * 2 * Math.max(0, Math.min(1, v / 10))); x.stroke();
    var ac = a0 + Math.PI * 2 * CORTE / 10, mx = Math.cos(ac), my = Math.sin(ac);
    x.strokeStyle = C.tinta; x.lineWidth = 8; x.beginPath();
    x.moveTo(cx + mx * (ra - gr / 2 - 16), cy + my * (ra - gr / 2 - 16)); x.lineTo(cx + mx * (ra + gr / 2 + 16), cy + my * (ra + gr / 2 + 16)); x.stroke();
    x.fillStyle = C.tinta; x.font = F(700, 30); x.textAlign = mx < 0 ? "right" : "left";
    x.fillText("corte 7,05", cx + mx * (ra + gr / 2 + 26), cy + my * (ra + gr / 2 + 26) + 10); x.textAlign = "center";
    x.font = F(800, 150); x.fillText(coma(v), cx, cy + 40);
    x.fillStyle = C.suave; x.font = F(700, 34); x.fillText("sobre 10", cx, cy + 96);
    x.textAlign = "left";
    // veredicto
    var vy = cy + ra + 150;
    x.fillStyle = ok ? C.verdeT : C.tinta; x.font = F(800, 64);
    x.fillText(ok ? "Dentro del corte" : "Fuera por " + coma(d), tx + 56, vy);
    if (ok && dentro > 0) {   // la marca de «dentro» se dibuja de un trazo
      var bx = tx + tw - 126, by = vy - 30, k = Math.min(1, dentro);
      x.fillStyle = C.verde; x.globalAlpha = k; x.beginPath(); x.arc(bx, by, 46, 0, Math.PI * 2); x.fill(); x.globalAlpha = 1;
      x.strokeStyle = "#fff"; x.lineWidth = 11; x.lineCap = "round"; x.lineJoin = "round"; x.beginPath();
      var p1 = [bx - 20, by + 2], p2 = [bx - 5, by + 17], p3 = [bx + 22, by - 14], t = k * 2;
      x.moveTo(p1[0], p1[1]);
      x.lineTo(p1[0] + (p2[0] - p1[0]) * Math.min(1, t), p1[1] + (p2[1] - p1[1]) * Math.min(1, t));
      if (t > 1) x.lineTo(p2[0] + (p3[0] - p2[0]) * (t - 1), p2[1] + (p3[1] - p2[1]) * (t - 1));
      x.stroke(); x.lineCap = "butt";
    }
    x.fillStyle = C.suave; x.font = F(500, 36);
    x.fillText(ok ? "Por encima del corte de 2026 por " + coma(-d) + "." : "El corte de 2026 fue un 7,05.", tx + 56, vy + 62);
    // aciertos · errores · en blanco
    var cw = (tw - 112 - 40) / 3, cyy = vy + 120, chh = 170;
    [[rp.a, "Aciertos", C.verdeT, C.fondo], [rp.f, "Errores", C.rojo, C.cobreT], [rp.b, "En blanco", C.tinta, C.fondo]].forEach(function (q, i) {
      var qx = tx + 56 + i * (cw + 20);
      x.fillStyle = q[3]; redondo(qx, cyy, cw, chh, 30); x.fill();
      if (i === 1) { x.strokeStyle = C.cobre; x.lineWidth = 3; x.stroke(); }
      x.fillStyle = q[2]; x.font = F(800, 66); x.fillText(String(q[0]), qx + 30, cyy + 82);
      x.fillStyle = C.suave; x.font = F(700, 30); x.fillText(q[1], qx + 30, cyy + 136);
    });
    x.fillStyle = C.suave; x.font = F(500, 32);
    x.fillText("Como en el examen: (" + rp.a + " − " + rp.f + " × 0,5) ÷ 100 × 10", tx + 56, cyy + chh + 66);
    // botón
    var by2 = ty + th - 160;
    x.fillStyle = C.cobre; redondo(tx + 56, by2, tw - 112, 108, 30); x.fill();
    x.fillStyle = "#fff"; x.font = F(800, 38); x.textAlign = "center";
    x.fillText(ok ? "Repasar los " + rp.f + " fallos" : "Ver dónde perdí las décimas", SW / 2, by2 + 68); x.textAlign = "left";
    x.restore();
  }

  // ---------- qué lleva cada móvil ----------
  var pantallas = (caja.dataset.pantallas || "dd").split(",").map(function (q) {
    q = q.trim(); if (q === "dd") return { dd: true, lienzo: lienzo, lista: Promise.resolve() };
    var cv = document.createElement("canvas"); cv.width = SW; cv.height = SH;
    var im = new Image(), p = { dd: false, lienzo: cv, img: im };
    p.lista = new Promise(function (ok) { im.onload = function () { pintarCaptura(cv, im); ok(); }; im.onerror = ok; });
    im.src = q; return p;
  });
  var conDD = pantallas.some(function (p) { return p.dd; });

  // ---------- estado: la nota que se pide y la que se ve, con el paso a «dentro» ----------
  var meta = barra ? barra.value / 100 : 6.85, vista = 5, dentro = 0, cambio = null, alPintar = null;
  function textos() {
    var v = meta;
    if (verNota) verNota.textContent = coma(v);
    if (barra) barra.setAttribute("aria-valuetext", coma(v));
    if (salida) salida.innerHTML = frase(v);
  }

  // ---------- sin 3D: la pantalla en un marco de móvil de HTML ----------
  function montarPlano() {
    var marco = caja.querySelector(".movil-dom"); marco.innerHTML = ""; caja.classList.add("plano");
    pantallas.forEach(function (p) { p.lienzo.setAttribute("role", "img"); p.lienzo.setAttribute("aria-label", caja.dataset.alt || "Pantalla de la app"); marco.appendChild(p.lienzo); });
    if (!conDD) return;
    vista = meta; dentro = 1; pintar(vista, dentro);
    alPintar = function () { vista = meta; dentro = 1; pintar(vista, dentro); };
  }

  // ---------- el móvil en 3D ----------
  function hayWebGL() {
    try { var c = document.createElement("canvas"); return !!(window.WebGLRenderingContext && (c.getContext("webgl") || c.getContext("experimental-webgl"))); }
    catch (e) { return false; }
  }
  function montar3d() {
    var T = window.THREE, sitio = caja.querySelector(".movil-3d");
    // medidas de un móvil de 6,1" (en cm)
    var W = 7.16, H = 14.76, D = 0.78, RC = 1.12, BEV = 0.06;
    function forma(w, h, r) {
      var s = new T.Shape(), a = -w / 2, b = -h / 2;
      s.moveTo(a + r, b); s.lineTo(a + w - r, b); s.quadraticCurveTo(a + w, b, a + w, b + r); s.lineTo(a + w, b + h - r);
      s.quadraticCurveTo(a + w, b + h, a + w - r, b + h); s.lineTo(a + r, b + h); s.quadraticCurveTo(a, b + h, a, b + h - r);
      s.lineTo(a, b + r); s.quadraticCurveTo(a, b, a + r, b); return s;
    }
    var escena = new T.Scene(), movil = new T.Group(), base = new T.Group();
    base.add(movil); escena.add(base);

    // reflejos: un estudio pequeño con tres focos, convertido en entorno
    var render = new T.WebGLRenderer({ antialias: true, alpha: true, powerPreference: "high-performance" });
    render.outputEncoding = T.sRGBEncoding; render.toneMapping = T.ACESFilmicToneMapping; render.toneMappingExposure = 1.05;
    render.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    var estudio = new T.Scene();
    estudio.add(new T.Mesh(new T.SphereGeometry(40, 32, 16), new T.MeshBasicMaterial({ color: 0x0c0c0c, side: T.BackSide })));
    [[0, 18, 6, 22, 6, 0xffffff, 2.2], [-20, 4, 4, 4, 26, 0xffffff, 1.4], [20, -2, -6, 4, 22, 0xc98a5b, 1.6]].forEach(function (f) {
      var m = new T.Mesh(new T.PlaneGeometry(f[3], f[4]), new T.MeshBasicMaterial({ color: new T.Color(f[5]).multiplyScalar(f[6]), side: T.DoubleSide }));
      m.position.set(f[0], f[1], f[2]); m.lookAt(0, 0, 0); estudio.add(m);
    });
    var pm = new T.PMREMGenerator(render); escena.environment = pm.fromScene(estudio, 0.02).texture; pm.dispose();

    var gCuerpo = new T.ExtrudeGeometry(forma(W - 2 * BEV, H - 2 * BEV, RC), { depth: D, bevelEnabled: true, bevelThickness: BEV * 2, bevelSize: BEV, bevelSegments: 6, curveSegments: 24 });
    var metal = new T.MeshPhysicalMaterial({ color: 0x2b2926, metalness: 0.92, roughness: 0.32, clearcoat: 0.4, clearcoatRoughness: 0.3 });
    var gCristal = new T.ShapeGeometry(forma(W - 0.08, H - 0.08, RC - 0.04), 24);
    var mCristal = new T.MeshPhysicalMaterial({ color: 0x050505, metalness: 0, roughness: 0.08, clearcoat: 1, clearcoatRoughness: 0.04 });
    var SWc = W - 0.62, SHc = SWc * SH / SW, gPantalla = new T.PlaneGeometry(SWc, SHc);
    var mBrillo = new T.MeshPhysicalMaterial({ color: 0x000000, transparent: true, opacity: 0.12, roughness: 0.05, metalness: 0, clearcoat: 1, envMapIntensity: 0.6 });
    var zCristal = D / 2 + BEV * 2 + 0.002, tex = null;
    function hacerMovil(p) {
      var g = new T.Group(), cuerpo = new T.Mesh(gCuerpo, metal); cuerpo.position.z = -D / 2; g.add(cuerpo);
      var cristal = new T.Mesh(gCristal, mCristal); cristal.position.z = zCristal; g.add(cristal);
      var t = new T.CanvasTexture(p.lienzo); t.encoding = T.sRGBEncoding; t.anisotropy = render.capabilities.getMaxAnisotropy();
      var pantalla = new T.Mesh(gPantalla, new T.MeshBasicMaterial({ map: t, transparent: true, toneMapped: false }));
      pantalla.position.z = zCristal + 0.003; g.add(pantalla);
      // un brillo muy suave sobre el cristal, que se mueve con el giro
      var brillo = new T.Mesh(gPantalla, mBrillo); brillo.position.z = zCristal + 0.005; g.add(brillo);
      // botones laterales
      [[-1, 3.2, 1.05], [-1, 1.7, 1.05], [-1, 4.4, 0.55], [1, 2.5, 1.6]].forEach(function (b) {
        var m = new T.Mesh(new T.BoxGeometry(0.12, b[2], 0.36), metal); m.position.set(b[0] * (W / 2 + 0.03), b[1], 0.02); g.add(m);
      });
      if (p.dd) tex = t; else p.lista.then(function () { t.needsUpdate = true; arrancar(); });
      return g;
    }
    // con dos móviles, el primero queda detrás y a la izquierda
    var N = pantallas.length, POS = N > 1 ? [[-3.1, 0.7, -2.2, 0.22], [3.0, -0.5, 0.6, 0]] : [[0, 0, 0, 0]];
    pantallas.forEach(function (p, i) { var g = hacerMovil(p), q = POS[i] || POS[0]; g.position.set(q[0], q[1], q[2]); g.rotation.y = q[3]; movil.add(g); });
    // sombra en el suelo (el móvil flota: es la única sombra de la página)
    var cs = document.createElement("canvas"); cs.width = cs.height = 128;
    var g = cs.getContext("2d"), rg = g.createRadialGradient(64, 64, 4, 64, 64, 64);
    rg.addColorStop(0, "rgba(0,0,0,.75)"); rg.addColorStop(1, "rgba(0,0,0,0)"); g.fillStyle = rg; g.fillRect(0, 0, 128, 128);
    var sombra = new T.Mesh(new T.PlaneGeometry(W * (N > 1 ? 3 : 1.7), W * 0.7), new T.MeshBasicMaterial({ map: new T.CanvasTexture(cs), transparent: true, depthWrite: false }));
    sombra.rotation.x = -Math.PI / 2; sombra.position.y = -H / 2 - 1.6; escena.add(sombra);

    escena.add(new T.AmbientLight(0xffffff, 0.15));
    var clave = new T.DirectionalLight(0xffffff, 0.8); clave.position.set(-6, 10, 12); escena.add(clave);
    var borde = new T.DirectionalLight(new T.Color(0xc98a5b).convertSRGBToLinear(), 1.4); borde.position.set(10, 2, -6); escena.add(borde);

    var lien3 = render.domElement; lien3.setAttribute("aria-hidden", "true"); sitio.appendChild(lien3);
    var cam = new T.PerspectiveCamera(26, 1, 0.1, 200);
    function encajar() {
      var w = sitio.clientWidth, h = sitio.clientHeight; if (!w || !h) return;
      render.setSize(w, h, false); cam.aspect = w / h;
      var t = Math.tan(T.MathUtils.degToRad(cam.fov / 2)), alto = H + 2.6 + (N > 1 ? 1.4 : 0), ancho = W + 3.4 + (N > 1 ? 6.6 : 0);
      cam.position.set(0, 0.6, Math.max(alto / (2 * t), ancho / (2 * t * cam.aspect)));
      cam.lookAt(0, -0.6, 0); cam.updateProjectionMatrix();
    }
    encajar();
    if ("ResizeObserver" in window) new ResizeObserver(encajar).observe(sitio); else addEventListener("resize", encajar);

    // movimiento: entrada, flotación, ratón, scroll y un pequeño «sí» con la cabeza al entrar en el corte
    var t0 = performance.now(), mx = 0, my = 0, rx = 0, ry = 0, desplaza = 0, salto = -1;
    addEventListener("pointermove", function (e) { if (e.pointerType === "mouse") { mx = e.clientX / innerWidth - 0.5; my = e.clientY / innerHeight - 0.5; } }, { passive: true });
    addEventListener("scroll", function () { var r = sitio.getBoundingClientRect(); desplaza = Math.max(0, Math.min(1, -r.top / Math.max(1, r.height))); }, { passive: true });
    alPintar = function (cruza) { if (cruza) salto = performance.now(); arrancar(); };

    var visible = true, corriendo = false, ultimo = t0, ultimaV = -1, ultimoD = -1;
    var suave = function (k) { return 1 - Math.pow(1 - k, 3); };
    function bucle(ahora) {
      var dt = Math.min(48, ahora - ultimo); ultimo = ahora;
      var e = Math.min(1, (ahora - t0) / 1500), ee = suave(e);
      // la nota corre hasta la pedida (en la entrada sube desde un 5)
      var objetivo = ahora - t0 < 500 ? 5 : meta;
      var dtr = Math.min(250, ahora - (bucle.antes || ahora)); bucle.antes = ahora;
      vista += (objetivo - vista) * (1 - Math.pow(0.86, dtr / 16)); if (Math.abs(objetivo - vista) < 0.004) vista = objetivo;
      var ok = vista >= CORTE - 1e-9; dentro = ok ? Math.min(1, dentro + dtr / 380) : 0;
      if (tex && (Math.abs(vista - ultimaV) > 0.0049 || dentro !== ultimoD)) { pintar(Math.round(vista * 100) / 100, dentro); tex.needsUpdate = true; ultimaV = vista; ultimoD = dentro; }
      var a = 1 - Math.pow(0.9, dt / 16), s = (ahora - t0) / 1000;
      ry += ((N > 1 ? -0.3 : -0.42) + mx * 0.3 - ry) * a; rx += (0.1 + my * 0.12 - desplaza * 0.35 - rx) * a;
      var cabeza = 0;
      if (salto > 0) { var k = (ahora - salto) / 700; if (k < 1) cabeza = Math.sin(k * Math.PI * 2) * 0.07 * (1 - k); else salto = -1; }
      movil.rotation.set(rx + cabeza, ry * ee + (1 - ee) * -1.1, 0.04);
      movil.position.y = (1 - ee) * -5 + Math.sin(s * 1.1) * 0.12;
      sombra.material.opacity = 0.55 * ee - Math.sin(s * 1.1) * 0.05;
      render.render(escena, cam);
      var quieta = e >= 1 && vista === meta && (dentro === 0 || dentro === 1);
      if (visible && !document.hidden) requestAnimationFrame(bucle); else corriendo = false;
      return quieta;
    }
    function arrancar() { if (!corriendo && visible && !document.hidden) { corriendo = true; ultimo = performance.now(); requestAnimationFrame(bucle); } }
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; arrancar(); }).observe(sitio);
    document.addEventListener("visibilitychange", arrancar);
    caja.classList.add("gl");
    arrancar();
  }

  // ---------- la barra ----------
  if (barra) barra.addEventListener("input", function () {
    var antes = meta; meta = barra.value / 100; textos();
    var cruza = antes < CORTE && meta >= CORTE;
    if (cruza && navigator.vibrate) try { navigator.vibrate(12); } catch (e) {}
    if (alPintar) alPintar(cruza);
  });
  textos();

  var fuente = document.fonts && document.fonts.load ? document.fonts.load('800 100px "Archivo"') : Promise.resolve();
  if (!quieto && hayWebGL()) {
    var cargar = function () {
      var s = document.createElement("script");
      s.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";
      s.crossOrigin = "anonymous"; s.referrerPolicy = "no-referrer";
      s.onload = function () { fuente.catch(function () {}).then(function () { try { montar3d(); } catch (e) { caja.classList.remove("gl"); montarPlano(); } }); };
      s.onerror = function () { fuente.catch(function () {}).then(montarPlano); };
      document.head.appendChild(s);
    };
    if (document.readyState === "complete") cargar(); else addEventListener("load", cargar);
  } else fuente.catch(function () {}).then(function () { return Promise.all(pantallas.map(function (p) { return p.lista; })); }).then(montarPlano);
})();
