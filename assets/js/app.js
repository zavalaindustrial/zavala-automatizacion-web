/**
 * app.js - Lógica Interactiva del Buscador y Catálogo B2B Industrial
 * Zavala Automatización y Control S.A. de C.V.
 */

document.addEventListener("DOMContentLoaded", () => {
  const WHATSAPP_BASE = "https://wa.me/5218132507130";
  let allProducts = [];
  let filteredProducts = [];
  let currentPage = 1;
  const itemsPerPage = 12;

  // Elementos DOM
  const heroSearchInput = document.getElementById("hero-search-input");
  const btnHeroSearch = document.getElementById("btn-hero-search");
  const customPartCard = document.getElementById("custom-part-card");
  const customPartQuery = document.getElementById("custom-part-query");
  const customPartWaBtn = document.getElementById("custom-part-wa-btn");
  
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

  // 1. Cargar datos de productos.json
  fetch("data/productos.json")
    .then(res => {
      if (!res.ok) throw new Error("Error cargando productos.json");
      return res.json();
    })
    .then(data => {
      allProducts = data;
      filteredProducts = [...allProducts];
      renderCatalog();
    })
    .catch(err => {
      console.warn("Fallo fetch local, cargando respaldo embebido:", err);
      // Respaldo de emergencia
      allProducts = [
        { id: 192, part_number: "1746-P2", description: "FUENTE DE ALIMENTACION 120/240 5A SLC 500", brand: "Allen-Bradley", category: "Fuentes de Alimentación" },
        { id: 114, part_number: "55.34.9.024.0040", description: "FINDER RELEVADOR ENCAPSULADO 24VDC", brand: "Finder", category: "Relevación y Seguridad" },
        { id: 191, part_number: "SMC SY3A0R-5U1-NA", description: "VALVULA SELENOIDE NEUMATICA 4/5", brand: "SMC", category: "Neumática y Válvulas" },
        { id: 194, part_number: "OT100F3", description: "INTERRUPTOR DESCONECTOR DE 3 POLOS ABB", brand: "ABB", category: "Maniobra y Protección Eléctrica" },
        { id: 178, part_number: "PRW12-4DP", description: "SENSOR DE PROXIMIDAD INDUCTIVO 12MM", brand: "Autonics", category: "Sensores e Instrumentación" }
      ];
      filteredProducts = [...allProducts];
      renderCatalog();
    });

  // 2. Buscador en Tiempo Real del Hero (Detección Inmediata de Stock y Sugerencias)
  function handleHeroSearch() {
    const query = (heroSearchInput ? heroSearchInput.value : "").trim();
    if (!query) {
      if (customPartCard) {
        customPartCard.style.display = "none";
        customPartCard.innerHTML = "";
      }
      filteredProducts = [...allProducts];
      currentPage = 1;
      renderCatalog();
      return;
    }

    if (!customPartCard) return;

    const qLower = query.toLowerCase();

    // 1. Buscar coincidencias en el inventario/catálogo
    const matches = allProducts.filter(p => {
      const pn = (p.part_number || p.code || "").toLowerCase();
      const desc = (p.description || "").toLowerCase();
      const br = (p.brand || "").toLowerCase();
      return pn.includes(qLower) || desc.includes(qLower) || br.includes(qLower);
    });

    // Ordenar coincidencias: prioridad a coincidencia exacta o inicio en part_number
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
      // CASO 1: SÍ HAY COINCIDENCIA EN EL CATÁLOGO (Stock Local / Catálogo)
      const matchedItem = matches[0];
      customPartCard.className = "custom-part-card is-in-stock";

      const urgentMsg = `Hola Zavala Automatización, me interesa cotizar para entrega inmediata el No. de Parte en stock: ${matchedItem.part_number} (${matchedItem.description}). ¿Tienen disponibilidad y tiempo de entrega?`;
      const waUrl = `${WHATSAPP_BASE}?text=${encodeURIComponent(urgentMsg)}`;

      let suggestionsHtml = "";
      if (matches.length > 1) {
        const others = matches.slice(1, 5);
        suggestionsHtml = `
          <div class="hero-matches-suggestions" style="margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 0.85rem;">
            <span style="color: #94a3b8; margin-right: 6px;">Otras coincidencias en almacén:</span>
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
              <span class="badge-stock">✓ EN INVENTARIO LOCAL / CATÁLOGO</span>
            </div>
            <h4 style="font-size: 1.15rem; color: #fff; margin-bottom: 4px;">
              No. de Parte: <strong class="part-number-code" style="color: #38bdf8;">${matchedItem.part_number}</strong> (${matchedItem.brand || 'Industrial'})
            </h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 4px;">${matchedItem.description}</p>
            <p style="color: #4ade80; font-size: 0.9rem; margin-top: 4px; font-weight: 500;">
              ✓ Pieza registrada en almacén. Suministro local y entrega inmediata disponible.
            </p>
          </div>
          <a href="${waUrl}" target="_blank" class="btn btn-wa-large">
            <span>💬</span> Cotizar Entrega Inmediata (Pieza en Stock)
          </a>
        </div>
        ${suggestionsHtml}
      `;

      // Event listeners para chips de sugerencias
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
      // CASO 2: NO HAY COINCIDENCIA (Importación y Suministro Directo)
      customPartCard.className = "custom-part-card is-custom";

      const urgentMsg = `Hola Zavala Automatización, me urge cotizar el No. de Parte: ${query.toUpperCase()}. ¿Lo tienen en almacén o tiempo de entrega por importación exprés?`;
      const waUrl = `${WHATSAPP_BASE}?text=${encodeURIComponent(urgentMsg)}`;

      customPartCard.innerHTML = `
        <div class="custom-part-card-content">
          <div class="custom-part-text">
            <div style="margin-bottom: 6px;">
              <span class="badge-cat" style="background: rgba(245, 158, 11, 0.15); color: #fbbf24; border-color: rgba(245, 158, 11, 0.3);">⚡ IMPORTACIÓN Y SUMINISTRO DIRECTO</span>
            </div>
            <h4 style="font-size: 1.15rem; color: #fff; margin-bottom: 4px;">
              ¿Buscas el No. de Parte <span class="part-number-code" style="color: #fbbf24;">${query.toUpperCase()}</span>?
            </h4>
            <p style="color: #cbd5e1; font-size: 0.95rem;">
              No está en mostrador local, pero lo localizamos y suministramos por importación express en tiempo récord.
            </p>
          </div>
          <a href="${waUrl}" target="_blank" class="btn btn-wa-large">
            <span>💬</span> Cotizar este No. de Parte por WhatsApp
          </a>
        </div>
      `;
    }

    filteredProducts = matches;
    currentPage = 1;
    renderCatalog();
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

  // Clicks en ejemplos del Hero
  document.querySelectorAll(".helper-example").forEach(chip => {
    chip.addEventListener("click", () => {
      const val = chip.getAttribute("data-val") || chip.textContent.trim();
      if (heroSearchInput) {
        heroSearchInput.value = val;
        handleHeroSearch();
      }
    });
  });

  // 3. Filtros por Categoría en Catálogo
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
    filteredProducts = allProducts.filter(p => {
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

  // 4. Renderizado y Paginación del Catálogo
  function renderCatalog() {
    if (!catalogTbody) return;

    if (catalogCount) {
      catalogCount.textContent = `Mostrando ${filteredProducts.length} productos`;
    }

    if (filteredProducts.length === 0) {
      catalogTbody.innerHTML = `
        <tr>
          <td colspan="5" class="text-center py-4">
            <p style="margin-bottom: 12px; color: #cbd5e1;">No se encontró ningún registro exacto en el listado base para esta búsqueda.</p>
            <p style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 16px;">Suministramos más de 50,000 números de parte por importación directa o convenio con fabricantes.</p>
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
          <td><strong class="part-number-code">${escapeHtml(item.part_number)}</strong></td>
          <td>${escapeHtml(item.description)}</td>
          <td><span class="badge-cat">${escapeHtml(item.brand || item.category)}</span></td>
          <td><span class="badge-stock">✓ Suministro Express</span></td>
          <td>
            <a href="${waUrl}" target="_blank" class="btn btn-table-wa">
              Cotizar WhatsApp
            </a>
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

  // 5. Envío de Formulario RFQ
  function getRfqData() {
    const empresa = document.getElementById("rfq-empresa")?.value.trim() || "No especificada";
    const contacto = document.getElementById("rfq-contacto")?.value.trim() || "No especificado";
    const telefono = document.getElementById("rfq-telefono")?.value.trim() || "No especificado";
    const email = document.getElementById("rfq-email")?.value.trim() || "No especificado";
    const partes = document.getElementById("rfq-partes")?.value.trim() || "";
    const urgente = document.getElementById("rfq-urgente")?.checked ? "SÍ - PARO DE PLANTA URGENTE" : "Cotización normal de suministro";

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

      let msg = `*SOLICITUD DE COTIZACIÓN ZAVALA*\n`;
      msg += `🚨 *Prioridad:* ${d.urgente}\n`;
      msg += `🏢 *Empresa:* ${d.empresa}\n`;
      msg += `👤 *Contacto:* ${d.contacto}\n`;
      msg += `📞 *Tel/WA:* ${d.telefono}\n`;
      msg += `✉️ *Correo:* ${d.email}\n\n`;
      msg += `📋 *Números de Parte Requeridos:*\n${d.partes}\n\n`;
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

      const subject = `[Cotización Web] ${d.empresa || 'Empresa'} - ${d.urgente ? 'URGENTE PARO' : 'Solicitud de Partes'}`;
      
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
            prioridad_urgente: d.urgente ? "SÍ - REQUERIMIENTO URGENTE" : "Normal",
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
        
        let body = `Estimado equipo de Ventas:\n\nEmpresa: ${d.empresa}\nContacto: ${d.contacto}\nTeléfono: ${d.telefono}\nCorreo: ${d.email}\nUrgente: ${d.urgente}\n\nPartes:\n${d.partes}`;
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
