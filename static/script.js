// Global variables
let currentEditingId = null;
let currentPage = null;

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    currentPage = window.currentPage;
    
    if (currentPage) {
        initializePage();
    }
});


function initializePage() {
    // Set up event listeners
    setupEventListeners();
    
    // Load data for the current page
    loadData();
    
    // Load dropdown data for transactions page
    if (currentPage === 'transactions') {
        loadDropdownData();
    }
}

// Set up all event listeners
function setupEventListeners() {
    // Add button click
    const addBtn = document.querySelector('.add-btn');
    if (addBtn) {
        addBtn.addEventListener('click', openAddModal);
    }
    
    // Modal close events
    const modal = document.querySelector('.modal');
    const closeBtn = document.querySelector('.close');
    const cancelBtn = document.querySelector('.cancel-btn');
    
    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', closeModal);
    }
    
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });
    }
    
    // Form submission
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
}

// Load data based on current page
async function loadData() {
    const tableBody = document.querySelector('tbody');
    if (!tableBody) return;
    
    tableBody.innerHTML = '<tr><td colspan="100%" class="loading">Loading data...</td></tr>';
    
    try {
        console.log(`Loading data from: /api/${currentPage}`);
        const response = await fetch(`/api/${currentPage}`);
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Data received:', data);
        
        if (data.length === 0) {
            showEmptyState(tableBody);
        } else {
            populateTable(data, tableBody);
        }
    } catch (error) {
        console.error('Error loading data:', error);
        showError(tableBody, `Failed to load data: ${error.message}`);
    }
}

// Load dropdown data for transactions
async function loadDropdownData() {
    try {
        const [farmersRes, cropsRes, marketsRes] = await Promise.all([
            fetch('/api/farmers-list'),
            fetch('/api/crops-list'),
            fetch('/api/markets-list')
        ]);
        
        const farmers = await farmersRes.json();
        const crops = await cropsRes.json();
        const markets = await marketsRes.json();
        
        populateDropdown('farmer-select', farmers, 'farmer_id', 'farmer_name');
        populateDropdown('crop-select', crops, 'crop_id', 'crop_name');
        populateDropdown('market-select', markets, 'market_id', 'market_name');
    } catch (error) {
        console.error('Error loading dropdown data:', error);
    }
}

// Populate dropdown with data
function populateDropdown(selectId, data, valueField, textField) {
    const select = document.getElementById(selectId);
    if (!select) return;
    
    // Clear existing options except the first one
    select.innerHTML = '<option value="">Select a ' + selectId.replace('-select', '') + '</option>';
    
    data.forEach(item => {
        const option = document.createElement('option');
        option.value = item[valueField];
        option.textContent = item[textField];
        select.appendChild(option);
    });
}

// Populate table with data
function populateTable(data, tableBody) {
    tableBody.innerHTML = '';
    
    data.forEach(item => {
        const row = createTableRow(item);
        tableBody.appendChild(row);
    });
}

// Create table row based on current page
function createTableRow(item) {
    const row = document.createElement('tr');
    
    switch (currentPage) {
        case 'farmers':
            row.innerHTML = `
                <td>${item.farmer_id}</td>
                <td>${item.farmer_name || ''}</td>
                <td>${item.village || ''}</td>
                <td>${item.phone || ''}</td>
                <td class="action-buttons">
                    <button class="edit-btn" data-id="${item.farmer_id}">Edit</button>
                    <button class="delete-btn" data-id="${item.farmer_id}">Delete</button>
                </td>
            `;
            break;
            
        case 'crops':
            row.innerHTML = `
                <td>${item.crop_id}</td>
                <td>${item.crop_name || ''}</td>
                <td>${item.season || ''}</td>
                <td class="action-buttons">
                    <button class="edit-btn" data-id="${item.crop_id}">Edit</button>
                    <button class="delete-btn" data-id="${item.crop_id}">Delete</button>
                </td>
            `;
            break;
            
        case 'markets':
            row.innerHTML = `
                <td>${item.market_id}</td>
                <td>${item.market_name || ''}</td>
                <td>${item.location || ''}</td>
                <td class="action-buttons">
                    <button class="edit-btn" data-id="${item.market_id}">Edit</button>
                    <button class="delete-btn" data-id="${item.market_id}">Delete</button>
                </td>
            `;
            break;
            
        case 'transactions':
            const total = (item.quantity * item.price).toFixed(2);
            row.innerHTML = `
                <td>${item.transaction_id}</td>
                <td>${item.farmer_name || ''}</td>
                <td>${item.crop_name || ''}</td>
                <td>${item.market_name || ''}</td>
                <td>${item.quantity || ''}</td>
                <td>$${item.price || ''}</td>
                <td id="total-amount">$${total}</td>
                <td class="action-buttons">
                    <button class="edit-btn" data-id="${item.transaction_id}">Edit</button>
                    <button class="delete-btn" data-id="${item.transaction_id}">Delete</button>
                </td>
            `;
            break;
    }
    
    // Add event listeners to action buttons
    const editBtn = row.querySelector('.edit-btn');
    const deleteBtn = row.querySelector('.delete-btn');
    
    if (editBtn) {
        editBtn.addEventListener('click', () => editItem(item));
    }
    
    if (deleteBtn) {
        deleteBtn.addEventListener('click', () => deleteItem(item));
    }
    
    return row;
}

