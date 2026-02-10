"""
9 регуляционных контуров с вариантами реакции на триггер.

Структура: X-Y → (V, S, D)

X-Y = Контур (стабильная часть)
  X = Физиологическая доминанта
  Y = Внешняя презентация

→ V, S, D = Варианты реакции на триггер (переменная часть)

Это упрощает модель с 27 профилей до 9 контуров,
где каждый контур может давать 3 типа ответа в зависимости от триггера.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class CircuitType(Enum):
    """9 регуляционных контуров"""
    # Вентральная база
    V_V = "V-V"      # Вентральный-Вентральный
    V_S = "V-S"      # Вентральный-Симпатический
    V_D = "V-D"      # Вентральный-Дорсальный
    
    # Симпатическая база
    S_Vp = "S-V(p)"  # Симпатический-Псевдовентральный
    S_S = "S-S"      # Симпатический-Симпатический
    S_D = "S-D"      # Симпатический-Дорсальный
    
    # Дорсальная база
    D_Vp = "D-V(p)"  # Дорсальный-Псевдовентральный
    D_S = "D-S"      # Дорсальный-Симпатический
    D_D = "D-D"      # Дорсальный-Дорсальный


class ResponseType(Enum):
    """Типы реакции на триггер"""
    V = "V"  # Вентральный ответ (адаптивный)
    S = "S"  # Симпатический ответ (борьба/бегство)
    D = "D"  # Дорсальный ответ (замирание/коллапс)


@dataclass
class StressResponse:
    """Описание конкретной реакции на стресс"""
    response_type: ResponseType
    description: str
    clinical_meaning: str
    associated_disorders: List[str]
    prognosis: str  # "favorable", "moderate", "concerning"


@dataclass
class RegulatoryCircuit:
    """Регуляционный контур"""
    circuit_type: CircuitType
    name: str
    
    # Описание контура
    physiology: str           # X-компонент
    presentation: str         # Y-компонент
    core_dynamic: str         # Суть контура
    
    # Психологическое содержание
    inner_experience: str     # Что человек переживает внутри
    outer_appearance: str     # Как выглядит снаружи
    core_conflict: str        # Центральный конфликт (если есть)
    
    # Три варианта реакции
    response_to_V: StressResponse  # Если реакция вентральная
    response_to_S: StressResponse  # Если реакция симпатическая
    response_to_D: StressResponse  # Если реакция дорсальная
    
    # Что определяет, какая реакция будет
    triggers_for_V: List[str]  # При каких условиях V-ответ
    triggers_for_S: List[str]  # При каких условиях S-ответ
    triggers_for_D: List[str]  # При каких условиях D-ответ
    
    # Терапевтические заметки
    therapeutic_approach: str
    key_resources: List[str]
    key_vulnerabilities: List[str]
    
    def get_full_profile(self, response: ResponseType) -> str:
        """Получить полную формулу профиля"""
        return f"{self.circuit_type.value}-{response.value}"
    
    def get_response(self, response: ResponseType) -> StressResponse:
        """Получить описание конкретной реакции"""
        if response == ResponseType.V:
            return self.response_to_V
        elif response == ResponseType.S:
            return self.response_to_S
        else:
            return self.response_to_D


# ============================================================
# 9 РЕГУЛЯЦИОННЫХ КОНТУРОВ
# ============================================================

REGULATORY_CIRCUITS: Dict[CircuitType, RegulatoryCircuit] = {
    
    # ════════════════════════════════════════════════════════
    # ВЕНТРАЛЬНАЯ БАЗА (V-X) — есть физиологический ресурс
    # ════════════════════════════════════════════════════════
    
    CircuitType.V_V: RegulatoryCircuit(
        circuit_type=CircuitType.V_V,
        name="Интегрированный контур",
        
        physiology="Высокий вагусный тонус, хорошая вариабельность",
        presentation="Открытый, социально вовлечённый, эмоционально доступный",
        core_dynamic="Согласованность внутреннего и внешнего — то, что внутри, то и снаружи",
        
        inner_experience="Относительное спокойствие, доступ к эмоциям, ощущение безопасности",
        outer_appearance="Живая мимика, модулированный голос, комфортный контакт",
        core_conflict="Минимальный — система интегрирована",
        
        response_to_V=StressResponse(
            response_type=ResponseType.V,
            description="Сохраняет социальный контакт, ищет поддержку, регулируется через связь",
            clinical_meaning="Здоровая адаптивная реакция — мобилизует социальные ресурсы",
            associated_disorders=["Норма", "Лёгкая адаптационная тревога"],
            prognosis="favorable"
        ),
        response_to_S=StressResponse(
            response_type=ResponseType.S,
            description="Активируется, действует, борется с проблемой",
            clinical_meaning="Адекватная мобилизация при угрозе, если восстановление быстрое",
            associated_disorders=["Ситуативная тревога", "Адаптивный стресс"],
            prognosis="favorable"
        ),
        response_to_D=StressResponse(
            response_type=ResponseType.D,
            description="Отключается, замирает, уходит в себя",
            clinical_meaning="Указывает на специфический травматический триггер, обходящий регуляцию",
            associated_disorders=["ПТСР (специфический триггер)", "Диссоциативная реакция"],
            prognosis="moderate"
        ),
        
        triggers_for_V=["Умеренный стресс", "Наличие поддержки", "Знакомая ситуация"],
        triggers_for_S=["Угроза, требующая действия", "Несправедливость", "Защита близких"],
        triggers_for_D=["Специфическая травма", "Непереносимый аффект", "Триггер ранней травмы"],
        
        therapeutic_approach="Поддерживающая терапия, развитие ресурсов, работа со специфическими триггерами при D-реакции",
        key_resources=["Социальная связь", "Телесная осознанность", "Эмоциональная гибкость"],
        key_vulnerabilities=["Специфические триггеры (индивидуальны)"]
    ),
    
    CircuitType.V_S: RegulatoryCircuit(
        circuit_type=CircuitType.V_S,
        name="Тревожная маска на здоровой базе",
        
        physiology="Хороший вагусный тонус в покое",
        presentation="Выглядит тревожным, напряжённым, беспокойным",
        core_dynamic="Внутри спокойнее, чем снаружи — выученный тревожный стиль",
        
        inner_experience="Базовое спокойствие, но привычка беспокоиться",
        outer_appearance="Суета, напряжение, \"надо всё контролировать\"",
        core_conflict="Разрешение на спокойствие vs выученное \"опасно расслабляться\"",
        
        response_to_V=StressResponse(
            response_type=ResponseType.V,
            description="Парадоксально успокаивается в кризисе, берёт себя в руки",
            clinical_meaning="Ресурс активируется при реальной угрозе — \"собирается\"",
            associated_disorders=["Скрытая компетентность", "Адаптивная тревога"],
            prognosis="favorable"
        ),
        response_to_S=StressResponse(
            response_type=ResponseType.S,
            description="Усиление тревоги, ажитация, паника",
            clinical_meaning="Тревожный стиль становится дезадаптивным при перегрузке",
            associated_disorders=["ГТР", "Панические атаки", "ОКР"],
            prognosis="moderate"
        ),
        response_to_D=StressResponse(
            response_type=ResponseType.D,
            description="Тревога → истощение → отключение",
            clinical_meaning="Паттерн перегрузки: сначала паника, потом коллапс",
            associated_disorders=["Тревожно-диссоциативное расстройство", "Конверсия"],
            prognosis="concerning"
        ),
        
        triggers_for_V=["Реальный кризис", "Когда нужно действовать", "Ответственность за других"],
        triggers_for_S=["Неопределённость", "Мелкие бытовые стрессоры", "Критика"],
        triggers_for_D=["Длительное напряжение", "Невозможность контролировать", "Истощение"],
        
        therapeutic_approach="Работа с убеждениями о тревоге, разрешение на спокойствие, экспозиция к расслаблению",
        key_resources=["Компетентность в кризисе", "Базовый вагусный тонус"],
        key_vulnerabilities=["Выученная тревога", "\"Опасно расслабляться\"", "Риск истощения"]
    ),
    
    CircuitType.V_D: RegulatoryCircuit(
        circuit_type=CircuitType.V_D,
        name="Изоляция при ресурсе",
        
        physiology="Хороший вагусный тонус",
        presentation="Отстранённый, закрытый, эмоционально недоступный",
        core_dynamic="Внутри есть ресурс, но снаружи — стена",
        
        inner_experience="Относительное спокойствие, богатый внутренний мир",
        outer_appearance="Холодность, дистанция, \"ему всё равно\"",
        core_conflict="Потребность в связи vs страх близости/поглощения",
        
        response_to_V=StressResponse(
            response_type=ResponseType.V,
            description="Раскрывается, становится живым, включается",
            clinical_meaning="Стена падает при безопасности или необходимости",
            associated_disorders=["Здоровая интроверсия", "Шизоидная адаптация (компенсированная)"],
            prognosis="favorable"
        ),
        response_to_S=StressResponse(
            response_type=ResponseType.S,
            description="Резкая агрессивная активация, \"взрыв\"",
            clinical_meaning="Прорыв подавленного через стену — непредсказуемо для окружающих",
            associated_disorders=["Пассивно-агрессивное", "ПТСР с онемением"],
            prognosis="moderate"
        ),
        response_to_D=StressResponse(
            response_type=ResponseType.D,
            description="Углубление ухода, полная изоляция",
            clinical_meaning="Защитная стена становится тюрьмой",
            associated_disorders=["Шизоидное расстройство", "Депрессия", "Деперсонализация"],
            prognosis="concerning"
        ),
        
        triggers_for_V=["Безопасная близость", "Необходимость помочь", "Творчество"],
        triggers_for_S=["Вторжение в границы", "Угроза автономии", "Накопленная фрустрация"],
        triggers_for_D=["Требование близости", "Эмоциональное давление", "Разочарование в людях"],
        
        therapeutic_approach="Медленное построение связи, уважение к границам, работа со страхом поглощения",
        key_resources=["Внутренний мир", "Автономия", "Базовая регуляция"],
        key_vulnerabilities=["Изоляция", "Страх близости", "Накопление эмоций"]
    ),
    
    # ════════════════════════════════════════════════════════
    # СИМПАТИЧЕСКАЯ БАЗА (S-X) — хроническая активация
    # ════════════════════════════════════════════════════════
    
    CircuitType.S_Vp: RegulatoryCircuit(
        circuit_type=CircuitType.S_Vp,
        name="Псевдо-адаптация (маска)",
        
        physiology="Симпатическая активация — тело в режиме угрозы",
        presentation="Выглядит спокойным, социально успешным (ПСЕВДО)",
        core_dynamic="Внутри — тревога, снаружи — маска благополучия",
        
        inner_experience="Напряжение, гипервигильность, \"держу лицо\"",
        outer_appearance="Улыбается, справляется, \"у меня всё хорошо\"",
        core_conflict="Истинное Я vs социальная маска, страх разоблачения",
        
        response_to_V=StressResponse(
            response_type=ResponseType.V,
            description="Сохраняет маску даже под давлением",
            clinical_meaning="Высокая цена адаптации — истощение ресурсов на поддержание фасада",
            associated_disorders=["Высокофункциональная тревога", "Нарциссизм (компенсаторный)"],
            prognosis="moderate"
        ),
        response_to_S=StressResponse(
            response_type=ResponseType.S,
            description="Маска спадает — проявляется реальная тревога",
            clinical_meaning="\"Срыв\" — окружающие удивлены, человек стыдится",
            associated_disorders=["Паническое расстройство", "Социальная фобия", "Импостор-синдром"],
            prognosis="moderate"
        ),
        response_to_D=StressResponse(
            response_type=ResponseType.D,
            description="Внезапный коллапс из-под маски",
            clinical_meaning="Самый опасный вариант — декомпенсация \"на ровном месте\"",
            associated_disorders=["ПТСР", "Диссоциативное расстройство", "Суицидальный кризис"],
            prognosis="concerning"
        ),
        
        triggers_for_V=["Привычные ситуации", "Поддержка близких", "Контролируемый стресс"],
        triggers_for_S=["Публичное выступление", "Оценка", "Невозможность подготовиться"],
        triggers_for_D=["Разоблачение", "Потеря статуса", "Предательство", "Триггер травмы"],
        
        therapeutic_approach="Работа с Ложным Я, разрешение на уязвимость, снятие маски в безопасности",
        key_resources=["Социальная компетентность", "Мотивация к изменению"],
        key_vulnerabilities=["Истощение", "Страх разоблачения", "Соматизация", "Риск внезапного срыва"]
    ),
    
    CircuitType.S_S: RegulatoryCircuit(
        circuit_type=CircuitType.S_S,
        name="Когерентная тревога",
        
        physiology="Симпатическая активация",
        presentation="Открыто тревожный, напряжённый",
        core_dynamic="Внутри тревога — снаружи тревога — честный паттерн",
        
        inner_experience="Беспокойство, напряжение, ожидание угрозы",
        outer_appearance="Нервозность, суетливость, телесное напряжение",
        core_conflict="Потребность в безопасности vs восприятие мира как опасного",
        
        response_to_V=StressResponse(
            response_type=ResponseType.V,
            description="Собирается, находит ресурс, справляется",
            clinical_meaning="Скрытый ресурс — человек недооценивает себя",
            associated_disorders=["Тревога с хорошим прогнозом", "Зависимое расстройство"],
            prognosis="favorable"
        ),
        response_to_S=StressResponse(
            response_type=ResponseType.S,
            description="Эскалация тревоги, паника, ажитация",
            clinical_meaning="Классический тревожный ответ — усиление того, что уже есть",
            associated_disorders=["ГТР", "Паническое расстройство", "ОКР", "Фобии"],
            prognosis="moderate"
        ),
        response_to_D=StressResponse(
            response_type=ResponseType.D,
            description="Тревога → истощение → коллапс",
            clinical_meaning="Паттерн выгорания: борьба-борьба-сдавайся",
            associated_disorders=["ПТСР", "Смешанное тревожно-депрессивное", "Конверсия"],
            prognosis="concerning"
        ),
        
        triggers_for_V=["Поддержка", "Структура", "Успешный опыт", "Реальный кризис"],
        triggers_for_S=["Неопределённость", "Потеря контроля", "Критика", "Ожидание"],
        triggers_for_D=["Длительный стресс без выхода", "Беспомощность", "Травматический триггер"],
        
        therapeutic_approach="КПТ, экспозиция, развитие толерантности к неопределённости, заземление",
        key_resources=["Честность с собой", "Мотивация к изменению", "Скрытая компетентность"],
        key_vulnerabilities=["Избегание", "Ритуализация", "Соматизация", "Выгорание"]
    ),
    
    CircuitType.S_D: RegulatoryCircuit(
        circuit_type=CircuitType.S_D,
        name="Замороженная тревога",
        
        physiology="Симпатическая активация — тело \"знает\" об угрозе",
        presentation="Отстранённый, пассивный, \"выключенный\"",
        core_dynamic="Внутри тревога, снаружи — оцепенение",
        
        inner_experience="Телесное напряжение, которое не осознаётся как тревога",
        outer_appearance="Апатия, безразличие, \"ничего не хочу\"",
        core_conflict="Тело сигнализирует об угрозе, но психика \"отключила звук\"",
        
        response_to_V=StressResponse(
            response_type=ResponseType.V,
            description="Размораживается, включается, оживает",
            clinical_meaning="Под льдом есть жизнь — ресурс заблокирован, но не уничтожен",
            associated_disorders=["Выученная беспомощность (обратимая)"],
            prognosis="favorable"
        ),
        response_to_S=StressResponse(
            response_type=ResponseType.S,
            description="Тревога прорывается — паника, flashbacks",
            clinical_meaning="Подавленное возвращается — непредсказуемо и интенсивно",
            associated_disorders=["ПТСР", "Скрытое паническое расстройство"],
            prognosis="moderate"
        ),
        response_to_D=StressResponse(
            response_type=ResponseType.D,
            description="Углубление отключения, уход в тотальный shutdown",
            clinical_meaning="Диссоциация от диссоциации — глубокое замораживание",
            associated_disorders=["Комплексный ПТСР", "Хронические боли", "Фибромиалгия"],
            prognosis="concerning"
        ),
        
        triggers_for_V=["Безопасная активация", "Соматическая работа", "Постепенное оттаивание"],
        triggers_for_S=["Специфические триггеры травмы", "Телесные ощущения", "Flashbacks"],
        triggers_for_D=["Требование чувствовать", "Давление", "Повторная травма"],
        
        therapeutic_approach="Соматическая терапия, мягкая активация, работа с телом, безопасность",
        key_resources=["Тело помнит ресурс", "Способность отключаться (была адаптивной)"],
        key_vulnerabilities=["Алекситимия", "Соматизация", "Хронические боли", "Ретравматизация"]
    ),
    
    # ════════════════════════════════════════════════════════
    # ДОРСАЛЬНАЯ БАЗА (D-X) — хронический shutdown
    # ════════════════════════════════════════════════════════
    
    CircuitType.D_Vp: RegulatoryCircuit(
        circuit_type=CircuitType.D_Vp,
        name="Функциональный автомат",
        
        physiology="Дорсальное доминирование — низкая вариабельность, \"плоский\" ритм",
        presentation="Выглядит адаптированным, социально функционирует (ПСЕВДО)",
        core_dynamic="Внутри — пустота, снаружи — нормальная жизнь",
        
        inner_experience="Деперсонализация, \"смотрю фильм о себе\", \"ничего не чувствую\"",
        outer_appearance="Делает всё правильно, улыбается, справляется",
        core_conflict="Быть vs казаться, живой vs мёртвый внутри",
        
        response_to_V=StressResponse(
            response_type=ResponseType.V,
            description="Сохраняет функционирование, \"автопилот работает\"",
            clinical_meaning="Адаптация без присутствия — опасная стабильность",
            associated_disorders=["Деперсонализационное расстройство", "Маскированная депрессия"],
            prognosis="moderate"
        ),
        response_to_S=StressResponse(
            response_type=ResponseType.S,
            description="Прорыв тревоги/паники из-под маски",
            clinical_meaning="\"Пустота\" заполняется ужасом — декомпенсация",
            associated_disorders=["Панические атаки", "ПТСР", "Острая тревога"],
            prognosis="concerning"
        ),
        response_to_D=StressResponse(
            response_type=ResponseType.D,
            description="Углубление отключения, потеря функционирования",
            clinical_meaning="Автопилот выключается — тотальный коллапс",
            associated_disorders=["Тяжёлая депрессия", "Диссоциативный ступор", "Суицидальность"],
            prognosis="concerning"
        ),
        
        triggers_for_V=["Рутина", "Структура", "Отсутствие сильных стимулов"],
        triggers_for_S=["Угроза разоблачения пустоты", "Требование подлинности", "Intimacy"],
        triggers_for_D=["Потеря структуры", "Болезнь", "Одиночество", "Экзистенциальные вопросы"],
        
        therapeutic_approach="Очень медленно, фокус на ощущениях, микро-контакт с чувствами",
        key_resources=["Функциональность", "Интеллект", "Социальные навыки"],
        key_vulnerabilities=["Пустота", "Суицидальность без видимых причин", "Внезапный срыв"]
    ),
    
    CircuitType.D_S: RegulatoryCircuit(
        circuit_type=CircuitType.D_S,
        name="Ажитированная депрессия",
        
        physiology="Дорсальное доминирование, но с тревожной надстройкой",
        presentation="Беспокойный, раздражительный, дисфоричный",
        core_dynamic="Внутри — пустота, снаружи — суета как защита от неё",
        
        inner_experience="\"Не могу остановиться, иначе провалюсь\"",
        outer_appearance="Тревожный, раздражительный, не может расслабиться",
        core_conflict="Бежать от пустоты vs остановиться и встретить её",
        
        response_to_V=StressResponse(
            response_type=ResponseType.V,
            description="Успокаивается, находит опору",
            clinical_meaning="Под тревогой есть ресурс — защитная тревога снимается",
            associated_disorders=["Тревога как защита от депрессии"],
            prognosis="favorable"
        ),
        response_to_S=StressResponse(
            response_type=ResponseType.S,
            description="Эскалация ажитации, усиление беспокойства",
            clinical_meaning="Ажитированная депрессия — высокий суицидальный риск!",
            associated_disorders=["Ажитированная депрессия", "Смешанное состояние"],
            prognosis="concerning"
        ),
        response_to_D=StressResponse(
            response_type=ResponseType.D,
            description="Коллапс — ажитация сменяется ступором",
            clinical_meaning="\"Батарейка села\" — истощение защитной тревоги",
            associated_disorders=["Тяжёлая депрессия", "Кататония"],
            prognosis="concerning"
        ),
        
        triggers_for_V=["Надёжная поддержка", "Медикаменты", "Структура"],
        triggers_for_S=["Одиночество", "Ночь", "Руминация", "Бессонница"],
        triggers_for_D=["Истощение", "Отказ защит", "Госпитализация"],
        
        therapeutic_approach="Стабилизация, антидепрессанты, снижение ажитации, безопасность!",
        key_resources=["Энергия (хоть и деструктивная)", "Способность просить помощь"],
        key_vulnerabilities=["ВЫСОКИЙ СУИЦИДАЛЬНЫЙ РИСК", "Импульсивность", "Бессонница"]
    ),
    
    CircuitType.D_D: RegulatoryCircuit(
        circuit_type=CircuitType.D_D,
        name="Глубокий shutdown",
        
        physiology="Глубокое дорсальное доминирование — система \"выключена\"",
        presentation="Отстранённый, безжизненный, \"пустой\"",
        core_dynamic="Внутри и снаружи — одно: отсутствие",
        
        inner_experience="Пустота, отсутствие желаний, \"зачем всё это\"",
        outer_appearance="Заторможенный, безынициативный, \"живой труп\"",
        core_conflict="Быть vs не быть — экзистенциальный уровень",
        
        response_to_V=StressResponse(
            response_type=ResponseType.V,
            description="Проблеск жизни, включение, контакт",
            clinical_meaning="Есть скрытый ресурс — важно его заметить и поддержать",
            associated_disorders=["Депрессия с потенциалом восстановления"],
            prognosis="moderate"
        ),
        response_to_S=StressResponse(
            response_type=ResponseType.S,
            description="Прорыв тревоги или агрессии",
            clinical_meaning="Энергия возвращается — это может быть началом выхода",
            associated_disorders=["Депрессия с тревожными эпизодами"],
            prognosis="moderate"
        ),
        response_to_D=StressResponse(
            response_type=ResponseType.D,
            description="Углубление shutdown, ступор",
            clinical_meaning="Нет сил даже на суицид — парадоксальная \"защита\"",
            associated_disorders=["Тяжёлая депрессия", "Кататония", "Диссоциативный ступор"],
            prognosis="concerning"
        ),
        
        triggers_for_V=["Безопасная связь", "Соматическая стимуляция", "Микро-активация"],
        triggers_for_S=["Угроза близким", "Несправедливость", "Возвращение энергии"],
        triggers_for_D=["Одиночество", "Отвержение", "Подтверждение бессмысленности"],
        
        therapeutic_approach="Госпитализация при необходимости, медикаменты, мягкое присутствие, телесная активация",
        key_resources=["Способность отключаться (сохранила жизнь)", "Внутренний наблюдатель"],
        key_vulnerabilities=["Суицид при возвращении энергии", "Хронификация", "Соматические осложнения"]
    ),
}


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def get_circuit(circuit_type: CircuitType) -> RegulatoryCircuit:
    """Получить контур по типу"""
    return REGULATORY_CIRCUITS[circuit_type]


def get_circuit_by_formula(formula: str) -> Optional[RegulatoryCircuit]:
    """Получить контур по формуле X-Y"""
    for circuit_type, circuit in REGULATORY_CIRCUITS.items():
        if circuit_type.value == formula:
            return circuit
    return None


def get_all_circuits() -> Dict[CircuitType, RegulatoryCircuit]:
    """Получить все контуры"""
    return REGULATORY_CIRCUITS


def print_circuit_summary(circuit: RegulatoryCircuit) -> str:
    """Краткое описание контура"""
    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
*{circuit.circuit_type.value}: {circuit.name}*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Суть:* {circuit.core_dynamic}

*Внутри:* {circuit.inner_experience}
*Снаружи:* {circuit.outer_appearance}

*Конфликт:* {circuit.core_conflict}

┌─────────────────────────────────────────────────────────┐
│ РЕАКЦИЯ НА ТРИГГЕР                                      │
├─────────────────────────────────────────────────────────┤
│ → V: {circuit.response_to_V.description[:50]}...        │
│   Прогноз: {circuit.response_to_V.prognosis}           │
├─────────────────────────────────────────────────────────┤
│ → S: {circuit.response_to_S.description[:50]}...        │
│   Прогноз: {circuit.response_to_S.prognosis}           │
├─────────────────────────────────────────────────────────┤
│ → D: {circuit.response_to_D.description[:50]}...        │
│   Прогноз: {circuit.response_to_D.prognosis}           │
└─────────────────────────────────────────────────────────┘

*Ресурсы:* {', '.join(circuit.key_resources)}
*Уязвимости:* {', '.join(circuit.key_vulnerabilities)}
*Терапия:* {circuit.therapeutic_approach}
"""


