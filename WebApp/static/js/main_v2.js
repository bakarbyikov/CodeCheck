// получаем HTML DOM
const textarea = document.getElementById('chatInput');
const submit = document.getElementById("submit");
const chat_body = document.getElementById('chat'); 
const add_test = document.getElementById('add-test');
const test_list = document.getElementById('test-list');
const add_tab = document.getElementById('add-tab');
const side_bar = document.getElementById('sidebar');

// класс для вкладок
class tab {
  name = "Новая вкладка"

  constructor (name) {
    this.name = name;
  }

  return_html() {
    return `<button type="button" class="btn sidebar-button" data-toggle="button" aria-pressed="true">${this.name}</button>`
  }
}

// класс для тестов
class test {
    input = "";
    output = "";
    result = "";

  constructor(input, output, result) {
    this.input = input;
    this.output = output;
    this.result = result;
  }

  return_html() {
    return `<input id='input' type="text" class="form-control roboto d-flex" name="" id="" placeholder="input" value = "${this.input}"/><output type="text" class="form-control roboto d-flex" name="" id="output" placeholder="output"><div>${this.output}</div></output><div class="test-result roboto"></div>`;
  }
}

function my_function(event) 
{
  let value = event.which;

  if (value == 13 && !event.shiftKey){
    event.preventDefault();
    manage_chat();
  };
}

//оформление полученного сообщения message в html документе
const message_el = (message, class_name) => {
    var chat_el = document.createElement(`div`);
    chat_el.classList.add(`chat`, `${class_name}`);
    let chat_content;    
  
    if (class_name == "user") {
      chat_content = `<p>${message}</p>`;
    }

    if (class_name == "chat-bot") {
      chat_content = `<div class="code-solvation"><pre><code class="hljs python-html jetbrains-mono">${message}</code></pre></div>`;
    }

    chat_el.innerHTML = chat_content;
      return chat_el;
}

//отправление сообщения и получение решения с сервера
function manage_chat() {
  var user_message = textarea.value.trim();

    if (!user_message) return;

    textarea.value = "";

    chat_body.appendChild(message_el(user_message, "user"));

    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: "https://olegpepeg.ru/api/chat",
      data: JSON.stringify({
        "messages" : [
          {
            "role" : "user", 
            "content" : `${user_message}`
          }
        ] 
      }),
      success: function (data) {
        chat_body.appendChild(message_el(data.solution, "chat-bot"));
      }
    });

    $.ajax({
    type: "POST",
    contentType: "application/json; charset=utf-8",
    url: "https://olegpepeg.ru/api/create_tests",
    data: JSON.stringify({
      "problem": `${user_message}`
    }),
    success: function (data) {
      for (let i = 0; i < data.tests.length; i++) {
        create_test(input = data.tests[i].input, output = data.tests[i].expected);
      }
    }
  });
}

/*
//получение тестов с сервера
function manageTest() {
  var user_message = textarea.value.trim();

  if (!user_message) return;

  textarea.value = "";

  $.ajax({
    type: "POST",
    contentType: "application/json; charset=utf-8",
    url: "https://olegpepeg.ru/api/create_tests",
    data: JSON.stringify({
      "problem": `${user_message}`
    }),
    success: function (data) {
      console.log(data.tests);
    }
  });
}
*/

/*
$.ajax({
  type: "POST",
  contentType: "application/json; charset=utf-8",
  url: "https://olegpepeg.ru/api/create_tests",
  data: JSON.stringify({
    "problem": `посчитай сумму двух переменных и протестируй на следующих парах чисел : 5 и 3, 2 и 1, 0 и 10`
  }),
  success: function (data) {
    for (let i = 0; i < data.tests.length; i++) { 
      console.log(data.tests[i]);
      create_test(input = data.tests[i].input, output = data.tests[i].expected);
    }
  }
});
*/

/*
// функция, добавляющая сгенерированные тесты
// сейчас она просто находит самый нижний див с классом chat-bot и добавляет ему класс found
function showTest () {
  $('#chat').each(function() {
        $(this).find(".chat-bot").filter(":last").addClass("found");
      });
} 
*/

// функция, создающая пустую вкладку
function create_tab(label = "Новая вкладка") {
  var tab_el = document.createElement(`div`);
  tab_el.classList.add(`d-flex`, `sidebar-pair`);
  tab_new_el = new tab(name = label);
  tab_el.innerHTML = tab_new_el.return_html();
  side_bar.appendChild(tab_el);
  side_bar.insertBefore(tab_el, add_tab);
}

// функция, создающая пустой тест
function create_test(input, output) {

  var test_el = document.createElement(`div`);
  test_el.classList.add(`test-box`, `d-flex`);

  if (!input || !output) {
    test_content = `<input name = "input" type="text" class="input form-control roboto" placeholder="input" /><output name = "output" type="text" class="output form-control roboto"></output><div class="test-result roboto"></div>`;
  }

  else {
    new_test = new test(input = input, output = output);
    test_content = new_test.return_html();
  }
  
  test_el.innerHTML = test_content;
  test_list.appendChild(test_el);
  test_list.insertBefore(test_el, add_test);

  // функциональная кнопка проверки результатов
  var All_results = document.querySelectorAll('.test-result');
  var All_inputs = document.querySelectorAll('input');
  var All_outputs = document.querySelectorAll('output div');
  var All_solutions = document.querySelectorAll('.python-html');

  for (let i = 0; i <= All_results.length; i++) {
    All_results[i].addEventListener("click", 
      function get_result() {
        All_results[i].innerHTML = `<div class = "loader"></div>`

        if (!All_inputs[i].value || !All_outputs[i].textContent) {
          All_results[i].innerHTML = "h";
        }

        else if (All_outputs[i].textContent || All_inputs[i].value) {
          $.ajax({
          type: "POST",
          contentType: "application/json; charset=utf-8",
          url: "https://olegpepeg.ru/api/test_solution",
          data: JSON.stringify({
            "solution": `${All_solutions.last}`,
            "tests": [
              {
                "input": `${All_inputs[i].value}`,
                "expected": `${All_outputs[i].textContent}`
              }
            ]
          }),
          success: function (data) {
            //удаление загрузки
            All_results[i].innerHTML = "";

            if (data[0].status == "Passed") {
              All_results[i].innerHTML = `<span>+</span>`;
              All_results[i].classList.add(`passed`);
            }
            else if (data[0].status == "Failed"){
              All_results[i].innerHTML = `<span>-</span>`;
              All_results[i].classList.add('failed');
            }
            else {
              All_results[i].innerHTML = `<span>error</span>`;
              All_results[i].classList.add('error');
            }
          }
        })
      }
      }
    );
  }
}

//тот же main.js, но с использованием библиотеки jQuery
$(document).ready(function(){
    let user_message;
    
    //считывание нажатия на кнопку "отправить"
    $('#submit').click(manage_chat);
    $('#add-test').click(create_test);
    $('#add-tab').click(create_tab);
});