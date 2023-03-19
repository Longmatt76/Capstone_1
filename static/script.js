const $input = $("#player_count");
const $table = $("#formtable");

function generateForms() {
  const cells = 2;
  const players = $input.val();
  const $table = $("#formtable");
  const body = document.createElement("tbody");
//   console.log(players);
  for (let x = 0; x < players -1; x++) {
    const head = document.createElement('th')
    head.setAttribute('scope', 'row');
    head.setAttribute('name', `${x + 2}`)
    head.innerHTML = x + 2;
    const row = document.createElement("tr");
    row.append(head)
    row.classList.add("border");
    for (let y = 0; y < cells; y++) {
      const cell = document.createElement("td");
      const input = document.createElement("input");
      input.setAttribute('name',`row${x + 2}input${y + 1}`)
      input.classList.add("form-control");
      cell.classList.add("border");
      cell.append(input);
      row.append(cell);
    }
   
    head.setAttribute
    body.append(row);
    $table.append(body);
  }
  $input.hide()
}

$input.change(function () {
  generateForms();
});
