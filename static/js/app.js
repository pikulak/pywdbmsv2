function apiCall(method, path, params, cb){
	var timeout = 300000;

	$.ajax({
		timeout: timeout,
		url: 'api' + path,
		method: method,
		cache: false,
		data: params,
		success: data => cb(data),
		error: (xhr, status, data) => {
			if (status == 'timeout'){
				return cb({error: 'Timeout after ' + (timeout/1000) + 's'})
			}
			cb(jQuery.parseJSON(xhr.responseText))
		}
	})
}

function addServer(params, callback)    { apiCall('POST', '/servers/', params, callback) }
function deleteServer(server, callback) { apiCall('DELETE', '/servers/${server}', {}, callback) }
function getServers(callback)           { apiCall('GET', '/servers/', {}, callback) }
function getDatabases(server, callback) { apiCall('GET', '/servers/${server}/databases/', {}, callback) }

function buildServerModal(event){
	var modalTitle = $('#modalTitle')
	var modal = $('#modalBody')
	var modalHTML = ''
	modalTitle.html('Add server')
	modalHTML += `
	<form id='addServerForm' action='#' method='POST'>
		<p id='modalInfo'></p>
		<label for='drivername'>drivername:</label>
		<input type='text' class='form-control' id='drivername' name='drivername'>
		<label for='host'>host:</label>
		<input type='text' class='form-control' id='host' name='host'>
		<label for='port'>port:</label>
		<input type='text' class='form-control' id='port' name='port'>
		<label for='database'>database:</label>
		<input type='text' class='form-control' id='database' name='database'>
		<label for='username'>username:</label>
		<input type='text' class='form-control' id='username' name='username'>
		<label for='password'>password:</label>
		<input type='password' class='form-control' id='password' name='password'>
		</br>
		<input type='submit' id='addServerSubmit' class='btn btn-default' value='Connect'>
		<button type='button' class='btn btn-default' data-dismiss='modal'>Close</button>
	</form>`
	modal.html(modalHTML)
}

function handleAddServerForm(event){
	var params = $('#addServerForm').serialize()
	var infoTag = $('#modalInfo')
	addServer(params, data => {
		data = data[0]
		if (data.status == 'error'){
			infoTag.html('<b>' + data.message + '</b>')
		} else if (data.status == 'success'){
			infoTag.html(data.message)
		} else {
			infoTag.html('')
		}
	})
	event.preventDefault()
}

function showServerNavbar(event){
	var navbar = $('#navbarServers')
	var itemsHTML = ''
	getServers(data =>{
		data = data[0]
		if (data.status == 'success'){
			var serversIPs = data.data
			serversIPs.forEach(serverIP =>{
				itemsHTML += `
				<li class='nav-item'>
					<a class='nav-link' href='/servers/${serverIP}/'>${serverIP}</a>
				</li>`
			})
		}
		navbar.html(itemsHTML)
	})
}

$('#toggleServerAddModal').bind('click', buildServerModal)
$('#modalBody').bind('submit', '#addServerForm', handleAddServerForm)
$(() => {
	showServerNavbar() 
})