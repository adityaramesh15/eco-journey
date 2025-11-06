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

function pref_to_int(value) {
    switch (value.toLowerCase()) {
      case "low": return 0;
      case "medium": return 1;
      case "high": return 2;
      default: return null;
    }
}

const trip_form_wrap = document.getElementById("trip_form");
if (trip_form_wrap) {
    trip_form_wrap.addEventListener("submit", () => {
  
    // Location Data Processing
    const city1 = document.querySelector("[name='city1']").value.trim();
    const state1 = document.querySelector("[name='state1']").value.trim();
    const city2 = document.querySelector("[name='city2']").value.trim();
    const state2 = document.querySelector("[name='state2']").value.trim();
    const city3 = document.querySelector("[name='city3']").value.trim();
    const state3 = document.querySelector("[name='state3']").value.trim();
  
    // Preferance Data Processing
    const tempPref = document.getElementById("temperature_pref").value;
    const precipPref = document.getElementById("precipitation_pref").value;
  
    // Date Data Processing
    const startMonth = parseInt(document.getElementById("start_month").value);
    const startDay = parseInt(document.getElementById("start_day").value);
    const endMonth = parseInt(document.getElementById("end_month").value);
    const endDay = parseInt(document.getElementById("end_day").value);
  
    // Checkbox Data Processing
    const checkBadDays = document.getElementById("check_bad_days").checked;
    const checkRainyDays = document.getElementById("check_rainy_days").checked;
  
    // Construct Input JSON Object
    const tripData = {
        user_id: 1, // PLACEHOLDER - FIGURE OUT USERS LATER
        trip_name: "My Trip", // PLACEHOLDER - ADD NAME INPUT BEFORE SAVE
        precipitation: pref_to_int(precipPref),
        temperature: pref_to_int(tempPref),
        location_1: { city: city1, state: state1 },
        location_2: { city: city2, state: state2 },
        location_3: { city: city3, state: state3 },
        date_start: { month: startMonth, day: startDay },
        date_end: { month: endMonth, day: endDay },
        // date_range - replace with
        check_bad_days: checkBadDays,
        check_rainy_days: checkRainyDays
    };

    // Generate Output JSON Object

    // TEST JSON OUTPUT - to check for proper trip generation:

    // Generate the Trip

    // Update Rank Elements

    // Update Checkbox and Trip Count Warnings

    });
}

// TODO: SAVE FUNCTION
const save_button_wrap = 0
// TODO: RESET/DELETE FUNCTION
const discard_button_wrap = 0