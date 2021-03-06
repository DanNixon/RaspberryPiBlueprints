var RSSFeed = function() {
  this.updateFeed = function(widgetDOM) {
    widgetDOM.getElementsByClassName('rss-items')[0].innerHTML = '';

    $.getJSON('/widget_data/' + widgetDOM.id, function(data) {
      var items = data.items;
      for(i = 0; i < items.length; i++) {
        var newItem = document.createElement('li');
        var itemTitle = document.createTextNode(items[i].title);
        newItem.appendChild(itemTitle);
        widgetDOM.getElementsByClassName('rss-items')[0].appendChild(newItem);
      }
    });
  };
}

RSSFeed.prototype.init = function(widgetDOM) {
  this.updateFeed(widgetDOM);
};

RSSFeed.prototype.update = function(widgetDOM) {
  this.updateFeed(widgetDOM);
};
