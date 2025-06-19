// Fonction pour formater les montants en FCFA
function formatAmount(amount) {
    return new Intl.NumberFormat('fr-FR').format(amount) + ' FCFA';
}

// Fonction pour calculer le prix total
function calculateTotal() {
    const quantity = parseFloat(document.getElementById('id_quantity').value) || 0;
    const unitPrice = parseFloat(document.getElementById('id_unit_price').value) || 0;
    const total = quantity * unitPrice;
    
    // Mettre à jour le champ total_price si présent
    const totalField = document.getElementById('id_total_price');
    if (totalField) {
        totalField.value = total;
    }
}

// Ajouter les écouteurs d'événements pour le calcul automatique
document.addEventListener('DOMContentLoaded', function() {
    const quantityField = document.getElementById('id_quantity');
    const unitPriceField = document.getElementById('id_unit_price');
    
    if (quantityField && unitPriceField) {
        quantityField.addEventListener('input', calculateTotal);
        unitPriceField.addEventListener('input', calculateTotal);
    }
    
    // Formater les montants dans les tableaux
    document.querySelectorAll('.amount').forEach(function(element) {
        const amount = parseFloat(element.textContent);
        if (!isNaN(amount)) {
            element.textContent = formatAmount(amount);
        }
    });
}); 