/**
 * app.js - Lógica Interactiva del Buscador y Catálogo B2B Industrial
 * Zavala Automatización y Control S.A. de C.V.
 */

document.addEventListener("DOMContentLoaded", () => {
  const WHATSAPP_BASE = "https://wa.me/5218132507130";
  let allProducts = [];         // Catálogo completo (11,619 productos) para hero search
  let catalogProducts = [];     // Catálogo Odoo verificado (143 productos) para tabla
  let filteredProducts = [];
  let currentPage = 1;
  const itemsPerPage = 12;

  // Elementos DOM
  const heroSearchInput = document.getElementById("hero-search-input");
  const btnHeroSearch = document.getElementById("btn-hero-search");
  const customPartCard = document.getElementById("custom-part-card");
  
  const catalogSearchInput = document.getElementById("catalog-search-input");
  const catalogTbody = document.getElementById("catalog-tbody");
  const catalogCount = document.getElementById("catalog-count");
  const pageInfo = document.getElementById("page-info");
  const btnPrevPage = document.getElementById("btn-prev-page");
  const btnNextPage = document.getElementById("btn-next-page");
  const filterButtons = document.querySelectorAll(".filter-btn");

  // RFQ Form
  const rfqForm = document.getElementById("rfq-form");
  const btnRfqWa = document.getElementById("btn-rfq-wa");
  const btnRfqEmail = document.getElementById("btn-rfq-email");

  // 1. Cargar productos Odoo (143) para el catálogo en vivo con entrega inmediata
  fetch("data/productos_odoo.json")
    .then(res => res.ok ? res.json() : [])
    .then(data => {
      catalogProducts = data;
      filteredProducts = [...catalogProducts];
      renderCatalog();
    })
    .catch(err => {
      console.warn("Fallo carga productos_odoo.json:", err);
    });

  // 2. Cargar catálogo completo (11,619) para el buscador global en tiempo real
  fetch("data/productos.json")
    .then(res => res.ok ? res.json() : [])
    .then(data => {
      allProducts = data;
      if (!catalogProducts || catalogProducts.length === 0) {
        catalogProducts = data.slice(0, 143);
        filteredProducts = [...catalogProducts];
        renderCatalog();
      }
    })
    .catch(err => {
      console.warn("Fallo carga productos.json:", err);
    });

  // 3. Buscador en Tiempo Real del Hero (Búsqueda sobre los 11,619 productos)
  function handleHeroSearch() {
    const query = (heroSearchInput ? heroSearchInput.value : "").trim();
    if (!query) {
      if (customPartCard) {
        customPartCard.style.display = "none";
        customPartCard.innerHTML = "";
      }
      return;
    }

    if (!customPartCard) return;

    const qLower = query.toLowerCase();

    // Buscar coincidencias en todo el inventario
    const matches = allProducts.filter(p => {
      const pn = (p.part_number || p.code || "").toLowerCase();
      const desc = (p.description || "").toLowerCase();
      const br = (p.brand || "").toLowerCase();
      return pn.includes(qLower) || desc.includes(qLower) || br.includes(qLower);
    });

    matches.sort((a, b) => {
      const aPn = (a.part_number || a.code || "").toLowerCase();
      const bPn = (b.part_number || b.code || "").toLowerCase();
      if (aPn === qLower) return -1;
      if (bPn === qLower) return 1;
      if (aPn.startsWith(qLower) && !bPn.startsWith(qLower)) return -1;
      if (!aPn.startsWith(qLower) && bPn.startsWith(qLower)) return 1;
      return 0;
    });

    customPartCard.style.display = "block";

    if (matches.length > 0) {
      const matchedItem = matches[0];
      customPartCard.className = "custom-part-card";

      const urgentMsg = `Hola Zavala Automatización, me interesa cotizar para entrega inmediata el No. de Parte ${matchedItem.part_number} (${matchedItem.description}). ¿Tienen disponibilidad y tiempo de entrega?`;
      const waUrl = `${WHATSAPP_BASE}?text=${encodeURIComponent(urgentMsg)}`;

      let suggestionsHtml = "";
      if (matches.length > 1) {
        const others = matches.slice(1, 5);
        suggestionsHtml = `
          <div class="hero-matches-suggestions" style="margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 0.85rem;">
            <span style="color: #94a3b8; margin-right: 6px;">Otras coincidencias en catálogo:</span>
            ${others.map(item => `
              <button type="button" class="search-suggestion-chip" data-part="${item.part_number}">
                ${item.part_number}
              </button>
            `).join("")}
          </div>
        `;
      }

      customPartCard.innerHTML = `
        <div class="custom-part-card-content">
          <div class="custom-part-text">
            <div style="margin-bottom: 6px;">
              <span class="badge-cat" style="background: rgba(14, 165, 233, 0.15); color: #38bdf8; border: 1px solid rgba(14, 165, 233, 0.3);">✓ REFERENCIA EN CATÁLOGO</span>
            </div>
            <h4 style="font-size: 1.15rem; color: #fff; margin-bottom: 4px;">
              No. de Parte: <strong class="part-number-code" style="color: #38bdf8;">${matchedItem.part_number}</strong> (${matchedItem.brand || 'Industrial'})
            </h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 4px;">${matchedItem.description}</p>
            <p style="color: #4ade80; font-size: 0.9rem; margin-top: 4px; font-weight: 500;">
              Suministro y cotización formal de componentes de automatización para plantas en todo México.
            </p>
          </div>
          <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px;">
            <a href="${waUrl}" target="_blank" class="btn btn-wa-large" style="flex: 1; min-width: 200px; justify-content: center;">
              <span>💬</span> Cotizar por WhatsApp
            </a>
            <a href="producto.html?p=${encodeURIComponent(matchedItem.part_number)}" class="btn btn-outline-cyan" style="flex: 1; min-width: 200px; justify-content: center;">
              🔍 Ver Ficha Técnica y Detalles
            </a>
          </div>
        </div>
        ${suggestionsHtml}
      `;

      customPartCard.querySelectorAll(".search-suggestion-chip").forEach(chip => {
        chip.addEventListener("click", (e) => {
          e.preventDefault();
          const pCode = chip.getAttribute("data-part");
          if (pCode && heroSearchInput) {
            heroSearchInput.value = pCode;
            handleHeroSearch();
          }
        });
      });

    } else {
      customPartCard.className = "custom-part-card";
      const urgentMsg = `Hola Zavala Automatización, me urge cotizar el No. de Parte: ${query.toUpperCase()}. ¿Lo tienen en almacén o tiempo de entrega por importación exprés?`;
      const waUrl = `${WHATSAPP_BASE}?text=${encodeURIComponent(urgentMsg)}`;

      customPartCard.innerHTML = `
        <div class="custom-part-card-content">
          <div class="custom-part-text">
            <div style="margin-bottom: 6px;">
              <span class="badge-cat" style="background: rgba(14, 165, 233, 0.15); color: #38bdf8; border: 1px solid rgba(14, 165, 233, 0.3);">🔍 BÚSQUEDA Y SUMINISTRO INDUSTRIAL</span>
            </div>
            <h4 style="font-size: 1.15rem; color: #fff; margin-bottom: 4px;">
              ¿Buscas el No. de Parte <span class="part-number-code" style="color: #38bdf8;">${query.toUpperCase()}</span>?
            </h4>
            <p style="color: #cbd5e1; font-size: 0.95rem;">
              Localizamos y suministramos refacciones y componentes de automatización industrial para plantas en todo México.
            </p>
          </div>
          <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px;">
            <a href="${waUrl}" target="_blank" class="btn btn-wa-large" style="flex: 1; min-width: 200px; justify-content: center;">
              <span>💬</span> Cotizar por WhatsApp
            </a>
            <a href="producto.html?p=${encodeURIComponent(query)}" class="btn btn-outline-cyan" style="flex: 1; min-width: 200px; justify-content: center;">
              🔍 Consultar Ficha Técnica
            </a>
          </div>
        </div>
      `;
    }
  }

  if (heroSearchInput) {
    heroSearchInput.addEventListener("input", handleHeroSearch);
    heroSearchInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        handleHeroSearch();
      }
    });
  }

  if (btnHeroSearch) {
    btnHeroSearch.addEventListener("click", () => {
      handleHeroSearch();
    });
  }

  document.querySelectorAll(".helper-example").forEach(chip => {
    chip.addEventListener("click", () => {
      const val = chip.getAttribute("data-val") || chip.textContent.trim();
      if (heroSearchInput) {
        heroSearchInput.value = val;
        handleHeroSearch();
      }
    });
  });

  // 4. Filtros por Categoría en Catálogo de Entrega Inmediata
  filterButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      filterButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      
      const cat = btn.getAttribute("data-category");
      const searchVal = (catalogSearchInput?.value || "").toLowerCase().trim();

      applyCatalogFilters(cat, searchVal);
    });
  });

  if (catalogSearchInput) {
    catalogSearchInput.addEventListener("input", () => {
      const activeBtn = document.querySelector(".filter-btn.active");
      const cat = activeBtn ? activeBtn.getAttribute("data-category") : "todos";
      applyCatalogFilters(cat, catalogSearchInput.value.toLowerCase().trim());
    });
  }

  function applyCatalogFilters(category, searchQuery) {
    const baseSource = (catalogProducts && catalogProducts.length > 0) ? catalogProducts : allProducts;
    filteredProducts = baseSource.filter(p => {
      const matchCat = (category === "todos" || !category) ? true : (p.category === category || p.brand === category);
      const matchSearch = !searchQuery ? true : (
        (p.part_number && p.part_number.toLowerCase().includes(searchQuery)) ||
        (p.description && p.description.toLowerCase().includes(searchQuery)) ||
        (p.brand && p.brand.toLowerCase().includes(searchQuery))
      );
      return matchCat && matchSearch;
    });

    currentPage = 1;
    renderCatalog();
  }

  // 5. Renderizado y Paginación del Catálogo
  function renderCatalog() {
    if (!catalogTbody) return;

    if (catalogCount) {
      catalogCount.textContent = `Mostrando ${filteredProducts.length} productos con entrega inmediata`;
    }

    if (filteredProducts.length === 0) {
      catalogTbody.innerHTML = `
        <tr>
          <td colspan="5" class="text-center py-4">
            <p style="margin-bottom: 12px; color: #cbd5e1;">No se encontró ningún registro exacto en el listado base para esta búsqueda.</p>
            <p style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 16px;">Suministramos más de 50,000 números de parte por importación directa o catálogo extendido.</p>
            <a href="${WHATSAPP_BASE}?text=Hola%20Zavala%2C%20busco%20un%20n%C3%BAmero%20de%20parte%20especial%20que%20no%20veo%20en%20el%20listado" target="_blank" class="btn btn-accent btn-sm">
              💬 Consultar No. de Parte con Asesor por WhatsApp
            </a>
          </td>
        </tr>
      `;
      if (pageInfo) pageInfo.textContent = "Página 0 de 0";
      if (btnPrevPage) btnPrevPage.disabled = true;
      if (btnNextPage) btnNextPage.disabled = true;
      return;
    }

    const totalPages = Math.ceil(filteredProducts.length / itemsPerPage);
    if (currentPage > totalPages) currentPage = totalPages;
    if (currentPage < 1) currentPage = 1;

    const startIdx = (currentPage - 1) * itemsPerPage;
    const endIdx = startIdx + itemsPerPage;
    const pageItems = filteredProducts.slice(startIdx, endIdx);

    let rowsHtml = "";
    pageItems.forEach(item => {
      const waUrl = item.whatsapp_url || `${WHATSAPP_BASE}?text=${encodeURIComponent(`Hola Zavala, requiero cotización del No. de Parte: ${item.part_number}`)}`;
      rowsHtml += `
        <tr>
          <td><a href="producto.html?p=${encodeURIComponent(item.part_number)}" style="color:#38bdf8;text-decoration:none;"><strong class="part-number-code">${escapeHtml(item.part_number)}</strong></a></td>
          <td>${escapeHtml(item.description)}</td>
          <td><span class="badge-cat">${escapeHtml(item.brand || item.category)}</span></td>
          <td><span class="badge-stock">⚡ Entrega Inmediata</span></td>
          <td>
            <div style="display:flex;gap:6px;align-items:center;">
              <a href="producto.html?p=${encodeURIComponent(item.part_number)}" class="btn btn-sm btn-outline-cyan" title="Ver Ficha Técnica y Especificaciones">🔍 Ficha</a>
              <a href="${waUrl}" target="_blank" class="btn btn-table-wa">Cotizar WhatsApp</a>
            </div>
          </td>
        </tr>
      `;
    });

    catalogTbody.innerHTML = rowsHtml;

    if (pageInfo) {
      pageInfo.textContent = `Página ${currentPage} de ${totalPages}`;
    }
    if (btnPrevPage) btnPrevPage.disabled = (currentPage === 1);
    if (btnNextPage) btnNextPage.disabled = (currentPage === totalPages);
  }

  if (btnPrevPage) {
    btnPrevPage.addEventListener("click", () => {
      if (currentPage > 1) {
        currentPage--;
        renderCatalog();
      }
    });
  }

  if (btnNextPage) {
    btnNextPage.addEventListener("click", () => {
      const totalPages = Math.ceil(filteredProducts.length / itemsPerPage);
      if (currentPage < totalPages) {
        currentPage++;
        renderCatalog();
      }
    });
  }

  // 6. Envío de Formulario RFQ
  function getRfqData() {
    const empresa = document.getElementById("rfq-empresa")?.value.trim() || "No especificada";
    const contacto = document.getElementById("rfq-contacto")?.value.trim() || "No especificado";
    const telefono = document.getElementById("rfq-telefono")?.value.trim() || "No especificado";
    const email = document.getElementById("rfq-email")?.value.trim() || "No especificado";
    const partes = document.getElementById("rfq-partes")?.value.trim() || "";
    const urgente = document.getElementById("rfq-urgente")?.checked ? "SÍ - REQUERIMIENTO URGENTE / ENTREGA INMEDIATA" : "Cotización normal de suministro";

    return { empresa, contacto, telefono, email, partes, urgente };
  }

  if (btnRfqWa) {
    btnRfqWa.addEventListener("click", (e) => {
      e.preventDefault();
      const d = getRfqData();
      if (!d.partes) {
        alert("Por favor escribe la lista o números de parte que necesitas cotizar.");
        document.getElementById("rfq-partes")?.focus();
        return;
      }

      let msg = `*SOLICITUD DE COTIZACIÓN ZAVALA*
`;
      msg += `⚡ *Prioridad:* ${d.urgente}
`;
      msg += `🏢 *Empresa:* ${d.empresa}
`;
      msg += `👤 *Contacto:* ${d.contacto}
`;
      msg += `📞 *Tel/WA:* ${d.telefono}
`;
      msg += `✉️ *Correo:* ${d.email}

`;
      msg += `📋 *Números de Parte Requeridos:*
${d.partes}

`;
      msg += `Por favor confirmar disponibilidad y cotización.`;

      window.open(`${WHATSAPP_BASE}?text=${encodeURIComponent(msg)}`, "_blank");
    });
  }

  if (btnRfqEmail) {
    btnRfqEmail.addEventListener("click", async (e) => {
      e.preventDefault();
      const d = getRfqData();
      if (!d.partes) {
        alert("Por favor escribe la lista o números de parte que necesitas cotizar.");
        document.getElementById("rfq-partes")?.focus();
        return;
      }

      const originalBtnText = btnRfqEmail.innerHTML;
      btnRfqEmail.innerHTML = "⏳ Enviando correo directo...";
      btnRfqEmail.disabled = true;

      const subject = `[Cotización Web] ${d.empresa || 'Empresa'} - ${d.urgente.includes('URGENTE') ? 'URGENTE ENTREGA INMEDIATA' : 'Solicitud de Partes'}`;
      
      try {
        const response = await fetch("https://formsubmit.co/ajax/ventas1@zavalaindustrial.net", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
          },
          body: JSON.stringify({
            _subject: subject,
            _template: "table",
            empresa: d.empresa || "No especificada",
            contacto: d.contacto || "No especificado",
            telefono_o_whatsapp: d.telefono || "No especificado",
            correo_cliente: d.email || "No especificado",
            prioridad_urgente: d.urgente,
            lista_de_refacciones: d.partes
          })
        });

        if (response.ok) {
          btnRfqEmail.innerHTML = "✓ ¡Cotización Enviada!";
          btnRfqEmail.style.background = "#10b981";
          btnRfqEmail.style.color = "#fff";
          
          let alertEl = document.getElementById("rfq-success-alert");
          if (!alertEl) {
            alertEl = document.createElement("div");
            alertEl.id = "rfq-success-alert";
            alertEl.style.cssText = "margin-top: 15px; padding: 12px 16px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 6px; color: #4ade80; font-size: 0.95rem; text-align: center;";
            rfqForm.appendChild(alertEl);
          }
          alertEl.innerHTML = "<strong>✓ ¡Mensaje enviado con éxito a ventas1@zavalaindustrial.net!</strong><br>Nuestro equipo te responderá a la brevedad con la cotización formal.";
          
          if (rfqForm) rfqForm.reset();
        } else {
          throw new Error("HTTP error " + response.status);
        }
      } catch (err) {
        console.warn("Fallo envio API, usando cliente local mailto:", err);
        btnRfqEmail.innerHTML = originalBtnText;
        btnRfqEmail.disabled = false;
        
        let body = `Estimado equipo de Ventas:

Empresa: ${d.empresa}
Contacto: ${d.contacto}
Teléfono: ${d.telefono}
Correo: ${d.email}
Urgente: ${d.urgente}

Partes:
${d.partes}`;
        window.location.href = `mailto:ventas1@zavalaindustrial.net?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      }
    });
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
});
