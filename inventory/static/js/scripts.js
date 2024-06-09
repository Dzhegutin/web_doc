function addRow() {
    const table = document.getElementById('items-table').getElementsByTagName('tbody')[0];
    const newRow = table.rows[0].cloneNode(true);
    const inputs = newRow.getElementsByTagName('input');
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].value = '';
    }
    table.appendChild(newRow);
}

function removeRow(button) {
    const row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
}