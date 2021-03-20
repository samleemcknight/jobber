const dateEl = document.getElementById('id_date');
M.Datepicker.init(dateEl, {
  format: 'yyyy-mm-dd',
  defaultDate: new Date(),
  setDefaultDate: true,
  autoClose: true
});

const time = document.getElementById('id_time');
M.Timepicker.init(time, {
  format: 'hh-mm-ss',
  defaultTime: 'now',
  twelveHour: false,
});
const selectEl = document.getElementById('id_time_zone');
M.FormSelect.init(selectEl);

document.addEventListener('DOMContentLoaded', function () {
  const elem = document.querySelector('.modal');
  const elem1 = document.querySelector('#modal2');
  M.Modal.init(elem);
  M.Modal.init(elem1);
});
document.addEventListener('DOMContentLoaded', function () {
  const elem = document.querySelector('.carousel');
  M.Carousel.init(elem);
});