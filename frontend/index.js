async function populateLists() {
    const response = await fetch("http://localhost:5000/lista", {
        method: "GET",
    });
    const [ ...lists ] = await response.json();
    const parentNode = document.getElementById("lists");
    for (const list of lists) {
        const { node, peopleNode } = createListNode(list);
        parentNode.appendChild(node);
        populateList(list.id, peopleNode);
    }
    parentNode.appendChild(createNewListComponent());
}

function createNewListComponent() {
    const node = document.createElement('div');
    const titleNode = document.createElement('input');
    titleNode.placeholder = "Nuova lista";
    const submitNode = document.createElement('button');
    submitNode.textContent = "Crea";
    submitNode.onclick = async () => {
        await fetch("http://localhost:5000/lista", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ titolo: titleNode.value }),
        });
        document.getElementById("lists").replaceChildren();
        populateLists();
    };
    node.appendChild(titleNode);
    node.appendChild(submitNode);
    return node;
}

function createNewGuestComponent(id) {
    const node = document.createElement('div');
    const nameNode = document.createElement('input');
    nameNode.placeholder = "Nome";
    const emailNode = document.createElement('input');
    emailNode.placeholder = "Email";
    const submitNode = document.createElement('button');
    submitNode.textContent = "Aggiungi";
    submitNode.onclick = async () => {
        await fetch(`http://localhost:5000/lista/${id}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ nome: nameNode.value, email: emailNode.value }),
        });
        document.getElementById("lists").replaceChildren();
        populateLists();
    };
    node.appendChild(nameNode);
    node.appendChild(emailNode);
    node.appendChild(submitNode);
    return node;
}

async function populateList(id, parentNode) {
    const response = await fetch(`http://localhost:5000/lista/${id}`, {
        method: "GET",
    });
    const [ ...people ] = await response.json();
    for (const guest of people) {
        const node = createListGuestNode(guest);
        parentNode.appendChild(node);
    }
    parentNode.appendChild(createNewGuestComponent(id));
}

function createListNode({ id, titolo }) {
    const node = document.createElement('li');
    const nodeText = document.createTextNode(titolo);
    node.appendChild(nodeText);
    const peopleNode = document.createElement('ul');
    node.appendChild(peopleNode);
    return { node, peopleNode };
}

function createListGuestNode({ nome, email }) {
    const node = document.createElement('li');
    const nodeText = document.createTextNode(`${nome} ~ ${email}`);
    node.appendChild(nodeText);
    return node;
}

function main() {
    populateLists();
}

main();
