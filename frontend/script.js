// Fonction pour récupérer et afficher les notes (GET)
const fetchAndDisplayNotes = () => {
    fetch('http://127.0.0.1:5000/api/notes')
        .then(response => response.json())
        .then(notes => {
            const tbody = document.querySelector('#notes-table tbody');
            // Vide le tableau avant de le remplir
            tbody.innerHTML = '';
            
            notes.forEach(note => {
                const row = tbody.insertRow();
                row.insertCell().textContent = note.nom;
                row.insertCell().textContent = note.matiere;
                row.insertCell().textContent = note.note;
            });
        })
        .catch(error => {
            console.error('Erreur lors de la récupération des notes:', error);
            document.getElementById('message').textContent = 'Erreur: Impossible de charger les notes.';
        });
};

// Fonction pour ajouter une note (POST)
const handleAddNote = (event) => {
    event.preventDefault(); // Empêche le rechargement de la page

    const nom = document.getElementById('nom').value;
    const matiere = document.getElementById('matiere').value;
    const note = document.getElementById('note').value;

    fetch('http://127.0.0.1:5000/api/notes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nom: nom, matiere: matiere, note: note })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Échec de l\'ajout de la note.');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('message').textContent = `Note ajoutée pour ${data.nom} !`;
        // Recharge la liste pour afficher la nouvelle note
        fetchAndDisplayNotes(); 
        document.getElementById('add-note-form').reset(); // Réinitialise le formulaire
    })
    .catch(error => {
        console.error('Erreur POST:', error);
        document.getElementById('message').textContent = 'Erreur lors de l\'ajout.';
    });
};

// Événements
document.addEventListener('DOMContentLoaded', () => {
    // 1. Charger les notes au démarrage
    fetchAndDisplayNotes();

    // 2. Écouter la soumission du formulaire
    document.getElementById('add-note-form').addEventListener('submit', handleAddNote);
});