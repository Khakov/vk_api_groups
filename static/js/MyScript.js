function startTime() {
  var today = new Date().getTime();
  document.getElementById('time').value = today;
}
window.onload = function load_on_start(){
    startTime();
};
