// auth
let tokenUrl = window.location.href.match(/\#(?:access_token)\=([\S\s]*?)\&/);
if (tokenUrl) {
  let token = tokenUrl[1];
  localStorage.setItem('token', token);

  // get permissions from token
  try {
    let permissions;
    permissions = JSON.parse(atob(token.split('.')[1])).permissions;
    localStorage.setItem('permissions', permissions);
    if (!localStorage.getItem('permissions')) {
      permissions = ['read:movies', 'read:actors']; // default permissions
      localStorage.setItem('permissions', permissions);
    }
  } catch (e) {
    iziToast.error({
      title: "Error",
      message: e,
    });
  }
}

if (localStorage.getItem('token') && localStorage.getItem('permissions')) {
  if (window.location.pathname === '/') {
    window.location.replace('/movies')
  }

  // hide log in button if logged in
  document.getElementById('loginButton').remove();

  // hide add actor button if no permissions
  if (!localStorage.getItem('permissions').includes('write:actors')) {
    document.getElementById('addActorButton').remove();
  }

  // hide add movie button if no permissions
  if (!localStorage.getItem('permissions').includes('write:movies')) {
    document.getElementById('addMovieButton').remove();
  }

  // hide edit actor button if no permissions
  if (!localStorage.getItem('permissions').includes('update:actors')) {
    document.querySelectorAll('.editActorButton').forEach(e => e.remove());
  }

  // hide edit movie button if no permissions
  if (!localStorage.getItem('permissions').includes('update:movies')) {
    document.querySelectorAll('.editMovieButton').forEach(e => e.remove());
  }

  // hide delete actor button if no permissions
  if (!localStorage.getItem('permissions').includes('delete:actors')) {
    document.querySelectorAll('.deleteActorButton').forEach(e => e.remove());
  }

  // hide delete movie button if no permissions
  if (!localStorage.getItem('permissions').includes('delete:movies')) {
    document.querySelectorAll('.deleteMovieButton').forEach(e => e.remove());
  }
} else {
  document.querySelectorAll('.card-footer').forEach(e => e.remove());
  document.getElementById('addActorButton').remove();
  document.getElementById('addMovieButton').remove();
  document.getElementById('logoutButton').remove();
  document.getElementById('movieLink').remove();
  document.getElementById('actorLink').remove();
  if (window.location.pathname !== '/') {
    window.location.replace('/')
  }
}

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
    headers: new Headers({
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    }),
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

// delete actor
const deleteActor = async (actorId) => {
  try {
    const data = await sendData(`/actors/${actorId}`, '', "DELETE");
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

// logout
const logOut = () => {
  localStorage.clear()
  window.location.href = 'https://dev-wsb8jitr.auth0.com/v2/logout'
};