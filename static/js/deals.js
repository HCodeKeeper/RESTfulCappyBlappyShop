const api_path = "/random_deal";

function insert_random_deal(deal){
    let offer = document.getElementById("offer");
    let dealName = Object.keys(deal)[0];
    offer.setAttribute("href", deal[dealName]);
    let text = document.createTextNode(dealName);
    offer.appendChild(text);
}

function getAndRenderRandomDeal() {
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let deal = JSON.parse(this.responseText);
        if (deal.hasOwnProperty("status")){
            throw "Exception status: " + deal.status + "! Couldn't retrieve categories"
        } else{
            insert_random_deal(deal);
        }
    }
  };
  xhttp.open("GET", api_path, true);
  xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
  xhttp.send();
}

getAndRenderRandomDeal()