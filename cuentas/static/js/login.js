/*!
 * @file login.js
 * @brief UX de formularios: spinner submit, validación signup y mostrar/ocultar contraseña.
 */

document.addEventListener("DOMContentLoaded", () => {
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
    });
  });

  const pass1 = document.getElementById("id_password1") || document.querySelector('input[name="password1"]');
  const pass2 = document.getElementById("id_password2") || document.querySelector('input[name="password2"]');
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

  window.togglePassword = function togglePassword(inputId, btn) {
    const input = document.getElementById(inputId);
    if (!input) return;
    const icon = btn?.querySelector("i");
    if (input.type === "password") {
      input.type = "text";
      input.style.webkitTextSecurity = "none";
      if (icon) icon.className = "fas fa-eye";
    } else {
      input.type = "password";
      input.style.webkitTextSecurity = "";
      if (icon) icon.className = "fas fa-eye-slash";
    }
  };

  ["id_password", "id_password1", "id_password2"].forEach((id) => {
    const lbl = document.querySelector(`label[for="${id}"]`);
    if (!lbl) return;
    lbl.addEventListener("dblclick", () => {
      const btn = lbl.closest(".form-group")?.querySelector(".toggle-password");
      window.togglePassword(id, btn);
      document.getElementById(id)?.focus();
    });
  });

  if (document.getElementById("loginForm")) {
    const css = `
#loginForm .password-wrapper { position: relative; }
#loginForm .password-wrapper input[type="password"],
#loginForm .password-wrapper input[type="text"] { padding-right: 48px; }
#loginForm .password-wrapper .toggle-password{
  position:absolute; right:12px; top:50% !important; bottom:auto !important;
  transform: translateY(calc(-50% + 18px)); /* ajusta aquí: +18px, +10px, etc. */
  width:36px; height:36px; display:flex; align-items:center; justify-content:center;
  border:0; background:transparent; cursor:pointer; color:var(--text-light); z-index:2;
}
#loginForm .password-wrapper .toggle-password:hover { color: var(--accent-blue); }
#loginForm .password-wrapper .toggle-password:focus-visible { outline: 2px solid var(--accent-blue); outline-offset: 2px; }
#loginForm .password-wrapper input[type="password"]::-ms-reveal,
#loginForm .password-wrapper input[type="password"]::-ms-clear { display:none; width:0; height:0; }
#loginForm .password-wrapper input::-webkit-textfield-decoration-container,
#loginForm .password-wrapper input::-webkit-clear-button,
#loginForm .password-wrapper input::-webkit-credentials-auto-fill-button,
#loginForm .password-wrapper input::-webkit-contacts-auto-fill-button {
  display:none !important; visibility:hidden !important; pointer-events:none !important;
}`;
    const style = document.createElement("style");
    style.setAttribute("data-injected", "login-only-eye");
    style.textContent = css;
    document.head.appendChild(style);
  }
});

if (document.getElementById("signupForm")) {
  const cssSignup = `
#signupForm .password-wrapper { position: relative; }

#signupForm .password-wrapper input[type="password"],
#signupForm .password-wrapper input[type="text"] {
  padding-right: 48px; /* espacio para el ojo */
}

#signupForm .password-wrapper .toggle-password{
  position: absolute;
  right: 12px;
  top: 50% !important;
  bottom: auto !important;
  transform: translateY(calc(-50% + 2px)) !important; 
  width: 36px; height: 36px;
  display: flex; align-items: center; justify-content: center;
  border: 0; background: transparent; cursor: pointer;
  color: var(--text-light); z-index: 2;
}

#signupForm .password-wrapper .toggle-password:hover { color: var(--accent-blue); }
#signupForm .password-wrapper .toggle-password:focus-visible { outline: 2px solid var(--accent-blue); outline-offset: 2px; }

#signupForm .password-wrapper input[type="password"]::-ms-reveal,
#signupForm .password-wrapper input[type="password"]::-ms-clear { display:none; width:0; height:0; }
#signupForm .password-wrapper input::-webkit-textfield-decoration-container,
#signupForm .password-wrapper input::-webkit-clear-button,
#signupForm .password-wrapper input::-webkit-credentials-auto-fill-button,
#signupForm .password-wrapper input::-webkit-contacts-auto-fill-button {
  display:none !important; visibility:hidden !important; pointer-events:none !important;
}`;
  const styleSignup = document.createElement("style");
  styleSignup.setAttribute("data-injected", "signup-only-eye");
  styleSignup.textContent = cssSignup;
  document.head.appendChild(styleSignup);
}
