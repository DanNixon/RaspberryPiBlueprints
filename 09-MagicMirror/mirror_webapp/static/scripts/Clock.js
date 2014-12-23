var Clock = function() {
  this.time = new Date();

  var that = this;

  this.setTimeData = function(data) {
    that.time = new Date(data.year, data.month, data.day, data.hour, data.minute, data.second, 0);
  };

}

Clock.prototype.init = function(widgetDOM) {
  $.getJSON('/widget_data/' + widgetDOM.id, this.setTimeData);
};

Clock.prototype.update = function(widgetDOM) {
  var sec = this.time.getSeconds() + 1;
  this.time.setSeconds(sec);

  var h = this.time.getHours();
  var m = this.time.getMinutes();
  var s = this.time.getSeconds();

  m = this.formatTime(m);
  s = this.formatTime(s);

  widgetDOM.getElementsByTagName('p')[0].innerText = h + ":" + m + ":" + s;
};

Clock.prototype.formatTime = function(i) {
  if(i < 10) {
    i = "0" + i
  };

  return i;
};
