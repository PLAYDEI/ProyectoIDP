document.addEventListener("DOMContentLoaded", function () {
    cargarProductos();
});

let productos = []; // Almacena los productos para filtrar

// Cargar productos desde la API
async function cargarProductos() {
    try {
        const respuesta = await fetch("/api/productos/");
        const lista = await respuesta.json();
        console.log("Productos cargados:", lista);  // Verifica que aquí sí hay datos
        mostrarProductos(lista);  // Aquí debe pasar la lista correctamente
    } catch (error) {
        console.error("Error al cargar los productos:", error);
    }
}

// Mostrar productos en el contenedor
function mostrarProductos(lista) {
    const contenedor = document.getElementById("productos-container");
    contenedor.innerHTML = "";

    lista.forEach(producto => {
        // Validar datos del producto antes de mostrarlo
        if (!producto.id || !producto.nombre || !producto.precio || !producto.foto) {
            console.warn("Producto incompleto:", producto);
            return;  // Omite productos incompletos
        }

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
                    <p class="card-text precio">${producto.precio.toLocaleString('es-CL', { style: 'currency', currency: 'CLP' })}</p>
                    <div class="text-center">
                    <button class="btn btn-primary agregar-carrito w-100"
                        data-id="${producto.id}"
                        data-nombre="${producto.nombre}"
                        data-precio="${producto.precio}"
                        data-foto="${producto.foto}">
                        agregar al carrito
                    </button>
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

    // Asociar el evento de agregar al carrito
    document.querySelectorAll('.agregar-carrito').forEach(btn => {
        btn.addEventListener('click', agregarProductoAlCarrito);
    });
}

// Cargar filtros para los productos (marca y tipo)
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

// Aplicar filtros a los productos
function aplicarFiltros() {
    const marcasSeleccionadas = [...document.querySelectorAll(".filtro-marca:checked")].map(e => e.value);
    const tiposSeleccionados = [...document.querySelectorAll(".filtro-tipo:checked")].map(e => e.value);

    const productosFiltrados = productos.filter(p => 
        (marcasSeleccionadas.length === 0 || marcasSeleccionadas.includes(p.marca)) &&
        (tiposSeleccionados.length === 0 || tiposSeleccionados.includes(p.tipo_producto))
    );

    mostrarProductos(productosFiltrados);
}

// Agregar un producto al carrito
function agregarProductoAlCarrito(event) {
    console.log("Botón presionado");
    const boton = event.target;
    const id = boton.getAttribute("data-id");
    const nombre = boton.getAttribute("data-nombre");
    const precio = parseInt(boton.getAttribute("data-precio"));
    const foto = boton.getAttribute("data-foto");

    if (!id || !nombre || !precio || !foto) {
        console.error("Datos del producto incompletos");
        return;  // No agregar el producto si los datos son incompletos
    }

    // Obtener el carrito actual del localStorage (si existe)
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

    // Verificar si el producto ya está en el carrito
    const productoExistente = carrito.find(item => item.id === id);
    if (productoExistente) {
        productoExistente.cantidad++;  // Aumentar cantidad si ya está en el carrito
    } else {
        carrito.push({ id, nombre, precio, foto, cantidad: 1 });
    }

    // Guardar el carrito actualizado en localStorage
    localStorage.setItem("carrito", JSON.stringify(carrito));

    // Mostrar mensaje de éxito
    alert(`${nombre} agregado al carrito`);
}
