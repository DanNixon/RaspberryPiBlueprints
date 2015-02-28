var TwitterSearchFeed = function() {
  this.updateFeed = function(widgetDOM) {
    widgetDOM.getElementsByClassName('tweets')[0].innerHTML = '';

    $.getJSON('/widget_data/' + widgetDOM.id, function(data) {
      var items = data.tweets;
      for(i = 0; i < items.length; i++) {
        var userElement = document.createElement('dt');
        var userText = document.createTextNode(items[i].username);
        userElement.appendChild(userText);

        var tweetElement = document.createElement('dd');
        var tweetText = document.createTextNode(items[i].tweet);
        tweetElement.appendChild(tweetText);

        widgetDOM.getElementsByClassName('tweets')[0].appendChild(userElement);
        widgetDOM.getElementsByClassName('tweets')[0].appendChild(tweetElement);
      }
    });
  };
}

TwitterSearchFeed.prototype.init = function(widgetDOM) {
  this.updateFeed(widgetDOM);
};

TwitterSearchFeed.prototype.update = function(widgetDOM) {
  this.updateFeed(widgetDOM);
};
