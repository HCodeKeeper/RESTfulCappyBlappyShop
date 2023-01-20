api_path_to_remove = "/cart/item/remove/";
api_path_to_remove_all = "/cart/clear/"

function getCSRF() {
    let name = "csrftoken";
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function remove_from_cart(product_id){
    let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        window.location.replace("");
    }
  }
  xhttp.open("POST", api_path_to_remove, true);

  xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
  xhttp.setRequestHeader("X-CSRFToken", getCSRF());
  xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhttp.send(JSON.stringify(
      {payload:{"product_id" : product_id}})
  );
}

function remove_all_from_cart(){
    let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        window.location.replace("");
    }
  }
  xhttp.open("POST", api_path_to_remove_all, true);

  xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
  xhttp.setRequestHeader("X-CSRFToken", getCSRF());
  xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhttp.send();
}