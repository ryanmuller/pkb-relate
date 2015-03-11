$(document).on('click', '#goRelate', function() {
  $.post("/related", { content: $("#main-content").val() }, function(data) {
    $("#cards .content").html("")
    var urls = data['related_urls']
    _.each(urls, function(url) { $("#cards .content").append($("<li>").append($("<a>").attr('href', url).text(url))) })
  })
})
