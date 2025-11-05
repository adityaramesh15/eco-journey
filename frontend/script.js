const create_button_wrap = document.getElementById("create_button");
if (create_button_wrap) {
    create_button_wrap.addEventListener("click", () => 
    {window.location.href="create.html";} );
}

const load_button_wrap = document.getElementById("load_button");
if (load_button_wrap) {
    load_button_wrap.addEventListener("click", () => 
    {window.location.href="load.html";} );
}

const logout_button_wrap = document.getElementById("logout_button");
if (logout_button_wrap){
    logout_button_wrap.addEventListener("click", () => 
    {window.location.href="login.html";} );
}

const home_button_wrap = document.getElementById("home_button");
if (home_button_wrap) {
    home_button_wrap.addEventListener("click", () => {
    window.location.href = "home.html";
  });
}