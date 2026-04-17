// Load notes on page load
window.onload = loadNotes;

function addNote() {
    const content = document.getElementById("noteInput").value;

    fetch('/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: content })
    })
        .then(() => {
            document.getElementById("noteInput").value = "";
            loadNotes();
        });
}

function loadNotes() {
    fetch('/get')
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("notesList");
            list.innerHTML = "";

            data.forEach(note => {
                const li = document.createElement("li");
                li.innerHTML = `
                ${note[1]} 
                <button onclick="deleteNote(${note[0]})">Delete</button>
            `;
                list.appendChild(li);
            });
        });
}

function deleteNote(id) {
    fetch(`/delete/${id}`, {
        method: 'DELETE'
    })
        .then(() => loadNotes());
}