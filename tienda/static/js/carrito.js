/* # Código encargado de gestionar la vista del carrito de compras */
document.addEventListener('DOMContentLoaded', () => {
    const carritoContainer = document.getElementById('carrito-container');
    const totalAmount = document.getElementById('total-amount');
    const emptyMessage = document.getElementById('empty-message');
    
    mostrarCarrito();
    
    function mostrarCarrito() {
        const carrito = obtenerCarrito();
        carritoContainer.innerHTML = '';
        const total = calcularTotal(carrito);
        totalAmount.textContent = formatearPrecio(total);

        if (carrito.length === 0) {
            emptyMessage.innerHTML = `
                <img src="/static/images/carrito_vacio.png" alt="Carrito vacío" style="max-width: 60px;">
                <h4></h4>
                <h4 style="color: #7a7a7a;">¡Tu carrito está vacío!</h4>
                <a href="/">volver al inicio</a>
            `;
        } else {
            emptyMessage.innerHTML = '';
            carrito.forEach(item => {
                const card = crearCardCarrito(item);
                carritoContainer.appendChild(card);
            });
        }
    }

    function crearCardCarrito(item) {
        const card = document.createElement('div');
        card.classList.add('card', 'mb-3', 'p-2');
        
        card.innerHTML = `
            <div class="d-flex align-items-center">
                <img src="${item.foto}" class="me-3" style="width: 80px;">
                <div class="flex-grow-1">
                    <h5>${item.nombre}</h5>
                    <p>${formatearPrecio(item.precio)}</p>
                </div>
                <div class="d-flex align-items-center">
                    <button class="btn btn-outline-primary btn-sm btn-decrementar" data-id="${item.id}">-</button>
                    <span class="mx-2">${item.cantidad}</span>
                    <button class="btn btn-outline-primary btn-sm btn-incrementar" data-id="${item.id}">+</button>
                    <button class="btn btn-outline-danger btn-sm btn-eliminar ms-3" data-id="${item.id}">🗑</button>
                </div>
            </div>
        `;
        return card;
    }

    function formatearPrecio(precio) {
        const formatter = new Intl.NumberFormat('es-CL', {
            style: 'currency',
            currency: 'CLP'
        });
        return formatter.format(precio);
    }
    
    
    carritoContainer.addEventListener('click', event => {
        const id = event.target.dataset.id;
        if (event.target.classList.contains('btn-incrementar')) incrementarCantidad(id);
        if (event.target.classList.contains('btn-decrementar')) decrementarCantidad(id);
        if (event.target.classList.contains('btn-eliminar')) eliminarProducto(id);
    });
    
    function obtenerCarrito() {
        return localStorage.getItem('carrito') ? JSON.parse(localStorage.getItem('carrito')) : [];
    }
    
    function calcularTotal(carrito) {
        return carrito.reduce((total, item) => total + item.precio * item.cantidad, 0);
    }
    
    function formatearPrecio(precio) {
        return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' }).format(precio);
    }
    
    function incrementarCantidad(id) {
        let carrito = obtenerCarrito();
        const producto = carrito.find(item => item.id === id);
        producto.cantidad++;
        localStorage.setItem('carrito', JSON.stringify(carrito));
        mostrarCarrito();
    }
    
    function decrementarCantidad(id) {
        let carrito = obtenerCarrito();
        const producto = carrito.find(item => item.id === id);
        if (producto.cantidad > 1) {
            producto.cantidad--;
            localStorage.setItem('carrito', JSON.stringify(carrito));
            mostrarCarrito();
        }
    }
    
    function eliminarProducto(id) {
        let carrito = obtenerCarrito();
        const index = carrito.findIndex(item => item.id === id);
        if (index !== -1) {
            carrito.splice(index, 1);
            localStorage.setItem('carrito', JSON.stringify(carrito));
            mostrarCarrito();
        }
    }
});