/* =========================================================
   VOYAGE AI — AI TRAVEL AGENT
   Frontend Application
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    initializeNumberControls();
    initializeInterestSelection();
    initializeQuickDestinations();
    initializePlanner();
});


/* =========================================================
   NUMBER CONTROLS
   ========================================================= */

function initializeNumberControls() {
    const buttons = document.querySelectorAll(".number-btn");

    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            const targetId = button.dataset.target;
            const action = button.dataset.action;
            const input = document.getElementById(targetId);

            if (!input) return;

            let value = parseInt(input.value, 10);

            if (Number.isNaN(value)) {
                value = 1;
            }

            const min = parseInt(input.min, 10) || 1;
            const max = parseInt(input.max, 10) || 100;

            if (action === "plus") {
                value += 1;
            }

            if (action === "minus") {
                value -= 1;
            }

            value = Math.max(min, Math.min(max, value));

            input.value = value;
        });
    });
}


/* =========================================================
   INTEREST SELECTION
   ========================================================= */

function initializeInterestSelection() {
    const chips = document.querySelectorAll(".interest-chip");
    const hiddenInput = document.getElementById("interests");

    if (!chips.length || !hiddenInput) return;

    chips.forEach((chip) => {
        chip.addEventListener("click", () => {
            chip.classList.toggle("selected");

            const selected = Array.from(
                document.querySelectorAll(".interest-chip.selected")
            ).map((item) => item.dataset.interest);

            hiddenInput.value = selected.join(", ");
        });
    });
}


/* =========================================================
   QUICK DESTINATIONS
   ========================================================= */

function initializeQuickDestinations() {
    const buttons = document.querySelectorAll(
        ".quick-destination-btn"
    );

    const destination = document.getElementById("destination");

    if (!buttons.length || !destination) return;

    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            destination.value =
                button.dataset.destination || "";

            destination.focus();

            destination.style.borderColor =
                "rgba(217,183,108,0.5)";

            setTimeout(() => {
                destination.style.borderColor = "";
            }, 1000);
        });
    });
}


/* =========================================================
   PLANNER
   ========================================================= */

function initializePlanner() {
    const form = document.getElementById("plannerForm");

    if (!form) return;

    const loading = document.getElementById("loading");
    const result = document.getElementById("result");
    const button = document.getElementById("generateBtn");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        await generateTrip();
    });


    async function generateTrip() {

        const originalButton = button
            ? button.innerHTML
            : "Generate Trip";

        try {

            /* -----------------------------------------
               SHOW LOADING
               ----------------------------------------- */

            if (loading) {
                loading.classList.remove("hidden");
            }

            if (result) {
                result.classList.add("hidden");
            }

            if (button) {

                button.disabled = true;

                button.innerHTML = `
                    <span class="generate-icon">
                        <span class="loading-spinner"></span>
                    </span>

                    <span>
                        <strong>AI is planning...</strong>
                        <small>Creating your journey</small>
                    </span>
                `;
            }


            /* -----------------------------------------
               COLLECT FORM DATA
               ----------------------------------------- */

            const formData = new FormData(form);

            const data = Object.fromEntries(
                formData.entries()
            );

            data.destination =
                String(data.destination || "").trim();

            data.origin =
                String(data.origin || "").trim();

            data.interests =
                String(data.interests || "").trim();

            data.hotel_style =
                String(
                    data.hotel_style || "Budget"
                ).trim();

            data.notes =
                String(data.notes || "").trim();

            data.days =
                parseInt(data.days, 10) || 1;

            data.travelers =
                parseInt(data.travelers, 10) || 1;

            data.budget =
                parseInt(data.budget, 10) || 0;


            /* -----------------------------------------
               VALIDATION
               ----------------------------------------- */

            if (!data.destination) {
                throw new Error(
                    "Please enter a destination."
                );
            }

            if (data.days < 1) {
                throw new Error(
                    "Trip duration must be at least 1 day."
                );
            }

            if (data.travelers < 1) {
                throw new Error(
                    "At least one traveler is required."
                );
            }

            if (data.budget < 0) {
                throw new Error(
                    "Budget cannot be negative."
                );
            }


            /* -----------------------------------------
               AI THINKING
               ----------------------------------------- */

            await simulateAIThinking();


            /* -----------------------------------------
               API REQUEST
               ----------------------------------------- */

            const csrfToken = getCSRFToken();

            const headers = {
                "Content-Type": "application/json"
            };

            if (csrfToken) {
                headers["X-CSRFToken"] = csrfToken;
            }

            const response = await fetch(
                "/api/plan/",
                {
                    method: "POST",
                    headers: headers,
                    body: JSON.stringify(data)
                }
            );


            /* -----------------------------------------
               RESPONSE
               ----------------------------------------- */

            let responseData;

            try {
                responseData = await response.json();
            } catch (error) {
                throw new Error(
                    "The server returned an invalid response."
                );
            }


            if (!response.ok) {

                throw new Error(
                    responseData.error ||
                    "Unable to generate your trip."
                );
            }


            if (!responseData.success) {

                throw new Error(
                    responseData.error ||
                    "The AI could not create your trip."
                );
            }


            /* -----------------------------------------
               DISPLAY RESULT
               ----------------------------------------- */

            renderTripResult(responseData);

            if (result) {

                result.classList.remove("hidden");

                setTimeout(() => {

                    result.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

                }, 150);
            }

        } catch (error) {

            console.error(
                "Voyage AI Error:",
                error
            );

            renderError(
                error.message
            );

            if (result) {
                result.classList.remove("hidden");
            }

        } finally {

            if (loading) {
                loading.classList.add("hidden");
            }

            if (button) {

                button.disabled = false;

                button.innerHTML =
                    originalButton;
            }
        }
    }
}


