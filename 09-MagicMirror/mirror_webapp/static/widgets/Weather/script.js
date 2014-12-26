var Weather = function() {
  var that = this;

  this.capitalise = function(s) {
    return s && s[0].toUpperCase() + s.slice(1);
  };

  // Function to handle updating weather info
  this.updateWeather = function(widgetDOM) {
    $.getJSON('/widget_data/' + widgetDOM.id, function(data) {
      widgetDOM.getElementsByClassName('weather-icon')[0].src = data.current.icon;

      currentName = widgetDOM.getElementsByClassName('weather-current')[0].getElementsByTagName('h2')[0]
      currentName.innerText = data.current.name;
      jQuery(currentName).fitText(0.6);

      currentDescription = widgetDOM.getElementsByClassName('weather-current')[0].getElementsByTagName('p')[0];
      currentDescription.innerText = that.capitalise(data.current.description);
      jQuery(currentDescription).fitText(0.9);

      widgetDOM.getElementsByClassName('weather-temp-current')[0].innerText = data.temperature.current;
      widgetDOM.getElementsByClassName('weather-temp-low')[0].innerText = data.temperature.min;
      widgetDOM.getElementsByClassName('weather-temp-high')[0].innerText = data.temperature.max;

      widgetDOM.getElementsByClassName('weather-wind-direction')[0].innerText = data.wind.direction_name;
      widgetDOM.getElementsByClassName('weather-wind-speed')[0].innerText = data.wind.speed;

      widgetDOM.getElementsByClassName('weather-humidity')[0].innerText = data.humidity;
      widgetDOM.getElementsByClassName('weather-pressure')[0].innerText = data.pressure;
    });
  };
}

Weather.prototype.init = function(widgetDOM) {
  this.updateWeather(widgetDOM);
};

Weather.prototype.update = function(widgetDOM) {
  this.updateWeather(widgetDOM);
};
