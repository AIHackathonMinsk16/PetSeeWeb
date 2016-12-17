function On(){
  $.ajax({
          type: 'GET',
          url: 'http://192.168.43.198:3000/on',
          dataType: 'application/json'
        });   // Ajax Call
}

function Off(){
  $.ajax({
          type: 'GET',
          url: 'http://192.168.43.198:3000/off',
          dataType: 'application/json'
        });   // Ajax Call
}

function Left(){
  $.ajax({
          type: 'GET',
          url: 'http://192.168.43.198:3000/left',
          dataType: 'application/json'
        });   // Ajax Call
}

function Right(){
  $.ajax({
          type: 'GET',
          url: 'http://192.168.43.198:3000/right',
          dataType: 'application/json'
        });   // Ajax Call
}

function Forward(){
  $.ajax({
          type: 'GET',
          url: 'http://192.168.43.198:3000/forward',
          dataType: 'application/json'
        });   // Ajax Call
}

function Reverse(){
  $.ajax({
          type: 'GET',
          url: 'http://192.168.43.198:3000/reverse',
          dataType: 'application/json'
        });   // Ajax Call
}
