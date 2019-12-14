// show and hide modal
let target;
document.querySelectorAll(".modal-button").forEach(function(el) {
  el.addEventListener("click", function() {
    target = document.querySelector(el.getAttribute("data-target"));
    target.classList.add("is-active");
    target.querySelector(".modal-close").addEventListener("click",   function() {
      target.classList.remove("is-active");
    });
  });
});

// reusable function for POST & PATCH requests
const sendData = async (url, data, method) => {
  // Default options are marked with *
  const response = await fetch(url, {
    method, // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
    },
    redirect: "follow", // manual, *follow, error
    referrer: "no-referrer", // no-referrer, *client
    // body: JSON.stringify(data) // body data type must match "Content-Type" header
    body: data
  });
  return await response.json(); // parses JSON response into native JavaScript objects
};

// submit actor
const submitActor = async () => {
  let actorForm = document.getElementById("actorForm");
  let formData = new FormData(actorForm);

  try {
    const data = await sendData("/actors", formData, "POST");
    if (data.success) {
      location.href = '/actors';
    } else {
      throw data.message;
    }
  } catch (error) {
    iziToast.error({
      title: "Error",
      message: error,
    });
  }
};

// submit movie
const submitMovie = async () => {
  let movieForm = document.getElementById("movieForm");
  let formData = new FormData(movieForm);

  try {
    const data = await sendData("/movies", formData, "POST");
    if (data.success) {
      location.href = '/movies';
    } else {
      throw data.message;
    }
  } catch (error) {
    iziToast.error({
      title: "Error",
      message: error,
    });
  }
};