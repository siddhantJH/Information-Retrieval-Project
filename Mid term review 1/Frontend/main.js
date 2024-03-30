let i = 0;
let txt = "";
let txt2= ""
let speed = 500;

function getText() {
    recordHistory();
    i = 0;
    txt = document.querySelector("#userInput").value;
    txt2 = getResult() // once the get result function is declared we will use this in the typeWrite function
    speed = 70;
    typeWriter();
    // txt.value=""; // This line is unnecessary and can be removed
}


function getResult()
{
//we get the result from the back end and we assign it to the txt and finllay display it ccording to the user format 
}


function typeWriter() {
     // Call recordHistory function to record user input history
    if (i < txt.length) {
        let d = document.querySelector('.attach');
        if (i % 52 == 0) {
            d.innerHTML += "<br>";
        }
        if (txt.charAt(i) ==" ") {
            console.log(txt.charAt(i));
            d.textContent += " ";
        }
        d.textContent += txt.charAt(i);
        i++;
        setTimeout(typeWriter, speed);
    } else {
        return;
    }
}

function recordHistory() {
    const d1 = document.querySelector('.history');
    const userInput = document.querySelector('#userInput').value;
    const userInputShortened = userInput.substring(0, 10); // Limiting to first 10 characters
    const h3 = document.createElement('h3');
    h3.appendChild(document.createTextNode(userInputShortened));
    const div = document.createElement('div');
    div.appendChild(h3);
    div.style.display="flex"
    div.style.justifyContent="center"
    div.className="smooth-border"
    const button = document.createElement("button");
    div.appendChild(button)
    button.innerText="X"
    button.className="delete-btn";
    button.setAttribute("onclick", "deleteEntry()");
    d1.appendChild(div); // Append created div to '.histor' element to display user input history
}


function deleteEntry()
{
    
}