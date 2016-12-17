String.prototype.replaceAt=function(index, character) {
    return this.substr(0, index) + character + this.substr(index+character.length);
}

$(function() {
  var video = $('#videoPlayer');

  function resizeVideo() {
    video.css({
      // width: $(window).width(),
      height: $(window).height()
    })
  }

  $(document).ready(function(){
    resizeVideo();

    var ws       = new WebSocket('ws://' + window.location.host + window.location.pathname);
    ws.onopen    = function()  { console.log('websocket opened2'); };
    ws.onclose   = function()  { console.log('websocket closed'); }
    ws.onmessage = function(m) { console.log('websocket message: ' +  m.data); };

    var pressedControls = "0000000000";
    $('.controls').each(function() {
      $(this).mousedown(function() {
        index = parseInt($(this).attr('data-key'));
        pressedControls = pressedControls.replaceAt(index, "1");
        console.log(pressedControls);
      });
      $(this).mouseup(function() {
        index = parseInt($(this).attr('data-key'));
        pressedControls = pressedControls.replaceAt(index, "0");
        console.log(pressedControls);
      });
    });
  });

  $(window).resize(function() {
    resizeVideo();
  })
});
