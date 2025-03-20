Добрый день ! 


координаты сравниваются с погрешностью +-5 единиц, потому что при создании тест даты и сохранении измненени
в pdf файле а acrobat reader, происходило смещение элементов на чуть чуть. Заменить acrobat reader на другое не успел.
настроить округление координат можно в tools/coordinate_rounding.py

тест дату помещайте в папку test/data


эталон в test/reference



Запустить тесты 


pytest -p no:warnings -vv -s --alluredir=reports/allure-results

Сгенерировать отчет в allure


tools\allure_2_32\bin\allure generate reports/allure-results -o reports/allure-report --clean

Открыть отчет в браузере по умолчанию 


allure open reports/allure-report

P.S.
Так как требований для проверок не было, проверил простые случаи
не успел отрефакторить некоторые места и кое какие доделать. Но идей полно
И шаги в тестах сделал специально такими, чтобы вы не подумали, что за меня писал ИИ :)