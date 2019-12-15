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

// forms
const actorForm = document.getElementById("actorForm");
const movieForm = document.getElementById("movieForm");
let formData;

// submit actor
const submitActor = async () => {
  formData = new FormData(actorForm);

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
  formData = new FormData(movieForm);

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

// set form values for easier editing
const setFormValues = (formName = '', data = {}) => {
  if (formName === 'editMovieForm') {
    document.forms['editMovieForm']['id'].value = data.id;
    document.forms['editMovieForm']['title'].value = data.title;
    document.forms['editMovieForm']['release_date'].value = data.release_date;
  } else if (formName === 'editActorForm') {
    document.forms['editActorForm']['id'].value = data.id;
    document.forms['editActorForm']['name'].value = data.name;
    document.forms['editActorForm']['gender'].value = data.gender;
  }
};

// edit movie
const editMovie = async () => {
  let editMovieForm = document.getElementById("editMovieForm");
  let formData = new FormData(editMovieForm);
  try {
    const data = await sendData(`/movies/${formData.get('id')}`, formData, "PATCH");
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

// delete movie
const deleteMovie = async (movieId) => {
  try {
    const data = await sendData(`/movies/${movieId}`, '', "DELETE");
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

// edit actor
const editActor = async () => {
  let editActorForm = document.getElementById("editActorForm");
  let formData = new FormData(editActorForm);
  try {
    const data = await sendData(`/actors/${formData.get('id')}`, formData, "PATCH");
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