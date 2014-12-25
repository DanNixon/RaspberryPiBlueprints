var DigitalClock = function() {
  this.time = new Date();

  var that = this;

  this.setTimeData = function(data) {
    that.time = new Date(data.year, data.month, data.day, data.hour, data.minute, data.second, 0);
  };

}

DigitalClock.prototype.init = function(widgetDOM) {
  $.getJSON('/widget_data/' + widgetDOM.id, this.setTimeData);

  this.updateUI(widgetDOM);
};

DigitalClock.prototype.update = function(widgetDOM) {
  var sec = this.time.getSeconds() + 1;
  this.time.setSeconds(sec);

  this.updateUI(widgetDOM);
};

DigitalClock.prototype.updateUI = function(widgetDOM) {
  var h = this.time.getHours();
  var m = this.time.getMinutes();
  var s = this.time.getSeconds();

  m = this.formatTime(m);
  s = this.formatTime(s);

  var timeText = widgetDOM.getElementsByTagName('h2')[0];
  timeText.innerText = h + ":" + m + ":" + s;
  jQuery(timeText).fitText(0.45);
};

DigitalClock.prototype.formatTime = function(i) {
  if(i < 10) {
    i = "0" + i
  };

  return i;
};
