const api_path = "/categories";

function insert_categories(categories){
    let menu = document.getElementsByName("dropdown-content");
    Object.entries(categories).forEach(
        (currentValue) => {
            let tag = document.createElement("a");
            tag.setAttribute("href", currentValue[1]);
            tag.appendChild(document.createTextNode(currentValue[0]));
            document.getElementById("categories").appendChild(tag);
        }
    )
}

function getAndRenderCategories() {
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let categories = JSON.parse(this.responseText);
        if (categories.hasOwnProperty("status")){
            throw "Exception status: " + categories.status + "! Couldn't retrieve categories"
        } else{
            insert_categories(categories);
        }
    }
  };
  xhttp.open("GET", api_path, true);
  xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
  xhttp.send();
}

getAndRenderCategories()