/*
This implements an autocomplete feature for an input field. When the user begins typing in the input field, the function searches through two arrays: arr and parr. 
For each element in the arrays that contains the input value as a substring, the function creates a new div element and appends it to a list of autocomplete suggestions. 
The div element also contains a link to a page with the corresponding information for that element. The function also handles keyboard navigation through the list of autocomplete suggestions.

The function takes in four arguments:
  - inp : input field element.
  - arr : array of strings representing autocomplete suggestions for the input field
  - heroidarr : array of integers corresponding to the hero ids for each element in arr
  - parr : array of strings representing autocomplete suggestions for the input field
  - pid : array of integers corresponding to the pokemon ids for each element in parr
*/

let autocomplete = (inp, arr, heroidarr, parr, pid) => {
  var heroid = heroidarr;
  let currentFocus;
  inp.addEventListener("input", function(e) {
    let a, b, i, t, p, val = this.value;
    closeAllLists();
    if (!val) {
      return false;
    }
    currentFocus = -1;
    a = document.createElement("DIV");
    a.setAttribute("id", this.id + "autocomplete-list");
    a.setAttribute("class", "autocomplete-items list-group text-left");
    a.style.maxHeight = "400px";
    a.style.overflowY = "scroll";
    this.parentNode.appendChild(a);
    for (i = 0; i < arr.length; i++) {
      for (i = 0; i < arr.length; i++) {
        if ((arr[i].toUpperCase()).indexOf(val.toUpperCase()) > -1) {
          t = (arr[i].toUpperCase()).indexOf(val.toUpperCase())
          p = t + val.length
          b = document.createElement("DIV");
          b.innerHTML = arr[i].substring(0,t);
          b.innerHTML = arr[i].substring(0,t) + "<strong>" + arr[i].substring(t, p) + "</strong>" + arr[i].substring(p);
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          var link = "/hero/"+heroid[i]
          b.innerHTML = "<a class = 'dropdown-item' href = " + link +">" + b.innerHTML + "</a>"
          b.addEventListener("click", function(e) {
            inp.value = this.getElementsByTagName("input")[0].value;
            closeAllLists();
          });
          a.appendChild(b);
        }
      }
      if (i === 9) {
        break;
      }
    }
    for (i = 0; i < parr.length; i++) {
      if ((parr[i].toUpperCase()).indexOf(val.toUpperCase()) > -1) {
        t = (parr[i].toUpperCase()).indexOf(val.toUpperCase())
        p = t + val.length
        b = document.createElement("DIV");
        b.innerHTML = parr[i].substring(0,t);
        b.innerHTML = parr[i].substring(0,t) + "<strong>" + parr[i].substring(t, p) + "</strong>" + parr[i].substring(p);
        b.innerHTML += "<input type='hidden' value='" + parr[i] + "'>";
        var link = "/pokemon/"+pid[i]
        b.innerHTML = "<a class = 'dropdown-item' href = " + link +">" + b.innerHTML + "</a>"
        b.addEventListener("click", function(e) {
          inp.value = this.getElementsByTagName("input")[0].value;
          closeAllLists();
        });
        a.appendChild(b);
      }
    }
  });

  inp.addEventListener("keydown", function(e) {
    var x = document.getElementById(this.id + "autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
      currentFocus++;
      addActive(x);
    } else if (e.keyCode == 38) {
      currentFocus--;
      addActive(x);
    } else if (e.keyCode == 13) {
      e.preventDefault();
      if (currentFocus > -1) {
        if (x) x[currentFocus].click();
      }
    }
  });

  // methods used for autocomplete
  let addActive = (x) => {
    if (!x) return false;
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = x.length - 1;
    x[currentFocus].classList.add("active");
  }
  let removeActive = (x) => {
    for (let i = 0; i < x.length; i++) {
      x[i].classList.remove("active");
    }
  }
  let closeAllLists = (elmt) => {
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmt != x[i] && elmt != inp) {
        x[i].parentNode.removeChild(x[i]);
    }
  }
}

document.addEventListener("click", function(e) {
  closeAllLists(e.target);
});
}