def get_circuit_matrix() -> str:
    """Матрица всех контуров"""
    matrix = """
    ┌───────────────────────────────────────────────────────────────────────┐
    │                    9 РЕГУЛЯЦИОННЫХ КОНТУРОВ                           │
    │                                                                       │
    │              Презентация (Y)                                         │
    │              V(ентрал)    S(импат)     D(орсал)                       │
    │         ┌────────────┬────────────┬────────────┐                     │
    │    V    │   V-V      │   V-S      │   V-D      │ ← Есть ресурс       │
    │  Ф      │ Интегриро- │ Тревожная  │ Изоляция   │                     │
    │  и      │ ванный     │ маска      │ при ресур- │                     │
    │  з      │            │            │ се         │                     │
    │  и      ├────────────┼────────────┼────────────┤                     │
    │  о S    │  S-V(p)    │   S-S      │   S-D      │ ← Хронич. активация │
    │  л      │ Псевдо-    │ Когерент-  │ Заморожен- │                     │
    │  о      │ адаптация  │ ная тревога│ ная тревога│                     │
    │  г      │ (МАСКА)    │            │            │                     │
    │  и      ├────────────┼────────────┼────────────┤                     │
    │  я D    │  D-V(p)    │   D-S      │   D-D      │ ← Хронич. shutdown  │
    │ (X)     │ Функцион.  │ Ажитиров.  │ Глубокий   │                     │
    │         │ автомат    │ депрессия  │ shutdown   │                     │
    │         │ (МАСКА)    │            │            │                     │
    │         └────────────┴────────────┴────────────┘                     │
    │                                                                       │
    │    Каждый контур → 3 варианта реакции на триггер: V, S, D            │
    └───────────────────────────────────────────────────────────────────────┘
    """
    return matrix
