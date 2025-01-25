function sortItems(order) {
    const resultsContainer = document.getElementById('item-container');
    const items = Array.from(resultsContainer.children); // Récupérer tous les éléments enfants

    // Trier les éléments en fonction de leur texte (nom des plats)
    items.sort((a, b) => {
        const nameA = a.querySelector('h3').textContent.trim().toLowerCase();
        const nameB = b.querySelector('h3').textContent.trim().toLowerCase();

        if (order === 'asc') {
            return nameA.localeCompare(nameB); // Tri croissant
        } else if (order === 'desc') {
            return nameB.localeCompare(nameA); // Tri décroissant
        }
    });

    // Réinitialiser le conteneur et ajouter les éléments triés
    resultsContainer.innerHTML = '';
    items.forEach(item => resultsContainer.appendChild(item));
}