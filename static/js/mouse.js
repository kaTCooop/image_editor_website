var last_point = null

// Post to the provided URL with the specified parameters.
function post(path, parameters) {
    var form = $('<form></form>')

    form.attr("method", "post")
    form.attr("action", path)

    $.each(parameters, function(key, value) {
        var field = $('<input></input>')

        field.attr("type", "hidden")
        field.attr("name", key)
        field.attr("value", value)

        form.append(field)
    })

    // The form needs to be a part of the document in
    // order for us to be able to submit it.
    $(document.body).append(form)
    form.submit()
}

function printMousePos(event) {
	var image = document.getElementById('IMG')
	var rect = image.getBoundingClientRect()	

	imageX = rect.left
	imageY = rect.top

	let x = event.clientX - imageX // offsetX or clientX
	let y = event.clientY - imageY

	var value = x.toString() + ';'  + y.toString()
	
	if (last_point != null)	{
		var yourUrl = window.location.href
		var par = {'value1' : last_point, 'value2' : value}
		post(yourUrl, par)
		last_point = null

	}

	else {
		last_point = value		
	}
}

window.onload = document.addEventListener("click", printMousePos)

