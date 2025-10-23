// AJAX CRUD Operations
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing AJAX...');
    initializeAJAX();
});

function initializeAJAX() {
    setupCSRFToken();
    loadProducts();
    setupEventListeners();
}

function setupCSRFToken() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

function setupEventListeners() {
    // Refresh button
    $('#refresh-btn').on('click', function() {
        loadProducts();
    });
    
    // Create product form
    $(document).on('submit', '#createProductForm', function(e) {
        e.preventDefault();
        createProduct();
    });
    
    // Edit product form
    $(document).on('submit', '#editProductForm', function(e) {
        e.preventDefault();
        const productId = $('#editProductId').val();
        updateProduct(productId);
    });
    
    // Delete confirmation
    $(document).on('click', '#confirmDeleteBtn', function() {
        const productId = $(this).data('product-id');
        deleteProduct(productId);
    });
}

function showLoadingState() {
    $('#products-container').html(`
        <div class="col-12 text-center py-5">
            <div class="spinner-border text-primary mb-3" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-muted">Loading products...</p>
        </div>
    `);
}

function showEmptyState() {
    $('#products-container').html(`
        <div class="col-12">
            <div class="text-center py-5">
                <i class="fas fa-box-open fa-3x text-muted mb-3"></i>
                <h3 class="text-muted">No Products Yet</h3>
                <p class="text-muted mb-4">Start by adding your first product to the store!</p>
                <button class="btn btn-primary btn-lg" data-bs-toggle="modal" data-bs-target="#createProductModal">
                    <i class="fas fa-plus me-2"></i>Add First Product
                </button>
            </div>
        </div>
    `);
}

function showErrorState(message = 'Failed to load products') {
    $('#products-container').html(`
        <div class="col-12">
            <div class="text-center py-5">
                <i class="fas fa-exclamation-triangle fa-3x text-danger mb-3"></i>
                <h3 class="text-danger">Something Went Wrong</h3>
                <p class="text-muted mb-3">${message}</p>
                <button class="btn btn-primary" onclick="loadProducts()">
                    <i class="fas fa-redo me-2"></i>Try Again
                </button>
            </div>
        </div>
    `);
}

function loadProducts() {
    showLoadingState();
    
    $.ajax({
        url: '/ajax/products/',
        type: 'GET',
        success: function(response) {
            if (response.success) {
                if (response.products && response.products.length > 0) {
                    renderProducts(response.products);
                    showToast('Products loaded successfully!', 'success');
                } else {
                    showEmptyState();
                }
            } else {
                showErrorState(response.error || 'Failed to load products');
            }
        },
        error: function(xhr, status, error) {
            showErrorState('Network error: ' + error);
        }
    });
}

function renderProducts(products) {
    let html = '<div class="row">';
    
    products.forEach(product => {
        const stockClass = product.stock > 10 ? 'bg-success' : 
                          product.stock > 0 ? 'bg-warning' : 'bg-danger';
        
        html += `
        <div class="col-xl-3 col-lg-4 col-md-6 mb-4">
            <div class="card product-card h-100 shadow-sm">
                <img src="${product.thumbnail}" class="card-img-top" alt="${product.name}" 
                     style="height: 200px; object-fit: cover;"
                     onerror="this.src='https://via.placeholder.com/300x200?text=No+Image'">
                
                ${product.is_featured ? `
                <div class="position-absolute top-0 start-0 m-2">
                    <span class="badge bg-warning">
                        <i class="fas fa-star me-1"></i>Featured
                    </span>
                </div>
                ` : ''}
                
                <div class="position-absolute top-0 end-0 m-2">
                    <span class="badge ${stockClass}">
                        Stock: ${product.stock}
                    </span>
                </div>

                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text text-muted small flex-grow-1">
                        ${product.description.length > 100 ? 
                          product.description.substring(0, 100) + '...' : 
                          product.description}
                    </p>
                    
                    <div class="mb-2">
                        <h4 class="text-primary mb-1">$${product.price}</h4>
                        <p class="card-text small mb-1">
                            <i class="fas fa-tag me-1 text-muted"></i>${product.brand}
                        </p>
                        <p class="card-text small">
                            <i class="fas fa-folder me-1 text-muted"></i>${product.category}
                        </p>
                    </div>

                    <div class="mt-auto">
                        <div class="d-grid gap-2">
                            <a href="/detail/${product.id}/" class="btn btn-outline-primary btn-sm">
                                <i class="fas fa-eye me-1"></i>Detail
                            </a>
                            <div class="btn-group w-100">
                                <button class="btn btn-warning btn-sm" onclick="openEditModal(${product.id})">
                                    <i class="fas fa-edit"></i> Edit
                                </button>
                                <button class="btn btn-danger btn-sm" onclick="confirmDelete(${product.id}, '${product.name.replace(/'/g, "\\'")}')">
                                    <i class="fas fa-trash"></i> Delete
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `;
    });
    
    html += '</div>';
    $('#products-container').html(html);
}

