// получаем HTML DOM
const textarea = document.getElementById('chatInput');
const submit = document.getElementById("submit");
const chat_body = document.getElementById('chat'); 
const add_test = document.getElementById('add-test');
const test_list = document.getElementById('test-list');
const add_tab = document.getElementById('add-tab');
const side_bar = document.getElementById('sidebar');

//позволяет делать спуск в поле текста на shift+enter
function textarea_input(event) 
{
  let value = event.which;

  if (value == 13 && !event.shiftKey){
    event.preventDefault();
    manage_chat();
  };
}

function input_tab_name(event) 
{
  let value = event.which;

  if (value == 13 && !event.shiftKey){
    event.preventDefault();
    $('#tab-change-name').click();
  };
}

// класс для вкладок
class tab {
  constructor (name) {
    this.name = name
    this.messages = { 
      user : [],
      bot : []
    }
    this.tests = {
      input: [],
      expected: [],
      result: []
    }
  }

  // добавление сообщений к вкладке
  add_message(whom, message) {
    this.messages[whom].push(message);
  }

  // добавление тестов
  add_tests(input, expected, result) {
    this.tests[input].push(input)
    this.tests[expected].push(expected)
    this.tests[result].push(result)
  }
  
  // возвращает оформленную вкладку
  return_html() {
    let html = `<button type="button" class="btn sidebar-button" data-toggle="button" aria-pressed="true"><span>${this.name}</span></button>`;
    return html;
  }
}

// функция, создающая пустую вкладку
function create_tab(label = "Новая вкладка") {
  var tab_el = document.createElement(`div`);
  tab_el.classList.add(`d-flex`, `sidebar-pair`);

  tab_new_el = new tab(label);
  tab_el.innerHTML = tab_new_el.return_html();

  sessionStorage.setItem(label, JSON.stringify({messages : ['<div class="chat chat-bot"><p>Здравствуйте! Что нужно решить для вас сегодня?</p></div>'], tests : []}));
  //console.log(label);

  // моё contextmenu с функцией удаление вкладки
  tab_el.addEventListener('contextmenu', function(event) {
    event.preventDefault();

    // гарантия наличия лишь одной выбранной вкладки для работы с contextmenu
    $('.sidebar-pair').removeClass('selected-tab');

    let e = window.event;
    let window_width = window.innerWidth;

    //граматное появление contextmenu относительно свободного места экрана
    if (window_width - e.clientX < 134) {
      var x = e.clientX - 134;
    }
    else {
      var x = e.clientX + 6;
    }

    if (window_width - e.clientY < 36*2) {
      var y = e.clientY - 40;
    }
    else {
      var y = e.clientY;
    }

    document.getElementById('contextmenu-tabs').className = "shown contextmenu";
    document.getElementById('contextmenu-tabs').style.top = y + 'px';
    document.getElementById('contextmenu-tabs').style.left = x + 'px';

    tab_el.classList.add('selected-tab');
  });

  // выделяет активную вкладку
  tab_el.addEventListener("click", function(event) {
    $('.sidebar-pair').removeClass('active-tab');
    
    tab_el.classList.add('active-tab');
    let stored_info = JSON.parse(sessionStorage.getItem(document.getElementsByClassName('active-tab')[0].firstChild.firstChild.textContent));

    chat_body.innerHTML = "";

    let full_tests = '';
    let full_message = '';

    // сделать добавление тестов !!!!!!!
    if (stored_info.tests.length > 0) {
      for (let i = 0; i < stored_info.tests.length; i++){
        full_tests += stored_info.tests[i];
      }
    }

    for (let i = 0; i < stored_info.messages.length; i++){
      full_message += stored_info.messages[i];
    }

    // console.log(full_message);
    // console.log(full_tests);
    chat_body.innerHTML = full_message;
    test_list.innerHTML = full_tests;
    test_list.appendChild(add_test);
    // var message = document.createElement('div');
    // message.innerHTML = stored_messages;
    // console.log(message);
    // message = message.childNodes;
    // console.log(message);
    //chat_body.appendChild(message);
  });

  side_bar.insertBefore(tab_el, add_tab);
}