/* =========================================================
   AI THINKING ANIMATION
   ========================================================= */

async function simulateAIThinking() {

    const steps =
        document.querySelectorAll(
            ".loading-step"
        );

    if (!steps.length) {

        await delay(500);

        return;
    }

    steps.forEach((step) => {

        step.classList.remove(
            "active",
            "completed"
        );

    });


    for (
        let i = 0;
        i < steps.length;
        i++
    ) {

        const current =
            steps[i];

        current.classList.add(
            "active"
        );

        await delay(550);

        current.classList.remove(
            "active"
        );

        current.classList.add(
            "completed"
        );
    }
}


/* =========================================================
   RENDER COMPLETE TRIP
   ========================================================= */

function renderTripResult(data) {

    const result =
        document.getElementById("result");

    if (!result) return;


    /* =====================================================
       BASIC TRIP DATA
       ===================================================== */

    const itinerary =
        Array.isArray(data.itinerary)
            ? data.itinerary
            : [];


    const destination =
        String(
            data.destination ||
            "Your Trip"
        );


    const travelers =
        Number(
            data.travelers || 1
        );


    const days =
        Number(
            data.days ||
            itinerary.length ||
            1
        );


    const userBudget =
        normalizeNumber(
            data.budget
        );


    /* =====================================================
       ESTIMATED TOTAL COST
       ===================================================== */

    let estimatedCost =
        normalizeNumber(
            data.estimated_total_cost
        );


    /*
     * First fallback:
     * Calculate from itinerary.
     */

    if (
        estimatedCost <= 0 &&
        itinerary.length > 0
    ) {

        estimatedCost =
            itinerary.reduce(
                (total, day) => {

                    return (
                        total +
                        normalizeNumber(
                            day.estimated_cost
                        )
                    );

                },
                0
            );
    }


    /*
     * IMPORTANT:
     *
     * Do not automatically display the user's
     * entire budget as the trip cost.
     *
     * If the AI returned no cost at all,
     * we will calculate a reasonable estimate
     * from the user's budget only as a final
     * frontend fallback.
     */

    if (
        estimatedCost <= 0 &&
        userBudget > 0
    ) {

        estimatedCost =
            calculateFallbackTripCost(
                userBudget,
                days,
                travelers
            );
    }


    /* =====================================================
       BUDGET ANALYSIS
       ===================================================== */

    const rawBudget =
        data.budget_analysis || {};


    let accommodation =
        normalizeNumber(
            rawBudget.accommodation
        );


    let transportation =
        normalizeNumber(
            rawBudget.transportation
        );


    let food =
        normalizeNumber(
            rawBudget.food
        );


    let activities =
        normalizeNumber(
            rawBudget.activities
        );


    let miscellaneous =
        normalizeNumber(
            rawBudget.miscellaneous
        );


    let breakdownTotal =
        accommodation +
        transportation +
        food +
        activities +
        miscellaneous;


    /* =====================================================
       FALLBACK BUDGET BREAKDOWN
       ===================================================== */

    /*
     * If backend/AI returns all categories as 0,
     * create a useful breakdown.
     */

    if (
        breakdownTotal <= 0 &&
        estimatedCost > 0
    ) {

        const breakdown =
            calculateBudgetBreakdown(
                estimatedCost
            );

        accommodation =
            breakdown.accommodation;

        transportation =
            breakdown.transportation;

        food =
            breakdown.food;

        activities =
            breakdown.activities;

        miscellaneous =
            breakdown.miscellaneous;

        breakdownTotal =
            estimatedCost;
    }


    /*
     * If breakdown exists but its total is
     * different from estimated cost, we keep
     * the actual AI values instead of changing
     * them.
     */


    /* =====================================================
       BUDGET PERCENTAGE
       ===================================================== */

    let budgetPercentage = 0;

    if (userBudget > 0) {

        budgetPercentage =
            Math.round(
                (
                    estimatedCost /
                    userBudget
                ) * 100
            );

        budgetPercentage =
            Math.max(
                0,
                Math.min(
                    100,
                    budgetPercentage
                )
            );
    }


    /* =====================================================
       BUDGET STATUS
       ===================================================== */

    let budgetStatus =
        "No budget limit";

    if (userBudget > 0) {

        if (
            estimatedCost >
            userBudget
        ) {

            budgetStatus =
                "Over budget";

        } else {

            budgetStatus =
                "Within budget";
        }
    }


    /* =====================================================
       TIPS
       ===================================================== */

    const tips =
        Array.isArray(data.tips)
            ? data.tips
            : [];


    /* =====================================================
       PACKING
       ===================================================== */

    const packingList =
        Array.isArray(data.packing_list)
            ? data.packing_list
            : [];


    /* =====================================================
       RENDER
       ===================================================== */

    result.innerHTML = `

        <div class="result-dashboard">


            <!-- =========================================
                 MAIN RESULT
            ========================================== -->

            <main class="result-main">


                <div class="result-header">

                    <div>

                        <span class="mini-label">
                            ✦ AI-GENERATED JOURNEY
                        </span>

                        <h2>
                            ${escapeHTML(
                                destination
                            )}
                        </h2>

                        <p>
                            ${escapeHTML(
                                data.summary ||
                                "Your personalized itinerary is ready."
                            )}
                        </p>

                    </div>


                    <div class="cost-pill">

                        ₹${formatCurrency(
                            estimatedCost
                        )}

                    </div>

                </div>


                <!-- TRIP OVERVIEW -->

                <div class="trip-overview">


                    <div class="overview-item">

                        <span>
                            TRAVELERS
                        </span>

                        <strong>
                            ${travelers}
                        </strong>

                    </div>


                    <div class="overview-item">

                        <span>
                            DURATION
                        </span>

                        <strong>
                            ${days} Days
                        </strong>

                    </div>


                    <div class="overview-item">

                        <span>
                            YOUR BUDGET
                        </span>

                        <strong>
                            ₹${formatCurrency(
                                userBudget
                            )}
                        </strong>

                    </div>


                    <div class="overview-item">

                        <span>
                            TRIP ID
                        </span>

                        <strong>
                            #${escapeHTML(
                                data.trip_id || "—"
                            )}
                        </strong>

                    </div>

                </div>


                <!-- ITINERARY -->

                <div class="itinerary-heading">

                    <span class="mini-label">
                        ✦ YOUR ITINERARY
                    </span>

                    <h3>
                        Day-by-Day Adventure
                    </h3>

                </div>


                ${
                    itinerary.length > 0
                        ? itinerary
                            .map((day) =>
                                createDayCard(day)
                            )
                            .join("")
                        : createEmptyItinerary()
                }


                <!-- TIPS -->

                ${createTipsSection(tips)}


                <!-- PACKING -->

                ${createPackingSection(
                    packingList
                )}

            </main>


            <!-- =========================================
                 SIDEBAR
            ========================================== -->

            <aside class="result-sidebar">


                <!-- ESTIMATED COST -->

                <div class="result-stat">

                    <span>
                        ESTIMATED TRIP COST
                    </span>

                    <strong class="big-cost">

                        ₹${formatCurrency(
                            estimatedCost
                        )}

                    </strong>

                </div>


                <!-- BUDGET -->

                <div class="result-stat">

                    <span>
                        AI BUDGET ANALYSIS
                    </span>


                    <div class="budget-breakdown">


                        <div class="budget-row">

                            <span>
                                🏨 Accommodation
                            </span>

                            <strong>
                                ₹${formatCurrency(
                                    accommodation
                                )}
                            </strong>

                        </div>


                        <div class="budget-row">

                            <span>
                                🚗 Transportation
                            </span>

                            <strong>
                                ₹${formatCurrency(
                                    transportation
                                )}
                            </strong>

                        </div>


                        <div class="budget-row">

                            <span>
                                🍴 Food
                            </span>

                            <strong>
                                ₹${formatCurrency(
                                    food
                                )}
                            </strong>

                        </div>


                        <div class="budget-row">

                            <span>
                                🎯 Activities
                            </span>

                            <strong>
                                ₹${formatCurrency(
                                    activities
                                )}
                            </strong>

                        </div>


                        <div class="budget-row">

                            <span>
                                ✦ Miscellaneous
                            </span>

                            <strong>
                                ₹${formatCurrency(
                                    miscellaneous
                                )}
                            </strong>

                        </div>

                    </div>


                    <!-- PROGRESS -->

                    ${
                        userBudget > 0
                            ? `

                                <div
                                    class="budget-progress-wrapper"
                                >

                                    <div
                                        class="budget-progress-label"
                                    >

                                        <span>
                                            Budget used
                                        </span>

                                        <strong>
                                            ${budgetPercentage}%
                                        </strong>

                                    </div>


                                    <div
                                        class="budget-progress"
                                    >

                                        <span
                                            style="
                                                width:${budgetPercentage}%;
                                            "
                                        ></span>

                                    </div>


                                    <small
                                        style="
                                            display:block;
                                            margin-top:8px;
                                            opacity:.7;
                                        "
                                    >
                                        ${budgetStatus}
                                    </small>

                                </div>

                            `
                            : ""
                    }

                </div>


                <!-- AI STATUS -->

                <div class="result-stat">

                    <span>
                        AI STATUS
                    </span>

                    <strong
                        style="
                            color:var(--success);
                            font-size:14px;
                        "
                    >
                        ✓ Plan optimized
                    </strong>

                </div>


                <!-- PLAN AGAIN -->

                <button
                    class="primary-btn"
                    style="
                        width:100%;
                        border:none;
                    "
                    onclick="
                        window.scrollTo({
                            top:0,
                            behavior:'smooth'
                        })
                    "
                >

                    ✦ Plan Another Trip

                </button>

            </aside>

        </div>
    `;
}


