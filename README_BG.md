# Документация на Симулатор за Пчелен Кошер

## Съдържание
1. [Общ преглед](#общ-преглед)
2. [Инсталация](#инсталация)
3. [Основни характеристики](#основни-характеристики)
4. [Детайлни компоненти](#детайлни-компоненти)
5. [Генериране на данни](#генериране-на-данни)
6. [Конфигурация](#конфигурация)
7. [Технически детайли](#технически-детайли)

## Общ преглед

Симулаторът за пчелен кошер е сложен инструмент, разработен за генериране на реалистични сензорни данни за системи за наблюдение на кошери. Той симулира сложните взаимодействия между условията на околната среда, дейността на пчелната колония и сезонните модели, специфични за българския климат. Симулаторът предоставя данни в реално време, които отразяват действителното поведение на кошера.

## Инсталация

1. Клониране на хранилището:
```bash
git clone [repository-url]
cd beehive-simulator
```

2. Инсталиране на необходимите зависимости:
```bash
pip install -r requirements.txt
```

3. Конфигуриране на вашия ThingSpeak API ключ в `beehive_simulator.py`:
```python
API_KEY = 'ВАШИЯТ_API_КЛЮЧ'
```

4. Стартиране на симулатора:
```bash
python beehive_simulator.py
```

## Основни характеристики

### 1. Симулация на околната среда

#### Метеорологични модели
- **Ясно време**
  - Промяна на температурата: +1°C
  - Промяна на влажността: -5%
  - Оптимални условия за събиране на нектар

- **Облачно време**
  - Неутрален ефект върху температурата
  - Неутрален ефект върху влажността
  - Намалена ефективност на събирането

- **Дъждовно време**
  - Промяна на температурата: -2°C
  - Промяна на влажността: +15%
  - Повишено съдържание на влага

- **Буря**
  - Промяна на температурата: -4°C
  - Промяна на влажността: +25%
  - Бързи промени в метеорологичните условия

#### Метеорологични тенденции
- Симулация на вятър (0-30 км/ч)
- Посока на вятъра (0-360 градуса)
- Атмосферно налягане (985-1035 hPa)
- Вариации в температурата (±3°C)
- Колебания във влажността (±10%)

### 2. Сезонни модели

#### Зима (Декември-Февруари)
- Температурен диапазон: 0-5°C
- Влажност: 70-80%
- Дневна светлина: 9 часа
- Пик на слънцето: 12:00
- Основна дейност: Зимно клъстериране

#### Пролет (Март-Май)
- Температура: 5-25°C (постепенно затопляне)
- Влажност: 60-70%
- Дневна светлина: 9-15 часа (увеличаване)
- Пик на слънцето: 12:00-14:00
- Ключови дейности: Отглеждане на пило, роене

#### Лято (Юни-Август)
- Температура: 25-33°C
- Влажност: 60-65%
- Дневна светлина: 15 часа
- Пик на слънцето: 14:00
- Пик в събирането на нектар и производството на мед

#### Есен (Септември-Ноември)
- Температура: 25-5°C (постепенно охлаждане)
- Влажност: 65-80%
- Дневна светлина: 15-9 часа (намаляване)
- Пик на слънцето: 14:00-12:00
- Фокус: Подготовка за зимата

## Детайлни компоненти

### 1. Система за управление на теглото

#### Базови компоненти
| Компонент | Диапазон (кг) | Описание |
|-----------|---------------|-----------|
| Базово тегло | 30 | Фиксирана структура на кошера |
| Запаси от мед | 0-25 | Променливи запаси от мед |
| Запаси от прашец | 0-5 | Съхранен прашец |
| Популация пчели | 0.5-2 | Маса на живите пчели |
| Маса на пилото | 0-1 | Развиващи се пчели |
| Влага | 0-0.5 | Влага от околната среда |

#### Дневна консумация
| Сезон | Консумация (г/ден) | Бележки |
|-------|-------------------|----------|
| Зимен клъстер | 50 | Минимална активност |
| Зима | 30 | Базово оцеляване |
| Пролет | 100 | Интензивно отглеждане на пило |
| Лято | 80 | Активно събиране |
| Есен | 50 | Фаза на подготовка |

### 2. Система за събития

#### Редовни събития
- **Нектарен поток**
  - Поява: Пролет/Лято
  - Увеличение на теглото: до 2г/минута
  - Зависи от дневната светлина
  - Влияе на: Запаси от мед

- **Събиране на прашец**
  - Събиране през активния сезон
  - Увеличение на теглото: до 1г/минута
  - Зависи от дневната светлина
  - Влияе на: Запаси от прашец

- **Отглеждане на пило**
  - Консумация на ресурси: 0.3г/минута
  - Ефективност на конверсия: 30%
  - Влияе на: Растеж на популацията

#### Специални събития
- **Роене**
  - Поява през пролетта
  - Влияние върху популацията: -50%
  - Увеличение на температурата: +4°C
  - Продължителност: 2-4 часа

- **Зимен клъстер**
  - Продължителност: 30-60 дни
  - Поддържане на температурата
  - Намалена консумация
  - Ограничена активност

### 3. Синергии между събитията

#### Съвместими комбинации
```
Нектарен поток + Събиране на прашец:
- Бонус към увеличението на теглото: 20%
- Повишена нужда от вентилация

Отглеждане на пило + Събиране на прашец:
- Ефективност на температурата: +30%
- Консумация на ресурси: +40%

Вентилация + Събиране на прополис:
- Контрол на влажността: +20%
- Бонус към регулацията на температурата
```

## Генериране на данни

### 1. Изход на сензорните данни
```json
{
    "field1": "Вътрешна температура (°C)",
    "field2": "Вътрешна влажност (%)",
    "field3": "Външна температура (°C)",
    "field4": "Външна влажност (%)",
    "field5": "Общо тегло (кг)"
}
```

### 2. Честота на обновяване
- Генериране на данни: Всяка минута
- Качване в ThingSpeak: В реално време
- Метеорологични обновления: На всеки 30 минути
- Проверка за събития: Непрекъсната

### 3. Диапазони на стойностите
| Параметър | Мин | Макс | Нормален диапазон |
|-----------|-----|------|-------------------|
| Вътрешна темп. | 25°C | 40°C | 34-36°C |
| Вътрешна влажност | 40% | 90% | 55-65% |
| Тегло | 20кг | 50кг | 30-45кг |

## Конфигурация

### 1. ThingSpeak настройки
```python
API_KEY = 'ВАШИЯТ_API_КЛЮЧ'
BASE_URL = 'https://api.thingspeak.com/update'
```

### 2. Параметри на симулацията
```python
UPDATE_INTERVAL = 60  # секунди
WEATHER_UPDATE = 30   # минути
MAX_HONEY = 25       # кг
MAX_POLLEN = 5       # кг
BASE_WEIGHT = 30     # кг
```

## Технически детайли

### 1. Зависимости
- Python 3.6+
- Необходими пакети:
  ```
  requests==2.31.0
  ```

### 2. Структура на кода
```
beehive_simulator/
├── beehive_simulator.py
├── requirements.txt
└── README.md
```

### 3. Класове
- `WeatherPattern`: Управление на метеорологичните условия
- `WeatherTrend`: Дългосрочни метеорологични тенденции
- `Season`: Сезонни изчисления
- `HiveWeight`: Проследяване на компонентите на теглото
- `HiveEvent`: Управление и ефекти на събитията

### 4. Обработка на грешки
- Логика за повторни опити при API комуникация
- Валидация на данните
- Проверка на граници
- Логване на изключения

### 5. Производителност
- Използване на памет: ~50MB
- Използване на процесор: Ниско
- Мрежов трафик: ~1KB на минута

## Принос към проекта

Приветстваме приноси! Моля, прочетете нашите указания за принос и изпратете вашите pull requests към нашето хранилище.

## Лиценз

Този проект е лицензиран под MIT License - вижте файла LICENSE за подробности.

## Благодарности

- Експертиза в пчеларството предоставена от BUZZWatch
- Метеорологични модели базирани на български метеорологични записи
- Модели на поведение на пчелите базирани на научни изследвания

---

*Последно обновяване: 21.02.2025*
*Версия: 1.0.0* 