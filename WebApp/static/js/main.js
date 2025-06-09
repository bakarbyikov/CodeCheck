// получаем HTML DOM
const textarea = document.getElementById('chatInput');
const submit = document.getElementById("submit");
const chat_body = document.getElementById('chat'); 
const add_test = document.getElementById('add-test');
const test_list = document.getElementById('test-list');
const add_tab = document.getElementById('add-tab');
const side_bar = document.getElementById('sidebar');
var tabs_storage = {

};

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

// объявление стартового сообщения
let start_message = document.createElement(`div`);
start_message.classList.add('chat', 'chat-bot');

let start_span = document.createElement(`span`);
start_span.textContent = 'Здравствуйте! Что нужно решить для вас сегодня?';

start_message.appendChild(start_span);

tabs_storage["Новая вкладка"] = {
  messages : [start_message],
  tests : []
};

// функция, создающая пустую вкладку
function create_tab(label = "Новая вкладка") {
  var tab_el = document.createElement(`div`);
  tab_el.classList.add(`d-flex`, `sidebar-pair`);

  tab_el.innerHTML = `<button type="button" class="btn sidebar-button" data-toggle="button" aria-pressed="true"><span>${label}</span></button>`;

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
    let stored_info = tabs_storage[document.getElementsByClassName('active-tab')[0].firstChild.firstChild.textContent];
    
    chat_body.innerHTML = '';
    test_list.innerHTML = '';

    // вывод сообщений и тестов
    if (stored_info.tests.length > 0) {
      for (let i = 0; i <= stored_info.tests.length - 1; i++) {
        test_list.appendChild(stored_info.tests[i]);
      };
    };

    if (stored_info.messages.length > 0) {
      for (let i = 0; i <= stored_info.messages.length - 1; i++) {
        chat_body.appendChild(stored_info.messages[i]);
      };
    };
    
    test_list.appendChild(add_test);
  });

  side_bar.insertBefore(tab_el, add_tab);
}

//  смена названия вкладки
$('#tab-change-name').click(function(event) {
  let new_tab_name = document.getElementById("tab-name");
  let tab_to_change_name = document.getElementsByClassName('selected-tab')[0];
  let all_tabs = document.getElementsByClassName('sidebar-pair');

  // предупреждение насчёт вкладок с одинаковыми названиями
  let checkNames = false;
  for (let i = 0; i < all_tabs.length - 1; i++) {
    if (new_tab_name.value == all_tabs[i].firstChild.firstChild.textContent) {
      checkNames = true;
    }
  };
  if (checkNames) {
    console.log('Предупреждение : вкладки с одинаковыми именами хранят общие сообщения и тесты!');
    return;
  }

  // изменяет ключ(название вкладки) в sessionStorage на новое
  let stored_info = tabs_storage[tab_to_change_name.firstChild.firstChild.textContent];
  tabs_storage[new_tab_name.value] = stored_info;

  if (tab_to_change_name.firstChild.firstChild.textContent != "Новая вкладка") {
    delete tabs_storage[tab_to_change_name.firstChild.firstChild.textContent];
    console.log(`deleted ${tab_to_change_name.firstChild.firstChild.textContent} from tabs_storage`);
  } else {
    // объявление стартового сообщения
    let start_message = document.createElement(`div`);
    start_message.classList.add('chat', 'chat-bot');

    let start_span = document.createElement(`span`);
    start_span.textContent = 'Здравствуйте! Что нужно решить для вас сегодня?';

    start_message.appendChild(start_span);

    tabs_storage["Новая вкладка"] = {
      messages : [start_message],
      tests : []
    };
  };

  console.log(tabs_storage);
  tab_to_change_name.firstChild.firstChild.textContent = new_tab_name.value;
});

//оформление полученного сообщения message в html документе
function message_el (message, class_name) {
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

  var current_active_tab = document.getElementsByClassName('active-tab')[0].firstChild.firstChild.textContent;
  var stored_info = tabs_storage[current_active_tab];
  
  // сохранение отправленного сообщения пользователя в tabs_storage к текущей открытой вкладке
  if (stored_info) {
    stored_info.messages.push(message_el(user_message, "user"));
    tabs_storage[current_active_tab] = stored_info;
  }

  //console.log(tabs_storage);

  var countOfMessages = document.getElementsByClassName('chat chat-bot').length;

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
      var botMessage = message_el(solution, "chat-bot");

      // сохранение полученного сообщения в tab_storage к текущей открытой вкладке
      var stored_info = tabs_storage[current_active_tab];

      if (countOfMessages == 1) {
        botMessage.classList.add('selected-solution');
      }

      if (stored_info) {
        stored_info.messages.push(botMessage);
        tabs_storage[current_active_tab] = stored_info;
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
            // сохранение полученного сообщения в tab_storage к текущей открытой вкладке
            let stored_info = tabs_storage[current_active_tab];

            if (stored_info) {
              stored_info.tests.push(create_test(input = data.tests[i].input, output = data.tests[i].expected, solution = solution));
              tabs_storage[current_active_tab] = stored_info;
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
function create_test(input = '', output = '') {
  var test_el = document.createElement(`div`);
  test_el.classList.add(`test-box`, `d-flex`);

  // if (document.getElementById("contextmenu").className == "hiddden contextmenu") {

  // }

  var result = document.createElement('div');
  result.classList.add('test-result', 'roboto');

  //проверка тестов на сервере
  result.addEventListener("click", function get_result(event) {
        var solution = document.getElementsByClassName('selected-solution')[0].firstChild.firstChild.firstChild.textContent;
        let input = event.target.parentNode.children[0].value;
        let output = event.target.parentNode.children[1].value;
        result.innerHTML = `<div class = "loader"></div>`

        if (input == '' || output == '' || solution == '') {
          console.log('input/output/solution is empty!');
          result.innerHTML = "!";
          console.log(input, output, solution);
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
                "input": `${event.target.parentNode.children[0].value}`,
                "expected": `${event.target.parentNode.children[1].value}`
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
              console.log(solution);
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
    
    return test_el;
  });

  test_el.appendChild(result);
  return test_el;
}

// тот же main.js, но с использованием библиотеки jQuery
// скрипт будет запущен тогда, когда прогрузится HTML страница с стилями 
$(document).ready(function(){
  // создание начальной вкладки
  create_tab();
  let start_tab = document.getElementsByClassName('sidebar-pair')[0];
  start_tab.click();

  $('#submit').click(function () {
    manage_chat();
  });
  
  $('#add-test').click(function() {
    let current_active_tab = document.getElementsByClassName('active-tab')[0].firstChild.firstChild.textContent;
    let stored_info = tabs_storage[current_active_tab];

    if (stored_info) {
      stored_info.tests.push(create_test());
      tabs_storage[current_active_tab] = stored_info;
    }

    document.getElementsByClassName('active-tab')[0].click();
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