/* =========================================================
   DAY CARD
   ========================================================= */

function createDayCard(day) {

    const dayNumber =
        day.day_number ||
        day.day ||
        1;


    const estimatedCost =
        normalizeNumber(
            day.estimated_cost
        );


    return `

        <article class="itinerary-day">


            <div class="day-card-top">

                <span class="day-label">

                    DAY ${String(
                        dayNumber
                    ).padStart(2, "0")}

                </span>


                <span class="day-cost">

                    ₹${formatCurrency(
                        estimatedCost
                    )}

                </span>

            </div>


            <h3>
                ${escapeHTML(
                    day.title ||
                    "Your adventure"
                )}
            </h3>


            <div class="timeline-item">

                <strong>
                    ☀ MORNING
                </strong>

                <p>
                    ${escapeHTML(
                        day.morning ||
                        "Explore the destination."
                    )}
                </p>

            </div>


            <div class="timeline-item">

                <strong>
                    ◐ AFTERNOON
                </strong>

                <p>
                    ${escapeHTML(
                        day.afternoon ||
                        "Enjoy local activities."
                    )}
                </p>

            </div>


            <div class="timeline-item">

                <strong>
                    ☾ EVENING
                </strong>

                <p>
                    ${escapeHTML(
                        day.evening ||
                        "Relax and enjoy the evening."
                    )}
                </p>

            </div>


            <div class="cost-line">

                Estimated day cost:

                <strong>
                    ₹${formatCurrency(
                        estimatedCost
                    )}
                </strong>

            </div>

        </article>
    `;
}


