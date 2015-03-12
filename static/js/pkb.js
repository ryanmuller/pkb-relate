$(document).ready(function() {
  var search_text = document.getElementById('search_text'),
      do_search = document.getElementById('do_search'),
      get_related = document.getElementById('get_related'),
      resource_area = document.getElementById('resource_area'),
      content_area = document.getElementById('content_area'),
      reference_area = document.getElementById('reference_area')
      medium = new Medium({
        element: content_area,
        mode: Medium.richMode,
        placeholder: 'Your Article',
        attributes: null,
        tags: null
      })

  sourceIndex = function(target_url) {
    var out = -1;
    _.each(reference_area.querySelectorAll('a.reference'), function(link, index) {
      if (link.getAttribute('href') === target_url) {
        out = index
      }
    })
    return out
  }

  $(document).on('click', '.insert', function() {
    var resource_url = $(this).next().attr('href'),
        source_count = reference_area.querySelectorAll('li').length
        source_index = sourceIndex(resource_url)
        source_num = source_index === -1 ? source_count + 1 : source_index + 1

    medium.focus()
    medium.insertHtml('['+source_num+']')

    if (source_index === -1) {
      reference_area.innerHTML +=
'<li>\
  <a class="insert" href="#">+</a>\
  <a class="reference" href="'+resource_url+'">'+resource_url+'</a>\
</li>'
    }
  })

  query_related = function(data) {
    resource_area.innerHTML = ''
    _.each(data['related_urls'], function(url) {
      resource_area.innerHTML +=
'<li>\
  <a class="insert" href="#">+</a>\
  <a href="'+url+'">'+url+'</a>\
</li>'
    })
  }

  do_search.onmousedown = function() { $.post('/related', { content: search_text.value }, query_related) }
  get_related.onmousedown = function() { $.post('/related', { content: medium.value() }, query_related) }
})
