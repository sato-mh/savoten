const eventKeyToDisplayNameMap = {
  "id": "ID",
  "name": "イベント名",
  "items": "項目",
  "start": "開始時刻",
  "end": "終了時刻",
  "description": "備考",
  "anonymous": "匿名投票",
  "created_at": "作成日時",
  "updated_at": "更新日時",
  "deleted_at": "削除日時"
}

const displayEventInfomationTable = () => {
  // アクセスURL/evests/${id}から${id}を取得
  const path = location.pathname;
  const event_id = path.split('/').pop();
  $.getJSON({
    url: `/api/v1/events/${event_id}`
  }).then(
    (data, status, xhr) => {
      const event = data["data"];
      if (!Object.keys(event).length) {
        alert(`Event(id: ${id}) does not exist.`);
        return;
      }
      const dataKeys = ["id", "name", "items", "start", "end", "description", "anonymous", "created_at", "updated_at", "deleted_at"];
      const tableId = "eventInfomationTable";
      makeTable(event, dataKeys, tableId);
    },
    (xhr, textStatus, errorThrown) => {
      showRequestError(xhr, textStatus, errorThrown);
    }
  );
};

const makeTable = (data, dataKeys, tableId) => {
  const table = document.getElementById(tableId);
  for (let key of dataKeys) {
    const row = table.insertRow(-1);
    let cell = row.insertCell(-1);
    cell.appendChild(document.createTextNode(eventKeyToDisplayNameMap[key]));
    cell = row.insertCell(-1);
    if (data[key] == null){
      cell.appendChild(document.createTextNode("No Data"));
    } else {
    cell.appendChild(document.createTextNode(data[key]));
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
      `${xhr.status} ${errorThrown} : Invalid Request. Please check input value.`
    );
  } else {
    alert(
      `${xhr.status} ${errorThrown} : Internal server error. Please contact server administrator.`
    );
  }
};

window.addEventListener("load", displayEventInfomationTable);
