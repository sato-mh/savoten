const setPostJsonEventToCreateEventButton = () => {
  const create_event_button = document.getElementById("create_event_button");
  create_event_button.addEventListener(
    "click",
    () => {
      const requestData = formDataToJson(document.forms["create_event_form"]);
      postJson(requestData);
    },
    false
  );
};

const formDataToJson = form => {
  const formData = $(form).serializeArray();
  const jsonData = parseJson(formData);
  return jsonData;
};

const parseJson = data => {
  const returnJson = {};
  for (let i = 0; i < data.length; i++) {
    returnJson[data[i].name] = data[i].value;
  }
  return returnJson;
};

const postJson = jsonData => {
  $.post({
    type: "post",
    url: "/api/v1/events",
    data: JSON.stringify(jsonData),
    contentType: "application/json"
  }).then(
    responseData => {
      alert("Create event success!! [event_id: " + responseData["id"] + "]");
      console.log(responseData);
      return;
    },
    (xhr, textStatus, errorThrown) => {
      try {
        const responseData = $.parseJSON(xhr.responseText);
        console.log(responseData);
      } catch (e) {
        console.log(e);
      }
      alert(
        xhr.status +
          " " +
          errorThrown +
          ": Server error. Please contact server administrator."
      );
    }
  );
};

setPostJsonEventToCreateEventbutton();