// Show empty state
function showEmptyState(tableBody) {
    tableBody.innerHTML = `
        <tr>
            <td colspan="100%" class="empty-state">
                <h3>No data available</h3>
                <p>Click "Add New" to create your first record.</p>
            </td>
        </tr>
    `;
}

// Show error message
function showError(tableBody, message) {
    tableBody.innerHTML = `
        <tr>
            <td colspan="100%" class="message error">
                ${message}
            </td>
        </tr>
    `;
}

// Open add modal
function openAddModal() {
    currentEditingId = null;
    const modal = document.querySelector('.modal');
    const modalTitle = document.querySelector('#modal-title');
    const form = document.querySelector('form');
    
    if (modalTitle) {
        modalTitle.textContent = `Add New ${currentPage.charAt(0).toUpperCase() + currentPage.slice(1, -1)}`;
    }
    
    if (form) {
        form.reset();
    }
    
    if (modal) {
        modal.style.display = 'block';
    }
}

// Edit item
function editItem(item) {
    currentEditingId = getItemId(item);
    const modal = document.querySelector('.modal');
    const modalTitle = document.querySelector('#modal-title');
    const form = document.querySelector('form');
    
    if (modalTitle) {
        modalTitle.textContent = `Edit ${currentPage.charAt(0).toUpperCase() + currentPage.slice(1, -1)}`;
    }
    
    if (form) {
        populateForm(form, item);
    }
    
    if (modal) {
        modal.style.display = 'block';
    }
}

// Get item ID based on current page
function getItemId(item) {
    switch (currentPage) {
        case 'farmers': return item.farmer_id;
        case 'crops': return item.crop_id;
        case 'markets': return item.market_id;
        case 'transactions': return item.transaction_id;
        default: return null;
    }
}

// Populate form with item data
function populateForm(form, item) {
    const inputs = form.querySelectorAll('input, select');
    
    inputs.forEach(input => {
        const fieldName = input.name;
        if (item.hasOwnProperty(fieldName)) {
            input.value = item[fieldName] || '';
        }
    });
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    console.log('Form data:', data);
    
    // Convert numeric fields
    if (currentPage === 'transactions') {
        data.quantity = parseFloat(data.quantity);
        data.price = parseFloat(data.price);
        data.farmer_id = parseInt(data.farmer_id);
        data.crop_id = parseInt(data.crop_id);
        data.market_id = parseInt(data.market_id);
    }
    
    try {
        let response;
        const url = currentEditingId ? `/api/${currentPage}/${currentEditingId}` : `/api/${currentPage}`;
        const method = currentEditingId ? 'PUT' : 'POST';
        
        console.log(`Submitting ${method} request to: ${url}`);
        console.log('Data being sent:', data);
        
        response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        console.log('Response status:', response.status);
        
        if (response.ok) {
            const result = await response.json();
            console.log('Success response:', result);
            closeModal();
            loadData();
            showMessage('Operation completed successfully!', 'success');
        } else {
            const errorData = await response.json();
            console.error('Error response:', errorData);
            showMessage(`Error: ${errorData.message || 'Operation failed'}`, 'error');
        }
    } catch (error) {
        console.error('Error submitting form:', error);
        showMessage(`Error: Failed to submit form - ${error.message}`, 'error');
    }
}

// Delete item
async function deleteItem(item) {
    const itemId = getItemId(item);
    const itemName = getItemName(item);
    
    if (confirm(`Are you sure you want to delete this ${currentPage.slice(0, -1)}: ${itemName}?`)) {
        try {
            const response = await fetch(`/api/${currentPage}/${itemId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                loadData();
                showMessage('Item deleted successfully!', 'success');
            } else {
                const errorData = await response.json();
                showMessage(`Error: ${errorData.message || 'Delete failed'}`, 'error');
            }
        } catch (error) {
            console.error('Error deleting item:', error);
            showMessage('Error: Failed to delete item', 'error');
        }
    }
}

// Get item name for confirmation dialog
function getItemName(item) {
    switch (currentPage) {
        case 'farmers': return item.farmer_name;
        case 'crops': return item.crop_name;
        case 'markets': return item.market_name;
        case 'transactions': return `Transaction #${item.transaction_id}`;
        default: return 'item';
    }
}

// Close modal
function closeModal() {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.style.display = 'none';
    }
    currentEditingId = null;
}

// Show message to user
function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    // Insert message at the top of the main content
    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(messageDiv, main.firstChild);
        
        // Auto-remove message after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.remove();
            }
        }, 5000);
    }
}

// Utility function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Utility function to format numbers
function formatNumber(number, decimals = 2) {
    return parseFloat(number).toFixed(decimals);
}

// Export functions for global access if needed
window.agriculturalApp = {
    loadData,
    openAddModal,
    editItem,
    deleteItem,
    closeModal
};
