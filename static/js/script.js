function getCSRFToken() {

    return document.querySelector(
        '[name=csrfmiddlewaretoken]'
    ).value;
}

const generateButton = document.getElementById("generate-btn");

const jobTitleInput = document.getElementById("job-title");

const loadingElement = document.getElementById("loading");

const questionsContainer = document.getElementById("questions-container");

const errorMessage = document.getElementById("error-message");



generateButton.addEventListener("click", () => {

    const jobTitle = jobTitleInput.value;


    if (jobTitle.trim() === "") {

        alert("Please enter a job title.");

        return;
    }


    loadingElement.classList.remove("hidden");

    errorMessage.classList.add("hidden");

    errorMessage.textContent = "";

    
    fetch("/generate/", {

    method: "POST",

    headers: {

        "Content-Type": "application/json",

        "X-CSRFToken": getCSRFToken(),
    },

    body: JSON.stringify({
        job_title: jobTitle
    })

})

    .then((response) => {

        if (!response.ok) {

            throw new Error("Failed to generate questions.");
        }

        return response.json();
    })

    .then((data) => {

        loadingElement.classList.add("hidden");

        questionsContainer.innerHTML = "";


        data.questions.forEach((question) => {

            const questionElement = document.createElement("div");

            questionElement.classList.add("question");

            questionElement.innerHTML = `<p>${question}</p>`;

            questionsContainer.appendChild(questionElement);

        });

    })

    .catch((error) => {

        loadingElement.classList.add("hidden");

        errorMessage.classList.remove("hidden");

        errorMessage.textContent = error.message;
    });
});

   