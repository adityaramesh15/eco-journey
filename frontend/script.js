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

// INPUT VALIDATION FUNCTIONS

const days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

function within_seven_days(start_day, start_month, end_day, end_month) {
    // Convert both dates to (1–365)
    const start = days_per_month.slice(0, start_month - 1).reduce((a, b) => a + b, 0) + start_day;
    const end = days_per_month.slice(0, end_month - 1).reduce((a, b) => a + b, 0) + end_day;
  
    // Compute forward difference (allow wrapping across years)
    let diff = end - start;
    if (diff < 0) {
      diff += 365;
    }
  
    // Return true if range is <= 7 days
    return diff <= 7;
}

function is_valid_date(month, day) {
    // Check that day is within valid range for that month
    return day <= days_per_month[month - 1];
}

function has_duplicate_locations(loc1, loc2, loc3) {
    // Normalize and combine all locations into an array
    const locations = [loc1, loc2, loc3].map(loc => ({
      city: loc.city.trim().toLowerCase(),
      state: loc.state.trim().toLowerCase()
    }));

    const seen = new Set();
    for (const loc of locations) {
      const key = `${loc.city},${loc.state}`;
      if (seen.has(key)) {
        // found a duplicate
        return true;
      }
      seen.add(key);
    }
    
    // no duplicates found
    return false; 
}

async function check_city_exists(city, state) {
    // try {
    //     // Encode user input to make it URL-safe
    //     const response = await fetch(`/check?city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}`);
        
    //     // If server returns an error (e.g., 400)
    //     if (!response.ok) {
    //         console.error(`Server error: ${response.status}`);
    //         return false;
    //     }
        
    //     // Parse JSON response
    //     const data = await response.json();
        
    //     // Expected response shape: { "exists": true } or { "exists": false }
    //     if (typeof data.exists === "boolean") {
    //         return data.exists;
    //     }
  
    //     // In case backend returns something unexpected
    //     console.error("Unexpected response format:", data);
    //     return false;

    // } catch (error) {
    //     console.error("Network or parsing error:", error);
    //     return false;
    // }

    // Non-Backend Testing
    if (city == "Fake City") {
        return false
    }
    if (city == "Real City") {
        return true
    }
    return true;
}

const trip_form_wrap = document.getElementById("trip_form");
if (trip_form_wrap) {
    trip_form_wrap.addEventListener("submit", async (event) => {
    event.preventDefault(); // prevent page reload

    // Reset Previous Error Messages
    const errorBox = document.getElementById("error_messages");
    errorBox.style.display = "none";
    errorBox.innerHTML = "";
    let errors = [];

    // Location Data Processing
    const city1 = document.querySelector("[name='city1']").value.trim();
    const state1 = document.querySelector("[name='state1']").value.trim();
    const city2 = document.querySelector("[name='city2']").value.trim();
    const state2 = document.querySelector("[name='state2']").value.trim();
    const city3 = document.querySelector("[name='city3']").value.trim();
    const state3 = document.querySelector("[name='state3']").value.trim();
    const loc1 = { city: city1, state: state1 };
    const loc2 = { city: city2, state: state2 };
    const loc3 = { city: city3, state: state3 };
    
    // Date Data Processing
    const startMonth = parseInt(document.getElementById("start_month").value);
    const startDay = parseInt(document.getElementById("start_day").value);
    const endMonth = parseInt(document.getElementById("end_month").value);
    const endDay = parseInt(document.getElementById("end_day").value);
    
    // Location and Date Data Input Validation
    if (has_duplicate_locations(loc1, loc2, loc3)) {
        errors.push("ERROR duplicate locations aren't allowed");
    }

    const cityExistsResults = await Promise.all([
        check_city_exists(city1, state1),
        check_city_exists(city2, state2),
        check_city_exists(city3, state3)
    ]);
    
    let nonexistentCities = [];
    if (!cityExistsResults[0]) nonexistentCities.push(`${city1}, ${state1}`);
    if (!cityExistsResults[1]) nonexistentCities.push(`${city2}, ${state2}`);
    if (!cityExistsResults[2]) nonexistentCities.push(`${city3}, ${state3}`);

    if (nonexistentCities.length > 0) {
        errors.push(`ERROR these cities don't exist: ${nonexistentCities.join("; ")}`);
    }
    
    let invalidDates = [];
    if (!is_valid_date(startMonth, startDay)) invalidDates.push(`Start Date: ${startMonth}/${startDay}`);
    if (!is_valid_date(endMonth, endDay)) invalidDates.push(`End Date: ${endMonth}/${endDay}`);

    if (invalidDates.length > 0) {
        errors.push(`ERROR these dates don't exist: ${invalidDates.join("; ")}`);
    }

    if (!within_seven_days(startDay, startMonth, endDay, endMonth)) {
        errors.push("ERROR the date range is greater than 7");
    }
    
    if (errors.length > 0) {
        errorBox.style.display = "block";
        const header = document.createElement("p");
        header.textContent = "ERROR(S) FOUND:";
        header.style.fontWeight = "bold";
        errorBox.appendChild(header);
  
        errors.forEach(msg => {
            const p = document.createElement("p");
            p.textContent = msg;
            errorBox.appendChild(p);
        });
  
        const footer = document.createElement("p");
        footer.textContent = "Please fix the error(s) and resubmit";
        errorBox.appendChild(footer);
  
        return; // terminate function
    }
    // for testing error generation:
    // return;

    // Preferance Data Processing
    const tempPref = parseFloat(document.getElementById("temp_pref").value);
    const precipPref = document.getElementById("precip_pref").value;
    const precipInt = pref_to_int(precipPref);

    // Checkbox Data Processing
    const checkBadDays = document.getElementById("check_bad_days").checked;
    const checkRainyDays = document.getElementById("check_rainy_days").checked;
    
    // Trip Name Data Processing
    const tripName = document.getElementById("trip_name").value.trim();

    // Construct Input JSON Object
    const tripData = {
        user_id: 1, // FIGURE OUT USER_ID LATER
        trip_name: tripName,
        date_range: {
            start_month: startMonth,
            start_day: startDay,
            end_month: endMonth,
            end_day: endDay
        },
        preferences: {
            temp: tempPref,
            precp: precipInt
        },
        locations: [loc1, loc2, loc3],
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