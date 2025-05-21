const textarea = document.getElementById('chatInput');
const submit = document.getElementById("submit");
const chatBody = document.getElementById('chat'); 
const addTest = document.getElementById('add-test');

let userMessage;

//listeners
submit.addEventListener("click", manageChat());


function myFunction(event) 
{
  let value = event.which;

  if (value == 13 && !event.shiftKey){
    event.preventDefault();
    manageChat();
  }
}

//get solution from the server
function get_solution(message) {
  let response = fetch("https://olegpepeg.ru/api/chat", {
    method: "POST",
    body: JSON.stringify({
      messages: [{
        "role" : "user",
        "content" : `${message}`
      }]
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  })
  .then((response) => response.json())
  .then((json) => {
    console.log(json.solution)
    return json.solution})
}

// //get solution from the server
// async function get_solution(message) {
//   try {
//   let response = await fetch("https://olegpepeg.ru:34839/chat", {
//     method: "POST",
//     body: JSON.stringify({
//       messages: [{
//         "role" : "user",
//         "content" : `${message}`
//       }]
//     }),
//     headers: {
//       "Content-type": "application/json; charset=UTF-8"
//     }
//   });

//   if (!response.ok) {
//     throw new Error(`Response status: ${response.status}`);
//   }

//   var json = await response.json();

//   } catch (error) {
//     console.error(error.message);
//   }

//   console.log("Что видит функция get_solution()")
//   console.log(json.solution);

//   var salvation = await json.solution;
//   return salvation
//   //.then((response) => response.json())
//   //.then((json) => {return json.solution});
// }

//adds messages
function manageChat() {
  userMessage = textarea.value.trim();

  if (!userMessage) return;

  document.getElementById("chatInput").value = "";

  chatBody.appendChild(messageEl(userMessage, "user"));

  let solution = get_solution(userMessage);

  chatBody.appendChild(messageEl(solution, "chat-bot"));

  // setTimeout(() => {
  //   chatBody.appendChild(messageEl("thinking...", "chat-bot"));
  // })
}

//writes messages
const messageEl = (message, className) => {
  const chatEl = document.createElement(`div`);
  chatEl.classList.add(`chat`, `${className}`);
  let chatContent;    

  if (className == "user") {
    chatContent = `<p>${message}</p>`;
  }
  else{
    console.log("Что видит функция вывода")
    console.log(message)
    chatContent = `<pre><code class="python-html jetbrains-mono hljs language-python">${message}</code></pre>`;
  }
  
    chatEl.innerHTML = chatContent;
    return chatEl;
}


/*
async function chatFunction(message) {
  try {
    const response = await fetch("https://olegpepeg.ru:34839/chat", {
      method: "POST",
      body: JSON.stringify({
        messages: [{
          "role" : "user",
          "content" : `${message}`
        }]
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    });

    const result = await response.json();
    console.log("Ответ от сервера:", result().solution);
    
    const chatEl = document.createElement(`div`);
    chatEl.classList.add(`chat chat bot`);

    let chatContent =
      className == ``

  } catch (error) {
    console.error("Ошибка при отправке запроса", error);
  }
}
*/

/*
fetch("https://olegpepeg.ru:34839/chat", {
  method: "POST",
  body: JSON.stringify({
    messages: [{
      "role" : "user",
      "content" : "посчитай сумму 2 и 5"
    }]
  }),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
})
.then((response) => response.json())
.then((json) => console.log(json.solution));
*/
