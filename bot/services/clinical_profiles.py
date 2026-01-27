"""
Клиническая карта вагусных профилей.

Все возможные комбинации формулы X-Y-Z и их связь с психопатологией.

X = Физиологическая доминанта (что показывает HRV)
Y = Внешняя презентация (как выглядит со стороны)
Z = Реакция на стресс (куда проваливается)

V = Вентральный (социальная вовлечённость)
S = Симпатический (борьба/бегство)
D = Дорсальный (замирание/shutdown)

(p) = pseudo — внешняя презентация не соответствует физиологии
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class ClinicalCategory(Enum):
    """Категории клинических проявлений"""
    ANXIETY = "Тревожный спектр"
    DEPRESSION = "Депрессивный спектр"
    DISSOCIATION = "Диссоциативный спектр"
    PSYCHOSOMATIC = "Психосоматика"
    OCD = "Обсессивно-компульсивный спектр"
    NARCISSISTIC = "Нарциссический спектр"
    BORDERLINE = "Пограничный спектр"
    AVOIDANT = "Избегающий спектр"
    DEPENDENT = "Зависимый спектр"
    TRAUMA = "Травматический спектр"
    ADAPTIVE = "Адаптивное функционирование"


@dataclass
class ClinicalProfile:
    """Клинический профиль с симптоматикой"""
    formula: str
    name: str
    description: str
    
    # Основные характеристики
    physiology: str           # Описание физиологии
    presentation: str         # Описание презентации
    stress_response: str      # Описание реакции на стресс
    
    # Клинические корреляты
    primary_categories: List[ClinicalCategory]
    secondary_categories: List[ClinicalCategory]
    
    # Симптоматика
    likely_symptoms: List[str]
    hidden_symptoms: List[str]  # Что может быть "спрятано"
    
    # Защитные механизмы
    defense_mechanisms: List[str]
    
    # Риски
    risks: List[str]
    
    # Терапевтические заметки
    therapeutic_focus: str
    
    # Частота встречаемости (субъективная оценка)
    prevalence: str  # "common", "moderate", "rare"


# ============================================================
# ВСЕ 27 ПРОФИЛЕЙ + ПСЕВДО-ВАРИАНТЫ
# ============================================================

CLINICAL_PROFILES = {
    
    # ========================================
    # ВЕНТРАЛЬНАЯ ДОМИНАНТА (V-X-X)
    # ========================================
    
    "V-V-V": ClinicalProfile(
        formula="V-V-V",
        name="Интегрированный адаптивный",
        description="""
        Редкий "идеальный" профиль. Физиология, презентация и стресс-ответ согласованы
        в вентральном режиме. Человек действительно спокоен, выглядит спокойным и при
        стрессе сохраняет способность к социальному контакту и регуляции.
        """,
        physiology="Высокий вагусный тонус, хорошая вариабельность",
        presentation="Открытый, социально вовлечённый, эмоционально доступный",
        stress_response="Умеренная активация с быстрым возвратом к спокойствию",
        
        primary_categories=[ClinicalCategory.ADAPTIVE],
        secondary_categories=[],
        
        likely_symptoms=[
            "Адекватная тревога в ситуациях реальной угрозы",
            "Способность к горю и восстановлению",
            "Гибкость эмоционального реагирования"
        ],
        hidden_symptoms=[
            "При определённых триггерах (Ta, Ti и др.) может показывать уязвимость",
            "Возможна 'слепая зона' — непроработанная травма в одной области"
        ],
        
        defense_mechanisms=["Зрелые: сублимация, юмор, альтруизм"],
        risks=["Низкий риск патологии при отсутствии тяжёлой травмы"],
        therapeutic_focus="Поддержание ресурсов, профилактика, развитие",
        prevalence="rare"
    ),
    
    "V-V-S": ClinicalProfile(
        formula="V-V-S",
        name="Адаптивный с тревожной реактивностью",
        description="""
        Хорошая база, но при стрессе включается симпатика. Это может быть нормальной
        реакцией на угрозу, если восстановление быстрое. При медленном восстановлении —
        склонность к тревожным реакциям.
        """,
        physiology="Хороший вагусный тонус в покое",
        presentation="Социально адаптирован, открыт",
        stress_response="Борьба/бегство — тревога, возбуждение, потребность действовать",
        
        primary_categories=[ClinicalCategory.ADAPTIVE, ClinicalCategory.ANXIETY],
        secondary_categories=[],
        
        likely_symptoms=[
            "Ситуативная тревога",
            "Гиперответственность",
            "Потребность контролировать ситуацию при стрессе",
            "Раздражительность при невозможности действовать"
        ],
        hidden_symptoms=[
            "Генерализованное тревожное расстройство (при хроническом стрессе)",
            "Панические атаки (при сильных триггерах)"
        ],
        
        defense_mechanisms=["Рационализация", "Компенсация", "Действие"],
        risks=["Выгорание при хроническом стрессе", "Переход в S-доминанту"],
        therapeutic_focus="Развитие толерантности к неопределённости, навыки релаксации",
        prevalence="common"
    ),
    
    "V-V-D": ClinicalProfile(
        formula="V-V-D",
        name="Адаптивный с диссоциативной реактивностью",
        description="""
        Парадоксальный профиль: хорошая база, но при сильном стрессе — дорсальный
        коллапс. Указывает на специфический травматический триггер, который
        "обходит" обычную регуляцию.
        """,
        physiology="Хороший вагусный тонус в покое",
        presentation="Социально адаптирован",
        stress_response="Замирание, оцепенение, уход в себя",
        
        primary_categories=[ClinicalCategory.TRAUMA, ClinicalCategory.DISSOCIATION],
        secondary_categories=[ClinicalCategory.ADAPTIVE],
        
        likely_symptoms=[
            "Внезапное 'отключение' при специфических триггерах",
            "Чувство нереальности в стрессе",
            "Эмоциональное онемение при угрозе",
            "Трудности с запоминанием травматических событий"
        ],
        hidden_symptoms=[
            "Диссоциативное расстройство",
            "ПТСР с диссоциативными симптомами",
            "Конверсионные симптомы"
        ],
        
        defense_mechanisms=["Диссоциация", "Отрицание", "Изоляция аффекта"],
        risks=["Ретравматизация", "Углубление диссоциации"],
        therapeutic_focus="Работа с травмой, заземление, окно толерантности",
        prevalence="moderate"
    ),
    
    "V-S-V": ClinicalProfile(
        formula="V-S-V",
        name="Скрытое спокойствие",
        description="""
        Физиологически спокоен, но презентует тревожно. При стрессе возвращается
        к вентральному. Возможно: выученный тревожный стиль, или гиперкомпенсация,
        или культурная норма ("надо беспокоиться").
        """,
        physiology="Хороший вагусный тонус",
        presentation="Выглядит тревожным, суетливым, напряжённым",
        stress_response="Парадоксально успокаивается, берёт себя в руки",
        
        primary_categories=[ClinicalCategory.ANXIETY],
        secondary_categories=[ClinicalCategory.ADAPTIVE],
        
        likely_symptoms=[
            "Хроническое беспокойство 'на ровном месте'",
            "Трудности с расслаблением в безопасности",
            "Собранность в кризисе",
            "'Лучше работаю под давлением'"
        ],
        hidden_symptoms=[
            "Генерализованная тревога как привычка",
            "Скрытая компетентность"
        ],
        
        defense_mechanisms=["Антиципация", "Гиперконтроль", "Ритуализация"],
        risks=["Психосоматика от хронического напряжения"],
        therapeutic_focus="Разрешение на спокойствие, работа с убеждениями о тревоге",
        prevalence="moderate"
    ),
    
    "V-S-S": ClinicalProfile(
        formula="V-S-S",
        name="Тревожная презентация",
        description="""
        Вентральная база, но тревожная презентация и реакция. Физиология говорит
        о ресурсе, но поведенчески человек в тревоге.
        """,
        physiology="Хороший базовый тонус",
        presentation="Напряжённый, беспокойный",
        stress_response="Усиление тревоги, ажитация",
        
        primary_categories=[ClinicalCategory.ANXIETY],
        secondary_categories=[ClinicalCategory.OCD],
        
        likely_symptoms=[
            "Генерализованная тревога",
            "Социальная тревожность",
            "Обсессивное беспокойство",
            "Физическое напряжение при эмоциональном ресурсе"
        ],
        hidden_symptoms=[
            "ОКР (как способ управлять тревогой)",
            "Ипохондрия"
        ],
        
        defense_mechanisms=["Контроль", "Изоляция аффекта", "Интеллектуализация"],
        risks=["Хронификация тревоги", "Развитие ОКР"],
        therapeutic_focus="Экспозиция, принятие неопределённости",
        prevalence="common"
    ),
    
    "V-S-D": ClinicalProfile(
        formula="V-S-D",
        name="Тревожно-диссоциативный",
        description="""
        Ресурсная база, тревожная презентация, но при перегрузке — shutdown.
        Паттерн: тревога-тревога-коллапс.
        """,
        physiology="Хороший базовый тонус",
        presentation="Напряжённый, беспокойный",
        stress_response="При превышении порога — замирание, отключение",
        
        primary_categories=[ClinicalCategory.ANXIETY, ClinicalCategory.DISSOCIATION],
        secondary_categories=[ClinicalCategory.TRAUMA],
        
        likely_symptoms=[
            "Тревога, переходящая в ступор",
            "Паника → диссоциация",
            "'Застреваю' при принятии решений",
            "Прокрастинация как замирание"
        ],
        hidden_symptoms=[
            "Смешанное тревожно-диссоциативное расстройство",
            "Обморочные состояния при тревоге"
        ],
        
        defense_mechanisms=["Тревожный контроль → диссоциация"],
        risks=["Конверсионные симптомы", "Панические атаки с обмороком"],
        therapeutic_focus="Расширение окна толерантности, работа с порогом перегрузки",
        prevalence="moderate"
    ),
    
    "V-D-V": ClinicalProfile(
        formula="V-D-V",
        name="Маска отстранённости",
        description="""
        Внутри спокоен, снаружи отстранён, при стрессе — адекватен.
        Возможно: интроверсия, шизоидная адаптация, или защита от близости.
        """,
        physiology="Хороший вагусный тонус",
        presentation="Отстранённый, эмоционально закрытый",
        stress_response="Включается, становится более живым",
        
        primary_categories=[ClinicalCategory.AVOIDANT],
        secondary_categories=[ClinicalCategory.ADAPTIVE],
        
        likely_symptoms=[
            "Предпочтение одиночества",
            "Трудности с эмоциональной близостью",
            "Оживление в кризисе",
            "'Холодность' в обычной жизни"
        ],
        hidden_symptoms=[
            "Шизоидная адаптация",
            "Высокофункциональный аутизм"
        ],
        
        defense_mechanisms=["Изоляция", "Интеллектуализация", "Уход"],
        risks=["Социальная изоляция", "Непонимание окружающими"],
        therapeutic_focus="Постепенное развитие эмоциональной близости",
        prevalence="rare"
    ),
    
    "V-D-S": ClinicalProfile(
        formula="V-D-S",
        name="Спящий воин",
        description="""
        Внутри ресурс, снаружи — отстранение, при стрессе — борьба.
        Человек 'выключен' в обычной жизни, но активируется при угрозе.
        """,
        physiology="Хороший базовый тонус",
        presentation="Отстранённый, 'отключённый'",
        stress_response="Резкая активация, борьба/бегство",
        
        primary_categories=[ClinicalCategory.AVOIDANT, ClinicalCategory.TRAUMA],
        secondary_categories=[],
        
        likely_symptoms=[
            "Эмоциональная плоскость в покое",
            "Взрывная реактивность при угрозе",
            "'Ни рыба ни мясо' → резкая агрессия",
            "Гипервигильность за маской безразличия"
        ],
        hidden_symptoms=[
            "ПТСР с эмоциональным онемением",
            "Пассивно-агрессивное расстройство"
        ],
        
        defense_mechanisms=["Отстранение", "Подавление", "Реактивное образование"],
        risks=["Внезапные вспышки", "Непредсказуемость для окружающих"],
        therapeutic_focus="Интеграция агрессии, безопасное выражение эмоций",
        prevalence="rare"
    ),
    
    "V-D-D": ClinicalProfile(
        formula="V-D-D",
        name="Глубокая изоляция",
        description="""
        Физиологический ресурс есть, но и презентация, и реакция — дорсальные.
        Человек 'ушёл в себя' при наличии возможности выйти.
        """,
        physiology="Сохранный вагусный тонус",
        presentation="Отстранённый, эмоционально недоступный",
        stress_response="Углубление отстранения, shutdown",
        
        primary_categories=[ClinicalCategory.AVOIDANT, ClinicalCategory.DEPRESSION],
        secondary_categories=[ClinicalCategory.DISSOCIATION],
        
        likely_symptoms=[
            "Глубокая интроверсия",
            "Ангедония",
            "Трудности с мотивацией",
            "Чувство 'наблюдателя жизни'"
        ],
        hidden_symptoms=[
            "Маскированная депрессия",
            "Деперсонализация",
            "Шизоидное расстройство"
        ],
        
        defense_mechanisms=["Изоляция", "Уход", "Схизоидная фантазия"],
        risks=["Социальная изоляция", "Суицидальность без видимых признаков"],
        therapeutic_focus="Мягкая активация, развитие связи с телом и другими",
        prevalence="rare"
    ),
    
    # ========================================
    # СИМПАТИЧЕСКАЯ ДОМИНАНТА (S-X-X)
    # ========================================
    
    "S-V(p)-V": ClinicalProfile(
        formula="S-V(p)-V",
        name="Псевдо-спокойный тревожный",
        description="""
        Физиологически в симпатике, но выглядит и реагирует вентрально.
        Высокий уровень маскировки. Истощает себя, играя спокойствие.
        """,
        physiology="Симпатическая активация в покое",
        presentation="Внешне спокойный, социально адаптированный (ПСЕВДО)",
        stress_response="Сохраняет маску спокойствия",
        
        primary_categories=[ClinicalCategory.ANXIETY, ClinicalCategory.NARCISSISTIC],
        secondary_categories=[ClinicalCategory.PSYCHOSOMATIC],
        
        likely_symptoms=[
            "Скрытая тревога за фасадом",
            "Психосоматика (тело 'выдаёт')",
            "Истощение от поддержания образа",
            "Перфекционизм"
        ],
        hidden_symptoms=[
            "Высокофункциональная тревога",
            "Скрытые панические атаки",
            "Психосоматические расстройства",
            "Нарциссическое расстройство (компенсаторный тип)"
        ],
        
        defense_mechanisms=["Компенсация", "Подавление", "Формирование реакции"],
        risks=["Внезапный срыв", "Соматизация", "Выгорание"],
        therapeutic_focus="Разрешение на уязвимость, работа с перфекционизмом",
        prevalence="common"
    ),
    
    "S-V(p)-S": ClinicalProfile(
        formula="S-V(p)-S",
        name="Псевдо-адаптация с тревогой",
        description="""
        Классическая 'утиная' модель: сверху спокойно плывёт, под водой лапками
        молотит. При стрессе маска спадает — проявляется реальная тревога.
        """,
        physiology="Симпатическая активация",
        presentation="Внешне собранный (ПСЕВДО)",
        stress_response="Тревога, паника, возбуждение",
        
        primary_categories=[ClinicalCategory.ANXIETY],
        secondary_categories=[ClinicalCategory.NARCISSISTIC, ClinicalCategory.PSYCHOSOMATIC],
        
        likely_symptoms=[
            "Тревожное расстройство за фасадом компетентности",
            "Панические атаки",
            "Социальная тревога с маскировкой",
            "Импостор-синдром"
        ],
        hidden_symptoms=[
            "Паническое расстройство",
            "Социальная фобия",
            "Психосоматика",
            "Скрытая агорафобия"
        ],
        
        defense_mechanisms=["Компенсация", "Реактивное образование", "Контроль"],
        risks=["Публичный срыв", "Панические атаки", "Избегание"],
        therapeutic_focus="Интеграция тревоги, отказ от маски",
        prevalence="common"
    ),
    
    "S-V(p)-D": ClinicalProfile(
        formula="S-V(p)-D",
        name="Псевдо-адаптация с коллапсом",
        description="""
        Самый 'опасный' псевдо-профиль. Внешне адаптирован, внутри тревога,
        при перегрузке — полный коллапс. Высокий риск острых состояний.
        """,
        physiology="Симпатическая активация",
        presentation="Внешне функционирует (ПСЕВДО)",
        stress_response="Shutdown, диссоциация, коллапс",
        
        primary_categories=[ClinicalCategory.TRAUMA, ClinicalCategory.DISSOCIATION],
        secondary_categories=[ClinicalCategory.ANXIETY, ClinicalCategory.BORDERLINE],
        
        likely_symptoms=[
            "Внезапные 'обрушения'",
            "Диссоциативные эпизоды",
            "Конверсионные симптомы",
            "Суицидальные кризисы 'на ровном месте'"
        ],
        hidden_symptoms=[
            "ПТСР",
            "Диссоциативное расстройство",
            "Пограничное расстройство",
            "Скрытая суицидальность"
        ],
        
        defense_mechanisms=["Диссоциация", "Отрицание", "Splitting"],
        risks=["Суицид", "Острые диссоциативные эпизоды", "Госпитализация"],
        therapeutic_focus="Стабилизация, развитие сигналов о перегрузке, безопасность",
        prevalence="moderate"
    ),
    
    "S-S-V": ClinicalProfile(
        formula="S-S-V",
        name="Открытый тревожный с ресурсом",
        description="""
        Тревожен и выглядит тревожно, но при стрессе может собраться.
        Честная тревога с хорошим прогнозом.
        """,
        physiology="Симпатическая активация",
        presentation="Открыто тревожный",
        stress_response="Мобилизация ресурсов, адаптация",
        
        primary_categories=[ClinicalCategory.ANXIETY],
        secondary_categories=[ClinicalCategory.ADAPTIVE],
        
        likely_symptoms=[
            "Явная тревожность",
            "Нервозность",
            "Хорошее функционирование в кризисе",
            "Потребность в поддержке"
        ],
        hidden_symptoms=[
            "Скрытая компетентность",
            "Недооценка своих ресурсов"
        ],
        
        defense_mechanisms=["Регрессия", "Зависимость", "Но с доступом к ресурсам"],
        risks=["Выученная беспомощность", "Зависимость от других"],
        therapeutic_focus="Опора на собственные ресурсы, уверенность",
        prevalence="moderate"
    ),
    
    "S-S-S": ClinicalProfile(
        formula="S-S-S",
        name="Хроническая симпатическая активация",
        description="""
        Когерентный тревожный профиль. Всё в симпатике: физиология, поведение,
        реакция. Классическое генерализованное тревожное расстройство.
        """,
        physiology="Хроническая симпатическая активация",
        presentation="Явно тревожный, напряжённый",
        stress_response="Усиление тревоги, паника",
        
        primary_categories=[ClinicalCategory.ANXIETY],
        secondary_categories=[ClinicalCategory.PSYCHOSOMATIC, ClinicalCategory.OCD],
        
        likely_symptoms=[
            "Генерализованное тревожное расстройство",
            "Панические атаки",
            "Мышечное напряжение",
            "Нарушения сна",
            "Гастроинтестинальные проблемы",
            "Гипервигильность"
        ],
        hidden_symptoms=[
            "ОКР (как попытка контроля)",
            "Соматоформные расстройства",
            "Скрытая депрессия (истощение)"
        ],
        
        defense_mechanisms=["Контроль", "Ритуалы", "Избегание"],
        risks=["Выгорание", "Соматизация", "Панические атаки"],
        therapeutic_focus="Снижение активации, заземление, медикаментозная поддержка",
        prevalence="common"
    ),
    
    "S-S-D": ClinicalProfile(
        formula="S-S-D",
        name="Тревога → коллапс",
        description="""
        Классический травматический паттерн истощения:
        борьба-борьба-сдавайся. Тревога до точки, затем обрушение.
        """,
        physiology="Симпатическая активация",
        presentation="Тревожный",
        stress_response="Дорсальный коллапс",
        
        primary_categories=[ClinicalCategory.ANXIETY, ClinicalCategory.TRAUMA],
        secondary_categories=[ClinicalCategory.DEPRESSION, ClinicalCategory.DISSOCIATION],
        
        likely_symptoms=[
            "Тревога, переходящая в опустошение",
            "Панические атаки с последующей 'отключкой'",
            "Циклы активации-истощения",
            "Обмороки при панике"
        ],
        hidden_symptoms=[
            "ПТСР",
            "Смешанное тревожно-депрессивное расстройство",
            "Диссоциация после панических атак"
        ],
        
        defense_mechanisms=["Борьба → капитуляция"],
        risks=["Острые состояния", "Госпитализация"],
        therapeutic_focus="Расширение окна толерантности, работа с порогом",
        prevalence="moderate"
    ),
    
    "S-D-V": ClinicalProfile(
        formula="S-D-V",
        name="Замаскированная тревога",
        description="""
        Физиологически тревожен, но 'играет мёртвого'. При стрессе может
        мобилизоваться. Часто — выученная беспомощность с сохранным ресурсом.
        """,
        physiology="Симпатическая активация",
        presentation="Отстранённый, 'выключенный'",
        stress_response="Мобилизация, активация",
        
        primary_categories=[ClinicalCategory.DEPRESSION, ClinicalCategory.TRAUMA],
        secondary_categories=[ClinicalCategory.AVOIDANT],
        
        likely_symptoms=[
            "Апатия при внутренней тревоге",
            "Выученная беспомощность",
            "'Замороженная' тревога",
            "Оживление в кризисе"
        ],
        hidden_symptoms=[
            "Скрытая тревога за маской депрессии",
            "Ресурс, заблокированный страхом"
        ],
        
        defense_mechanisms=["Регрессия", "Отрицание", "Уход"],
        risks=["Неправильная диагностика (депрессия вместо тревоги)"],
        therapeutic_focus="Активация ресурсов, работа с выученной беспомощностью",
        prevalence="rare"
    ),
    
    "S-D-S": ClinicalProfile(
        formula="S-D-S",
        name="Скрытая гипервигильность",
        description="""
        Выглядит отстранённым, но внутри — тревога, и при стрессе она
        прорывается. Часто встречается при хронической травме.
        """,
        physiology="Симпатическая активация",
        presentation="Отстранённый, 'заторможенный'",
        stress_response="Тревожная активация, паника",
        
        primary_categories=[ClinicalCategory.TRAUMA, ClinicalCategory.ANXIETY],
        secondary_categories=[ClinicalCategory.DEPRESSION],
        
        likely_symptoms=[
            "Внешняя пассивность при внутреннем напряжении",
            "Взрывная тревога при триггере",
            "'Тихий' с внезапными паниками",
            "Ночные кошмары, flashbacks"
        ],
        hidden_symptoms=[
            "ПТСР с избегающими симптомами",
            "Скрытое паническое расстройство"
        ],
        
        defense_mechanisms=["Избегание", "Подавление", "Изоляция"],
        risks=["Непредсказуемые панические атаки", "Ретравматизация"],
        therapeutic_focus="Безопасная экспозиция, работа с триггерами",
        prevalence="moderate"
    ),
    
    "S-D-D": ClinicalProfile(
        formula="S-D-D",
        name="Тревожное истощение",
        description="""
        Внутри тревога, снаружи и при стрессе — shutdown. Тело сигнализирует
        об угрозе, но система уже 'сдалась'. Часто — хроническая травма.
        """,
        physiology="Симпатическая активация (тело 'знает' об угрозе)",
        presentation="Отстранённый, пассивный",
        stress_response="Углубление shutdown",
        
        primary_categories=[ClinicalCategory.TRAUMA, ClinicalCategory.DEPRESSION],
        secondary_categories=[ClinicalCategory.DISSOCIATION],
        
        likely_symptoms=[
            "Хроническая усталость при внутреннем напряжении",
            "Апатия с тревожным телом",
            "Соматические симптомы тревоги без субъективной тревоги",
            "Ощущение 'ничего не чувствую, но тело трясётся'"
        ],
        hidden_symptoms=[
            "Комплексный ПТСР",
            "Маскированная депрессия",
            "Фибромиалгия и хронические боли"
        ],
        
        defense_mechanisms=["Диссоциация от тревоги", "Соматизация"],
        risks=["Хронические соматические заболевания", "Суицидальность"],
        therapeutic_focus="Мягкая активация, соматический подход, безопасность",
        prevalence="moderate"
    ),
    
    # ========================================
    # ДОРСАЛЬНАЯ ДОМИНАНТА (D-X-X)
    # ========================================
    
    "D-V(p)-V": ClinicalProfile(
        formula="D-V(p)-V",
        name="Функциональное замирание",
        description="""
        Физиологически в shutdown, но презентует и реагирует вентрально.
        Крайняя степень адаптации — 'работает на автопилоте'.
        """,
        physiology="Дорсальное доминирование, низкая вариабельность",
        presentation="Внешне адаптирован (ПСЕВДО)",
        stress_response="Сохраняет функционирование",
        
        primary_categories=[ClinicalCategory.DISSOCIATION, ClinicalCategory.DEPRESSION],
        secondary_categories=[ClinicalCategory.TRAUMA],
        
        likely_symptoms=[
            "Жизнь 'на автомате'",
            "Ангедония при сохранном функционировании",
            "Деперсонализация/дереализация",
            "'Делаю всё правильно, но ничего не чувствую'"
        ],
        hidden_symptoms=[
            "Хроническое диссоциативное расстройство",
            "Маскированная депрессия",
            "Деперсонализационное расстройство"
        ],
        
        defense_mechanisms=["Высокофункциональная диссоциация", "Автоматизм"],
        risks=["Внезапный срыв", "Суицидальность без видимых признаков"],
        therapeutic_focus="Возвращение к ощущениям, медленная интеграция",
        prevalence="rare"
    ),
    
    "D-V(p)-S": ClinicalProfile(
        formula="D-V(p)-S",
        name="Псевдо-адаптация → тревожный прорыв",
        description="""
        В основе — дорсальный shutdown, маска адаптации, но при стрессе
        прорывается тревога. Паттерн 'замороженный с тревожными вспышками'.
        """,
        physiology="Дорсальное доминирование",
        presentation="Внешне функционирует (ПСЕВДО)",
        stress_response="Тревожная активация, паника",
        
        primary_categories=[ClinicalCategory.DISSOCIATION, ClinicalCategory.ANXIETY],
        secondary_categories=[ClinicalCategory.TRAUMA],
        
        likely_symptoms=[
            "'Плоский' в обычной жизни, паника при триггере",
            "Неожиданные тревожные вспышки",
            "Соматизация тревоги",
            "Flashbacks"
        ],
        hidden_symptoms=[
            "ПТСР с диссоциативными и тревожными компонентами",
            "Конверсионное расстройство"
        ],
        
        defense_mechanisms=["Диссоциация → прорыв тревоги"],
        risks=["Непредсказуемые панические атаки", "Дезорганизация"],
        therapeutic_focus="Стабилизация, работа с триггерами, интеграция",
        prevalence="rare"
    ),
    
    "D-V(p)-D": ClinicalProfile(
        formula="D-V(p)-D",
        name="Глубокая псевдо-адаптация",
        description="""
        Дорсальная база и реакция, но маска вентральной презентации.
        Человек 'играет жизнь', будучи внутренне 'мёртвым'.
        """,
        physiology="Дорсальное доминирование",
        presentation="Внешне адаптирован (ПСЕВДО)",
        stress_response="Углубление shutdown",
        
        primary_categories=[ClinicalCategory.DISSOCIATION, ClinicalCategory.DEPRESSION],
        secondary_categories=[ClinicalCategory.NARCISSISTIC],
        
        likely_symptoms=[
            "Хроническая деперсонализация",
            "Жизнь как 'фильм о себе'",
            "Отсутствие субъективного страдания при объективном неблагополучии",
            "Алекситимия"
        ],
        hidden_symptoms=[
            "Тяжёлое диссоциативное расстройство",
            "Маскированная суицидальность",
            "Нарциссическое расстройство (пустой грандиозный)"
        ],
        
        defense_mechanisms=["Глубокая диссоциация", "Ложное Я"],
        risks=["Суицид без предупреждающих знаков", "Психотический эпизод"],
        therapeutic_focus="Очень медленная работа, построение безопасности",
        prevalence="rare"
    ),
    
    "D-S-V": ClinicalProfile(
        formula="D-S-V",
        name="Защитная тревожность",
        description="""
        Дорсальная база, тревожная маска, но при реальном стрессе может
        адаптироваться. Тревога как защита от более глубокого shutdown.
        """,
        physiology="Дорсальное доминирование",
        presentation="Тревожный, беспокойный",
        stress_response="Мобилизация ресурсов",
        
        primary_categories=[ClinicalCategory.DEPRESSION, ClinicalCategory.ANXIETY],
        secondary_categories=[ClinicalCategory.ADAPTIVE],
        
        likely_symptoms=[
            "Тревога на фоне депрессии",
            "Тревога как 'спасение' от апатии",
            "Скрытый ресурс",
            "'Лучше тревога, чем пустота'"
        ],
        hidden_symptoms=[
            "Депрессия под маской тревоги",
            "Скрытая витальность"
        ],
        
        defense_mechanisms=["Тревога как защита от депрессии"],
        risks=["При снятии тревоги — депрессивный провал"],
        therapeutic_focus="Осторожная работа с тревогой, активация ресурсов",
        prevalence="rare"
    ),
    
    "D-S-S": ClinicalProfile(
        formula="D-S-S",
        name="Ажитированная депрессия",
        description="""
        Дорсальная база с тревожной презентацией и реакцией.
        Классическая ажитированная депрессия.
        """,
        physiology="Дорсальное доминирование, но с тревожной надстройкой",
        presentation="Тревожный, беспокойный",
        stress_response="Усиление тревоги",
        
        primary_categories=[ClinicalCategory.DEPRESSION, ClinicalCategory.ANXIETY],
        secondary_categories=[],
        
        likely_symptoms=[
            "Ажитированная депрессия",
            "Тревожная депрессия",
            "Психомоторное возбуждение на фоне опустошения",
            "Бессонница",
            "'Не могу успокоиться, но нет сил'"
        ],
        hidden_symptoms=[
            "Смешанное аффективное состояние",
            "Биполярное расстройство (смешанный эпизод)"
        ],
        
        defense_mechanisms=["Ажитация как защита от shutdown"],
        risks=["Высокий суицидальный риск (есть энергия на действие)"],
        therapeutic_focus="Стабилизация, медикаменты, снижение ажитации",
        prevalence="moderate"
    ),
    
    "D-S-D": ClinicalProfile(
        formula="D-S-D",
        name="Тревожно-дисфорическая депрессия",
        description="""
        Дорсальная база, тревожная презентация, дорсальная реакция.
        Раздражительная депрессия с уходом в shutdown при стрессе.
        """,
        physiology="Дорсальное доминирование",
        presentation="Раздражительный, дисфоричный",
        stress_response="Коллапс, уход",
        
        primary_categories=[ClinicalCategory.DEPRESSION],
        secondary_categories=[ClinicalCategory.ANXIETY, ClinicalCategory.BORDERLINE],
        
        likely_symptoms=[
            "Раздражительность при депрессии",
            "Дисфория",
            "'Бесит всё' → 'ничего не хочу'",
            "Изоляция после конфликтов"
        ],
        hidden_symptoms=[
            "Пограничное расстройство",
            "Биполярная депрессия"
        ],
        
        defense_mechanisms=["Проекция", "Отреагирование → shutdown"],
        risks=["Импульсивные действия", "Суицидальность"],
        therapeutic_focus="Регуляция аффекта, работа с дисфорией",
        prevalence="moderate"
    ),
    
    "D-D-V": ClinicalProfile(
        formula="D-D-V",
        name="Депрессия с ресурсом",
        description="""
        Дорсальная база и презентация, но при стрессе может мобилизоваться.
        Депрессия с сохранным ядром.
        """,
        physiology="Дорсальное доминирование",
        presentation="Отстранённый, подавленный",
        stress_response="Мобилизация, адаптация",
        
        primary_categories=[ClinicalCategory.DEPRESSION],
        secondary_categories=[ClinicalCategory.ADAPTIVE],
        
        likely_symptoms=[
            "Депрессия с сохранным функционированием в кризисе",
            "'Включается' только при необходимости",
            "Скрытые ресурсы",
            "Выборочная активность"
        ],
        hidden_symptoms=[
            "Ресурс, заблокированный депрессией",
            "Дистимия"
        ],
        
        defense_mechanisms=["Регрессия", "Уход"],
        risks=["Хронификация депрессии"],
        therapeutic_focus="Активация ресурсов, поведенческая активация",
        prevalence="moderate"
    ),
    
    "D-D-S": ClinicalProfile(
        formula="D-D-S",
        name="Депрессия с тревожным прорывом",
        description="""
        Дорсальная база и презентация, но при стрессе — тревога.
        Депрессия, из которой 'выбрасывает' в панику.
        """,
        physiology="Дорсальное доминирование",
        presentation="Отстранённый, подавленный",
        stress_response="Тревожная активация",
        
        primary_categories=[ClinicalCategory.DEPRESSION, ClinicalCategory.ANXIETY],
        secondary_categories=[],
        
        likely_symptoms=[
            "Депрессия с паническими атаками",
            "Апатия → внезапная тревога",
            "'Ничего не хочу' → 'что-то случится'"
        ],
        hidden_symptoms=[
            "Паническое расстройство на фоне депрессии",
            "Коморбидная тревога"
        ],
        
        defense_mechanisms=["Уход → тревожное отреагирование"],
        risks=["Панические атаки", "Избегание"],
        therapeutic_focus="Лечение обоих компонентов, стабилизация",
        prevalence="common"
    ),
    
    "D-D-D": ClinicalProfile(
        formula="D-D-D",
        name="Глубокий дорсальный shutdown",
        description="""
        Когерентный дорсальный профиль. Полный shutdown: физиология,
        презентация и реакция — всё в дорсальном. Тяжёлое состояние.
        """,
        physiology="Глубокое дорсальное доминирование",
        presentation="Отстранённый, 'пустой', безжизненный",
        stress_response="Углубление shutdown, обездвиженность",
        
        primary_categories=[ClinicalCategory.DEPRESSION, ClinicalCategory.DISSOCIATION],
        secondary_categories=[ClinicalCategory.TRAUMA],
        
        likely_symptoms=[
            "Тяжёлая депрессия",
            "Психомоторная заторможенность",
            "Ступор",
            "Кататонические черты",
            "Полная ангедония",
            "'Живой труп'"
        ],
        hidden_symptoms=[
            "Кататоническая депрессия",
            "Диссоциативный ступор",
            "Комплексный ПТСР с shutdown"
        ],
        
        defense_mechanisms=["Тотальный shutdown"],
        risks=["Суицид (когда появится энергия)", "Госпитализация", "Кататония"],
        therapeutic_focus="Госпитализация, медикаменты, мягкая активация, безопасность",
        prevalence="rare"
    ),
}


# ============================================================
# ДИАГНОСТИЧЕСКИЕ КАРТЫ
# ============================================================

# Где искать конкретные расстройства
DISORDER_PROFILE_MAP = {
    "Тревожное расстройство (ГТР)": [
        "S-S-S",      # Классическое
        "S-V(p)-S",   # Скрытое за фасадом
        "V-S-S",      # С ресурсной базой
        "V-V-S",      # Начальные стадии
    ],
    
    "Паническое расстройство": [
        "S-S-S",      # Классическое
        "S-V(p)-S",   # С маскировкой
        "S-S-D",      # С коллапсом
        "D-D-S",      # На фоне депрессии
    ],
    
    "Депрессия": [
        "D-D-D",      # Тяжёлая
        "D-D-V",      # С ресурсом
        "D-D-S",      # С тревогой
        "D-S-S",      # Ажитированная
        "D-S-D",      # Дисфорическая
        "S-D-D",      # Тревожное истощение
    ],
    
    "Диссоциативные расстройства": [
        "V-V-D",      # При триггере
        "D-V(p)-D",   # Глубокое
        "D-V(p)-V",   # Функциональное
        "S-V(p)-D",   # Псевдо с коллапсом
    ],
    
    "ПТСР": [
        "S-V(p)-D",   # Классический
        "S-S-D",      # Тревожный с коллапсом
        "S-D-S",      # С избеганием
        "D-D-D",      # Хронический shutdown
        "V-V-D",      # С сохранной базой
    ],
    
    "Комплексный ПТСР": [
        "S-V(p)-D",   # С псевдо-адаптацией
        "D-V(p)-D",   # Глубокая диссоциация
        "S-D-D",      # Тревожное истощение
        "D-D-D",      # Тотальный shutdown
    ],
    
    "ОКР": [
        "S-S-S",      # Тревога → ритуалы
        "V-S-S",      # С ресурсной базой
        "S-V(p)-S",   # Скрытое
    ],
    
    "Психосоматика": [
        "S-V(p)-V",   # Подавленная тревога → тело
        "S-V(p)-S",   # Тревога в теле
        "S-D-D",      # Тревога без осознания → тело
        "D-V(p)-S",   # Диссоциация → тело
    ],
    
    "Пограничное расстройство": [
        "S-V(p)-D",   # Нестабильность
        "D-S-D",      # Дисфория
        "S-S-D",      # Тревога → коллапс
    ],
    
    "Нарциссическое расстройство": [
        "S-V(p)-V",   # Компенсаторный (грандиозный)
        "S-V(p)-S",   # С тревогой под маской
        "D-V(p)-D",   # Пустой/дефицитарный
    ],
    
    "Шизоидная адаптация": [
        "V-D-V",      # Интроверсия с ресурсом
        "V-D-D",      # Глубокая изоляция
        "D-D-D",      # Тяжёлая
    ],
    
    "Избегающее расстройство": [
        "S-D-S",      # Скрытая тревога
        "S-D-D",      # Истощение
        "V-D-D",      # С ресурсом
    ],
    
    "Зависимое расстройство": [
        "S-S-V",      # Тревога + потребность в поддержке
        "D-D-V",      # Депрессия + ресурс при помощи
    ],
    
    "Истерическое/Конверсионное": [
        "S-V(p)-D",   # Классическое (la belle indifférence)
        "D-V(p)-S",   # Прорывы
        "S-S-D",      # Конверсионные обмороки
    ],
    
    "Биполярное расстройство": [
        "D-S-S",      # Смешанное состояние
        "D-D-S",      # Депрессивная фаза
        # Маниакальная фаза — отдельный профиль (M-M-M)
    ],
}


def get_profiles_for_symptom(symptom: str) -> list:
    """Получить профили, связанные с симптомом"""
    return DISORDER_PROFILE_MAP.get(symptom, [])


def get_profile(formula: str) -> Optional[ClinicalProfile]:
    """Получить клинический профиль по формуле"""
    return CLINICAL_PROFILES.get(formula)


def get_all_profiles() -> dict:
    """Получить все профили"""
    return CLINICAL_PROFILES


def print_profile_summary(formula: str) -> str:
    """Краткое описание профиля"""
    profile = CLINICAL_PROFILES.get(formula)
    if not profile:
        return f"Профиль {formula} не найден"
    
    categories = ", ".join([c.value for c in profile.primary_categories])
    
    return f"""
*{profile.formula}: {profile.name}*

{profile.description.strip()}

*Основные категории:* {categories}

*Вероятные симптомы:*
{chr(10).join(['• ' + s for s in profile.likely_symptoms[:3]])}

*Что может быть скрыто:*
{chr(10).join(['• ' + s for s in profile.hidden_symptoms[:2]])}

*Защитные механизмы:* {', '.join(profile.defense_mechanisms)}

*Фокус терапии:* {profile.therapeutic_focus}
"""
