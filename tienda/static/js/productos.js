document.addEventListener("DOMContentLoaded", function () {
    cargarProductos();
});

let productos = []; // Almacena los productos para filtrar

function cargarProductos() {
    fetch("/api/productos/")
        .then(response => response.json())
        .then(data => {
            productos = data;
            mostrarProductos(data);
            cargarFiltros(data);
        });
}

function mostrarProductos(lista) {
    const contenedor = document.getElementById("productos-container");
    contenedor.innerHTML = "";

    lista.forEach(producto => {
        const card = document.createElement("div");
        card.classList.add("col-md-2", "mb-4"); // 5 cards por fila
        
        let nombreCorto = producto.nombre.length > 52 ? producto.nombre.substring(0, 52) + "..." : producto.nombre;

        card.innerHTML = `
            <div class="card producto-card" title="${producto.nombre}">
                <div class="producto-img-container">
                    <img src="${producto.foto}" class="producto-img" alt="${producto.nombre}">
                </div>
                <div class="card-body">
                    <h6 class="card-title">${nombreCorto}</h6>
                    <p class="card-text precio">${producto.precio.toLocaleString('es-CL', { style: 'currency', currency: 'CLP' })}</p>
                    <div class="text-center">
                        <button class="btn btn-success agregar-carrito">Agregar al carrito</button>
                    </div>
                </div>
            </div>
        `;
        contenedor.appendChild(card);
    });

    // Activar tooltips de Bootstrap
    document.querySelectorAll('.producto-card').forEach(card => {
        new bootstrap.Tooltip(card);
    });
}

function cargarFiltros(productos) {
    const marcas = [...new Set(productos.map(p => p.marca))];
    const tipos = [...new Set(productos.map(p => p.tipo_producto))];

    document.getElementById("filtro-marca").innerHTML = marcas.map(m => `
        <div class="form-check">
            <input class="form-check-input filtro-marca" type="checkbox" value="${m}">
            <label class="form-check-label">${m}</label>
        </div>
    `).join("");

    document.getElementById("filtro-tipo").innerHTML = tipos.map(t => `
        <div class="form-check">
            <input class="form-check-input filtro-tipo" type="checkbox" value="${t}">
            <label class="form-check-label">${t}</label>
        </div>
    `).join("");
}

function aplicarFiltros() {
    const marcasSeleccionadas = [...document.querySelectorAll(".filtro-marca:checked")].map(e => e.value);
    const tiposSeleccionados = [...document.querySelectorAll(".filtro-tipo:checked")].map(e => e.value);

    const productosFiltrados = productos.filter(p => 
        (marcasSeleccionadas.length === 0 || marcasSeleccionadas.includes(p.marca)) &&
        (tiposSeleccionados.length === 0 || tiposSeleccionados.includes(p.tipo_producto))
    );

    mostrarProductos(productosFiltrados);
}