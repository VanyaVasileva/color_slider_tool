import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Pattern Background Color",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      .block-container {padding-top: 1.2rem; padding-bottom: 1.5rem; max-width: 980px;}
      header[data-testid="stHeader"] {background: transparent;}
      #MainMenu, footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Pattern Background Color")
st.caption("Transparentes PNG hochladen, über den Farbbalken gleiten und direkt exportieren.")

html = r'''
<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
<style>
  :root {
    --panel: #ffffff;
    --line: #dedede;
    --text: #202020;
    --muted: #6b6b6b;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: var(--text);
    background: transparent;
  }
  .app {
    width: 100%;
    display: grid;
    gap: 16px;
  }
  .card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 14px;
  }
  .upload {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
  }
  input[type=file] {
    width: 100%;
    font-size: 16px;
  }
  .preview-wrap {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 280px;
    overflow: hidden;
    border-radius: 14px;
    background:
      linear-gradient(45deg, #f2f2f2 25%, transparent 25%),
      linear-gradient(-45deg, #f2f2f2 25%, transparent 25%),
      linear-gradient(45deg, transparent 75%, #f2f2f2 75%),
      linear-gradient(-45deg, transparent 75%, #f2f2f2 75%);
    background-size: 22px 22px;
    background-position: 0 0, 0 11px, 11px -11px, -11px 0px;
  }
  #previewCanvas {
    display: block;
    margin: 0 auto;
    max-width: 100%;
    max-height: 560px;
    width: auto;
    height: auto;
    border-radius: 10px;
  }
  .label {
    font-size: 14px;
    font-weight: 650;
    margin-bottom: 8px;
  }
  .palette-shell {
    position: relative;
    width: 100%;
    height: 72px;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(0,0,0,.18);
    touch-action: none;
    user-select: none;
    -webkit-user-select: none;
    cursor: crosshair;
  }
  #palette {
    display: block;
    width: 100%;
    height: 100%;
    touch-action: none;
  }
  #marker {
    position: absolute;
    width: 22px;
    height: 22px;
    border: 3px solid white;
    border-radius: 50%;
    box-shadow: 0 0 0 2px rgba(0,0,0,.55), 0 2px 7px rgba(0,0,0,.35);
    transform: translate(-50%, -50%);
    pointer-events: none;
    left: 50%;
    top: 50%;
  }
  .row {
    display: grid;
    grid-template-columns: minmax(0,1fr) auto;
    gap: 10px;
    align-items: center;
    margin-top: 12px;
  }
  .hexbox {
    display: flex;
    align-items: center;
    gap: 9px;
    min-width: 0;
  }
  #swatch {
    width: 42px;
    height: 42px;
    border-radius: 11px;
    border: 1px solid rgba(0,0,0,.2);
    flex: 0 0 auto;
  }
  #hex {
    font: 650 17px ui-monospace, SFMono-Regular, Menlo, monospace;
    border: 1px solid var(--line);
    border-radius: 11px;
    padding: 10px 12px;
    width: 140px;
    background: #fff;
  }
  button {
    appearance: none;
    border: 0;
    border-radius: 12px;
    padding: 12px 15px;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
  }
  .secondary { background: #eeeeee; color: #222; }
  .primary { background: #222; color: white; width: 100%; margin-top: 12px; }
  button:disabled { opacity: .45; cursor: default; }
  .hint { color: var(--muted); font-size: 13px; margin-top: 7px; line-height: 1.35; }
  #status { font-size: 13px; color: var(--muted); margin-top: 8px; min-height: 18px; }
  @media (max-width: 520px) {
    .card { border-radius: 15px; padding: 11px; }
    .preview-wrap { min-height: 240px; }
    .palette-shell { height: 82px; }
    .row { grid-template-columns: 1fr; }
    .secondary { width: 100%; }
    #hex { width: 100%; }
    .hexbox { width: 100%; }
  }
</style>
</head>
<body>
<div class="app">
  <div class="card upload">
    <input id="fileInput" type="file" accept="image/png" aria-label="Transparentes PNG hochladen" />
    <div class="hint">Das PNG sollte einen transparenten Hintergrund haben.</div>
  </div>

  <div class="card">
    <div class="label">Live-Vorschau</div>
    <div class="preview-wrap" id="previewWrap">
      <canvas id="previewCanvas" width="900" height="900"></canvas>
    </div>
    <div id="status">Noch kein PNG geladen.</div>
  </div>

  <div class="card">
    <div class="label">Mit Finger, Apple Pencil oder Maus über den Balken gleiten</div>
    <div class="palette-shell" id="paletteShell">
      <canvas id="palette"></canvas>
      <div id="marker"></div>
    </div>

    <div class="row">
      <div class="hexbox">
        <div id="swatch"></div>
        <input id="hex" type="text" value="#D8C4B6" maxlength="7" spellcheck="false" aria-label="HEX Farbe" />
      </div>
      <button class="secondary" id="copyBtn" type="button">HEX kopieren</button>
    </div>
    <button class="primary" id="downloadBtn" type="button" disabled>PNG mit Hintergrund speichern</button>
    <div class="hint">Der Export behält die Originalgröße deines hochgeladenen PNGs.</div>
  </div>
</div>

<script>
(() => {
  const fileInput = document.getElementById('fileInput');
  const previewCanvas = document.getElementById('previewCanvas');
  const pctx = previewCanvas.getContext('2d');
  const palette = document.getElementById('palette');
  const paletteShell = document.getElementById('paletteShell');
  const marker = document.getElementById('marker');
  const hexInput = document.getElementById('hex');
  const swatch = document.getElementById('swatch');
  const copyBtn = document.getElementById('copyBtn');
  const downloadBtn = document.getElementById('downloadBtn');
  const status = document.getElementById('status');

  let image = null;
  let bgColor = '#D8C4B6';
  let activePointer = null;

  function normalizeHex(value) {
    let v = value.trim().toUpperCase();
    if (!v.startsWith('#')) v = '#' + v;
    if (/^#[0-9A-F]{6}$/.test(v)) return v;
    if (/^#[0-9A-F]{3}$/.test(v)) {
      return '#' + v.slice(1).split('').map(c => c + c).join('');
    }
    return null;
  }

  function rgbToHex(r, g, b) {
    return '#' + [r,g,b].map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2,'0')).join('').toUpperCase();
  }

  function hslToRgb(h, s, l) {
    h /= 360; s /= 100; l /= 100;
    let r, g, b;
    if (s === 0) {
      r = g = b = l;
    } else {
      const hue2rgb = (p, q, t) => {
        if (t < 0) t += 1;
        if (t > 1) t -= 1;
        if (t < 1/6) return p + (q-p)*6*t;
        if (t < 1/2) return q;
        if (t < 2/3) return p + (q-p)*(2/3-t)*6;
        return p;
      };
      const q = l < 0.5 ? l*(1+s) : l+s-l*s;
      const p = 2*l-q;
      r = hue2rgb(p,q,h+1/3);
      g = hue2rgb(p,q,h);
      b = hue2rgb(p,q,h-1/3);
    }
    return [r*255,g*255,b*255];
  }

  function drawPalette() {
    const rect = paletteShell.getBoundingClientRect();
    const dpr = Math.max(1, window.devicePixelRatio || 1);
    palette.width = Math.round(rect.width * dpr);
    palette.height = Math.round(rect.height * dpr);
    palette.style.width = rect.width + 'px';
    palette.style.height = rect.height + 'px';
    const ctx = palette.getContext('2d');
    const img = ctx.createImageData(palette.width, palette.height);

    for (let y = 0; y < palette.height; y++) {
      const yn = y / Math.max(1, palette.height - 1);
      const lightness = 96 - yn * 76;
      const saturation = 18 + Math.sin(Math.PI * yn) * 82;
      for (let x = 0; x < palette.width; x++) {
        const hue = (x / Math.max(1, palette.width - 1)) * 360;
        const [r,g,b] = hslToRgb(hue, saturation, lightness);
        const i = (y * palette.width + x) * 4;
        img.data[i] = r;
        img.data[i+1] = g;
        img.data[i+2] = b;
        img.data[i+3] = 255;
      }
    }
    ctx.putImageData(img, 0, 0);
  }

  // Setzt NUR die Canvas-Groesse (Pixel-Buffer). Wird ausschliesslich beim
  // Bild-Upload aufgerufen - NICHT bei jeder Farbaenderung. Das ist der Fix:
  // vorher wurde previewCanvas.width/height bei jeder Mausbewegung ueber die
  // Palette neu gesetzt, was die Canvas komplett geleert und einen Reflow
  // ausgeloest hat -> das Design "sprang" sichtbar.
  function sizeCanvasToImage() {
    const maxPreview = 1000;
    let w = 900, h = 900;
    if (image) {
      const scale = Math.min(1, maxPreview / Math.max(image.naturalWidth, image.naturalHeight));
      w = Math.max(1, Math.round(image.naturalWidth * scale));
      h = Math.max(1, Math.round(image.naturalHeight * scale));
    }
    if (previewCanvas.width !== w || previewCanvas.height !== h) {
      previewCanvas.width = w;
      previewCanvas.height = h;
    }
  }

  // Malt nur die Pixel neu (Hintergrundfarbe + Motiv), ohne die Canvas-Groesse
  // anzufassen. Das ist die einzige Funktion, die beim Farbwechsel laeuft.
  function paintPreview() {
    const w = previewCanvas.width;
    const h = previewCanvas.height;
    pctx.clearRect(0,0,w,h);
    pctx.fillStyle = bgColor;
    pctx.fillRect(0,0,w,h);
    if (image) pctx.drawImage(image, 0, 0, w, h);
  }

  function setColor(hex, updateInput=true) {
    bgColor = hex.toUpperCase();
    swatch.style.background = bgColor;
    if (updateInput) hexInput.value = bgColor;
    paintPreview();
  }

  function pickFromPointer(e) {
    const rect = paletteShell.getBoundingClientRect();
    const x = Math.max(0, Math.min(rect.width, e.clientX - rect.left));
    const y = Math.max(0, Math.min(rect.height, e.clientY - rect.top));
    marker.style.left = x + 'px';
    marker.style.top = y + 'px';

    const hue = (x / Math.max(1, rect.width)) * 360;
    const yn = y / Math.max(1, rect.height);
    const lightness = 96 - yn * 76;
    const saturation = 18 + Math.sin(Math.PI * yn) * 82;
    const [r,g,b] = hslToRgb(hue, saturation, lightness);
    setColor(rgbToHex(r,g,b));
  }

  paletteShell.addEventListener('pointerdown', e => {
    activePointer = e.pointerId;
    paletteShell.setPointerCapture(e.pointerId);
    pickFromPointer(e);
    e.preventDefault();
  });
  paletteShell.addEventListener('pointermove', e => {
    if (activePointer === e.pointerId) {
      pickFromPointer(e);
      e.preventDefault();
    }
  });
  const endPointer = e => {
    if (activePointer === e.pointerId) activePointer = null;
  };
  paletteShell.addEventListener('pointerup', endPointer);
  paletteShell.addEventListener('pointercancel', endPointer);

  fileInput.addEventListener('change', () => {
    const file = fileInput.files && fileInput.files[0];
    if (!file) return;
    if (file.type !== 'image/png') {
      status.textContent = 'Bitte eine PNG-Datei auswählen.';
      return;
    }
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => {
      image = img;
      sizeCanvasToImage();
      paintPreview();
      downloadBtn.disabled = false;
      status.textContent = `${img.naturalWidth} × ${img.naturalHeight} px geladen`;
      URL.revokeObjectURL(url);
    };
    img.onerror = () => {
      status.textContent = 'Das PNG konnte nicht geladen werden.';
      URL.revokeObjectURL(url);
    };
    img.src = url;
  });

  hexInput.addEventListener('input', () => {
    const hex = normalizeHex(hexInput.value);
    if (hex) setColor(hex, false);
  });
  hexInput.addEventListener('blur', () => {
    const hex = normalizeHex(hexInput.value);
    hexInput.value = hex || bgColor;
    if (hex) setColor(hex);
  });

  copyBtn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(bgColor);
      copyBtn.textContent = 'Kopiert ✓';
      setTimeout(() => copyBtn.textContent = 'HEX kopieren', 1200);
    } catch {
      hexInput.select();
      document.execCommand('copy');
    }
  });

  downloadBtn.addEventListener('click', () => {
    if (!image) return;
    const out = document.createElement('canvas');
    out.width = image.naturalWidth;
    out.height = image.naturalHeight;
    const ctx = out.getContext('2d');
    ctx.fillStyle = bgColor;
    ctx.fillRect(0,0,out.width,out.height);
    ctx.drawImage(image,0,0);
    out.toBlob(blob => {
      const a = document.createElement('a');
      const safeHex = bgColor.replace('#','');
      a.href = URL.createObjectURL(blob);
      a.download = `pattern_background_${safeHex}.png`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => URL.revokeObjectURL(a.href), 1000);
    }, 'image/png');
  });

  const ro = new ResizeObserver(() => drawPalette());
  ro.observe(paletteShell);
  window.addEventListener('resize', drawPalette);

  drawPalette();
  sizeCanvasToImage();
  setColor(bgColor);
})();
</script>
</body>
</html>
'''

components.html(html, height=980, scrolling=True)
