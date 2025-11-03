console.log("Frontend chargé avec succès !");

// Example: Fetch notes from backend and populate table
async function loadNotes() {
  try {
    const response = await fetch('/api/notes');
    if (!response.ok) throw new Error('API error');
    const notes = await response.json();
    const tableBody = document.querySelector('#table-notes tbody');
    tableBody.innerHTML = '';  // Clear existing
    notes.forEach(note => {
      const row = document.createElement('tr');
      row.innerHTML = `<td>${note.id}</td><td>${note.title}</td><td>${note.content}</td>`;
      tableBody.appendChild(row);
    });
  } catch (error) {
    console.error('Error loading notes:', error);
  }
}

// Load on DOM ready
document.addEventListener('DOMContentLoaded', loadNotes);