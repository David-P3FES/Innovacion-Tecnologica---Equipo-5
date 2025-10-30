document.addEventListener('DOMContentLoaded', () => {

  const toast = (msg, ok = true) => {
    const n = document.createElement('div');
    n.className = 'notification ' + (ok ? 'success' : 'error');
    n.textContent = msg;
    
    n.style.cssText = `
      position:fixed; left:50%; top:18px; transform:translateX(-50%);
      background:${ok ? '#16a34a' : '#dc2626'}; color:#fff; font-weight:800;
      padding:10px 14px; border-radius:10px; box-shadow:0 10px 22px rgba(0,0,0,.15);
      z-index:9999; letter-spacing:.3px;
    `;
    document.body.appendChild(n);
    setTimeout(() => n.remove(), 2000);
  };

  
  document.querySelectorAll('.btn-guardar, .btn-secundario').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const r = document.createElement('span');
      r.className = 'ripple';
      const rect = btn.getBoundingClientRect();
      r.style.position = 'absolute';
      r.style.inset = '0';
      r.style.pointerEvents = 'none';
      const x = e.clientX - rect.left, y = e.clientY - rect.top;
      r.style.background = 'radial-gradient(circle at ' + x + 'px ' + y + 'px, rgba(255,255,255,.35), rgba(255,255,255,0) 40%)';
      btn.appendChild(r);
      setTimeout(() => r.remove(), 450);
    });
  });

  
  const form = document.querySelector('.profile-form')?.closest('form') || document.querySelector('form') || document;
  const saveBtn = document.querySelector('.btn-guardar');
  const cancelBtn = document.querySelector('.btn-secundario');
  const avatar = document.querySelector('.profile-avatar');

  
  const getSnapshot = () => {
    const fd = new FormData(form instanceof HTMLFormElement ? form : document.createElement('form'));
    
    if (!(form instanceof HTMLFormElement)) {
      document.querySelectorAll('.profile-form input, .profile-form select, .profile-form textarea')
        .forEach(el => fd.append(el.name || el.id || '', el.value ?? ''));
    }
    
    const obj = {};
    for (const [k, v] of fd.entries()) obj[k] = v;
    return JSON.stringify(obj);
  };
  let initial = getSnapshot();

  
  const setSaveEnabled = (enabled) => {
    if (!saveBtn) return;
    saveBtn.disabled = !enabled;
    saveBtn.style.opacity = enabled ? '1' : '.6';
    saveBtn.style.cursor = enabled ? 'pointer' : 'not-allowed';
  };
  setSaveEnabled(false);

  const checkDirty = () => {
    const now = getSnapshot();
    setSaveEnabled(now !== initial);
  };

  
  const elRFC = document.querySelector('[name="rfc"], #rfc');
  const elWA  = document.querySelector('[name="whatsapp"], #whatsapp');
  const elMail= document.querySelector('[name="email"], #email');

  if (elRFC) {
    elRFC.addEventListener('input', () => {
      elRFC.value = elRFC.value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 13);
      checkDirty();
    });
  }
  if (elWA) {
    elWA.addEventListener('input', () => {
      elWA.value = elWA.value.replace(/\D/g, '').slice(0, 15);
      checkDirty();
    });
  }
  if (elMail) {
    elMail.addEventListener('input', () => {
      checkDirty();
    });
  }

  
  document.querySelectorAll('.profile-form textarea').forEach(t => {
    const grow = () => { t.style.height = 'auto'; t.style.height = (t.scrollHeight) + 'px'; };
    t.addEventListener('input', grow); grow();
  });

  
  const elNombre   = document.querySelector('[name="nombre"], #nombre');
  const elApellido = document.querySelector('[name="apellido"], #apellido');
  const elUsuario  = document.querySelector('[name="username"], [name="usuario"], #username, #usuario');

  const computeInitials = () => {
    const n = (elNombre?.value || '').trim();
    const a = (elApellido?.value || '').trim();
    const u = (elUsuario?.value || '').trim();
    let ini = '';
    if (n || a) {
      ini = (n[0] || '') + (a[0] || '');
    } else if (u) {
      const parts = u.split(/[.\s_-]+/).filter(Boolean);
      ini = (parts[0]?.[0] || '') + (parts[1]?.[0] || '');
    }
    ini = ini.toUpperCase() || 'N';
    if (avatar) avatar.setAttribute('data-initials', ini);
  };
  [elNombre, elApellido, elUsuario].forEach(el => el && el.addEventListener('input', () => { computeInitials(); checkDirty(); }));
  computeInitials();

  
  document.querySelectorAll('.profile-form input, .profile-form select, .profile-form textarea')
    .forEach(el => el.addEventListener('input', checkDirty));

  if (cancelBtn) {
    cancelBtn.addEventListener('click', (e) => {
      e.preventDefault();
      if (form instanceof HTMLFormElement) {
        form.reset();
      } else {
        
        document.querySelectorAll('.profile-form input, .profile-form select, .profile-form textarea')
          .forEach(el => { if ('value' in el) el.value = el.defaultValue ?? ''; });
      }
      computeInitials();
      initial = getSnapshot();
      setSaveEnabled(false);
      toast('Cambios cancelados');
    });
  }

  if (saveBtn) {
    saveBtn.addEventListener('click', async (e) => {
      
      if (!(form instanceof HTMLFormElement)) e.preventDefault();

      if (elMail && elMail.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(elMail.value)) {
        toast('Email no válido', false);
        return;
      }
      if (elRFC && elRFC.value && elRFC.value.length < 12) {
        toast('RFC incompleto', false);
        return;
      }

      if (saveBtn.disabled) return;

      const originalText = saveBtn.textContent;
      saveBtn.textContent = 'Guardando...';
      saveBtn.style.pointerEvents = 'none';

      try {
        if (form instanceof HTMLFormElement && form.action) {
          form.submit();
          return;
        } else {
          await new Promise(r => setTimeout(r, 800));
          initial = getSnapshot();
          setSaveEnabled(false);
          toast('Datos guardados');
        }
      } catch (err) {
        console.error(err);
        toast('No se pudo guardar', false);
      } finally {
        saveBtn.textContent = originalText;
        saveBtn.style.pointerEvents = 'auto';
      }
    });
  }
});
