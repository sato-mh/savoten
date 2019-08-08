var create_event_btn = document.getElementById("create_event_btn")
  create_event_btn.addEventListener('click', function () {
    requestData = formDataToJson(document.forms["create_event_form"])
    postJson(requestData);
}, false);

// 各フォームのnameをkey, 入力値をⅴalueとしてjson形式で取得
var formDataToJson = function (form) {
  formData = $(form).serializeArray();
  jsonData = parseJson(formData);
  return jsonData
}
var parseJson = function (data) {
  var returnJson = {};
  for (idx = 0; idx < data.length; idx++) {
    returnJson[data[idx].name] = data[idx].value
  }
  return returnJson;
}
var postJson = function (data) {
  $.ajax({
    type: 'post',
    url: '/events',
    data: JSON.stringify(data),
    contentType: 'application/json',
    dataType: 'json',
  })
  .done(function (responseData) {
    alert('Create event success!! [event_id: ' + responseData['id'] + ']');
    console.log(responseData);
    return;
  })
  .fail(function (xhr, textStatus, errorThrown) {
    try {
      responseData = $.parseJSON(xhr.responseText);
      console.log(responseData)
    } catch (e) {
      console.log(e)
    }
    if (Number(xhr.status) < 500){
      alert(xhr.status + ' ' + errorThrown + ': Invalid Request. Please check input value.');
    } else {
      alert(xhr.status + ' ' + errorThrown + ': Internal server error. Please contact server administrator.');
    }
  })
  .always(function () {
  })
}