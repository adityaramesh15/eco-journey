// NAVIGATION BUTTONS

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
    try {
        // Encode user input
        const response = await fetch(`/check?city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}`);
        
        // If server returns an error
        if (!response.ok) {
            console.error(`Server error: ${response.status}`);
            return false;
        }
        
        // Parse JSON response
        const data = await response.json();
        
        // Expected response shape: { "exists": true } or { "exists": false }
        if (typeof data.exists === "boolean") {
            return data.exists;
        }
  
        // In case backend returns something unexpected
        console.error("Unexpected response format:", data);
        return false;

    } catch (error) {
        console.error("Network or parsing error:", error);
        return false;
    }

    // Non-Backend Testing
    // if (city == "Fake City") {
    //     return false
    // }
    // if (city == "Real City") {
    //     return true
    // }
    // return true;
}

// TRIP COUNT FUNCTION

async function get_trip_count(user_id) {
	try {
		const response = await fetch(`/users/${user_id}/trips/count`);

		if (!response.ok) {
			console.error(`Failed to fetch trip count: ${response.status}`);
			return null;
		}

		const data = await response.json();
		if (typeof data.count === "number") {
			return data.count;
		} else {
			console.error("Unexpected response format:", data);
			return null;
		}
	} catch (error) {
		console.error("Error fetching trip count:", error);
		return null;
	}
}

// TRIP RANK FUNCTION

async function get_trip_rank(input_json) {
	try {
		const response = await fetch("/trips/rank", {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(input_json)
		});

		if (!response.ok) {
			console.error(`Failed to fetch trip rank: ${response.status}`);
			return null;
		}

		const data = await response.json();
		console.log("Trip rank response:", data);
		return data;
	} catch (error) {
		console.error("Error fetching trip rank:", error);
		return null;
	}
}

// RESET PAGE HELPER FUNCTIONS

function clear_messages() {
    const error_box = document.getElementById("error_messages");
    error_box.style.display = "none";
    error_box.innerHTML = "";
    const warning_box = document.getElementById("warning_messages");
    warning_box.style.display = "none";
    warning_box.innerHTML = "";
}

function clear_ranks() {
    const r1 = document.getElementById("rank1");
    const r2 = document.getElementById("rank2");
    const r3 = document.getElementById("rank3");
    r1.textContent = "Rank 1:";
    r2.textContent = "Rank 2:";
    r3.textContent = "Rank 3:";
}

function clear_form_inputs() {
	const form = document.getElementById("trip_form");
	if (form) form.reset();
}

function clear_success_message() {
    const success_box = document.getElementById("success_message");
    success_box.style.display = "none";
	success_box.textContent = "";
}

// TRIP FORM PROCESSOR AND GENERATOR FUNCTION

