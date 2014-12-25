var TextCalendar = function() {
  this.time = new Date();

  var that = this;

  this.setTimeData = function(data) {
    that.time = new Date(data.epoch_seconds * 1000);
  };
}

TextCalendar.prototype.init = function(widgetDOM) {
  $.getJSON('/widget_data/' + widgetDOM.id, this.setTimeData);

  this.updateUI(widgetDOM);
};

TextCalendar.prototype.update = function(widgetDOM) {
  this.time.setTime(this.time.getTime() + 1000);

  this.updateUI(widgetDOM);
};

TextCalendar.prototype.updateUI = function(widgetDOM) {
  var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  var year = this.time.getFullYear();
  var date = this.time.getDate();
  var month = months[this.time.getMonth()];
  var day = days[this.time.getDay()];

  widgetDOM.getElementsByClassName('textcal-dayname')[0].innerText = day;
  widgetDOM.getElementsByClassName('textcal-daymonth')[0].innerHTML = '<span class="textcal-date">' + date + '</span>|' + month;
  widgetDOM.getElementsByClassName('textcal-year')[0].innerText = year;

  jQuery(widgetDOM.getElementsByClassName('textcal-dayname')[0]).fitText(0.6);
  jQuery(widgetDOM.getElementsByClassName('textcal-daymonth')[0]).fitText(0.35);
  jQuery(widgetDOM.getElementsByClassName('textcal-year')[0]).fitText(0.8);
};
