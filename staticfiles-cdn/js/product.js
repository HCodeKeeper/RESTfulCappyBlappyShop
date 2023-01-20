api_path_to_add = "/cart/item/add/";
api_path_to_remove = "/cart/item/remove/";


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


function add_to_cart(product_id){
    let count = document.getElementById("counter");
    let addon_id = document.getElementById("addons").value;
    let purchase_buttons = document.getElementsByClassName("purchase_button");
    let add_button;
    let isPressed = true;
    if (purchase_buttons.length > 0){
        add_button = purchase_buttons[0];
        isPressed = false;
    }
    else{
        add_button = document.getElementsByClassName("not_active_button")[0];
    }

    let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let deal = JSON.parse(this.responseText);
        if (deal.hasOwnProperty("status") && deal.status == "200") {
           if (!isPressed){
               add_button.setAttribute("class", "not_active_button");
               clear_element(add_button);
               add_button.appendChild(document.createTextNode("In cart"));
               isPressed = true;
           }
           else{
               add_button.setAttribute("class", "purchase_button");
               clear_element(add_button);
               add_button.appendChild(document.createTextNode("Buy"));
               isPressed = false;
           }
        }
    }
  }
  if (isPressed){
      xhttp.open("POST", api_path_to_add, true);
  }
  else{
      xhttp.open("POST", api_path_to_remove, true);
  }

  xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
  xhttp.send(JSON.stringify(
      {
          "product_id" : product_id,
          "count" : count,
          "addon_id" : addon_id
      }
  ));
}