//  смена названия вкладки
$('#tab-change-name').click(function(event) {
  let new_tab_name = document.getElementById("tab-name");
  let tab_to_change_name = document.getElementsByClassName('selected-tab')[0];
  let old_name = tab_to_change_name.firstChild.firstChild.textContent;
  let all_tabs = document.getElementsByClassName('sidebar-pair');

  // предупреждение насчёт вкладок с одинаковыми названиями
  for (let i = 0; i < all_tabs.length; i++) {
    if (new_tab_name.value == all_tabs[i].firstChild.firstChild.textContent) {
      console.log('Предупреждение : вкладки с одинаковыми именами хранят общие сообщения и тесты!');
    }
  }

  // изменяет ключ(название вкладки) в sessionStorage на новое
  let stored_messages = sessionStorage.getItem(tab_to_change_name.firstChild.firstChild.textContent);
  sessionStorage.setItem(new_tab_name.value, stored_messages);

  if (tab_to_change_name.firstChild.firstChild.textContent != "Новая вкладка") {
    sessionStorage.removeItem(tab_to_change_name.firstChild.firstChild.textContent);
  }
  // console.log(new_tab_name.value);
  // console.log(sessionStorage.getItem(new_tab_name.value));
  // console.log('все, что есть в sessionStorage');
  // for (let i = 0; i < sessionStorage.length; i++) {
  //   let key = sessionStorage.key(i);
  //   console.log(`ключ: ${key}`)
  //   console.log(sessionStorage.getItem(key));
  // }
  // console.log('konec');

  tab_to_change_name.innerHTML = `<button type="button" class="btn sidebar-button" data-toggle="button" aria-pressed="true"><span>${new_tab_name.value}</span></button>`;
});

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

      chat_el.addEventListener('contextmenu', function(event) {
        event.preventDefault();
        let e = window.event;
        let window_width = window.innerWidth;

        //граматное появление contextmenu относительно свободного места экрана
        if (window_width - e.clientX < 134) {
          var x = e.clientX - 134;
        }
        else {
          var x = e.clientX + 6;
        }

        if (window_width - e.clientY < 36*2) {
          var y = e.clientY - 40;
        }
        else {
          var y = e.clientY;
        }

        document.getElementById('contextmenu-selected-solution').className = "shown contextmenu";
        document.getElementById('contextmenu-selected-solution').style.top = y + 'px';
        document.getElementById('contextmenu-selected-solution').style.left = x + 'px';

        $("#select-solution").click(function() {
          $('.chat-bot').removeClass('selected-solution');

          chat_el.classList.add('selected-solution');
        });

      });
    }

    chat_el.innerHTML = chat_content;
      return chat_el;
}

//возможность нажатия на кнопки на contextmenu при помощи пкм
document.getElementById("detele-test").addEventListener('contextmenu', function(e) {
  e.preventDefault();
  $("#detele-test").click();
})

document.getElementById("select-solution").addEventListener('contextmenu', function(e) {
  e.preventDefault();
  $("#select-solution").click();
})

//отправление сообщения и получение решения с сервера
function manage_chat() {
  var user_message = textarea.value.trim();

  if (!user_message) return;

  textarea.value = "";

  //chat_body.appendChild(message_el(user_message, "user"));
  var current_active_tab = document.getElementsByClassName('active-tab')[0].firstChild.firstChild.textContent;
  let stored_info = sessionStorage.getItem(current_active_tab);
  
  // сохранение отправленного сообщения пользователя в sessionStorage к текущей открытой вкладке
  if (stored_info) {
    let parsed_info = JSON.parse(stored_info);
    parsed_info.messages.push(message_el(user_message, "user").outerHTML);
    sessionStorage.setItem(current_active_tab, JSON.stringify(parsed_info));
    //console.log(sessionStorage.getItem(current_active_tab));
  }

  //console.log(stored_messages);

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
      var solution = data.solution;
      //chat_body.appendChild(message_el(solution, "chat-bot"));

      // сохранение полученного сообщения в sessionStorage к текущей открытой вкладке
      let stored_info = sessionStorage.getItem(current_active_tab);

      if (stored_info) {
        let parsed_info = JSON.parse(stored_info);
        parsed_info.messages.push(message_el(solution, "chat-bot").outerHTML);
        sessionStorage.setItem(current_active_tab, JSON.stringify(parsed_info));
      }

      document.getElementsByClassName('active-tab')[0].click();

      $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: "https://olegpepeg.ru/api/create_tests",
        data: JSON.stringify({
          "problem": `${user_message}`
        }),
        success: function (data) {
          for (let i = 0; i < data.tests.length; i++) {
            // сохранение полученного сообщения в sessionStorage к текущей открытой вкладке
            let stored_info = sessionStorage.getItem(current_active_tab);

            if (stored_info) {
              let parsed_info = JSON.parse(stored_info);
              parsed_info.tests.push(create_test(input = data.tests[i].input, output = data.tests[i].expected, solution = solution).outerHTML);
              sessionStorage.setItem(current_active_tab, JSON.stringify(parsed_info))
            }
          }
          document.getElementsByClassName('active-tab')[0].click();
        }
      });
    }
  });
  document.getElementsByClassName('active-tab')[0].click();
}

