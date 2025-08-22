document.addEventListener("DOMContentLoaded", () => {
  // Spinner y bloqueo de botón al enviar (sin impedir el submit)
  document.querySelectorAll("form.login-form").forEach((form) => {
    form.addEventListener("submit", () => {
      const btn = form.querySelector("button[type='submit']");
      if (!btn) return;
      const original = btn.textContent.trim();
      const loadingText = btn.dataset.loadingText || "Enviando…";
      btn.dataset.originalText = original;
      btn.classList.add("loading");
      btn.textContent = loadingText;
      btn.disabled = true;
      // NO prevention: dejamos que el form se envíe a Django
    });
  });

  // Validación en vivo: contraseñas iguales en signup
  const pass1 = document.getElementById("password1");
  const pass2 = document.getElementById("password2");
  if (pass1 && pass2) {
    const validate = () => {
      if (pass2.value && pass1.value !== pass2.value) {
        pass2.setCustomValidity("Las contraseñas no coinciden");
      } else {
        pass2.setCustomValidity("");
      }
    };
    pass1.addEventListener("input", validate);
    pass2.addEventListener("input", validate);
  }

  // UX: mostrar/ocultar contraseña con doble clic en el label (opcional)
  document.querySelectorAll("label[for='password1'], label[for='id_password']").forEach((lbl) => {
    lbl.addEventListener("dblclick", () => {
      const input = document.getElementById(lbl.getAttribute("for"));
      if (!input) return;
      input.type = input.type === "password" ? "text" : "password";
      input.focus();
    });
  });
});
