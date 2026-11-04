/* La portada de Stellaria (generar.py escribe el marcado). Sin dependencias.

   1. La estrella: la primera partida del juego, jugable en la web. El octaedro y sus ocho
      huecos; cada pieza llega girada: se gira con un toque a un lado u otro (o con ← →) y se
      lanza deslizando hacia arriba (o con ↑). Si no está bien orientada, rebota. Mientras
      nadie juega, la estrella se monta sola; con «menos movimiento», se queda quieta y entera.
      <div data-estrella data-textos='{"invita": …, "pieza": "… {n} …", …}'>
        <canvas tabindex="0"></canvas>
        <div class="consola" hidden>              (sin JavaScript no sirve: se queda oculta)
          <p data-estado aria-live="polite"></p>
          <button data-accion="jugar">…</button>
          <div data-mandos hidden> izq · lanza · der </div>
          <button data-accion="otra" hidden>…</button>
        </div>
      </div>
      Al completarla, las tiendas marcadas con data-brilla destellan un momento.
   2. Los bucles: los vídeos con data-bucle se cargan y se reproducen solo mientras se ven. */
(function () {
  "use strict";
  var raiz = document.querySelector("[data-estrella]");
  if (!raiz) return;
  var lienzo = raiz.querySelector("canvas");
  var g = lienzo.getContext("2d");
  var TX = {};
  try { TX = JSON.parse(raiz.getAttribute("data-textos") || "{}"); } catch (e) { TX = {}; }
  var estado = raiz.querySelector("[data-estado]");
  var mandos = raiz.querySelector("[data-mandos]");
  var bJugar = raiz.querySelector('[data-accion="jugar"]');
  var bOtra = raiz.querySelector('[data-accion="otra"]');
  var poco = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var tactil = window.matchMedia && window.matchMedia("(pointer: coarse)").matches;
  TX.ayuda = (tactil ? TX.ayuda_toque : TX.ayuda_teclas) || TX.ayuda || "";
  var consola = raiz.querySelector(".consola");
  if (consola) consola.hidden = false;

  // ---------------------------------------------------------------- colores de la casa y del juego
  var TINTA = "#211F1C", PAPEL = [246, 242, 230], BANDA = "rgba(150,140,118,0.20)";
  var COLORES = [[232, 87, 60], [244, 205, 106], [164, 122, 85], [243, 230, 190],
                 [87, 80, 74], [247, 134, 106], [184, 200, 210], [201, 170, 126]];
  var ORO = [226, 174, 72];
  var LUZ = norm([-0.5, 0.7, 0.5]);

  // ---------------------------------------------------------------- álgebra mínima
  function norm(v) { var n = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / n, v[1] / n, v[2] / n]; }
  function resta(a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; }
  function suma(a, b) { return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]; }
  function esc(a, k) { return [a[0] * k, a[1] * k, a[2] * k]; }
  function cruz(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
  function punto(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  // cuaterniones [w, x, y, z]
  function qMul(a, b) {
    return [a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3],
            a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2],
            a[0] * b[2] - a[1] * b[3] + a[2] * b[0] + a[3] * b[1],
            a[0] * b[3] + a[1] * b[2] - a[2] * b[1] + a[3] * b[0]];
  }
  function qEje(eje, ang) { var s = Math.sin(ang / 2), e = norm(eje); return [Math.cos(ang / 2), e[0] * s, e[1] * s, e[2] * s]; }
  function qRot(q, v) {
    var u = [q[1], q[2], q[3]], w = q[0];
    var t = esc(cruz(u, v), 2);
    return suma(suma(v, esc(t, w)), cruz(u, t));
  }
  function qNorm(q) { var n = Math.hypot(q[0], q[1], q[2], q[3]) || 1; return [q[0] / n, q[1] / n, q[2] / n, q[3] / n]; }
  function qDesde(a, b) {           // el giro más corto que lleva a hasta b (unitarios)
    var d = punto(a, b);
    if (d < -0.9999) { var o = Math.abs(a[0]) < 0.9 ? [1, 0, 0] : [0, 1, 0]; return qEje(cruz(a, o), Math.PI); }
    var c = cruz(a, b);
    return qNorm([1 + d, c[0], c[1], c[2]]);
  }
  function qSlerp(a, b, t) {
    var d = a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3];
    if (d < 0) { b = [-b[0], -b[1], -b[2], -b[3]]; d = -d; }
    if (d > 0.9995) return qNorm([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t, a[3] + (b[3] - a[3]) * t]);
    var th = Math.acos(d), s = Math.sin(th), k0 = Math.sin((1 - t) * th) / s, k1 = Math.sin(t * th) / s;
    return [a[0] * k0 + b[0] * k1, a[1] * k0 + b[1] * k1, a[2] * k0 + b[2] * k1, a[3] * k0 + b[3] * k1];
  }
  function suave(t) { t = Math.max(0, Math.min(1, t)); return 1 - Math.pow(1 - t, 3); }
  function vaiven(t) { t = Math.max(0, Math.min(1, t)); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

  // ---------------------------------------------------------------- la estrella octángula
  // El octaedro (vértices en los ejes) y, sobre cada cara, un tetraedro: las ocho piezas.
  var NUCLEO = [];                  // caras del octaedro, hacia fuera
  var HUECOS = [];                  // por cara: base, punta, centro, dirección
  [1, -1].forEach(function (sx) { [1, -1].forEach(function (sy) { [1, -1].forEach(function (sz) {
    var a = [sx, 0, 0], b = [0, sy, 0], c = [0, 0, sz], p = [sx, sy, sz];
    var n = cruz(resta(b, a), resta(c, a));
    if (punto(n, p) < 0) { var t = b; b = c; c = t; }
    NUCLEO.push([a, b, c]);
    HUECOS.push({ base: [a, b, c], punta: p, dir: norm(p), centro: esc(suma(suma(a, b), suma(c, p)), 0.25) });
  }); }); });
  function carasPieza(h) {          // las cuatro caras del tetraedro, hacia fuera
    var a = h.base[0], b = h.base[1], c = h.base[2], p = h.punta;
    return [[a, c, b], [a, b, p], [b, c, p], [c, a, p]];
  }
  // Orden de montaje: cada pieza cerca de la anterior, para que la estrella gire poco.
  var ORDEN = [0, 1, 3, 2, 6, 7, 5, 4];

  // ---------------------------------------------------------------- estado
  var modo = "solo";                // "solo" (se monta sola), "juego", "fin"
  var Q = qNorm(qMul(qEje([1, 0, 0], 0.5), qEje([0, 1, 0], 0.6)));   // giro de la estrella
  var giro = null;                  // {de, a, t0, dur}
  var puestas = [];                 // índices de huecos ya montados
  var turno = 0;                    // cuántas piezas van
  var pieza = null;                 // {hueco, k (cuartos de vuelta), ang, angDe, angT0, vuelo, t0}
  var oro = 0, oroT0 = 0;           // 0..1, cuánto oro
  var explota = null;               // t0 de la explosión del modo solo
  var guion = [];                   // pasos pendientes del modo solo
  var esperaHasta = 0;
  var giroLibre = 0;                // giro continuo al terminar
  var aviso = "", avisoHasta = 0;
  var ahora = 0, ultimo = 0, vivo = false, visible = true;
  var dpr = 1, ancho = 0;
  var puestasT = [];                // cuándo encajó cada pieza (destello)
  var chispas = [];                 // cuadraditos de la celebración
  var alto = 0.39;                  // altura del centro de la estrella, en anchos de lienzo

  var DIR_HUECO = norm([0.42, -0.78, 0.46]);  // hacia dónde se coloca el hueco que espera: abajo, delante, a un lado
  var CAIDA = 1.5;                  // cuánto cuelga la pieza bajo su hueco

  function texto(clave, n) { return (TX[clave] || "").replace("{n}", n); }
  function decir(t) { if (estado) estado.textContent = t; }

  // ---------------------------------------------------------------- partida
  function reiniciar() {
    puestas = []; puestasT = []; turno = 0; pieza = null; oro = 0; explota = null; giroLibre = 0;
    avisoHasta = 0; guion = [];
  }
  function siguiente() {
    if (turno >= 8) { terminar(); return; }
    var h = ORDEN[turno];
    var dirCam = qRot(Q, HUECOS[h].dir);
    var destino = qNorm(qMul(qDesde(dirCam, DIR_HUECO), Q));
    giro = { de: Q, a: destino, t0: ahora, dur: poco ? 1 : 650 };
    var k = turno === 0 ? 1 : 1 + Math.floor(Math.random() * 3);   // nunca llega derecha
    if (modo === "solo" && turno % 3 === 1) k = 3;
    pieza = { hueco: h, k: k, ang: k * Math.PI / 2, angDe: k * Math.PI / 2, angT0: 0, vuelo: null, t0: ahora + (poco ? 0 : 520) };
    if (modo === "juego") decir(texto("pieza", turno + 1));
  }
  function girar(dir) {
    if (!pieza || pieza.vuelo || ahora < pieza.t0) return;
    pieza.angDe = pieza.ang; pieza.angT0 = ahora;
    pieza.k = (pieza.k + dir + 4) % 4;
    pieza.destAng = pieza.angDe + dir * Math.PI / 2;   // un cuarto de vuelta, en el sentido del toque
    if (modo === "juego" && ahora < avisoHasta) { avisoHasta = 0; decir(texto("pieza", turno + 1) + " · " + texto("ayuda")); }
  }
  function lanzar() {
    if (!pieza || pieza.vuelo || ahora < pieza.t0) return;
    var bien = pieza.k === 0;
    pieza.vuelo = { t0: ahora, bien: bien, dur: poco ? 1 : (bien ? 300 : 520) };
    if (!bien && modo === "juego") { aviso = texto("no_encaja"); avisoHasta = ahora + 60000; decir(aviso); }
  }
  function encajar() {
    puestas.push(pieza.hueco); puestasT.push(ahora); turno += 1; pieza = null;
    if (turno >= 8) terminar(); else siguiente();
  }
  function terminar() {
    var enMandos = mandos && mandos.contains(document.activeElement);
    pieza = null; oroT0 = ahora; giroLibre = poco ? 0 : 0.0007;
    if (modo === "juego") {
      modo = "fin";
      decir(texto("completa"));
      celebrar();
      var tiendas = document.querySelector("[data-brilla]");
      if (tiendas && !poco) { tiendas.classList.remove("brilla"); void tiendas.offsetWidth; tiendas.classList.add("brilla"); }
      if (mandos) mandos.hidden = true;
      if (bOtra) { bOtra.hidden = false; if (enMandos) bOtra.focus(); }   // que el foco no se pierda
      lienzo.style.touchAction = "";
    } else {
      esperaHasta = ahora + (poco ? 999999 : 2600);
      guion = ["explota"];
    }
  }
  // Al completarla, un puñado de cuadraditos: el bermellón de la marca y los colores de las piezas.
  function celebrar() {
    if (poco) return;
    chispas = [];
    for (var i = 0; i < 34; i++) {
      var a = Math.random() * Math.PI * 2, v = 2.4 + Math.random() * 2.4;
      chispas.push({ x: 0, y: 0, vx: Math.cos(a) * v, vy: Math.sin(a) * v + 1.2, r: Math.random() * 6.28,
        vr: (Math.random() - 0.5) * 9, c: i % 3 === 0 ? [213, 69, 41] : COLORES[i % 8],
        t0: ahora + Math.random() * 90, vida: 1200 + Math.random() * 700, lado: 0.07 + Math.random() * 0.06 });
    }
  }
  function empezarSolo() {
    modo = "solo"; reiniciar(); siguiente();
    if (bJugar) bJugar.hidden = false;
    if (mandos) mandos.hidden = true;
    if (bOtra) bOtra.hidden = true;
    lienzo.style.touchAction = "";
    decir(texto(poco ? "invita_quieta" : "invita"));
  }
  function empezarJuego() {
    modo = "juego"; reiniciar();
    if (bJugar) bJugar.hidden = true;
    if (bOtra) bOtra.hidden = true;
    if (mandos) mandos.hidden = false;
    lienzo.style.touchAction = "none";
    siguiente();
    decir(texto("pieza", 1) + " · " + texto("ayuda"));
    try { lienzo.focus({ preventScroll: true }); } catch (e) { /* nada */ }
    despertar();
  }

  // El modo solo juega como un jugador tranquilo: espera, gira por el lado corto y lanza.
  function piloto() {
    if (modo !== "solo" || ahora < esperaHasta) return;
    if (guion.length && guion[0] === "explota") {
      guion.shift(); explota = ahora; esperaHasta = ahora + 900; guion = ["reinicia"]; return;
    }
    if (guion.length && guion[0] === "reinicia") { guion = []; reiniciar(); siguiente(); esperaHasta = ahora + 300; return; }
    if (!pieza || pieza.vuelo || ahora < pieza.t0 + 380) return;
    if (pieza.destAng !== undefined && ahora < pieza.angT0 + 260) return;
    if (pieza.k !== 0) { girar(pieza.k === 3 ? 1 : -1); esperaHasta = ahora + 420; return; }
    lanzar(); esperaHasta = ahora + 300;
  }

  // ---------------------------------------------------------------- dibujo
  function color(base, n, alfa) {
    // dos tonos, como en el juego: la cara a la sombra oscurece, la de la luz se aclara un poco
    var d = Math.max(0, punto(n, LUZ));
    var sombra = [base[0] * 0.74, base[1] * 0.64, base[2] * 0.58], luz = mezcla(base, [255, 252, 240], 0.2);
    var c = mezcla(sombra, luz, Math.pow(d, 0.8));
    var r = Math.min(255, Math.round(c[0])), gg = Math.min(255, Math.round(c[1])), b = Math.min(255, Math.round(c[2]));
    return alfa === undefined || alfa >= 1 ? "rgb(" + r + "," + gg + "," + b + ")" : "rgba(" + r + "," + gg + "," + b + "," + alfa.toFixed(3) + ")";
  }
  function mezcla(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }
  var cx = 0, cy = 0, S = 1;
  function pantalla(v) { return [cx + v[0] * S, cy - v[1] * S]; }

  function cuerpo(caras, base, alfa, filo) {
    // caras ya en espacio de cámara; dibuja las que miran hacia aquí
    for (var i = 0; i < caras.length; i++) {
      var f = caras[i], n = norm(cruz(resta(f[1], f[0]), resta(f[2], f[0])));
      if (n[2] <= 0.001) continue;
      g.beginPath();
      for (var j = 0; j < f.length; j++) { var p = pantalla(f[j]); if (j) g.lineTo(p[0], p[1]); else g.moveTo(p[0], p[1]); }
      g.closePath();
      g.fillStyle = color(base, n, alfa); g.fill();
      g.strokeStyle = alfa !== undefined && alfa < 1 ? "rgba(33,31,28," + alfa.toFixed(3) + ")" : TINTA;
      g.lineWidth = filo; g.lineJoin = "round"; g.stroke();
    }
  }
  function fantasma(h, Qd, objetivo, lw) {
    var p = qRot(Qd, h.punta);
    if (objetivo) {
      var tono = COLORES[turno % 8];
      carasPieza(h).forEach(function (f) {
        var cf = f.map(function (v) { return qRot(Qd, v); });
        var n = norm(cruz(resta(cf[1], cf[0]), resta(cf[2], cf[0])));
        if (n[2] <= 0.001) return;
        g.beginPath();
        cf.forEach(function (v, j) { var q = pantalla(v); if (j) g.lineTo(q[0], q[1]); else g.moveTo(q[0], q[1]); });
        g.closePath(); g.fillStyle = "rgba(" + tono.join(",") + ",0.22)"; g.fill();
      });
    }
    g.beginPath();
    h.base.forEach(function (v) { var a = pantalla(qRot(Qd, v)), b = pantalla(p); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); });
    if (objetivo) {
      g.setLineDash([lw * 3, lw * 2.2]); g.strokeStyle = TINTA; g.lineWidth = lw * 1.25;
    } else {
      g.setLineDash([]); g.strokeStyle = "rgba(33,31,28,0.2)"; g.lineWidth = lw;
    }
    g.stroke(); g.setLineDash([]);
  }
  function fondo(w) {
    // las bandas grises del fondo del juego, quietas
    g.save(); g.fillStyle = BANDA;
    g.translate(w * 0.5, w * 0.5); g.rotate(-0.42);
    g.fillRect(-w, -w * 0.05, w * 2, w * 0.1);
    g.rotate(1.2); g.fillRect(-w, w * 0.18, w * 2, w * 0.035);
    g.restore();
  }

  function dibujar() {
    var w = lienzo.width;
    g.clearRect(0, 0, w, w);
    fondo(w);
    var dt = Math.min(64, Math.max(0, ahora - ultimo));
    var meta = (turno >= 8 && !explota) ? 0.47 : 0.39;      // completa, sube al centro
    alto = poco ? meta : alto + (meta - alto) * Math.min(1, dt / 220);
    S = w / 5.1; cx = w / 2; cy = w * alto;
    var lw = Math.max(1, w / 420);

    // giro de la estrella
    if (giro) {
      var t = (ahora - giro.t0) / giro.dur;
      Q = qSlerp(giro.de, giro.a, vaiven(t));
      if (t >= 1) { Q = giro.a; giro = null; }
    }
    if (giroLibre) Q = qNorm(qMul(qEje([0, 1, 0], giroLibre * (ahora - ultimo)), Q));
    var Qd = Q;

    // oro al terminar
    if (oroT0 && (modo === "fin" || (modo === "solo" && turno >= 8))) oro = Math.min(1, (ahora - oroT0) / (poco ? 1 : 900));
    var exp = explota ? Math.min(1, (ahora - explota) / 800) : 0;

    // cuerpos: núcleo, piezas puestas, huecos vacíos; ordenados de lejos a cerca
    var cosas = [{ z: 0, tipo: "nucleo" }];
    for (var i = 0; i < 8; i++) {
      var h = HUECOS[i], zc = qRot(Qd, h.centro)[2];
      var puesta = puestas.indexOf(i);
      if (puesta >= 0) cosas.push({ z: zc, tipo: "pieza", h: h, orden: puesta, i: i });
      else cosas.push({ z: zc, tipo: "hueco", h: h, i: i });
    }
    cosas.sort(function (a, b) { return a.z - b.z; });
    var objetivo = pieza ? pieza.hueco : -1;
    cosas.forEach(function (c) {
      if (c.tipo === "nucleo") {
        var al = 1 - exp * 0.0;
        NUCLEO.forEach(function (f) {
          var cf = f.map(function (v) { return qRot(Qd, v); });
          var n = norm(cruz(resta(cf[1], cf[0]), resta(cf[2], cf[0])));
          if (n[2] <= 0.001) return;
          g.beginPath();
          cf.forEach(function (v, j) { var p = pantalla(v); if (j) g.lineTo(p[0], p[1]); else g.moveTo(p[0], p[1]); });
          g.closePath();
          var d = Math.max(0, punto(n, LUZ)), k = 0.8 + 0.2 * d;
          g.fillStyle = "rgb(" + Math.round(PAPEL[0] * k) + "," + Math.round(PAPEL[1] * k) + "," + Math.round(PAPEL[2] * k) + ")";
          g.globalAlpha = al; g.fill(); g.strokeStyle = TINTA; g.lineWidth = lw; g.stroke(); g.globalAlpha = 1;
        });
      } else if (c.tipo === "hueco") {
        if (!explota) fantasma(c.h, Qd, c.i === objetivo, lw);
      } else {
        var base = mezcla(COLORES[c.orden % 8], ORO, Math.max(0, Math.min(1, oro * 1.6 - c.orden * 0.075)));
        var fl = puestasT[c.orden] && !poco ? Math.max(0, 1 - (ahora - puestasT[c.orden]) / 320) : 0;
        if (fl > 0) base = mezcla(base, [255, 252, 240], 0.55 * fl);
        var desv = esc(c.h.dir, exp * 2.8);
        var caras = carasPieza(c.h).map(function (f) { return f.map(function (v) { return qRot(Qd, suma(v, desv)); }); });
        cuerpo(caras, base, 1 - exp, lw);
      }
    });

    // la pieza que espera, colgando bajo su hueco
    if (pieza && ahora >= pieza.t0) {
      var hh = HUECOS[pieza.hueco];
      // ángulo actual (cuartos de vuelta alrededor del eje vertical de la pantalla)
      if (pieza.destAng !== undefined) {
        var tg = (ahora - pieza.angT0) / (poco ? 1 : 200);
        pieza.ang = pieza.angDe + (pieza.destAng - pieza.angDe) * suave(tg);
        if (tg >= 1) { pieza.ang = pieza.destAng; pieza.destAng = undefined; }
      }
      var caida = CAIDA, aparece = Math.min(1, (ahora - pieza.t0) / (poco ? 1 : 220));
      if (pieza.vuelo) {
        var tv = (ahora - pieza.vuelo.t0) / pieza.vuelo.dur;
        if (pieza.vuelo.bien) caida = CAIDA * (1 - suave(tv));
        else caida = CAIDA * (1 - 0.62 * Math.sin(Math.PI * Math.min(1, tv)));
        if (tv >= 1) {
          if (pieza.vuelo.bien) { encajar(); return dibujarFin(); }
          pieza.vuelo = null;
        }
      }
      if (pieza) {
        var centroCam = qRot(Qd, hh.centro);
        var qy = qEje([0, 1, 0], pieza.ang);
        var abajo = [0, -caida - (1 - aparece) * 0.6, 0];
        var carasP = carasPieza(hh).map(function (f) {
          return f.map(function (v) {
            var rel = resta(qRot(Qd, v), centroCam);
            return suma(suma(qRot(qy, rel), centroCam), abajo);
          });
        });
        // el hilo que la une a su hueco, como en el juego
        var desde = pantalla(suma(centroCam, abajo)), hasta = pantalla(centroCam);
        g.beginPath(); g.moveTo(desde[0], desde[1]); g.lineTo(hasta[0], hasta[1]);
        g.strokeStyle = "rgba(33,31,28,0.55)"; g.lineWidth = lw * 0.8; g.stroke();
        cuerpo(carasP, COLORES[turno % 8], aparece, lw);
      }
    }
    dibujarFin();
  }
  function dibujarFin() {
    if (!chispas.length) return;
    var dts = Math.min(0.064, Math.max(0, (ahora - ultimo) / 1000));
    chispas = chispas.filter(function (p) {
      if (ahora < p.t0) return true;
      var e = (ahora - p.t0) / p.vida; if (e >= 1) return false;
      p.x += p.vx * dts; p.y += p.vy * dts; p.vy -= 4.2 * dts; p.vx *= 0.985; p.vy *= 0.985; p.r += p.vr * dts;
      var q = pantalla([p.x, p.y, 0]), l = p.lado * S;
      g.save(); g.translate(q[0], q[1]); g.rotate(p.r); g.globalAlpha = 1 - e * e;
      g.fillStyle = "rgb(" + p.c.join(",") + ")"; g.fillRect(-l / 2, -l / 2, l, l); g.restore();
      return true;
    });
  }

  // ---------------------------------------------------------------- bucle
  var quietos = 0;
  function paso(t) {
    ahora = t;
    if (!ultimo) ultimo = t;
    if (modo === "solo") piloto();
    dibujar();
    ultimo = t;
    // Con menos movimiento, solo hay animación mientras se juega (y tres cuadros más, para
    // dejar dibujado el final); lo demás está quieto.
    quietos = (poco && modo !== "juego") ? quietos + 1 : 0;
    if (vivo && visible && quietos < 3) requestAnimationFrame(paso); else { vivo = false; quietos = 0; }
  }
  function despertar() { if (!vivo && visible) { vivo = true; ultimo = 0; requestAnimationFrame(paso); } }

  function medir() {
    var lado = lienzo.getBoundingClientRect().width || 320;
    dpr = Math.min(2, window.devicePixelRatio || 1);
    var px = Math.round(lado * dpr);
    if (px !== ancho) { ancho = px; lienzo.width = px; lienzo.height = px; }
    if (!vivo) { dibujar(); }
  }

  // ---------------------------------------------------------------- mandos
  var toque = null;
  // Con ratón o dedo no hace falta el marco de foco; con teclado, sí.
  raiz.addEventListener("pointerdown", function () { raiz.classList.add("puntero"); });
  raiz.addEventListener("keydown", function () { raiz.classList.remove("puntero"); }, true);
  lienzo.addEventListener("pointerdown", function (e) {
    if (modo === "solo") return;
    toque = { x: e.clientX, y: e.clientY, id: e.pointerId };
    try { lienzo.setPointerCapture(e.pointerId); } catch (er) { /* nada */ }
  });
  lienzo.addEventListener("pointerup", function (e) {
    if (modo === "solo") { empezarJuego(); return; }
    if (!toque || modo !== "juego") { toque = null; return; }
    var dx = e.clientX - toque.x, dy = toque.y - e.clientY;
    toque = null;
    if (dy > 24 && dy > Math.abs(dx)) lanzar();
    else if (Math.abs(dx) < 14 && Math.abs(dy) < 14) {
      var r = lienzo.getBoundingClientRect();
      girar(e.clientX - r.left < r.width / 2 ? -1 : 1);
    }
    despertar();
  });
  lienzo.addEventListener("pointercancel", function () { toque = null; });
  // Las teclas valen con el foco en la estrella o en cualquiera de sus botones; Intro y
  // espacio, solo sobre la estrella (en un botón ya lo pulsan).
  raiz.addEventListener("keydown", function (e) {
    var enLienzo = e.target === lienzo;
    if (modo === "solo") {
      if (enLienzo && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); empezarJuego(); }
      return;
    }
    if (modo !== "juego") return;
    if (e.key === "ArrowLeft") { e.preventDefault(); girar(-1); }
    else if (e.key === "ArrowRight") { e.preventDefault(); girar(1); }
    else if (e.key === "ArrowUp" || (enLienzo && (e.key === " " || e.key === "Enter"))) { e.preventDefault(); lanzar(); }
    despertar();
  });
  raiz.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-accion]");
    if (!b) return;
    var a = b.getAttribute("data-accion");
    if (a === "jugar" || a === "otra") empezarJuego();
    else if (a === "izq") girar(-1);
    else if (a === "der") girar(1);
    else if (a === "lanza") lanzar();
    despertar();
  });

  // Solo se anima cuando se ve.
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (ent) {
      visible = ent[0].isIntersecting && !document.hidden;
      if (visible) despertar();
    }, { threshold: 0.05 }).observe(lienzo);
  }
  document.addEventListener("visibilitychange", function () { visible = !document.hidden; if (visible) despertar(); });
  window.addEventListener("resize", medir);

  medir();
  empezarSolo();
  if (poco) {                       // con menos movimiento: la estrella entera, quieta
    puestas = [0, 1, 2, 3, 4, 5, 6, 7]; turno = 8; pieza = null; giro = null;
    oroT0 = 0; oro = 0; ahora = performance.now(); dibujar();
  } else {
    despertar();
  }
  // Para las pruebas automáticas: estado de la partida, sin efectos.
  raiz.estrella = { modo: function () { return modo; }, turno: function () { return turno; },
    pieza: function () { return pieza ? { k: pieza.k, volando: !!pieza.vuelo, lista: ahora >= pieza.t0 } : null; } };
})();

// ---------------------------------------------------------------- los bucles
(function () {
  "use strict";
  var videos = [].slice.call(document.querySelectorAll("video[data-bucle]"));
  if (!videos.length) return;
  var poco = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (poco || !("IntersectionObserver" in window)) {
    // Con menos movimiento, nada arranca solo: el vídeo espera con sus controles.
    videos.forEach(function (v) { v.controls = true; });
    return;
  }
  var io = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (e) {
      var v = e.target;
      if (e.isIntersecting) {
        var p = v.play();
        if (p && p.catch) p.catch(function () { v.controls = true; });
      } else if (!v.paused) {
        v.pause();
      }
    });
  }, { threshold: 0.3 });
  videos.forEach(function (v) { v.muted = true; io.observe(v); });
})();
