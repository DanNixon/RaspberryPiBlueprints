var RSSTicker = function() {
  var that = this;

  var items = [];
  var currentItemIndex = 0;
  var interval;
  var widgetDOM;

  this.updateItemsList = function() {
    $.getJSON('/widget_data/' + this.widgetDOM.id, function(data) {
      items = data.items;

      clearInterval(interval);
      interval = setInterval(that.newItem, data.update_time * 1000);

      that.newItem();
    });
  };

  this.newItem = function() {
    var itemText = items[currentItemIndex];

    var widgetTextDOM = that.widgetDOM.getElementsByClassName('rss-ticker-item')[0];
    $(widgetTextDOM).fadeOut(400, function() {
      widgetTextDOM.innerText = itemText;
      $(widgetTextDOM).fadeIn(400);
    });

    currentItemIndex += 1;

    if(currentItemIndex == items.length) {
      currentItemIndex = 0;
    }
  };
}

RSSTicker.prototype.init = function(widgetDOM) {
  this.widgetDOM = widgetDOM;
  this.updateItemsList();
};

RSSTicker.prototype.update = function(widgetDOM) {
  this.updateItemsList();
};