const trip_form_wrap = document.getElementById("trip_form");
if (trip_form_wrap) {
    trip_form_wrap.addEventListener("submit", async (event) => {
    event.preventDefault(); // prevent page reload

    // Clear Previous Messages and Ranks
    clear_messages();
    clear_ranks();
    clear_success_message();

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
    let errors = [];
    const error_box = document.getElementById("error_messages");

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
        error_box.style.display = "block";
        const header = document.createElement("p");
        header.textContent = "ERROR(S) FOUND:";
        header.style.fontWeight = "bold";
        error_box.appendChild(header);
  
        errors.forEach(msg => {
            const p = document.createElement("p");
            p.textContent = msg;
            error_box.appendChild(p);
        });
  
        const footer = document.createElement("p");
        footer.textContent = "Please fix the error(s) and resubmit";
        error_box.appendChild(footer);
  
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
    // current_user_id
    const userId = sessionStorage.getItem("current_user_id");
    const trip_input_data = {
        user_id: userId,
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
    // const trip_output_data = {
    //     rank_1_location: {
    //         city: "Chicago",
    //         state: "IL",
    //         bad_days: true,
    //         rainy_days: true
    //     },
    //     rank_2_location: {
    //         city: "Denver",
    //         state: "CO",
    //         bad_days: true,
    //         rainy_days: true
    //     },
    //     rank_3_location: {
    //         city: "Miami",
    //         state: "FL",
    //         bad_days: true,
    //         rainy_days: true
    //     }
    // };

    const trip_output_data = await get_trip_rank(trip_input_data);

    // Generate the Trip

    // Update Rank Elements
    const r1 = document.getElementById("rank1");
    const r2 = document.getElementById("rank2");
    const r3 = document.getElementById("rank3");
    r1.textContent = `Rank 1: ${trip_output_data.rank_1_location.city}, 
    ${trip_output_data.rank_1_location.state}`;
	r2.textContent = `Rank 2: ${trip_output_data.rank_2_location.city}, 
    ${trip_output_data.rank_2_location.state}`;
	r3.textContent = `Rank 3: ${trip_output_data.rank_3_location.city}, 
    ${trip_output_data.rank_3_location.state}`;

    // Update Checkbox and Trip Count Warnings
    let warnings = [];
    const warning_box = document.getElementById("warning_messages");

    // Get Trip Count
    // const trip_count = 4;
    const trip_count = await get_trip_count(userId);

    if (trip_count >= 5) {
        warnings.push("WARNING you've reached your 5 trip limit, saving this trip will replace your oldest trip");
    }

    let bad_day_locations = [];
    for (const [key, location] of Object.entries(trip_output_data)) {
        if (location.bad_days === true) {
            bad_day_locations.push(`${location.city}, ${location.state}`);
        }
    }
    if (bad_day_locations.length > 0) {
        warnings.push(`WARNING these locations contain bad days: ${bad_day_locations.join("; ")}`);
    }

    let rainy_day_locations = [];
    for (const [key, location] of Object.entries(trip_output_data)) {
        if (location.rainy_days === true) {
            rainy_day_locations.push(`${location.city}, ${location.state}`);
        }
    }
    if (rainy_day_locations.length > 0) {
        warnings.push(`WARNING these locations contain rainy days: ${rainy_day_locations.join("; ")}`);
    }

    if (warnings.length > 0) {
        warning_box.style.display = "block";

        const header = document.createElement("p");
        header.textContent = "WARNINGS:";
        header.style.fontWeight = "bold";
        warning_box.appendChild(header);

        warnings.forEach((msg) => {
            const p = document.createElement("p");
            p.textContent = msg;
            warning_box.appendChild(p);
        });

        const footer = document.createElement("p");
        footer.textContent = "Please consider these warnings before saving your trip";
        warning_box.appendChild(footer);
    }
    
    // Save JSON Data to Memory - so it can be used by save function
    sessionStorage.setItem("current_trip_input_data", JSON.stringify(trip_input_data));
    sessionStorage.setItem("current_trip_output_data", JSON.stringify(trip_output_data));
    });
}

// CONFIRM TRIP BUTTON
const save_button_wrap = document.getElementById("confirm_button");
if (save_button_wrap) {
	save_button_wrap.addEventListener("click", async () => {
        // Retrieve stored trip data
		const stored_input = sessionStorage.getItem("current_trip_input_data");
		const stored_output = sessionStorage.getItem("current_trip_output_data");

        // Parse and format JSON
		const trip_input_data = JSON.parse(stored_input);
		const trip_output_data = JSON.parse(stored_output);

        const formatted_trip_json = {
            user_id: trip_data.user_id,
            trip_name: trip_data.trip_name,
            date_range: {
                start_month: trip_data.date_range.start_month,
                start_day: trip_data.date_range.start_day,
                end_month: trip_data.date_range.end_month,
                end_day: trip_data.date_range.end_day
            },
            preferences: {
                temp: trip_data.preferences.temp,
                precp: trip_data.preferences.precp
            },
            locations: [
                { city: trip_data.locations[0].city, state: trip_data.locations[0].state },
                { city: trip_data.locations[1].city, state: trip_data.locations[1].state },
                { city: trip_data.locations[2].city, state: trip_data.locations[2].state }
            ]
        };

        // Generate Success Message
        const success_box = document.getElementById("success_message");
        success_box.style.display = "block";
        success_box.textContent = "Trip confirmed successfully";

        // Clear the page
        clear_messages();
        clear_ranks();
        clear_form_inputs();
        sessionStorage.removeItem("current_trip_data");
    });
}

// DISCARD TRIP BUTTON
const discard_button_wrap = document.getElementById("discard_button");
if (discard_button_wrap) {
    discard_button_wrap.addEventListener("click", () => {
        // Generate Success Message
        const success_box = document.getElementById("success_message");
        success_box.style.display = "block";
        success_box.textContent = "Trip discarded successfully";
        // Clear the page
        clear_messages();
        clear_ranks();
        clear_form_inputs();
        sessionStorage.removeItem("current_trip_data");
    });
}