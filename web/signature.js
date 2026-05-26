/**
 * Chicken Kitchen HR — Signature Pad.
 * Touch + mouse canvas for drawing a signature.
 * Exports PNG as base64 string.
 */

let _sigCanvas = null;
let _sigCtx = null;
let _sigDrawing = false;
let _sigHasContent = false;

function initSignaturePad(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = '';

  // Label
  const label = document.createElement('label');
  label.textContent = t('sig_label') || 'Signature / Firma';
  label.style.cssText = 'display:block;margin-bottom:6px;font-weight:600;color:#333;';
  container.appendChild(label);

  // Canvas wrapper
  const wrapper = document.createElement('div');
  wrapper.style.cssText = 'position:relative;border:2px solid #D32F2F;border-radius:8px;background:#fff;overflow:hidden;touch-action:none;';
  container.appendChild(wrapper);

  // Canvas
  const canvas = document.createElement('canvas');
  canvas.width = 400;
  canvas.height = 150;
  canvas.style.cssText = 'width:100%;height:150px;cursor:crosshair;display:block;';
  wrapper.appendChild(canvas);

  // Placeholder text
  const placeholder = document.createElement('div');
  placeholder.textContent = t('sig_placeholder') || 'Sign here / Firme aqui / Siyen isit';
  placeholder.style.cssText = 'position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);color:#ccc;font-size:14px;pointer-events:none;';
  placeholder.id = 'sigPlaceholder';
  wrapper.appendChild(placeholder);

  // Clear button
  const clearBtn = document.createElement('button');
  clearBtn.textContent = t('sig_clear') || 'Clear / Borrar';
  clearBtn.style.cssText = 'margin-top:6px;padding:5px 16px;background:#f44336;color:#fff;border:none;border-radius:4px;cursor:pointer;font-size:12px;';
  clearBtn.onclick = clearSignature;
  container.appendChild(clearBtn);

  _sigCanvas = canvas;
  _sigCtx = canvas.getContext('2d');
  _sigCtx.strokeStyle = '#1a237e';
  _sigCtx.lineWidth = 2.5;
  _sigCtx.lineCap = 'round';
  _sigCtx.lineJoin = 'round';
  _sigHasContent = false;

  // Mouse events
  canvas.addEventListener('mousedown', sigStart);
  canvas.addEventListener('mousemove', sigMove);
  canvas.addEventListener('mouseup', sigEnd);
  canvas.addEventListener('mouseleave', sigEnd);

  // Touch events
  canvas.addEventListener('touchstart', sigTouchStart, { passive: false });
  canvas.addEventListener('touchmove', sigTouchMove, { passive: false });
  canvas.addEventListener('touchend', sigEnd);
}

function _sigPos(e) {
  const rect = _sigCanvas.getBoundingClientRect();
  const scaleX = _sigCanvas.width / rect.width;
  const scaleY = _sigCanvas.height / rect.height;
  return {
    x: (e.clientX - rect.left) * scaleX,
    y: (e.clientY - rect.top) * scaleY,
  };
}

function sigStart(e) {
  _sigDrawing = true;
  const p = _sigPos(e);
  _sigCtx.beginPath();
  _sigCtx.moveTo(p.x, p.y);
}

function sigMove(e) {
  if (!_sigDrawing) return;
  const p = _sigPos(e);
  _sigCtx.lineTo(p.x, p.y);
  _sigCtx.stroke();
  _sigHasContent = true;
  const ph = document.getElementById('sigPlaceholder');
  if (ph) ph.style.display = 'none';
}

function sigEnd() {
  _sigDrawing = false;
}

function sigTouchStart(e) {
  e.preventDefault();
  const touch = e.touches[0];
  const rect = _sigCanvas.getBoundingClientRect();
  const scaleX = _sigCanvas.width / rect.width;
  const scaleY = _sigCanvas.height / rect.height;
  _sigDrawing = true;
  _sigCtx.beginPath();
  _sigCtx.moveTo(
    (touch.clientX - rect.left) * scaleX,
    (touch.clientY - rect.top) * scaleY
  );
}

function sigTouchMove(e) {
  e.preventDefault();
  if (!_sigDrawing) return;
  const touch = e.touches[0];
  const rect = _sigCanvas.getBoundingClientRect();
  const scaleX = _sigCanvas.width / rect.width;
  const scaleY = _sigCanvas.height / rect.height;
  _sigCtx.lineTo(
    (touch.clientX - rect.left) * scaleX,
    (touch.clientY - rect.top) * scaleY
  );
  _sigCtx.stroke();
  _sigHasContent = true;
  const ph = document.getElementById('sigPlaceholder');
  if (ph) ph.style.display = 'none';
}

function clearSignature() {
  if (!_sigCanvas) return;
  _sigCtx.clearRect(0, 0, _sigCanvas.width, _sigCanvas.height);
  _sigHasContent = false;
  const ph = document.getElementById('sigPlaceholder');
  if (ph) ph.style.display = '';
}

function getSignatureBase64() {
  if (!_sigCanvas || !_sigHasContent) return '';
  return _sigCanvas.toDataURL('image/png');
}

function hasSignature() {
  return _sigHasContent;
}
