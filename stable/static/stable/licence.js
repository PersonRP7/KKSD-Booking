var translate_button = document.getElementById('translate_button');
translate_button.addEventListener('click', translate);

function translate() {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/licence_eng/', true);

  xhr.onload = function () {
    if (this.status == 200) {
      var response_text = this.responseText;
      var licence_txt = document.getElementById('licence_txt');
      licence_txt.innerHTML = response_text;
    }
  }
  xhr.send();
}
