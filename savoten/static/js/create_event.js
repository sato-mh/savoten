const setPostJsonEventToCreateEventButton = () => {
  const createEventButton = document.getElementById("create_event_button");
  createEventButton.addEventListener(
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
  const jsonData = parseFormNameAndValueToJson(formData);
  return jsonData;
};

const parseFormNameAndValueToJson = formData => {
  const returnJson = {};
  formData.forEach(target => {
    returnJson[target.name] = target.value;
  });
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

setPostJsonEventToCreateEventButton();
