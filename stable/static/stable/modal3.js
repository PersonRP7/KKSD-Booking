var modal = document.getElementById('simpleModal');
var closeBtn = document.getElementsByClassName('closeBtn')[0];
var ok_button = document.getElementById('ok_button');
var translate_button = document.getElementById('translate_button');

window.onload = function () {
  modal.style.display = 'block';
}

closeBtn.addEventListener('click', closeModal);
function closeModal() {
  modal.style.display = 'none';
}

ok_button.addEventListener('click', closeModal);
translate_button.addEventListener('click', translate);

function translate() {
  var modal_txt = document.getElementById('modal_txt');
  modal_txt.textContent = "By opening a profile you accept the end user licence agreement.";

  var licence_eng = document.getElementById('licence_eng');
  licence_eng.textContent = 'Licence';

  var cookies_eng = document.getElementById('cookies_eng');
  cookies_eng.textContent = 'Cookies';
}