document.getElementById('sidebar').addEventListener('contextmenu', function(event) {
    event.preventDefault();
});

document.getElementById('tests').addEventListener('contextmenu', function(event) {
  event.preventDefault();
});

document.getElementById('chat').addEventListener('contextmenu', function(event) {
  event.preventDefault();
});

// функция, создающая пустой тест
function create_test(input = '', output = '', solution = '') {

  var test_el = document.createElement(`div`);
  test_el.classList.add(`test-box`, `d-flex`);

  if (document.getElementById("contextmenu").className == "hiddden contextmenu") {

  }

  var result = document.createElement('div');
  result.classList.add('test-result', 'roboto');

  //проверка тестов на сервере
  result.addEventListener("click", 
      function get_result() {
        result.innerHTML = `<div class = "loader"></div>`

        if (input == '' || output == '' || solution == '') {
          console.log('input/output/solution is empty!');
          result.innerHTML = "!";
        }

        else {
          $.ajax({
          type: "POST",
          contentType: "application/json; charset=utf-8",
          url: "https://olegpepeg.ru/api/test_solution",
          data: JSON.stringify({
            "solution": `${solution}`,
            "tests": [
              {
                "input": `${input}`,
                "expected": `${output}`
              }
            ]
          }),
          success: function (data) {
            if (data[0].status == "Passed") {
              result.innerHTML = `<span>+</span>`;
              result.classList.add(`passed`);
            }
            else if (data[0].status == "Failed"){
              result.innerHTML = `<span>-</span>`;
              result.classList.add('failed');
            }
            else {
              result.innerHTML = `<span>!</span>`;
              result.classList.add('error');
              console.log(data[0].message);
            }
          }
        })
      }
      }
    );
  
  inner_html = `<input type="text" class="input form-control roboto d-flex" placeholder="input" value="${input}" /><input type="text" class="output form-control roboto d-flex" placeholder="output" value="${output}" />`;
  test_el.innerHTML = inner_html;

  test_el.addEventListener('contextmenu', function(event) {
    event.preventDefault();

    let e = window.event;
    let window_width = window.innerWidth;

    test_el.classList.add('selected-test-box');

    //граматное появление contextmenu относительно свободного места экрана
    if (window_width - e.clientX < 134) {
      var x = e.clientX - 134;
    }
    else {
      var x = e.clientX;
    }

    if (window_width - e.clientY < (36*2 + 12)) {
      var y = e.clientY - (36*2 + 20);
    }
    else {
      var y = e.clientY;
    }

    document.getElementById('contextmenu').className = "shown contextmenu";
    document.getElementById('contextmenu').style.top = y + 'px';
    document.getElementById('contextmenu').style.left = x + 'px';
  });

  //помещает текст внутри input'ов внутрь их value
  test_el.addEventListener('contextmenu', function(event) {
    var input_value = test_el.firstChild.value;
    var output_value = test_el.children[1].value;

    let updated_html = test_el.innerHTML.replace(/placeholder="input" value="(.*?)"/, `placeholder="input" value="${input_value}"`)
                                        .replace(/placeholder="output" value="(.*?)"/, `placeholder="output" value="${output_value}"`);

    test_el.innerHTML = updated_html;
  });


  test_el.appendChild(result);
  return test_el;
}

// тот же main.js, но с использованием библиотеки jQuery
// скрипт будет запущен тогда, когда прогрузится HTML страница с стилями 
$(document).ready(function(){
  sessionStorage.clear();
  // создание начальной вкладки
  create_tab();
  let start_tab = document.getElementsByClassName('sidebar-pair')[0];
  start_tab.click();

  $('#submit').click(function () {
    manage_chat();
  });
  
  $('#add-test').click(function() {
    create_test();
  });
  
  $('#add-tab').click(function() {
    create_tab();
  });
  
  $(document).bind("click", function(event) {
    $('.selected-test-box').removeClass('selected-test-box');
    document.getElementById('contextmenu').className = 'hidden contextmenu';
    document.getElementById('contextmenu-selected-solution').className = 'hidden contextmenu';

    if ((!document.getElementById('contextmenu-tabs').contains(event.target)) || (document.getElementById('tab-change-name').contains(event.target))) {
      //console.log(event.target.id);
      document.getElementById('contextmenu-tabs').className = 'hidden contextmenu';
      $('.sidebar-pair').removeClass('selected-tab');
    }
  });

  $('#detele-test').click(function() {
    $('.selected-test-box').remove();
  });
});