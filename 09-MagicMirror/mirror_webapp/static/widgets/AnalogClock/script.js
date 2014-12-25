var AnalogClock = function() {
  this.time = new Date();

  var that = this;

  this.setTimeData = function(data) {
    that.time = new Date(data.epoch_seconds * 1000);
  };
}

AnalogClock.prototype.init = function(widgetDOM) {
  $.getJSON('/widget_data/' + widgetDOM.id, this.setTimeData);

  this.updateUI(widgetDOM);
};

AnalogClock.prototype.update = function(widgetDOM) {
  this.time.setSeconds(this.time.getSeconds() + 1);

  this.updateUI(widgetDOM);
};

AnalogClock.prototype.updateUI = function(widgetDOM) {
  var angle = 360 / 60;

  var hour = this.time.getHours();
  if(hour > 12) {
    hour = hour - 12;
  }

  var minute = this.time.getMinutes();
  var second = this.time.getSeconds();

  hourAngle = (360/12) * hour + (360/(12*60)) * minute;

  widgetDOM.getElementsByClassName('second-hand')[0].style['transform'] = 'rotate(' + angle * second + 'deg)';
  widgetDOM.getElementsByClassName('minute-hand')[0].style['transform'] = 'rotate(' + angle * minute + 'deg)';
  widgetDOM.getElementsByClassName('hour-hand')[0].style['transform'] = 'rotate(' + hourAngle + 'deg)';
};
