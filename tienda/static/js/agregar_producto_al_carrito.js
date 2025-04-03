/* # Código encargado de agregar elementos al carrito de compras */
document.addEventListener('DOMContentLoaded', function () {
    agregarEventListeners();
    actualizarBadge(); // Asegura que el badge se actualice al cargar la página
});

function agregarEventListeners() {
    const productosContainer = document.getElementById('productos-container');

    productosContainer.addEventListener('click', event => {
        if (event.target.classList.contains('agregar-carrito')) {
            const button = event.target;
            const id = button.dataset.id;
            const nombre = button.dataset.nombre;
            const precio = parseFloat(button.dataset.precio);
            const foto = button.dataset.foto;

            agregarProductoAlCarrito(id, nombre, precio, foto);
            iniciarAnimacionProducto(button);
        }
    });
}

function agregarProductoAlCarrito(id, nombre, precio, foto) {
    console.log("Producto a agregar:", id, nombre, precio, foto);
    // Verificar que los datos sean correctos
    if (!id || !nombre || !precio || !foto) {
        console.error('Error: Datos del producto incompletos', { id, nombre, precio, foto });
        return;
    }

    // Obtener el carrito desde localStorage
    let carrito = obtenerCarrito();

    // Comprobar si el producto ya está en el carrito
    const productoExistente = carrito.find(item => item.id === id);

    if (productoExistente) {
        // Si ya existe, incrementar la cantidad
        productoExistente.cantidad++;
    } else {
        // Si no existe, agregarlo al carrito
        carrito.push({ id, nombre, precio, foto, cantidad: 1 });
    }

    // Guardar el carrito actualizado en localStorage
    localStorage.setItem('carrito', JSON.stringify(carrito));

    // Actualizar el badge de la cantidad de productos en el carrito
    actualizarBadge();

    // Mostrar un mensaje de éxito
    const toastElement = document.getElementById('toastAdded');
    if (toastElement) {
        const toastInstance = new bootstrap.Toast(toastElement, { delay: 2000 });
        toastInstance.show();
    }
}

function obtenerCarrito() {
    return localStorage.getItem('carrito') ? JSON.parse(localStorage.getItem('carrito')) : [];
}

function actualizarBadge() {
    const carrito = obtenerCarrito();
    const cantidadProductos = carrito.reduce((total, item) => total + item.cantidad, 0);
    const badgeElement = document.getElementById('carrito-badge');

    if (!badgeElement) return;

    if (cantidadProductos === 0) {
        badgeElement.style.display = 'none';
    } else {
        badgeElement.textContent = cantidadProductos > 9 ? '9+' : cantidadProductos;
        badgeElement.style.display = 'block';
    }
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
