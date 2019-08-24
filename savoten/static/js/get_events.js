const displayEventsTable = () => {
  $.getJSON({
    url: "/api/v1/events"
  }).then(
    (data, status, xhr) => {
      const events = data["events"];
      if (events.length == 0) {
        alert("Event does not exist.");
        return;
      }
      // テーブルの項目行のデータ
      const dataKeys = ["id", "name", "description"];
      const tableId = "eventTable";
      makeTable(events, dataKeys, tableId);
    },
    (xhr, textStatus, errorThrown) => {
      showRequestError(xhr, textStatus, errorThrown);
    }
  );
};

const makeTable = (data, dataKeys, tableId) => {
  const table = document.getElementById(tableId);
  // set table_head
  const thead = table.createTHead();
  const thRow = thead.insertRow(0);
  for (let i = 0; i < dataKeys.length; i++) {
    const cell = thRow.insertCell();
    cell.textContent = dataKeys[i];
  }
  // set table_body
  for (let i = 0; i < data.length; i++) {
    const bodyRow = table.insertRow(-1);
    for (let j = 0; j < dataKeys.length; j++) {
      const cell = bodyRow.insertCell(-1);
      cell.appendChild(document.createTextNode(data[i][dataKeys[j]]));
    }
  }
};

const showRequestError = (xhr, textStatus, errorThrown) => {
  try {
    const responseData = $.parseJSON(xhr.responseText);
    console.log(responseData);
  } catch (e) {
    console.log(e);
  }
  if (Number(xhr.status) < 500) {
    alert(
      xhr.status +
        " " +
        errorThrown +
        ": Invalid Request. Please check input value."
    );
  } else {
    alert(
      xhr.status +
        " " +
        errorThrown +
        ": Internal server error. Please contact server administrator."
    );
  }
};

window.addEventListener("load", displayEventsTable);
