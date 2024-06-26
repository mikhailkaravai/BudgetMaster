1. Тип приложения:

Финансовое приложение для учета транзакций и управления финансами.
2. Стратегия развертывания:

Выбор облачного (Cloud) развертывания для обеспечения гибкости, масштабируемости и удобства доступа для пользователей из различных мест.
3. Обоснование выбора технологии:

    Язык программирования: Python - для быстрого прототипирования и разработки, а также для широкой поддержки библиотек для работы с базами данных и веб-фреймворков.
    Фреймворк для веб-разработки: Flask - для создания веб-интерфейса с минимальными накладными расходами и простотой в использовании.
    База данных: SQLite - для легкости внедрения и минимизации настроек.
    Интерфейс пользователя: Tkinter - для создания простого графического интерфейса, интегрированного непосредственно в Python.

4. Показатели качества:

    Производительность: Отзывчивость интерфейса и скорость обработки транзакций.
    Надежность: Безопасность данных и минимум сбоев при использовании.
    Удобство использования: Интуитивно понятный интерфейс для удобства пользователей.
    Масштабируемость: Возможность масштабирования приложения для обработки больших объемов данных и расширения функциональности.

5. Пути реализации сквозной функциональности:

    Аутентификация и авторизация: Использование сессий и ролевой модели доступа для защиты данных и ограничения прав доступа.
    Управление транзакциями: Реализация функционала добавления, удаления и отображения транзакций с помощью соответствующих методов.
    Учет категорий: Реализация возможности добавления, удаления и просмотра категорий транзакций.
6. Структурная схема приложения в виде функциональных блоков:
![alt-текст](https://github.com/mikhailkaravai/BudgetMaster/blob/main/Documentation/UML/To%20be.png)
 Интерфейс пользователя: Отвечает за взаимодействие с пользователем через графический интерфейс.
    Контроллер: Осуществляет связь между пользовательским интерфейсом и функционалом приложения.
    FinancialApp: Содержит основную логику приложения, такую как управление транзакциями и работа с базой данных.
    База данных: Хранит информацию о пользователях, транзакциях и категориях.
Это простая структурная схема, иллюстрирующая основные функциональные блоки приложения и их взаимосвязь.

Эта диаграмма представляет классы и их связи в системе учета финансов:
![alt-текст](https://github.com/mikhailkaravai/BudgetMaster/blob/main/Documentation/UML/As%20is.png)
    Класс User имеет атрибуты id, username и password, а также связь с классом Transaction через атрибут username.
    Класс Transaction имеет атрибуты id, description, amount, category, type и date, а также связи с классами User и Category.
    Класс FinancialApp имеет методы для работы с базой данных и связь с классом Transaction для управления транзакциями.
    Класс DateEntry представляет собой инструмент для выбора даты и имеет связь с классом FinancialApp для отправки выбранной даты.
Для начала проведем первый Sprint Review. В данном ревью мы будем обсуждать достижения команды за первый спринт и презентовать результаты.
Первый Sprint Review
Цели спринта:

    Разработать систему аутентификации пользователей.
    Реализовать добавление и отображение транзакций.
    Добавить возможность регистрации новых пользователей.
    Предоставить возможность переключения валюты и конвертации суммы транзакций.

Достижения:

    Система аутентификации:
        Реализована проверка логина и пароля при входе.
        Пользователи могут зарегистрироваться в системе.
    Добавление и отображение транзакций:
        Реализовано добавление новых транзакций.
        Транзакции отображаются в соответствии с выбранной валютой.
    Регистрация новых пользователей:
        Пользователи могут зарегистрироваться с уникальным именем пользователя и паролем.
    Переключение валюты и конвертация:
        Добавлена возможность выбора валюты.
        Суммы транзакций автоматически конвертируются в выбранную валюту.

Демонстрация:

    Показать процесс входа в систему существующим пользователем.
    Продемонстрировать добавление новой транзакции.
    Показать отображение списка транзакций с возможностью переключения валюты и конвертации суммы.
    Представить процесс регистрации нового пользователя.

Обратная связь:

    Пользовательский интерфейс: Оценить удобство использования и понятность интерфейса.
    Функциональность: Проверить работоспособность всех функций и их соответствие требованиям.
    Замечания и предложения по улучшению.

Давайте сначала сравним архитектуры "As is" и "To be", а затем выделим отличия, проанализируем их причины и предложим пути улучшения архитектуры.
Сравнение архитектур "As is" и "To be":
"As is" (как есть):

    Структура:
        Программа состоит из нескольких основных компонентов: пользовательского интерфейса, контроллера, классов для работы с финансовыми данными и базой данных.
        Используется простая архитектура на основе функциональных блоков.

"To be" (как должно быть):

    Структура:
        Внедрена модель MVC (Model-View-Controller) для более четкого разделения логики приложения, представления данных и взаимодействия с пользователем.
        Внедрены различные слои для лучшей модульности и сопровождаемости.

Отличия и их причины:

    Модель архитектуры:
        "As is": Применяется простая блочная архитектура.
        "To be": Используется более сложная, но более эффективная модель MVC, что позволяет разделить компоненты приложения на три отдельных слоя.

    Уровень детализации:
        "As is": Представление достаточно низкого уровня детализации, что затрудняет понимание внутренней структуры и взаимосвязей компонентов.
        "To be": Более высокий уровень детализации за счет применения MVC, что делает архитектуру более модульной и гибкой.

Пути улучшения архитектуры:

    Внедрение MVC:
        Применение MVC позволит четко разделить логику приложения, представление данных и взаимодействие с пользователем, что улучшит модульность и сопровождаемость приложения.

    Использование архитектурных шаблонов:
        Применение шаблонов проектирования, таких как Dependency Injection, Observer, Facade, позволит улучшить гибкость и расширяемость системы.

    Разделение на уровни:
        Разделение приложения на уровни (например, уровень представления, бизнес-логики и доступа к данным) поможет сделать архитектуру более понятной и легкой для сопровождения.

    Объяснение решений:
        Документирование и объяснение архитектурных решений поможет улучшить понимание структуры приложения и обеспечить лучшее сотрудничество в команде разработки.

    Улучшение инструментов и процессов:
        Внедрение современных инструментов разработки и процессов CI/CD поможет улучшить качество, стабильность и производительность приложения.