function createProduct() {
    const formData = new FormData(document.getElementById('createProductForm'));
    
    $.ajax({
        url: '/ajax/create-product/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.success) {
                showToast('Product created successfully!', 'success');
                loadProducts();
                $('#createProductModal').modal('hide');
                document.getElementById('createProductForm').reset();
            } else {
                showToast(response.error || 'Failed to create product', 'error');
            }
        },
        error: function(xhr, status, error) {
            showToast('Network error: ' + error, 'error');
        }
    });
}

function openEditModal(productId) {
    $.ajax({
        url: `/ajax/get-product/${productId}/`,
        type: 'GET',
        success: function(response) {
            if (response.success) {
                const product = response.product;
                // Populate form fields
                $('#editProductId').val(product.id);
                $('#editProductName').val(product.name);
                $('#editProductDescription').val(product.description);
                $('#editProductPrice').val(product.price);
                $('#editProductCategory').val(product.category);
                $('#editProductStock').val(product.stock);
                $('#editProductBrand').val(product.brand);
                $('#editProductThumbnail').val(product.thumbnail);
                $('#editProductFeatured').prop('checked', product.is_featured);
                
                $('#editProductModal').modal('show');
            } else {
                showToast('Failed to load product data', 'error');
            }
        },
        error: function(xhr, status, error) {
            showToast('Network error: ' + error, 'error');
        }
    });
}

function updateProduct(productId) {
    const formData = new FormData(document.getElementById('editProductForm'));
    
    $.ajax({
        url: `/ajax/update-product/${productId}/`,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.success) {
                showToast('Product updated successfully!', 'success');
                loadProducts();
                $('#editProductModal').modal('hide');
            } else {
                showToast(response.error || 'Failed to update product', 'error');
            }
        },
        error: function(xhr, status, error) {
            showToast('Network error: ' + error, 'error');
        }
    });
}

function confirmDelete(productId, productName) {
    $('#deleteProductName').text(productName);
    $('#confirmDeleteBtn').data('product-id', productId);
    $('#deleteConfirmModal').modal('show');
}

function deleteProduct(productId) {
    $.ajax({
        url: `/ajax/delete-product/${productId}/`,
        type: 'POST',
        success: function(response) {
            if (response.success) {
                showToast('Product deleted successfully!', 'success');
                loadProducts();
                $('#deleteConfirmModal').modal('hide');
            } else {
                showToast(response.error || 'Failed to delete product', 'error');
            }
        },
        error: function(xhr, status, error) {
            showToast('Network error: ' + error, 'error');
        }
    });
}

function showToast(message, type = 'success') {
    const toastHtml = `
        <div class="toast align-items-center text-bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    $('.toast-container').append(toastHtml);
    const toastElement = $('.toast-container .toast').last()[0];
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    $(toastElement).on('hidden.bs.toast', function() {
        $(this).remove();
    });
}