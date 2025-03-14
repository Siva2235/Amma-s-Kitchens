// Load cart items from localStorage
function loadCartItems() {
    const cartItems = JSON.parse(localStorage.getItem('cart')) || [];
    const cartContainer = document.getElementById('cartItems');

    if (cartItems.length === 0) {
        cartContainer.innerHTML = `
            <div class="empty-cart">
                <i class="fas fa-shopping-cart"></i>
                <h3>Your cart is empty</h3>
                <p>Please add items to your cart to proceed with checkout</p>
            </div>`;
        document.querySelector('button[type="submit"]').disabled = true;
        return;
    }

    cartContainer.innerHTML = cartItems.map(item => `
        <div class="cart-item">
            <img src="${item.image}" alt="${item.name}">
            <div class="cart-item-info">
                <h4>${item.name}</h4>
                <div class="cart-item-price">₹${item.price} x ${item.quantity}</div>
                <div class="item-total">Total: ₹${(item.price * item.quantity).toFixed(2)}</div>
            </div>
        </div>
    `).join('');

    calculateTotals(cartItems);
    document.querySelector('button[type="submit"]').disabled = false;
}

// Calculate order totals
function calculateTotals(cartItems) {
    const subtotal = cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
    const deliveryFee = 20;
    const tax = subtotal * 0.05;
    const total = subtotal + deliveryFee + tax;

    document.getElementById('subtotal').textContent = `₹${subtotal.toFixed(2)}`;
    document.getElementById('deliveryFee').textContent = `₹${deliveryFee.toFixed(2)}`;
    document.getElementById('tax').textContent = `₹${tax.toFixed(2)}`;
    document.getElementById('total').textContent = `₹${total.toFixed(2)}`;
}

// Handle payment method selection
function setupPaymentMethods() {
    const paymentMethods = document.querySelectorAll('.payment-method');
    const cardDetails = document.getElementById('cardDetails');
    const upiDetails = document.getElementById('upiDetails');

    paymentMethods.forEach(method => {
        method.addEventListener('click', function() {
            paymentMethods.forEach(m => m.classList.remove('active'));
            this.classList.add('active');

            const selectedMethod = this.dataset.method;
            cardDetails.style.display = selectedMethod === 'card' ? 'block' : 'none';
            upiDetails.style.display = selectedMethod === 'upi' ? 'block' : 'none';
        });
    });
}

// Format phone number input
function formatPhoneNumber() {
    const phoneInput = document.getElementById('phone');
    if (!phoneInput) return;

    phoneInput.addEventListener('input', function(e) {
        e.target.value = e.target.value.replace(/\D/g, '').substring(0, 10);
    });
}

// Get CSRF Token for Django request
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1];
}

// Show alert message
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i> <span>${message}</span>`;

    const form = document.querySelector('.payment-form');
    const existingAlert = form.querySelector('.alert');
    if (existingAlert) existingAlert.remove();

    form.insertBefore(alertDiv, form.firstChild);
    setTimeout(() => alertDiv.remove(), 5000);
}

// Validate form data
function validateForm(data) {
    if (!data.address.trim()) {
        showAlert('Please enter delivery address', 'danger');
        return false;
    }
    if (!data.phone.trim() || data.phone.length !== 10) {
        showAlert('Please enter a valid 10-digit phone number', 'danger');
        return false;
    }
    return true;
}

// Send order data to Django backend
async function submitOrder(data) {
    try {
        let response = await fetch('/payment/', {  // Change `/checkout/` to `/payment/`
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify(data)
        });

        let result = await response.json();
        if (response.ok) {
            localStorage.removeItem('cart');  // Clear cart
            showAlert('Order placed successfully!', 'success');
            setTimeout(() => {
                window.location.href = '/order-success/'; // Redirect to success page
            }, 2000);
        } else {
            showAlert(result.error || 'Error placing order', 'danger');
        }
    } catch (error) {
        showAlert('Something went wrong', 'danger');
    }
}

// Handle form submission
function setupFormSubmission() {
    const form = document.getElementById('paymentForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const selectedMethod = document.querySelector('.payment-method.active');
        if (!selectedMethod) {
            showAlert('Please select a payment method', 'danger');
            return;
        }

        const cartItems = JSON.parse(localStorage.getItem('cart')) || [];
        const totalAmount = document.getElementById('total').textContent.replace('₹', '');

        const formData = {
            address: document.getElementById('address').value,
            phone: document.getElementById('phone').value,
            instructions: document.getElementById('instructions').value,
            paymentMethod: selectedMethod.dataset.method,
            total: totalAmount,
            cartItems: cartItems
        };

        if (!validateForm(formData)) return;

        submitOrder(formData);
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    loadCartItems();
    setupPaymentMethods();
    formatPhoneNumber();
    setupFormSubmission();
});
