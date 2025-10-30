document.addEventListener('DOMContentLoaded', () => {
  
  document.querySelectorAll('.btn-guardar').forEach(btn=>{
    btn.addEventListener('click', (e)=>{
      const r = document.createElement('span');
      r.className = 'ripple';
      const rect = btn.getBoundingClientRect();
      r.style.left = (e.clientX - rect.left) + 'px';
      r.style.top  = (e.clientY - rect.top)  + 'px';
      btn.appendChild(r);
      setTimeout(()=> r.remove(), 700);
    });
  });

  
  const copyables = document.querySelectorAll('.profile-info p');
  const toast = (msg, ok=true)=>{
    const n = document.createElement('div');
    n.className = 'notification ' + (ok ? 'success' : 'error');
    n.textContent = msg;
    document.body.appendChild(n);
    setTimeout(()=> n.remove(), 2000);
  };
  copyables.forEach(el=>{
    if(el.textContent.includes('@') || el.textContent.match(/^\d{8,}$/)){
      el.style.cursor = "pointer";
      el.addEventListener('click', async ()=>{
        const text = el.textContent.replace(/^[^:]+:/,'').trim();
        try{
          await navigator.clipboard.writeText(text);
          toast('Copiado al portapapeles');
        }catch{
          toast('No se pudo copiar', false);
        }
      });
    }
  });
});
