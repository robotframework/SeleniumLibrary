users = { 'demo' : 'mode', 
          'dave' : 'wibble' }

function login(username, password) { 
    return users[username] == password
}
