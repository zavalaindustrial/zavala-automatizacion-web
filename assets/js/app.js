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

  // 2. Buscador en Tiempo Real del Hero (Función Estrella)
  function handleHeroSearch() {
    const query = (heroSearchInput.value || "").trim();
    if (!query) {
      if (customPartCard) customPartCard.style.display = "none";
      filteredProducts = [...allProducts];
      currentPage = 1;
      renderCatalog();
      return;
    }

    // Mostrar tarjeta dinámica para CUALQUIER número de parte
    if (customPartCard && customPartQuery && customPartWaBtn) {
      customPartCard.style.display = "block";
      customPartQuery.textContent = query.toUpperCase();
      
      const urgentMsg = `Hola Zavala Automatización, me urge cotizar el No. de Parte: ${query.toUpperCase()}. ¿Lo tienen en almacén o tiempo de entrega por importación exprés?`;
      customPartWaBtn.href = `${WHATSAPP_BASE}?text=${encodeURIComponent(urgentMsg)}`;
    }

    // Filtrar catálogo general
    const qLower = query.toLowerCase();
    filteredProducts = allProducts.filter(p => 
      (p.part_number && p.part_number.toLowerCase().includes(qLower)) ||
      (p.description && p.description.toLowerCase().includes(qLower)) ||
      (p.brand && p.brand.toLowerCase().includes(qLower))
    );

    currentPage = 1;
    renderCatalog();
  }

  if (heroSearchInput) {
    heroSearchInput.addEventListener("input", handleHeroSearch);
    heroSearchInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        const catalogEl = document.getElementById("catalogo");
        if (catalogEl) catalogEl.scrollIntoView({ behavior: "smooth" });
      }
    });
  }

  if (btnHeroSearch) {
    btnHeroSearch.addEventListener("click", () => {
      handleHeroSearch();
      const catalogEl = document.getElementById("catalogo");
      if (catalogEl) catalogEl.scrollIntoView({ behavior: "smooth" });
    });
  }

  // Clicks en ejemplos del Hero
  document.querySelectorAll(".helper-example").forEach(chip => {
    chip.addEventListener("click", () => {
      const val = chip.getAttribute("data-val") || chip.textContent.trim();
      if (heroSearchInput) {
        heroSearchInput.value = val;
        handleHeroSearch();
        const catalogEl = document.getElementById("catalogo");
        if (catalogEl) catalogEl.scrollIntoView({ behavior: "smooth" });
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
    btnRfqEmail.addEventListener("click", (e) => {
      e.preventDefault();
      const d = getRfqData();
      if (!d.partes) {
        alert("Por favor escribe la lista o números de parte que necesitas cotizar.");
        document.getElementById("rfq-partes")?.focus();
        return;
      }

      const subject = `[Cotización Express] ${d.empresa} - ${d.urgente ? 'URGENTE PARO' : 'Solicitud de Partes'}`;
      let body = `Estimado equipo de Ventas Zavala Automatización y Control:\n\n`;
      body += `Solicito cotización urgente para el siguiente requerimiento:\n\n`;
      body += `Empresa: ${d.empresa}\n`;
      body += `Contacto: ${d.contacto}\n`;
      body += `Teléfono: ${d.telefono}\n`;
      body += `Correo: ${d.email}\n`;
      body += `Prioridad: ${d.urgente}\n\n`;
      body += `Números de Parte / Detalle:\n${d.partes}\n\n`;
      body += `Quedo a la espera de su respuesta formal con tiempos de entrega y condiciones.\n`;

      window.location.href = `mailto:ventas1@zavalaindustrial.net?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
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
