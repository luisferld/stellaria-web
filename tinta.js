// Tinta: el renderizador plano de la casa, en el navegador. Es el mismo
// dibujo que hace la cuadrícula de la app (SolidDrawing): girar el
// sólido, proyectar en perspectiva, quedarse con las caras que miran a
// la cámara, pintarlas de atrás adelante con su cuerpo de los Proun
// sombreado por dos luces, y el canto a tinta. Nada de fotos: la
// geometría la exporta el motor del juego (tools/bench web).
(function (global) {
  const BODIES = [[0.835,0.27,0.16],[0.85,0.66,0.31],[0.55,0.61,0.64],[0.72,0.70,0.54],[0.48,0.34,0.20],[0.25,0.24,0.22]];
  const INK = '#211F1C';
  const HALF_FOV = 17.5 * Math.PI / 180;
  const norm = v => { const l = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0]/l, v[1]/l, v[2]/l]; };
  const DIRECTION = norm([0.35, 0.3, 1]);
  const KEY = norm([1.0, 1.4, 1.2]);
  const FILL = norm([-1.2, 0.4, 0.8]);
  const dot = (a, b) => a[0]*b[0] + a[1]*b[1] + a[2]*b[2];
  const cross = (a, b) => [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];

  // Un cuaternión por (eje, ángulo) y su acción sobre un vector.
  function quat(axis, angle) { const s = Math.sin(angle/2); return [axis[0]*s, axis[1]*s, axis[2]*s, Math.cos(angle/2)]; }
  function qmul(a, b) {
    return [a[3]*b[0] + a[0]*b[3] + a[1]*b[2] - a[2]*b[1],
            a[3]*b[1] - a[0]*b[2] + a[1]*b[3] + a[2]*b[0],
            a[3]*b[2] + a[0]*b[1] - a[1]*b[0] + a[2]*b[3],
            a[3]*b[3] - a[0]*b[0] - a[1]*b[1] - a[2]*b[2]];
  }
  function act(q, v) {
    const u = [q[0], q[1], q[2]], s = q[3];
    const uv = cross(u, v), uuv = cross(u, uv);
    return [v[0] + 2*(s*uv[0] + uuv[0]), v[1] + 2*(s*uv[1] + uuv[1]), v[2] + 2*(s*uv[2] + uuv[2])];
  }

  class Figure {
    constructor(data) {
      this.vertices = data.vertices; this.faces = data.faces; this.bodies = data.bodies;
      this.radius = data.radius;
      this.normals = this.faces.map(f => {
        const a = this.vertices[f[0]], b = this.vertices[f[1]], c = this.vertices[f[2]];
        return norm(cross([b[0]-a[0], b[1]-a[1], b[2]-a[2]], [c[0]-a[0], c[1]-a[1], c[2]-a[2]]));
      });
      const lengths = (data.edges || []).map(e => { const a = this.vertices[e[0]], b = this.vertices[e[1]]; return Math.hypot(a[0]-b[0], a[1]-b[1], a[2]-b[2]); }).sort((x, y) => x - y);
      this.lead = lengths.length ? lengths[lengths.length >> 1] * 0.012 : 0.01;
    }
    draw(ctx, w, h, orientation, opts = {}) {
      const forward = DIRECTION;
      let right = cross([0, 1, 0], forward); if (Math.hypot(...right) < 1e-4) right = [1, 0, 0]; right = norm(right);
      const up = cross(forward, right);
      const distance = this.radius / Math.tan(HALF_FOV) * 1.15 / (opts.zoom || 1);
      const focal = Math.min(w, h) / 2 / Math.tan(HALF_FOV);
      const cx = w / 2, cy = h / 2;
      const eye = [forward[0]*distance, forward[1]*distance, forward[2]*distance];
      const turned = this.vertices.map(v => act(orientation, v));
      const project = p => { const depth = distance - dot(p, forward); const k = focal / Math.max(depth, 1e-3); return [cx + dot(p, right)*k, cy - dot(p, up)*k]; };
      const visible = [];
      for (let i = 0; i < this.faces.length; i++) {
        const f = this.faces[i], n = act(orientation, this.normals[i]);
        let c = [0, 0, 0]; for (const vi of f) { c[0] += turned[vi][0]; c[1] += turned[vi][1]; c[2] += turned[vi][2]; }
        c = [c[0]/f.length, c[1]/f.length, c[2]/f.length];
        if (dot(n, [eye[0]-c[0], eye[1]-c[1], eye[2]-c[2]]) <= 0) continue;
        const light = 3000 * Math.max(0, dot(n, KEY)) + 1200 * Math.max(0, dot(n, FILL));
        visible.push({ depth: dot(c, forward), shade: Math.min(1, light / 3200), pts: f.map(vi => project(turned[vi])), body: this.bodies[i] });
      }
      visible.sort((a, b) => a.depth - b.depth);
      const lead = Math.max(0.8, 2 * this.lead * focal / distance * (opts.edgeScale || 1));
      ctx.lineJoin = 'round'; ctx.lineWidth = lead; ctx.strokeStyle = INK;
      for (const face of visible) {
        ctx.beginPath(); face.pts.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])); ctx.closePath();
        if (face.body >= 0 && !opts.wire) {
          const paint = BODIES[face.body % 6], body = 0.72 + 0.28 * face.shade, white = 0.10 + 0.16 * face.shade;
          const ch = x => Math.round(255 * Math.min(1, x * body + white));
          ctx.fillStyle = `rgb(${ch(paint[0])},${ch(paint[1])},${ch(paint[2])})`; ctx.fill();
        }
        ctx.stroke();
      }
    }
  }

  const cache = new Map();
  async function load(url) {
    if (!cache.has(url)) cache.set(url, fetch(url).then(r => r.json()));
    return cache.get(url);
  }

  // Monta una figura en un canvas: gira sola (0,4 rad/s, con su fase),
  // y se deja arrastrar; al soltar, vuelve a girar sola.
  function mount(canvas, data, opts = {}) {
    const figure = data instanceof Figure ? data : new Figure(data);
    const ctx = canvas.getContext('2d');
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    let yaw = opts.phase || 0, pitch = 0, dragging = false, last = null, holdUntil = 0, visible = true;
    function size() {
      const r = canvas.getBoundingClientRect();
      const w = Math.max(1, Math.round(r.width * dpr)), h = Math.max(1, Math.round(r.height * dpr));
      if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
      return [w, h];
    }
    function frame(now) {
      if (visible) {
        const [w, h] = size();
        if (!dragging && now > holdUntil && opts.spin !== false) yaw += 0.4 * (frame.dt || 0);
        ctx.clearRect(0, 0, w, h);
        const q = qmul(quat([1, 0, 0], pitch), quat([0, 1, 0], yaw));
        figure.draw(ctx, w, h, q, opts);
      }
      frame.dt = frame.last ? Math.min(0.1, (now - frame.last) / 1000) : 0; frame.last = now;
      if (opts.spin !== false || dragging) requestAnimationFrame(frame); else frame.armed = false;
    }
    frame.armed = true; requestAnimationFrame(frame);
    if (opts.drag !== false) {
      canvas.style.touchAction = 'none'; canvas.style.cursor = 'grab';
      canvas.addEventListener('pointerdown', e => { dragging = true; last = [e.clientX, e.clientY]; canvas.setPointerCapture(e.pointerId); if (!frame.armed) { frame.armed = true; requestAnimationFrame(frame); } });
      canvas.addEventListener('pointermove', e => { if (!dragging) return; yaw += (e.clientX - last[0]) * 0.008; pitch += (e.clientY - last[1]) * 0.008; last = [e.clientX, e.clientY]; });
      const release = () => { dragging = false; holdUntil = performance.now() + 3000; };
      canvas.addEventListener('pointerup', release); canvas.addEventListener('pointercancel', release);
    }
    if ('IntersectionObserver' in window) new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(canvas);
    return { figure };
  }

  global.Tinta = { Figure, load, mount };
})(window);
