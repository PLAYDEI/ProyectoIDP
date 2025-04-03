document.addEventListener("DOMContentLoaded", function () {
    cargarProductos();
    actualizarBadge();
});

let productos = []; 

async function cargarProductos() {
    try {
        const respuesta = await fetch("/api/productos/");
        const lista = await respuesta.json();

        if (Array.isArray(lista)) {
            productos = lista; 
            mostrarProductos(lista);
            cargarFiltros(productos);
        } else {
            console.error("La respuesta de la API no es una lista:", lista);
        }
    } catch (error) {
        console.error("Error al cargar los productos:", error);
    }
}

function mostrarProductos(lista) {
    const contenedor = document.getElementById("productos-container");
    contenedor.innerHTML = "";

    lista.forEach(producto => {
        if (!producto.id || !producto.nombre || !producto.precio || !producto.foto) return;

        const card = document.createElement("div");
        card.classList.add("col-md-2", "mb-4");

        let nombreCorto = producto.nombre.length > 52 ? producto.nombre.substring(0, 52) + "..." : producto.nombre;

        card.innerHTML = `
            <div class="card producto-card" title="${producto.nombre}">
                <div class="producto-img-container">
                    <img src="${producto.foto}" class="producto-img" alt="${producto.nombre}">
                </div>
                <div class="card-body">
                    <h6 class="card-title">${nombreCorto}</h6>
                    <p class="card-text precio">${formatearPrecio(producto.precio)}</p>
                    <div class="text-center">
                    <button class="btn btn-primary agregar-carrito w-100"
                        data-id="${producto.id}"
                        data-nombre="${producto.nombre}"
                        data-precio="${producto.precio}"
                        data-foto="${producto.foto}">
                        Agregar al carrito
                    </button>
                    </div>
                </div>
            </div>
        `;
        contenedor.appendChild(card);
    });

    document.querySelectorAll('.agregar-carrito').forEach(btn => {
        btn.addEventListener('click', agregarProductoAlCarrito);
    });
}

function formatearPrecio(precio) {
    return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' }).format(precio);
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

    document.querySelectorAll(".filtro-marca, .filtro-tipo").forEach(input => {
        input.addEventListener("change", aplicarFiltros);
    });

    // Agregar botón de "Eliminar Filtros"
    const contenedorBoton = document.getElementById("filtro-boton-container");
    contenedorBoton.innerHTML = `
        <button id="reset-filtros" class="btn btn-secondary mt-2 w-100">Eliminar filtros</button>
    `;
    document.getElementById("reset-filtros").addEventListener("click", resetearFiltros);
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

// Nueva función para resetear filtros
function resetearFiltros() {
    document.querySelectorAll(".filtro-marca:checked, .filtro-tipo:checked").forEach(input => {
        input.checked = false;
    });

    mostrarProductos(productos);
}

function agregarProductoAlCarrito(event) {
    const boton = event.target;
    const id = boton.getAttribute("data-id");
    const nombre = boton.getAttribute("data-nombre");
    const precio = parseInt(boton.getAttribute("data-precio"));
    const foto = boton.getAttribute("data-foto");

    if (!id || !nombre || !precio || !foto) return;

    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

    const productoExistente = carrito.find(item => item.id === id);
    if (productoExistente) {
        productoExistente.cantidad++;
    } else {
        carrito.push({ id, nombre, precio, foto, cantidad: 1 });
    }

    localStorage.setItem("carrito", JSON.stringify(carrito));

    actualizarBadge();
    iniciarAnimacionProducto(boton);
}

function actualizarBadge() {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const cantidadProductos = carrito.reduce((total, item) => total + item.cantidad, 0);
    const badgeElement = document.getElementById('carrito-badge');

    if (!badgeElement) return;

    badgeElement.textContent = cantidadProductos > 99 ? '99+' : cantidadProductos;
    badgeElement.style.display = cantidadProductos > 0 ? 'block' : 'none';
}

function iniciarAnimacionProducto(button) {
    const cart = document.getElementById('botonCarrito');
    const img = button.closest('.card').querySelector("img");

    if (img) {
        const imgClone = img.cloneNode(true);
        imgClone.style.position = 'absolute';
        imgClone.style.zIndex = '1000';
        imgClone.style.opacity = '0.5';
        imgClone.style.width = '150px';
        imgClone.style.height = '150px';
        imgClone.style.top = `${img.getBoundingClientRect().top}px`;
        imgClone.style.left = `${img.getBoundingClientRect().left}px`;

        document.body.appendChild(imgClone);

        const cartRect = cart.getBoundingClientRect();
        imgClone.animate([
            { top: `${img.getBoundingClientRect().top}px`, left: `${img.getBoundingClientRect().left}px`, opacity: 0.5 },
            { top: `${cartRect.top}px`, left: `${cartRect.left}px`, width: '50px', height: '50px', opacity: 0 }
        ], {
            duration: 1000,
            easing: 'ease-in-out'
        }).onfinish = () => imgClone.remove();
    }
}
