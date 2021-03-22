// activates materialize datepicker
const dateEl = document.getElementById('id_date');
M.Datepicker.init(dateEl, {
  format: 'yyyy-mm-dd',
  defaultDate: new Date(),
  setDefaultDate: true,
  autoClose: true
});

const selectEl = document.getElementById('id_time_zone');
M.FormSelect.init(selectEl);

// materialize time picker
const time = document.getElementById('id_time');
M.Timepicker.init(time, {
  format: 'hh-mm-ss',
  defaultTime: 'now',
  twelveHour: false,
});

document.addEventListener('DOMContentLoaded', function () {
  const modal1 = document.querySelector('.modal');
  const modal2 = document.querySelector('#modal2');
  const modal3 = document.querySelector('#modal3');
  M.Modal.init(modal1);
  M.Modal.init(modal2);
  M.Modal.init(modal3);
});

const elDropdown = document.getElementById("dropdown-trigger")
const instancesDropdown = M.Dropdown.init(elDropdown);