console.log("working");

function addToStorage(movie) {
  let movies = JSON.parse(localStorage.getItem("movies")) || [];
  movies.push(movie);
  localStorage.setItem("movies", JSON.stringify(movies));
  console.log(JSON.parse(localStorage.getItem("movies")));
}

window.onload = function () {
  let xhr = new XMLHttpRequest();
  let history = localStorage.getItem("movies") || null;
  let data = [];
  if (history) {
    history = JSON.parse(history);
    for (let i = 0; i < history.length; i++) {
      if (history[i] != null) {
        data.push(history[i]);
      }
    }
  }

  // console.log(data);
  // localStorage.setItem("movies", JSON.stringify(data));
  let wrapper = document.getElementById("movies");
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      let recommended = JSON.parse(xhr.response);
      console.log(recommended["recommended"][0]["movies"]);
      for (let i = 0; i < recommended["recommended"][0]["movies"].length; i++) {
        (function (i) {
          let movies_list = recommended["recommended"][0]["movies"];
          let posters_list = recommended["recommended"][0]["posters"];
          let main_div = document.createElement("div");
          main_div.classList.add("col-md-4");
          let card = document.createElement("div");
          card.classList.add("card", "mb-3");
          let card_body = document.createElement("div");
          card_body.classList.add("card-body");
          let h2 = document.createElement("h2");
          let image = document.createElement("img");
          image.src = posters_list[i];
          image.classList.add("card-img-top");
          h2.classList.add("card-title");
          h2.innerText = movies_list[i];
          card.appendChild(image);
          card_body.appendChild(h2);
          card.appendChild(card_body);
          main_div.appendChild(card);
          main_div.addEventListener("click", function () {
            addToStorage(movies_list[i]);
            console.log("called");
          });
          wrapper.appendChild(main_div);
        })(i);
      }

      console.log("d");
    }
  };

  xhr.open(
    "GET",
    `http://localhost:8000/get_recommendation?history=${JSON.stringify(
      history
    )}`,
    true
  );
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send();
};
function makeRequest(q, wrapper) {
  console.log("called makeRequest");
  let xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      let recommended = JSON.parse(xhr.response);
      wrapper.innerHTML = "";

      for (let i = 0; i < recommended["movies"].length; i++) {
        (function (i) {
          let movies_list = recommended["movies"][i]["title"];
          let posters_list = recommended["movies"][i]["poster"];
          let main_div = document.createElement("div");
          main_div.classList.add("col-md-4");
          let card = document.createElement("div");
          card.classList.add("card", "mb-3");
          let card_body = document.createElement("div");
          card_body.classList.add("card-body");
          let h2 = document.createElement("h2");
          let image = document.createElement("img");
          image.src = posters_list;
          image.classList.add("card-img-top");
          h2.classList.add("card-title");
          h2.innerText = movies_list;
          card.appendChild(image);
          card_body.appendChild(h2);
          card.appendChild(card_body);
          main_div.appendChild(card);
          main_div.addEventListener("click", function () {
            addToStorage(movies_list);
            console.log("called");
          });
          wrapper.appendChild(main_div);
        })(i);
      }
    }
  };

  xhr.open("GET", `http://localhost:8000/search?q=${q}`, true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send();
}
function changeFunction(q) {
  let wrapper = document.getElementById("movies");
  let wrapperContent = wrapper.innerHTML;
  makeRequest(q, wrapper);
  document
    .getElementById("search_movie")
    .addEventListener("keydown", function (event) {
      if (event.key === "Backspace") {
        console.log("Backspace key is pressed");
        wrapper.innerHTML = "";
        wrapper.innerHTML = wrapperContent;
      }
      if (event.key == "Enter") {
        makeRequest(q, wrapper);
        console.log("Enter key is pressed");
      }
    });
}
