async function populateLists() {
    const response = await fetch("http://localhost:5000/lista", {
        method: "GET",
    });
    const [ ...lists ] = await response.json();
    for (const { id, titolo } of lists) {
        const node = document.createElement('li');
        const nodeText = document.createTextNode(titolo);
        node.appendChild(nodeText);
        const peopleNode = document.createElement('ul');
        peopleNode.id = `lista${id}`;
        node.appendChild(peopleNode);
        document.getElementById("lists").appendChild(node);
        populateList(id, peopleNode);
    }
}

async function populateList(id, parentNode) {
    const response = await fetch(`http://localhost:5000/lista/${id}`, {
        method: "GET",
    });
    const [ ...people ] = await response.json();
    for (const { nome, email } of people) {
        const node = document.createElement('li');
        const nodeText = document.createTextNode(`${nome} ~ ${email}`);
        node.appendChild(nodeText);
        parentNode.appendChild(node);
    }
}

populateLists();
