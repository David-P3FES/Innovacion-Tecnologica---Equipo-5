/**
 * @file login.js
 * @brief Script de interacción para formularios de Login/Registro en Django.
 * @details
 *  - Añade un spinner y bloquea el botón de enviar durante el submit.
 *  - Valida en vivo la coincidencia de contraseñas en el registro.
 *  - Permite mostrar/ocultar contraseñas con doble clic en el label.
 */

document.addEventListener("DOMContentLoaded", () => {
  /**
   * @section SpinnerSubmit
   * @brief Añade spinner y deshabilita el botón submit al enviar formulario.
   *
   * - Evita múltiples envíos del formulario.
   * - Cambia el texto del botón por uno de "cargando".
   * - No cancela el submit: Django recibe la petición normalmente.
   */
  document.querySelectorAll("form.login-form").forEach((form) => {
    form.addEventListener("submit", () => {
      const btn = form.querySelector("button[type='submit']");
      if (!btn) return;

      const original = btn.textContent.trim();                ///< Texto original del botón
      const loadingText = btn.dataset.loadingText || "Enviando…"; ///< Texto de carga opcional
      btn.dataset.originalText = original;                    ///< Se guarda el texto original
      btn.classList.add("loading");                           ///< Clase CSS para mostrar loader
      btn.textContent = loadingText;                          ///< Texto visible de carga
      btn.disabled = true;                                    ///< Bloquea el botón
    });
  });

  /**
   * @section PasswordValidation
   * @brief Validación en vivo de contraseñas iguales en el formulario de registro.
   *
   * @details
   * - Verifica que los campos `password1` y `password2` coincidan.
   * - Si no coinciden, agrega un mensaje de error al input `password2`.
   */
  const pass1 = document.getElementById("password1");
  const pass2 = document.getElementById("password2");
  if (pass1 && pass2) {
    const validate = () => {
      if (pass2.value && pass1.value !== pass2.value) {
        pass2.setCustomValidity("Las contraseñas no coinciden"); ///< Mensaje de error
      } else {
        pass2.setCustomValidity(""); ///< Elimina error si coinciden
      }
    };
    pass1.addEventListener("input", validate);
    pass2.addEventListener("input", validate);
  }

  /**
   * @section TogglePassword
   * @brief UX extra: mostrar/ocultar contraseña con doble clic en el label.
   *
   * @details
   * - Aplica a labels asociados a `password1` o `id_password`.
   * - Cambia el tipo de input entre `password` y `text`.
   */
  document.querySelectorAll("label[for='password1'], label[for='id_password']").forEach((lbl) => {
    lbl.addEventListener("dblclick", () => {
      const input = document.getElementById(lbl.getAttribute("for"));
      if (!input) return;
      input.type = input.type === "password" ? "text" : "password"; ///< Alterna tipo
      input.focus();
    });
  });
});
