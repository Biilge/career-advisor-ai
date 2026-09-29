// ==========================================
// CAREER PROFILE & RECOMMENDATIONS
// ==========================================

const careerForm =
    document.getElementById("careerForm");

const resultsSection =
    document.getElementById("results");

const recommendationList =
    document.getElementById("recommendationList");

const loading =
    document.getElementById("loading");


// ==========================================
// CAREER PROFILE SUBMIT
// ==========================================

careerForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        // ------------------------------------------
        // GET PROFILE DATA
        // ------------------------------------------

        const skills = document
            .getElementById("skills")
            .value
            .split(",")
            .map(skill => skill.trim())
            .filter(skill => skill.length > 0);


        const interests = document
            .getElementById("interests")
            .value
            .split(",")
            .map(interest => interest.trim())
            .filter(interest => interest.length > 0);


        const education = document
            .getElementById("education")
            .value
            .trim();


        const experienceLevel =
            document
                .getElementById("experience")
                .value;


        const preferredLocation =
            document
                .getElementById("location")
                .value
                .trim();


        // ------------------------------------------
        // CREATE PROFILE
        // ------------------------------------------

        const profile = {

            skills: skills,

            interests: interests,

            education: education,

            experience_level:
                experienceLevel,

            preferred_location:
                preferredLocation

        };


        // ------------------------------------------
        // UI STATE
        // ------------------------------------------

        loading.classList.remove(
            "hidden"
        );

        resultsSection.classList.add(
            "hidden"
        );

        recommendationList.innerHTML = "";


        // ------------------------------------------
        // SEND REQUEST
        // ------------------------------------------

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/recommend",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(profile)
                }
            );


            if (!response.ok) {

                throw new Error(
                    `Server returned ${response.status}`
                );

            }


            const data =
                await response.json();


            if (!data.success) {

                throw new Error(
                    "Career recommendation request failed."
                );

            }


            // ------------------------------------------
            // DISPLAY RESULTS
            // ------------------------------------------

            displayRecommendations(
                data.recommendations
            );


        } catch (error) {

            console.error(
                "Recommendation error:",
                error
            );


            recommendationList.innerHTML = `

                <div class="recommendation-card">

                    <div class="recommendation-number">
                        ERROR
                    </div>

                    <h3>
                        Unable to get recommendations
                    </h3>

                    <div class="recommendation-company">

                        Please make sure the backend is running
                        and try again.

                    </div>

                </div>

            `;


            resultsSection.classList.remove(
                "hidden"
            );


        } finally {

            loading.classList.add(
                "hidden"
            );

        }

    }
);


// ==========================================
// DISPLAY RECOMMENDATIONS
// ==========================================

function displayRecommendations(text) {


    const recommendations = text
        .split("\n\n")
        .filter(
            item =>
                item.trim().length > 0
        );


    recommendations.forEach(
        function (
            recommendation,
            index
        ) {


            const lines =
                recommendation
                    .split("\n")
                    .map(
                        line =>
                            line.trim()
                    )
                    .filter(
                        line =>
                            line.length > 0
                    );


            if (lines.length === 0) {
                return;
            }


            // ------------------------------------------
            // TITLE
            // ------------------------------------------

            const title =
                lines[0]
                    .replace(
                        /^\d+\.\s*/,
                        ""
                    )
                    .trim();


            let company = "";
            let category = "";
            let location = "";


            // ------------------------------------------
            // EXTRACT INFORMATION
            // ------------------------------------------

            lines.forEach(
                function (line) {


                    if (
                        line.startsWith(
                            "Company:"
                        )
                    ) {

                        company =
                            line
                                .replace(
                                    "Company:",
                                    ""
                                )
                                .trim();

                    }


                    if (
                        line.startsWith(
                            "Category:"
                        )
                    ) {

                        category =
                            line
                                .replace(
                                    "Category:",
                                    ""
                                )
                                .trim();

                    }


                    if (
                        line.startsWith(
                            "Location:"
                        )
                    ) {

                        location =
                            line
                                .replace(
                                    "Location:",
                                    ""
                                )
                                .trim();

                    }

                }
            );


            // ------------------------------------------
            // CREATE CARD
            // ------------------------------------------

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "recommendation-card";


            card.innerHTML = `

                <div class="recommendation-number">

                    ${String(index + 1)
                        .padStart(2, "0")}

                </div>


                <h3>

                    ${escapeHtml(title)}

                </h3>


                <div class="recommendation-company">

                    ${escapeHtml(company)}

                </div>


                <div class="recommendation-info">

                    <span class="info-tag">

                        ${escapeHtml(category)}

                    </span>


                    <span class="info-tag">

                        ${escapeHtml(location)}

                    </span>

                </div>

            `;


            recommendationList.appendChild(
                card
            );

        }
    );


    // ------------------------------------------
    // SHOW RESULTS
    // ------------------------------------------

    resultsSection.classList.remove(
        "hidden"
    );


    resultsSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}


