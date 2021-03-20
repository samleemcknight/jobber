const dateEl = document.getElementById('id_date');
M.Datepicker.init(dateEl, {
  format: 'yyyy-mm-dd-hh-mm-ss',
  defaultDate: new Date(),
  setDefaultDate: true,
  autoClose: true
});
const selectEl = document.getElementById('id_time_zone');
M.FormSelect.init(selectEl);