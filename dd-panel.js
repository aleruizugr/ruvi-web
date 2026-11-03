/* Dos Décimas · el panel de tablillas de la portada.
   El panel de HTML (.panel-dom) siempre está y es la versión sin 3D (sin WebGL, sin JS o con «reducir movimiento»).
   Si hay WebGL, se monta encima el panel en 3D con Three.js: cada tablilla gira de verdad y pasa por las letras de en medio.
   La barra de la nota cambia las filas 3 y 5, como la calculadora de antes. */
(function () {
  "use strict";
  var raiz = document.querySelector(".panel");
  if (!raiz) return;
  var COLS = 16, CORTE = 7.05;
  var filas = JSON.parse(raiz.dataset.filas);              // [[texto, "crema"|"cobre"], ...]
  var celdasDom = raiz.querySelectorAll(".panel-dom .fila-p");
  var quieto = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var barra = document.getElementById("nota"), verNota = document.getElementById("nota-ver"), salida = document.getElementById("salida");

  var coma = function (x) { return x.toFixed(2).replace(".", ","); };
  var relleno = function (izq, der) { var h = COLS - izq.length - der.length; return izq + " ".repeat(Math.max(1, h)) + der; };
  var pl = function (k, a, b) { return k + " " + (k === 1 ? a : b); };

  // ---------- la cuenta (cada acierto +0,10; cada fallo −0,05; pasar un fallo a blanco recupera 0,05) ----------
  function cuenta(v) {
    var d = Math.round((CORTE - v) * 100) / 100;
    if (d <= 0) return { fila3: relleno("TU NOTA", coma(v)), fila5: relleno("DENTRO", "+" + coma(-d)),
      frase: "Con un <b>" + coma(v) + "</b> habrías superado el corte de 2026. Ahora, a no perder ni una décima." };
    var ac = Math.ceil(d / 0.1 - 1e-9), bl = Math.ceil(d / 0.05 - 1e-9);
    return { fila3: relleno("TU NOTA", coma(v)), fila5: relleno("TE FALTAN", coma(d)),
      frase: "Te faltan <b>" + coma(d) + "</b>: " + pl(ac, "acierto", "aciertos") + " más o " + pl(bl, "fallo", "fallos") + " dejados en blanco." };
  }

  // ---------- panel de HTML ----------
  function pintarDom(i, texto) {
    var cs = celdasDom[i].children;
    for (var c = 0; c < COLS; c++) cs[c].textContent = (texto[c] || " ").trim() ? texto[c] : " ";
  }

  var panel3d = null;
  function ponerFila(i, texto) {
    filas[i][0] = texto;
    pintarDom(i, texto);
    if (panel3d) panel3d.fila(i, texto);
  }
  function alMover() {
    var v = barra.value / 100, r = cuenta(v);
    verNota.textContent = coma(v);
    barra.setAttribute("aria-valuetext", coma(v));
    ponerFila(2, r.fila3); ponerFila(4, r.fila5);
    salida.innerHTML = r.frase;
  }
  if (barra) {
    barra.addEventListener("input", alMover);
    barra.addEventListener("input", function () { if (sonido.on) sonido.listo(); }, { once: false });
  }

  // ---------- sonido: un «clac» sintetizado por tablilla, solo si alguien lo activa ----------
  var sonido = { on: false, ctx: null, buf: null, ultimo: 0,
    listo: function () {
      if (this.ctx) return;
      var C = window.AudioContext || window.webkitAudioContext; if (!C) return;
      this.ctx = new C(); var n = Math.floor(this.ctx.sampleRate * 0.012);
      this.buf = this.ctx.createBuffer(1, n, this.ctx.sampleRate);
      var d = this.buf.getChannelData(0);
      for (var k = 0; k < n; k++) d[k] = (Math.random() * 2 - 1) * Math.pow(1 - k / n, 6);
    },
    clac: function () {
      if (!this.on || !this.ctx) return;
      var t = this.ctx.currentTime; if (t - this.ultimo < 0.014) return; this.ultimo = t;
      var s = this.ctx.createBufferSource(), g = this.ctx.createGain(), f = this.ctx.createBiquadFilter();
      f.type = "bandpass"; f.frequency.value = 1800 + Math.random() * 1400; f.Q.value = 1.4;
      g.gain.value = 0.16; s.buffer = this.buf; s.connect(f); f.connect(g); g.connect(this.ctx.destination); s.start();
    } };
  var botonSonido = document.getElementById("sonido");
  if (botonSonido) botonSonido.addEventListener("click", function () {
    sonido.on = !sonido.on; botonSonido.setAttribute("aria-pressed", sonido.on);
    botonSonido.textContent = sonido.on ? "Sonido: sí" : "Sonido: no";
    if (sonido.on) { sonido.listo(); if (sonido.ctx.state === "suspended") sonido.ctx.resume(); if (panel3d) panel3d.repasar(); }
  });

  // ---------- panel en 3D ----------
  function hayWebGL() {
    try { var c = document.createElement("canvas"); return !!(window.WebGLRenderingContext && (c.getContext("webgl") || c.getContext("experimental-webgl"))); }
    catch (e) { return false; }
  }

  function montar3d() {
    var T = window.THREE, caja = raiz.querySelector(".panel-3d");
    var ORDEN = " ABCDEFGHIJKLMNÑOPQRSTUVWXYZÉÍÓÚ0123456789,.+-:€%";
    var ACOLS = 10, AROWS = Math.ceil(ORDEN.length / ACOLS), GW = 128, GH = 184;
    var W = 1, H = GH / GW, HUECO_X = 0.1, HUECO_Y = 0.2, RAYA = 0.014;

    function atlas(fondo, tinta) {
      var cv = document.createElement("canvas"); cv.width = GW * ACOLS; cv.height = GH * AROWS;
      var x = cv.getContext("2d");
      x.fillStyle = fondo; x.fillRect(0, 0, cv.width, cv.height);
      x.fillStyle = tinta; x.textAlign = "center"; x.textBaseline = "middle";
      x.font = '800 ' + Math.round(GH * 0.74) + 'px "Archivo"';
      if ("fontStretch" in x) x.fontStretch = "condensed";
      for (var i = 0; i < ORDEN.length; i++) {
        var cx = (i % ACOLS) * GW + GW / 2, cy = Math.floor(i / ACOLS) * GH + GH / 2 + GH * 0.04;
        x.fillText(ORDEN[i], cx, cy);
      }
      var t = new T.CanvasTexture(cv); t.anisotropy = 4; t.encoding = T.sRGBEncoding;
      return new T.MeshStandardMaterial({ map: t, roughness: 0.5, metalness: 0.05 });
    }
    var mats = { crema: atlas("#1D1D1D", "#F2EADF"), cobre: atlas("#C98A5B", "#0A0A0A") };

    // cada media tablilla es un plano con sus propias coordenadas de textura
    function medio() {
      var g = new T.PlaneGeometry(W, H / 2 - RAYA / 2);
      return g;
    }
    function glifo(geo, ch, mitad) {
      var i = Math.max(0, ORDEN.indexOf(ch)), col = i % ACOLS, row = Math.floor(i / ACOLS);
      var u0 = col / ACOLS, u1 = (col + 1) / ACOLS, vb = 1 - (row + 1) / AROWS, vt = 1 - row / AROWS, vm = (vb + vt) / 2;
      var a = mitad === "arriba" ? [vm, vt] : [vb, vm], uv = geo.attributes.uv;
      // PlaneGeometry: vértices 0 (arriba izq), 1 (arriba der), 2 (abajo izq), 3 (abajo der)
      uv.setXY(0, u0, a[1]); uv.setXY(1, u1, a[1]); uv.setXY(2, u0, a[0]); uv.setXY(3, u1, a[0]);
      uv.needsUpdate = true;
    }

    var escena = new T.Scene(), tablero = new T.Group(); escena.add(tablero);
    var ancho = COLS * W + (COLS - 1) * HUECO_X, alto = filas.length * H + (filas.length - 1) * HUECO_Y;
    var carcasa = new T.Mesh(new T.BoxGeometry(ancho + 0.9, alto + 0.9, 0.5), new T.MeshStandardMaterial({ color: new T.Color(0x0e0e0e).convertSRGBToLinear(), roughness: 0.9 }));
    carcasa.position.z = -0.3; tablero.add(carcasa);

    var celdas = [];
    filas.forEach(function (f, r) {
      for (var c = 0; c < COLS; c++) {
        var m = mats[f[1]], x = -ancho / 2 + W / 2 + c * (W + HUECO_X), y = alto / 2 - H / 2 - r * (H + HUECO_Y);
        var arriba = new T.Mesh(medio(), m), abajo = new T.Mesh(medio(), m);
        arriba.position.set(x, y + H / 4 + RAYA / 4, 0); abajo.position.set(x, y - H / 4 - RAYA / 4, 0);
        var eje = new T.Group(); eje.position.set(x, y, 0.004);
        var frente = new T.Mesh(medio(), m), dorso = new T.Mesh(medio(), m);
        frente.position.y = H / 4 + RAYA / 4; dorso.position.y = H / 4 + RAYA / 4; dorso.rotation.x = Math.PI;
        eje.add(frente); eje.add(dorso); eje.visible = false;
        tablero.add(arriba); tablero.add(abajo); tablero.add(eje);
        var cel = { arriba: arriba, abajo: abajo, eje: eje, frente: frente, dorso: dorso, ch: " ", meta: " ", paso: null, espera: 0 };
        [arriba, abajo].forEach(function (p, k) { glifo(p.geometry, " ", k ? "abajo" : "arriba"); });
        celdas.push(cel);
      }
    });

    escena.add(new T.AmbientLight(0xffffff, 0.42));
    var luz = new T.DirectionalLight(0xfff2e6, 0.62); luz.position.set(-4, 8, 10); escena.add(luz);
    var luz2 = new T.DirectionalLight(new T.Color(0xc98a5b).convertSRGBToLinear(), 0.25); luz2.position.set(8, -4, 6); escena.add(luz2);

    var render = new T.WebGLRenderer({ antialias: true, alpha: true, powerPreference: "high-performance" });
    render.outputEncoding = T.sRGBEncoding;
    render.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    var lienzo = render.domElement; lienzo.setAttribute("aria-hidden", "true"); caja.appendChild(lienzo);
    var cam = new T.PerspectiveCamera(28, 1, 0.1, 200);

    function encajar() {
      var w = caja.clientWidth, h = caja.clientHeight; if (!w || !h) return;
      render.setSize(w, h, false); cam.aspect = w / h;
      var t = Math.tan(T.MathUtils.degToRad(cam.fov / 2));
      var dAncho = (ancho + 1.2) / (2 * t * cam.aspect), dAlto = (alto + 1.2) / (2 * t);
      cam.position.set(0, 0, Math.max(dAncho, dAlto)); cam.lookAt(0, 0, 0); cam.updateProjectionMatrix();
    }
    encajar();
    if ("ResizeObserver" in window) new ResizeObserver(encajar).observe(caja); else addEventListener("resize", encajar);

    // una tablilla avanza letra a letra por ORDEN hasta su meta (como las de verdad); como mucho 10 pasos
    var PASO = 72;
    function siguiente(a, b) {
      var ia = ORDEN.indexOf(a), ib = ORDEN.indexOf(b); if (ia < 0) ia = 0; if (ib < 0) ib = 0;
      var dist = (ib - ia + ORDEN.length) % ORDEN.length;
      if (dist > 10) ia = (ib - 10 + ORDEN.length) % ORDEN.length;
      return ORDEN[(ia + 1) % ORDEN.length];
    }
    function empezar(cel, t) {
      var sig = siguiente(cel.ch, cel.meta);
      glifo(cel.arriba.geometry, sig, "arriba");      // la nueva mitad de arriba ya asoma detrás
      glifo(cel.frente.geometry, cel.ch, "arriba");   // la que cae: la vieja de arriba...
      glifo(cel.dorso.geometry, sig, "abajo");        // ...con la nueva de abajo por detrás
      cel.eje.rotation.x = 0; cel.eje.visible = true;
      cel.paso = { sig: sig, t: t };
    }
    // va por el reloj, no por los fotogramas: si el móvil se atasca, las tablillas se ponen al día de golpe
    function avanzar(cel, ahora) {
      for (var vueltas = 0; vueltas < 12; vueltas++) {
        if (!cel.paso) {
          if (cel.ch === cel.meta || ahora < cel.espera) return;
          empezar(cel, Math.max(cel.espera, cel.fin || 0));
        }
        var k = (ahora - cel.paso.t) / PASO;
        if (k < 1) { cel.eje.rotation.x = -Math.PI * k * k; return; }   // cae acelerando, como con gravedad
        cel.ch = cel.paso.sig; cel.fin = cel.paso.t + PASO; cel.paso = null;
        glifo(cel.abajo.geometry, cel.ch, "abajo"); cel.eje.visible = false;
        if (vueltas === 0) sonido.clac();
      }
    }

    var mx = 0, my = 0, rx = 0, ry = 0, desplaza = 0;
    addEventListener("pointermove", function (e) { if (e.pointerType === "mouse") { mx = e.clientX / innerWidth - 0.5; my = e.clientY / innerHeight - 0.5; } }, { passive: true });
    addEventListener("scroll", function () { var r = caja.getBoundingClientRect(); desplaza = Math.max(0, Math.min(1, -r.top / Math.max(1, r.height))); }, { passive: true });

    var visible = true, corriendo = false, ultimo = performance.now();
    function bucle(ahora) {
      var dt = Math.min(48, ahora - ultimo); ultimo = ahora;
      for (var i = 0; i < celdas.length; i++) avanzar(celdas[i], ahora);
      var a = 1 - Math.pow(0.9, dt / 16);
      ry += (mx * 0.16 - ry) * a; rx += (-0.07 + my * 0.08 + desplaza * 0.5 - rx) * a;
      tablero.rotation.set(rx, ry, 0);
      render.render(escena, cam);
      if (visible && !document.hidden) requestAnimationFrame(bucle); else corriendo = false;
    }
    function arrancar() { if (!corriendo && visible && !document.hidden) { corriendo = true; ultimo = performance.now(); requestAnimationFrame(bucle); } }
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; arrancar(); }).observe(caja);
    document.addEventListener("visibilitychange", arrancar);

    var api = {
      fila: function (r, texto, retraso) {
        var ahora = performance.now();
        for (var c = 0; c < COLS; c++) {
          var cel = celdas[r * COLS + c], ch = (texto[c] || " ").toUpperCase();
          if (ORDEN.indexOf(ch) < 0) ch = " ";
          if (cel.meta !== ch) { cel.meta = ch; cel.espera = ahora + (retraso || 0) + c * 28; }
        }
        arrancar();
      },
      repasar: function () { filas.forEach(function (f, r) { api.fila(r, f[0], r * 60); }); }
    };
    // entrada: el panel empieza en blanco y las filas caen de arriba abajo
    filas.forEach(function (f, r) { api.fila(r, f[0], 350 + r * 260); });
    raiz.classList.add("gl");
    arrancar();
    return api;
  }

  if (!quieto && hayWebGL()) {
    var cargar = function () {
      var s = document.createElement("script");
      s.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";
      s.crossOrigin = "anonymous"; s.referrerPolicy = "no-referrer";
      s.onload = function () {
        var fuente = document.fonts && document.fonts.load ? document.fonts.load('800 100px "Archivo"') : Promise.resolve();
        fuente.catch(function () {}).then(function () { try { panel3d = montar3d(); } catch (e) { raiz.classList.remove("gl"); } });
      };
      document.head.appendChild(s);
    };
    if (document.readyState === "complete") cargar(); else addEventListener("load", cargar);
  }
  if (barra) alMover();
})();
