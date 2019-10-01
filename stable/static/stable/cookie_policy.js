function trnslt() {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/cookies_eng/', true);

  xhr.onload = function () {
    if (this.status == 200) {
      document.getElementById('cookies_txt').innerHTML = this.responseText;
    }
  }
  xhr.send();
}
