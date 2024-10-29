// Récupération de l'élément header
const header = document.querySelector('header');

// Fonction pour changer l'opacité et la taille du header
function handleScroll() {
    const scrollPosition = window.scrollY;

    if (scrollPosition > 50) { // Si défilé de plus de 50px
        header.style.backgroundColor = '#394228'; // Opaque, vert prairie clair
        header.style.padding = '10px 0'; // Réduit la taille
    } else {
        header.style.backgroundColor = 'rgba(200, 255, 200, 0)'; // Transparent
        header.style.padding = '20px 0'; // Taille initiale
    }
}

// Écouteur d'événement pour le défilement
window.addEventListener('scroll', handleScroll);
