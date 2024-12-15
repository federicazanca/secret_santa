async function add_persona() {
    const nameInput = document.getElementById("nameInput").value;
    if (!nameInput) {
        alert("Please enter a name");
        return;
    }
    const response = await fetch("http://localhost:5000/names", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome: nameInput }),
    });
    const result = await response.json();
    alert(result.message || "Name added successfully");
}

async function extract_random_name() {
    const response = await fetch("http://localhost:5000/extract", {
        method: "GET",
    });
    const result = await response.json();
    if (result.random_name) {
        alert(`Randomly selected name: ${result.random_name}`);
    } else {
        alert(result.message || "No names found in the list");
    }
}