/* =========================================================
   BUDGET BREAKDOWN HELPER
   ========================================================= */

function calculateBudgetBreakdown(total) {

    total =
        Math.max(
            0,
            Math.round(
                Number(total) || 0
            )
        );


    const accommodation =
        Math.round(total * 0.30);

    const transportation =
        Math.round(total * 0.20);

    const food =
        Math.round(total * 0.20);

    const activities =
        Math.round(total * 0.15);

    const miscellaneous =
        total -
        accommodation -
        transportation -
        food -
        activities;


    return {
        accommodation,
        transportation,
        food,
        activities,
        miscellaneous
    };
}


/* =========================================================
   FALLBACK TOTAL COST
   ========================================================= */

function calculateFallbackTripCost(
    userBudget,
    days,
    travelers
) {

    /*
     * Use the user's budget as the maximum planning
     * target, but don't blindly display it as an
     * exact AI cost.
     *
     * This gives a reasonable estimated value.
     */

    const budget =
        Number(userBudget) || 0;


    if (budget <= 0) {
        return 0;
    }


    /*
     * The backend should normally provide
     * estimated_total_cost.
     *
     * This fallback is only for missing AI data.
     */

    return Math.round(
        budget * 0.90
    );
}


/* =========================================================
   TIPS
   ========================================================= */