// ==========================================
// CHATBOT
// ==========================================

const chatForm =
    document.getElementById(
        "chatForm"
    );


const chatInput =
    document.getElementById(
        "chatInput"
    );


const chatMessages =
    document.getElementById(
        "chatMessages"
    );


// ==========================================
// CHAT SUBMIT
// ==========================================

chatForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const message =
            chatInput.value.trim();


        if (!message) {
            return;
        }


        // ------------------------------------------
        // GET CURRENT PROFILE
        // ------------------------------------------

        const skills = document
            .getElementById("skills")
            .value
            .split(",")
            .map(skill => skill.trim())
            .filter(
                skill =>
                    skill.length > 0
            );


        const interests = document
            .getElementById("interests")
            .value
            .split(",")
            .map(interest => interest.trim())
            .filter(
                interest =>
                    interest.length > 0
            );


        const education =
            document
                .getElementById("education")
                .value
                .trim();


        const experienceLevel =
            document
                .getElementById("experience")
                .value;


        const preferredLocation =
            document
                .getElementById("location")
                .value
                .trim();


        // ------------------------------------------
        // CHECK PROFILE
        // ------------------------------------------

        if (

            skills.length === 0 ||

            interests.length === 0 ||

            !education ||

            !experienceLevel ||

            !preferredLocation

        ) {

            addChatMessage(
                "assistant",

                "Please complete your career profile before starting the conversation."
            );


            return;

        }


        // ------------------------------------------
        // ADD USER MESSAGE
        // ------------------------------------------

        addChatMessage(
            "user",
            message
        );


        chatInput.value = "";

        chatInput.disabled = true;


        // ------------------------------------------
        // THINKING MESSAGE
        // ------------------------------------------

        const loadingMessage =
            addChatMessage(
                "assistant",
                "Thinking..."
            );


        // ------------------------------------------
        // SEND REQUEST
        // ------------------------------------------

        try {

            const response =
                await fetch(
                    "http://127.0.0.1:8000/chat",
                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify({

                                skills:
                                    skills,

                                interests:
                                    interests,

                                education:
                                    education,

                                experience_level:
                                    experienceLevel,

                                preferred_location:
                                    preferredLocation,

                                message:
                                    message

                            })

                    }
                );


            if (!response.ok) {

                throw new Error(
                    `Server returned ${response.status}`
                );

            }


            const data =
                await response.json();


            if (!data.success) {

                throw new Error(
                    "Chat request failed."
                );

            }


            // ------------------------------------------
            // REMOVE THINKING
            // ------------------------------------------

            loadingMessage.remove();


            // ------------------------------------------
            // ADD AI RESPONSE
            // ------------------------------------------

            addChatMessage(
                "assistant",
                data.message
            );


        } catch (error) {

            console.error(
                "Chat error:",
                error
            );


            loadingMessage.remove();


            addChatMessage(
                "assistant",

                "I couldn't process your question. Please make sure the backend is running and try again."
            );


        } finally {

            chatInput.disabled = false;

            chatInput.focus();

        }

    }
);


// ==========================================
// ADD CHAT MESSAGE
// ==========================================

function addChatMessage(
    sender,
    message
) {


    const messageElement =
        document.createElement(
            "div"
        );


    // ------------------------------------------
    // USER MESSAGE
    // ------------------------------------------

    if (sender === "user") {

        messageElement.className =
            "chat-message user-message";


        messageElement.innerHTML = `

            <div class="message-content">

                <div class="message-label">
                    You
                </div>


                <div class="message-bubble">

                    ${escapeHtml(message)}

                </div>

            </div>

        `;

    }


    // ------------------------------------------
    // ASSISTANT MESSAGE
    // ------------------------------------------

    else {

        messageElement.className =
            "chat-message assistant-message";


        messageElement.innerHTML = `

            <div class="assistant-avatar">
                ✦
            </div>


            <div class="message-content">

                <div class="message-label">
                    Career Advisor
                </div>


                <div class="message-bubble">

                    ${escapeHtml(message)}

                </div>

            </div>

        `;

    }


    // ------------------------------------------
    // ADD TO CHAT
    // ------------------------------------------

    chatMessages.appendChild(
        messageElement
    );


    // ------------------------------------------
    // SCROLL TO BOTTOM
    // ------------------------------------------

    chatMessages.scrollTop =
        chatMessages.scrollHeight;


    return messageElement;

}


// ==========================================
// SUGGESTED CHAT QUESTIONS
// ==========================================

const suggestions =
    document.querySelectorAll(
        ".suggestion"
    );


suggestions.forEach(
    function (suggestion) {


        suggestion.addEventListener(
            "click",
            function () {


                const question =
                    suggestion.dataset.question;


                // Put question into input

                chatInput.value =
                    question;


                // Focus input

                chatInput.focus();

            }
        );

    }
);


// ==========================================
// HTML SECURITY
// ==========================================

function escapeHtml(value) {

    return String(value)

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );

}