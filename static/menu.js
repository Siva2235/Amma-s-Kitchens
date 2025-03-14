// Mobile menu toggle
function toggleMenu() {
    const navMenu = document.getElementById('navMenu');
    navMenu.classList.toggle('active');
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(event) {
    const navMenu = document.getElementById('navMenu');
    const menuToggle = document.querySelector('.menu-toggle');

    if (!navMenu.contains(event.target) && !menuToggle.contains(event.target)) {
        navMenu.classList.remove('active');
    }
});

// Cart functionality
let cartItems = [];
let cartCount = 0;

// Load cart from Django when page loads
function loadCart() {
    fetch("/load-cart/")
        .then(response => response.json())
        .then(data => {
            cartItems = data.cart; // Store the fetched cart items
            cartCount = cartItems.reduce((total, item) => total + item.quantity, 0);
            document.getElementById("cartCount").innerText = cartCount;
            updateCart();
        });
}

// Save cart to Django
function saveCartToBackend(name, price, quantity,image) {
    fetch("/update-cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ name: name, price: price, quantity: quantity,image: image })
    });
}

// Add item to cart
function addToCart(name, price, image) {
    const existingItem = cartItems.find(item => item.name === name);

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cartItems.push({ name, price, image, quantity: 1 });
    }

    cartCount++;
    document.getElementById("cartCount").innerText = cartCount;
    updateCart();
    saveCartToBackend(name, price, 1,image); // Save to Django
    showItemAddedPopup();
}

// Update cart UI
function updateCart() {
    let cartBody = document.getElementById("cartBody");
    let cartFooter = document.querySelector(".cart-footer");
    cartBody.innerHTML = "";

    if (cartItems.length === 0) {
        cartBody.innerHTML = `
            <div class="empty-cart">
                <i class="fas fa-shopping-cart"></i>
                <h3 class="text-warning">Empty Cart !!</h3>
                <p>Fill cart to enjoy your food <span>😋</span></p>
            </div>`;
        cartFooter.style.display = 'none';
    } else {
        cartFooter.style.display = 'block';
        cartItems.forEach((item, index) => {
            cartBody.innerHTML += `
                <div class="cart-item">
                    <img src="${item.image}" alt="${item.name}">
                    <div class="cart-item-info">
                        <h4>${item.name}</h4>
                        <div class="price">Rs ${item.price}/-</div>
                        <div class="item-total">Total: Rs ${item.price * item.quantity}/-</div>
                    </div>
                    <div class="cart-item-controls">
                        <div class="quantity-controls">
                            <button class="quantity-btn" onclick="updateQuantity('${item.name}', -1)">-</button>
                            <span class="quantity">${item.quantity}</span>
                            <button class="quantity-btn" onclick="updateQuantity('${item.name}', 1)">+</button>
                        </div>
                        <button class="delete-btn" onclick="removeItem('${item.name}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>`;
        });
    }
    
    // Store updated cart in localStorage
    localStorage.setItem('cart', JSON.stringify(cartItems));

    document.getElementById("cartCount").innerText = cartItems.reduce((total, item) => total + item.quantity, 0);
    calculateCartTotals();
}

// Update quantity of an item
function updateQuantity(name, change) {
    const item = cartItems.find(cartItem => cartItem.name === name);
    if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
            removeItem(name);
        } else {
            saveCartToBackend(name, item.price, item.quantity, item.image); // Update in Django
        }
    }
    updateCart();
}

// Remove item from cart
function removeItem(name) {
    cartItems = cartItems.filter(item => item.name !== name);
    fetch("/remove-from-cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ name: name })
    })
    .then(() => {
        updateCart();
    });
}

// Get CSRF token for Django requests
function getCSRFToken() {
    return document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
}

// Calculate cart totals
function calculateCartTotals() {
    const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const taxes = subtotal * 0.05;
    const deliveryFee = 20;
    const total = subtotal + taxes + deliveryFee;

    document.getElementById('subtotal').textContent = `Rs ${subtotal}/-`;
    document.getElementById('taxes').textContent = `Rs ${taxes}/-`;
    document.getElementById('total').textContent = `Rs ${total}/-`;
}

// Show "Item Added" popup
function showItemAddedPopup() {
    const popup = document.getElementById('itemAddedPopup');
    popup.style.display = 'block';
    setTimeout(() => {
        popup.style.display = 'none';
    }, 2000);
}

// Open and close cart popup
function openCartPopup() {
    document.getElementById("cartPopup").classList.add('active');
    document.querySelector('.cart-overlay').classList.add('active');
}

function closeCartPopup() {
    document.getElementById("cartPopup").classList.remove('active');
    document.querySelector('.cart-overlay').classList.remove('active');
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
        cartItems = JSON.parse(savedCart);
        updateCart();
    } else {
        loadCart(); // Load from backend if localStorage is empty
    }
});
function filterMenu(category) {
    const categories = document.querySelectorAll('.category');
    categories.forEach(cat => {
        cat.classList.remove('active');
        if (cat.querySelector('span').textContent.trim() === category) {
            cat.classList.add('active');
        }
    });

    const menuCards = document.querySelectorAll('.menu-card');
    menuCards.forEach(card => {
        const cardCategory = card.getAttribute('data-category')?.trim();
        console.log(`Filtering for: ${category}, Item Category: ${cardCategory}`);

        if (category === 'All' || cardCategory === category) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

