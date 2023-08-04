// document.getElementById("inputForm").addEventListener("submit", function (event) {
//     event.preventDefault();
//     const inputs = document.querySelectorAll(".input");
//     let allInputsValid = true;

//     inputs.forEach((input, index) => {
//         if (input.id.includes("micro")) {
//             // For binary input, check the pattern (only 0's and 1's) and length
//             if (!input.value.match(/^[01]{200}$/)) {
//                 allInputsValid = false;
//             } 
//         } else {
//             // For regular inputs, check the value against min and max
//             const value = parseInt(input.value);
//             const min = parseInt(input.min);
//             const max = parseInt(input.max);
//             if (value < min || value > max) {
//                 allInputsValid = false;
//             }
//         }
//     });

//     if (allInputsValid) {
//         // Hide input column and show output column
//         document.getElementById("inputForm").classList.remove("show");
//         document.getElementById("outputDiv").classList.add("show");
//     }
// });

document.getElementById("editBtn").addEventListener("click", function () {
    // Hide output column and show input column
    document.getElementById("outputDiv").classList.remove("show");
    document.getElementById("inputForm").classList.add("show");
});

const inputs = document.querySelectorAll("input");
inputs.forEach((input, index) => {
    const warning = document.querySelector(`#warning${index}`);
    const isBinaryInput = input.id.includes("micro");

    input.addEventListener("input", function () {
        let isValid = false;

        if (isBinaryInput) {
            isValid = input.value.match(/^[01]{200}$/);
        } else {
            const value = parseInt(input.value);
            const min = parseInt(input.min);
            const max = parseInt(input.max);
            isValid = value >= min && value <= max;
        }
    });
});

document.getElementById("randomMicro").addEventListener("click", function () {
    const binaryInput = document.getElementById("micro");
    binaryInput.value = generateRandomBinaryString(200);
});

document.getElementById("randomAll").addEventListener("click", function () {
    const inputs = document.querySelectorAll(".input");
    inputs.forEach((input) => {
        if (input.id.includes("micro")) {
            input.value = generateRandomBinaryString(200);
        } else {
            const min = parseInt(input.min);
            const max = parseInt(input.max);
            input.value = getRandomNumberInRange(min, max);
        }
    });
});

function generateRandomBinaryString(length) {
    let result = "";
    for (let i = 0; i < length; i++) {
        result += Math.random() < 0.5 ? "0" : "1";
    }
    return result;
}

function getRandomNumberInRange(min, max) {
    return (Math.random() * (max - min) + min);
}
