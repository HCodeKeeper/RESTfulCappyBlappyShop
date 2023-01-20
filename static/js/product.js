api_path_to_add = "/cart/item/add/";
api_reviews = "/reviews/get/product/";
api_review_add = "/reviews/add/product/";


const MIN = 1;
const MAX = 100;

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


function get_element(){
    return document.getElementsByClassName("body_section")[0];
}


function clear_element(element){
    element.innerHTML = "";
}


function render_description(text){
    let section = get_element();
    clear_element(section);
    let text_element = document.createElement("p");
    text_element.appendChild(document.createTextNode(text));
    section.appendChild(text_element);
}


function render_reviews(product_id, page){
    let xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        }
      };
      xhttp.onload = () => {
          let reviews = JSON.parse(xhttp.responseText);
            get_reviews(product_id, page, reviews);
      }
      xhttp.open("GET", api_reviews + product_id + "/page/"+ page + "/", true);
      xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
      xhttp.send();
}

function get_review_form(product_id){
    let form = document.createElement("form");
    form.setAttribute("method", "POST");
    form.setAttribute("action", api_review_add + product_id + "/");
    //rating
    //let rating = document.createElement("");
    let text = document.createElement("input");
    text.setAttribute("type", "text");

    let submit = document.createElement("input");
    submit.setAttribute("type", "submit");
    //form.appendChild(rating);
    form.appendChild(text);
    form.appendChild(submit);
    return form;
}

function get_reviews(product_id, page, reviews) {
    let section = get_element();
    clear_element(section);
    let reviews_section = document.createElement("div");
    section.appendChild(reviews_section);
    section.appendChild(
        get_review_form(product_id)
    );

    for (const review of reviews["reviews"]) {
        let user = review["user"];
        let rating = review["rating"];
        let review = review["self"];
        let username = user["name"];
        let review_container = document.createElement("div");
        let review_element = document.createElement("p");
        let left_section = document.createElement("div");
        let right_section = document.createElement("div");
        left_section.setAttribute("class", "left_section");
        right_section.setAttribute("class", "right_section");
        let username_element = document.createElement("h6");
        let rating_element = document.createElement("p");
        username_element.appendChild(document.createTextNode(username));
        rating_element.appendChild(document.createTextNode(rating));
        review_element.appendChild(document.createTextNode(review));
        left_section.appendChild(username_element);
        left_section.appendChild(rating_element);
        right_section.appendChild(review_element);

        review_container.appendChild(left_section);
        review_container.appendChild(right_section);
        reviews_section.appendChild(review_container);
    }
    let pagination = document.createElement("div");
    if (page > 1){
        let prev_page = document.createElement("button");
        prev_page.setAttribute("onclick", "get_reviews(product_id, reviews['previous_page'])");
        pagination.appendChild(prev_page);
    }
    let next_page = document.createElement("button");
        next_page.setAttribute("onclick", "get_reviews(product_id, reviews['next_page'])");
    pagination.appendChild(next_page);
    reviews_section.appendChild(pagination);
}


function render_contacts(manufacturer, contact_info){
    let section = get_element();
    clear_element(section);
    let manufacturer_element = document.createElement("p");
    manufacturer_element.setAttribute("id", "manufacturer");
    manufacturer_element.appendChild(document.createTextNode(manufacturer));
    section.appendChild(manufacturer_element)

    let contacts_info = document.createElement("p");
    contacts_info.setAttribute("id", "contacts");
    contacts_info.appendChild(document.createTextNode(contact_info));
    section.appendChild(contacts_info);
}

function boundaries(number, min, max){
    return (number >= min && number <= max);
}

function validate_number(number, min, max){
    let is_valid = false;
    if (!isNaN(number)){
        is_valid = boundaries(number, min, max);
    }
    return is_valid;
}


function add_to_cart(product_id){
    let count = document.getElementById("counter").value;
    let addon_id = document.getElementById("addons").value;
    if (!validate_number(count, MIN, MAX)){
        return;
    }

    let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

    }
  }
  xhttp.open("POST", api_path_to_add, true);

  xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
  xhttp.setRequestHeader("X-CSRFToken", getCSRF());
  xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  if (!isNaN(parseInt(count)) && parseInt(count) >= 1){
      xhttp.send(JSON.stringify(
          {payload:{
          "product_id" : product_id,
          "count" : count,
          "addon_id" : addon_id
      }}
  ));
  }
}