function createTipsSection(tips) {

    if (!Array.isArray(tips) || !tips.length) {
        return "";
    }


    return `

        <section class="ai-extra-section">

            <div class="section-heading">

                <span class="mini-label">
                    ✦ AI INSIGHTS
                </span>

                <h3>
                    Smart Travel Tips
                </h3>

            </div>


            <div class="tips-grid">

                ${tips.map(
                    (tip) => `

                        <div class="tip-card">

                            <span class="tip-icon">
                                ✦
                            </span>

                            <p>
                                ${escapeHTML(
                                    tip
                                )}
                            </p>

                        </div>

                    `
                ).join("")}

            </div>

        </section>
    `;
}


/* =========================================================
   PACKING LIST
   ========================================================= */

function createPackingSection(items) {

    if (
        !Array.isArray(items) ||
        !items.length
    ) {
        return "";
    }


    return `

        <section class="ai-extra-section">

            <div class="section-heading">

                <span class="mini-label">
                    ✦ SMART PACKING
                </span>

                <h3>
                    What to Pack
                </h3>

            </div>


            <div class="packing-grid">

                ${items.map(
                    (item) => `

                        <div class="packing-item">

                            <span>
                                ✓
                            </span>

                            <p>
                                ${escapeHTML(
                                    item
                                )}
                            </p>

                        </div>

                    `
                ).join("")}

            </div>

        </section>
    `;
}


/* =========================================================
   EMPTY ITINERARY
   ========================================================= */

function createEmptyItinerary() {

    return `

        <div class="empty-state">

            <h3>
                No itinerary was returned.
            </h3>

            <p>
                Try generating the trip again.
            </p>

        </div>
    `;
}


/* =========================================================
   ERROR
   ========================================================= */

function renderError(message) {

    const result =
        document.getElementById(
            "result"
        );

    if (!result) return;


    result.innerHTML = `

        <div class="result-main">

            <div class="result-header">

                <div>

                    <span class="mini-label">
                        VOYAGE AI
                    </span>

                    <h2>
                        We couldn't build your trip
                    </h2>

                    <p>
                        ${escapeHTML(
                            message ||
                            "Please try again."
                        )}
                    </p>

                </div>


                <div class="cost-pill">
                    !
                </div>

            </div>


            <div class="error-help">

                <p>
                    Check your trip details
                    and try again.
                </p>

            </div>

        </div>
    `;
}


/* =========================================================
   FORM VALUE HELPER
   ========================================================= */

function getFormValue(
    id,
    fallback = ""
) {

    const element =
        document.getElementById(id);

    if (!element) {
        return fallback;
    }

    return element.value || fallback;
}


/* =========================================================
   NUMBER NORMALIZER
   ========================================================= */

function normalizeNumber(value) {

    /*
     * Handles:
     *
     * 5000
     * "5000"
     * "₹5,000"
     * "5,000"
     * null
     * undefined
     */

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return 0;
    }


    if (typeof value === "number") {

        return Number.isFinite(value)
            ? Math.max(0, Math.round(value))
            : 0;
    }


    const cleaned =
        String(value)
            .replace(/[₹,\s]/g, "")
            .replace(/[^\d.-]/g, "");


    const number =
        Number(cleaned);


    if (!Number.isFinite(number)) {
        return 0;
    }


    return Math.max(
        0,
        Math.round(number)
    );
}


/* =========================================================
   CURRENCY
   ========================================================= */

function formatCurrency(value) {

    return normalizeNumber(
        value
    ).toLocaleString(
        "en-IN"
    );
}


/* =========================================================
   CSRF
   ========================================================= */

function getCSRFToken() {

    const cookie =
        document.cookie
            .split("; ")
            .find(
                row =>
                    row.startsWith(
                        "csrftoken="
                    )
            );


    if (cookie) {

        return decodeURIComponent(
            cookie.split("=")[1]
        );
    }


    const input =
        document.querySelector(
            "[name=csrfmiddlewaretoken]"
        );


    return input
        ? input.value
        : "";
}


/* =========================================================
   HTML ESCAPE
   ========================================================= */

function escapeHTML(value) {

    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,
        (character) => {

            const entities = {

                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                '"': "&quot;",
                "'": "&#039;"

            };

            return entities[
                character
            ];
        }
    );
}


/* =========================================================
   DELAY
   ========================================================= */

function delay(milliseconds) {

    return new Promise(
        (resolve) =>
            setTimeout(
                resolve,
                milliseconds
            )
    );
}