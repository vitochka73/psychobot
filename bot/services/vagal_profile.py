"""
Модуль классификации вагусных профилей на основе полевагальной теории.

Формула профиля: X-Y-Z (T)
- X: Физиологическая доминанта (S/V/D) - по данным HRV в покое
- Y: Внешняя презентация (S/V/D + флаг pseudo) - поведенческая оценка  
- Z: Реакция на аффект (S/V/D) - куда "проваливается" при стрессе
- T: Триггерный профиль - на какой тип стресса реагирует сильнее всего

Пример: S-V(p)-D (Ta) означает:
- Физиологически доминирует симпатика
- Внешне выглядит вентрально-адаптированным (но это псевдо)
- При стрессе уходит в дорсальный shutdown
- Максимальная уязвимость к триггерам привязанности
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, List
import math


class VagalState(Enum):
    """Состояния по полевагальной теории"""
    VENTRAL = "V"      # Вентральный вагус - социальная вовлечённость, спокойствие
    SYMPATHETIC = "S"  # Симпатика - борьба/бегство
    DORSAL = "D"       # Дорсальный вагус - замирание, shutdown


class TriggerType(Enum):
    """Типы триггеров уязвимости"""
    ATTACHMENT = "Ta"      # Привязанность: отвержение, потеря, одиночество
    CONTROL = "Tc"         # Контроль: неопределённость, хаос, беспомощность
    SAFETY = "Ts"          # Безопасность: угроза, агрессия, конфликт
    IDENTITY = "Ti"        # Идентичность: стыд, обесценивание, критика
    BODY = "Tb"            # Телесное: боль, болезнь, интероцепция
    UNKNOWN = "T?"         # Не определён (нужно больше данных)
    
    @property
    def description(self) -> str:
        """Описание триггера"""
        descriptions = {
            TriggerType.ATTACHMENT: "Привязанность (отвержение, потеря, одиночество)",
            TriggerType.CONTROL: "Контроль (неопределённость, хаос, беспомощность)",
            TriggerType.SAFETY: "Безопасность (угроза, агрессия, конфликт)",
            TriggerType.IDENTITY: "Идентичность (стыд, обесценивание, критика)",
            TriggerType.BODY: "Телесное (боль, болезнь, телесные ощущения)",
            TriggerType.UNKNOWN: "Требуется дополнительное тестирование",
        }
        return descriptions.get(self, "")
    
    @property
    def stress_instruction(self) -> str:
        """Инструкция для стресс-теста"""
        instructions = {
            TriggerType.ATTACHMENT: 
                "Вспомните момент, когда вы чувствовали себя отвергнутым, "
                "покинутым или глубоко одиноким. Позвольте этому воспоминанию развернуться.",
            TriggerType.CONTROL: 
                "Вспомните ситуацию полной неопределённости, когда вы не могли "
                "ничего контролировать и не знали, что произойдёт.",
            TriggerType.SAFETY: 
                "Вспомните момент, когда вы чувствовали угрозу своей безопасности, "
                "конфликт или агрессию в ваш адрес.",
            TriggerType.IDENTITY: 
                "Вспомните ситуацию глубокого стыда, когда вас критиковали, "
                "обесценивали или вы чувствовали себя 'не таким'.",
            TriggerType.BODY: 
                "Сосредоточьтесь на неприятных телесных ощущениях, вспомните "
                "момент боли, болезни или телесного дискомфорта.",
        }
        return instructions.get(self, "Подумайте о чём-то неприятном.")


@dataclass
class TriggerTestResult:
    """Результат теста на конкретный триггер"""
    trigger_type: TriggerType
    stress_data: 'KubiosData'           # Данные при активации триггера
    reactivity_score: float = 0.0        # Сила реакции (0-100)
    response_type: VagalState = None     # Тип ответа (S или D)
    recovery_speed: float = 0.0          # Скорость восстановления после этого триггера


@dataclass
class KubiosData:
    """Данные из Kubios HRV анализа"""
    # Временные показатели (Time-domain)
    mean_rr: float          # Средний RR интервал (мс)
    sdnn: float             # Стандартное отклонение NN интервалов (мс)
    rmssd: float            # Квадратный корень средних квадратов разностей (мс)
    pnn50: float            # Процент NN50 (%)
    mean_hr: float          # Средний пульс (уд/мин)
    
    # Спектральные показатели (Frequency-domain)
    vlf_power: float        # Очень низкие частоты (мс²)
    lf_power: float         # Низкие частоты (мс²) - симпатика + парасимпатика
    hf_power: float         # Высокие частоты (мс²) - парасимпатика
    lf_hf_ratio: float      # Соотношение LF/HF
    total_power: float      # Общая мощность спектра (мс²)
    
    # Нелинейные показатели (Poincaré plot)
    sd1: float              # Краткосрочная вариабельность (мс)
    sd2: float              # Долгосрочная вариабельность (мс)
    
    # Опционально: энтропия
    sample_entropy: Optional[float] = None  # SampEn


@dataclass 
class BehavioralAssessment:
    """Оценка внешней презентации (поведенческая)"""
    # Шкала 1-5 для каждого параметра
    eye_contact: int            # Зрительный контакт
    voice_prosody: int          # Просодика голоса (интонации, модуляции)
    facial_expressivity: int    # Выразительность мимики
    social_engagement: int      # Социальная вовлечённость
    body_relaxation: int        # Расслабленность тела
    
    # Дополнительные маркеры
    reports_dissociation: bool = False   # Субъективный отчёт о диссоциации
    reports_anxiety: bool = False        # Субъективный отчёт о тревоге
    reports_numbness: bool = False       # Субъективный отчёт об оцепенении


@dataclass
class ThreePhaseMeasurement:
    """Три замера по протоколу (базовый)"""
    baseline: KubiosData        # Замер 1: Спокойное состояние
    stress: KubiosData          # Замер 2: При негативных мыслях/воспоминаниях  
    recovery: KubiosData        # Замер 3: После восстановления
    
    recovery_time_seconds: float  # Время восстановления в секундах
    
    # Опционально: тип триггера, использованного в этом тесте
    trigger_type: Optional[TriggerType] = None


@dataclass
class MultiTriggerMeasurement:
    """
    Расширенный протокол с тестированием нескольких триггеров.
    
    Позволяет определить, на какой тип стресса человек реагирует сильнее.
    """
    baseline: KubiosData                           # Общий baseline в покое
    trigger_tests: List[TriggerTestResult] = field(default_factory=list)
    final_recovery: Optional[KubiosData] = None    # Финальное восстановление
    
    def add_trigger_test(
        self, 
        trigger_type: TriggerType, 
        stress_data: KubiosData,
        recovery_data: Optional[KubiosData] = None
    ):
        """Добавить результат теста на триггер"""
        test = TriggerTestResult(
            trigger_type=trigger_type,
            stress_data=stress_data
        )
        self.trigger_tests.append(test)
    
    def get_most_reactive_trigger(self) -> Optional[TriggerType]:
        """Получить триггер с максимальной реактивностью"""
        if not self.trigger_tests:
            return None
        return max(self.trigger_tests, key=lambda t: t.reactivity_score).trigger_type
    
    def get_trigger_ranking(self) -> List[tuple[TriggerType, float]]:
        """Получить рейтинг триггеров по силе реакции"""
        return sorted(
            [(t.trigger_type, t.reactivity_score) for t in self.trigger_tests],
            key=lambda x: x[1],
            reverse=True
        )


@dataclass
class VagalProfile:
    """Итоговый вагусный профиль"""
    physiological_dominant: VagalState    # X: Физиологическая доминанта
    behavioral_presentation: VagalState   # Y: Внешняя презентация
    is_pseudo: bool                       # Флаг псевдо-презентации
    stress_response: VagalState           # Z: Реакция на аффект
    
    # Детальные метрики
    recovery_speed_percent: float         # Скорость восстановления (%)
    reactivity_index: float               # Индекс реактивности
    coherence_score: float                # Согласованность профиля (0-1)
    
    # Триггерный профиль
    primary_trigger: TriggerType = TriggerType.UNKNOWN    # Главный триггер
    secondary_trigger: Optional[TriggerType] = None        # Вторичный триггер
    trigger_sensitivity_map: Dict[TriggerType, float] = field(default_factory=dict)
    
    def __str__(self) -> str:
        """Формула профиля"""
        pseudo_marker = "(p)" if self.is_pseudo else ""
        base = f"{self.physiological_dominant.value}-{self.behavioral_presentation.value}{pseudo_marker}-{self.stress_response.value}"
        
        if self.primary_trigger != TriggerType.UNKNOWN:
            return f"{base} ({self.primary_trigger.value})"
        return base
    
    def get_full_formula(self) -> str:
        """Полная формула с вторичным триггером"""
        pseudo_marker = "(p)" if self.is_pseudo else ""
        base = f"{self.physiological_dominant.value}-{self.behavioral_presentation.value}{pseudo_marker}-{self.stress_response.value}"
        
        triggers = []
        if self.primary_trigger != TriggerType.UNKNOWN:
            triggers.append(self.primary_trigger.value)
        if self.secondary_trigger and self.secondary_trigger != TriggerType.UNKNOWN:
            triggers.append(self.secondary_trigger.value)
        
        if triggers:
            return f"{base} ({', '.join(triggers)})"
        return base
    
    def get_interpretation(self) -> str:
        """Клиническая интерпретация профиля"""
        base_interpretation = PROFILE_INTERPRETATIONS.get(
            (self.physiological_dominant, self.behavioral_presentation, self.is_pseudo, self.stress_response),
            "Профиль требует индивидуальной интерпретации."
        )
        
        trigger_interpretation = ""
        if self.primary_trigger != TriggerType.UNKNOWN:
            trigger_interpretation = TRIGGER_INTERPRETATIONS.get(
                self.primary_trigger,
                ""
            )
        
        if trigger_interpretation:
            return f"{base_interpretation}\n\n*Триггерная уязвимость:* {trigger_interpretation}"
        return base_interpretation
    
    def get_trigger_report(self) -> str:
        """Отчёт по триггерной чувствительности"""
        if not self.trigger_sensitivity_map:
            return "Триггерное тестирование не проводилось."
        
        lines = ["*Карта триггерной чувствительности:*\n"]
        
        # Сортируем по силе реакции
        sorted_triggers = sorted(
            self.trigger_sensitivity_map.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for trigger, score in sorted_triggers:
            bar_length = int(score / 10)
            bar = "█" * bar_length + "░" * (10 - bar_length)
            marker = "🔴" if score >= 70 else "🟡" if score >= 40 else "🟢"
            lines.append(f"{marker} {trigger.value}: {bar} {score:.0f}%")
            lines.append(f"   ↳ {trigger.description}")
        
        return "\n".join(lines)


class VagalProfileClassifier:
    """Классификатор вагусных профилей"""
    
    # Пороговые значения (настраиваемые)
    # Основаны на нормативных данных Kubios и исследованиях HRV
    
    # RMSSD пороги (мс) - основной маркер парасимпатики
    RMSSD_HIGH = 42.0      # Выше = хороший вагусный тонус (V)
    RMSSD_LOW = 20.0       # Ниже = сниженный тонус (S или D)
    
    # SDNN пороги (мс) - общая вариабельность
    SDNN_HIGH = 50.0
    SDNN_LOW = 30.0
    SDNN_VERY_LOW = 15.0   # Очень низкий = возможно D (shutdown)
    
    # LF/HF ratio пороги
    LFHF_HIGH = 2.0        # Выше = симпатическое доминирование
    LFHF_LOW = 0.5         # Ниже = парасимпатическое доминирование
    
    # HF power пороги (мс²) - вагусная активность
    HF_HIGH = 400.0
    HF_LOW = 100.0
    
    # Total Power пороги (мс²)
    TP_VERY_LOW = 500.0    # Очень низкий = возможно D
    
    # Скорость восстановления (%)
    RECOVERY_FAST = 80.0   # Быстрое восстановление
    RECOVERY_SLOW = 50.0   # Медленное восстановление
    
    # Поведенческая оценка
    BEHAVIORAL_HIGH = 4.0  # Средний балл для V-презентации
    BEHAVIORAL_LOW = 2.5   # Средний балл для S/D-презентации
    
    def __init__(self, custom_thresholds: Optional[dict] = None):
        """
        Инициализация с возможностью кастомных порогов.
        
        Args:
            custom_thresholds: Словарь с кастомными пороговыми значениями
        """
        if custom_thresholds:
            for key, value in custom_thresholds.items():
                if hasattr(self, key):
                    setattr(self, key, value)
    
    def classify_physiological_state(self, data: KubiosData) -> VagalState:
        """
        Классификация физиологического состояния по данным HRV.
        
        Логика:
        - V (Ventral): высокий RMSSD, высокий HF, низкий LF/HF
        - S (Sympathetic): низкий RMSSD, высокий LF/HF, нормальный Total Power
        - D (Dorsal): низкий SDNN, низкий Total Power, слабая реактивность
        """
        # Проверка на дорсальный shutdown
        if self._is_dorsal_pattern(data):
            return VagalState.DORSAL
        
        # Проверка вентрального vs симпатического
        ventral_score = 0
        sympathetic_score = 0
        
        # RMSSD анализ
        if data.rmssd >= self.RMSSD_HIGH:
            ventral_score += 2
        elif data.rmssd <= self.RMSSD_LOW:
            sympathetic_score += 2
        else:
            ventral_score += 1
        
        # LF/HF ratio анализ
        if data.lf_hf_ratio >= self.LFHF_HIGH:
            sympathetic_score += 2
        elif data.lf_hf_ratio <= self.LFHF_LOW:
            ventral_score += 2
        else:
            # Нейтральная зона
            pass
        
        # HF power анализ
        if data.hf_power >= self.HF_HIGH:
            ventral_score += 1
        elif data.hf_power <= self.HF_LOW:
            sympathetic_score += 1
        
        # SD1 анализ (краткосрочная вариабельность, связана с парасимпатикой)
        if data.sd1 >= 30:
            ventral_score += 1
        elif data.sd1 <= 15:
            sympathetic_score += 1
        
        if ventral_score > sympathetic_score:
            return VagalState.VENTRAL
        else:
            return VagalState.SYMPATHETIC
    
    def _is_dorsal_pattern(self, data: KubiosData) -> bool:
        """
        Определение дорсального паттерна (shutdown/freeze).
        
        Характеристики D:
        - Очень низкая общая вариабельность
        - Низкая мощность во всех диапазонах
        - "Плоский" ритм
        """
        dorsal_markers = 0
        
        # Очень низкий SDNN
        if data.sdnn <= self.SDNN_VERY_LOW:
            dorsal_markers += 2
        
        # Очень низкий Total Power
        if data.total_power <= self.TP_VERY_LOW:
            dorsal_markers += 2
        
        # Низкие SD1 и SD2 одновременно (плоская Пуанкаре)
        if data.sd1 <= 10 and data.sd2 <= 20:
            dorsal_markers += 2
        
        # Низкая энтропия (если доступна)
        if data.sample_entropy is not None and data.sample_entropy <= 1.0:
            dorsal_markers += 1
        
        # Парадокс: RMSSD не очень низкий, но SDNN очень низкий
        if data.rmssd > self.RMSSD_LOW and data.sdnn <= self.SDNN_VERY_LOW:
            dorsal_markers += 1
        
        return dorsal_markers >= 3
    
    def classify_behavioral_presentation(
        self, 
        assessment: BehavioralAssessment
    ) -> tuple[VagalState, bool]:
        """
        Классификация внешней презентации.
        
        Returns:
            tuple: (VagalState, is_pseudo)
        """
        # Средний балл по социальным маркерам
        social_markers = [
            assessment.eye_contact,
            assessment.voice_prosody,
            assessment.facial_expressivity,
            assessment.social_engagement,
            assessment.body_relaxation
        ]
        avg_score = sum(social_markers) / len(social_markers)
        
        # Определяем презентацию
        if avg_score >= self.BEHAVIORAL_HIGH:
            presentation = VagalState.VENTRAL
        elif avg_score <= self.BEHAVIORAL_LOW:
            # Дифференциация S vs D по дополнительным маркерам
            if assessment.reports_numbness or assessment.reports_dissociation:
                presentation = VagalState.DORSAL
            else:
                presentation = VagalState.SYMPATHETIC
        else:
            presentation = VagalState.SYMPATHETIC
        
        # Псевдо-флаг определяется позже при сравнении с физиологией
        return presentation, False
    
    def classify_stress_response(
        self, 
        baseline: KubiosData, 
        stress: KubiosData
    ) -> VagalState:
        """
        Классификация реакции на стресс.
        
        Логика:
        - S: резкое падение HRV, рост LF/HF
        - D: слабая реакция или парадоксальное снижение активности
        - V: умеренное снижение с сохранением адаптивности
        """
        # Расчёт изменений
        rmssd_change = (stress.rmssd - baseline.rmssd) / baseline.rmssd * 100
        lfhf_change = stress.lf_hf_ratio - baseline.lf_hf_ratio
        sdnn_change = (stress.sdnn - baseline.sdnn) / baseline.sdnn * 100
        tp_change = (stress.total_power - baseline.total_power) / baseline.total_power * 100
        
        # Паттерн дорсального ответа: минимальная реакция
        if abs(rmssd_change) < 10 and abs(sdnn_change) < 10:
            return VagalState.DORSAL
        
        # Паттерн симпатического ответа: резкое падение + рост LF/HF
        if rmssd_change < -30 and lfhf_change > 0.5:
            return VagalState.SYMPATHETIC
        
        # Паттерн сильного дорсального: резкое падение Total Power
        if tp_change < -50 and sdnn_change < -40:
            return VagalState.DORSAL
        
        # Умеренная реакция = вентральная адаптивность
        if -30 <= rmssd_change <= -10:
            return VagalState.VENTRAL
        
        # По умолчанию симпатика
        return VagalState.SYMPATHETIC
    
    def calculate_recovery_speed(
        self,
        baseline: KubiosData,
        stress: KubiosData,
        recovery: KubiosData
    ) -> float:
        """
        Расчёт скорости восстановления (%).
        
        100% = полное восстановление до baseline
        >100% = восстановление выше baseline (ребаунд)
        <100% = неполное восстановление
        """
        # Используем RMSSD как основной маркер
        baseline_rmssd = baseline.rmssd
        stress_rmssd = stress.rmssd
        recovery_rmssd = recovery.rmssd
        
        # Избегаем деления на ноль
        drop = baseline_rmssd - stress_rmssd
        if abs(drop) < 0.1:
            return 100.0  # Не было падения
        
        recovered = recovery_rmssd - stress_rmssd
        recovery_percent = (recovered / drop) * 100
        
        return min(max(recovery_percent, 0), 150)  # Ограничиваем 0-150%
    
    def calculate_reactivity_index(
        self,
        baseline: KubiosData,
        stress: KubiosData
    ) -> float:
        """
        Индекс реактивности: насколько система реагирует на стресс.
        
        Низкий индекс может указывать на:
        - Дорсальное состояние (система не реагирует)
        - Или очень хорошую регуляцию (минимальное воздействие)
        """
        changes = [
            abs(stress.rmssd - baseline.rmssd) / baseline.rmssd,
            abs(stress.sdnn - baseline.sdnn) / baseline.sdnn,
            abs(stress.lf_hf_ratio - baseline.lf_hf_ratio) / max(baseline.lf_hf_ratio, 0.1),
            abs(stress.total_power - baseline.total_power) / baseline.total_power
        ]
        
        return sum(changes) / len(changes) * 100
    
    def calculate_coherence(
        self,
        physiological: VagalState,
        behavioral: VagalState,
        stress_response: VagalState
    ) -> float:
        """
        Когерентность профиля: насколько согласованы все компоненты.
        
        1.0 = все компоненты совпадают (V-V-V или S-S-S)
        0.0 = полное рассогласование
        """
        states = [physiological, behavioral, stress_response]
        
        # Считаем совпадения
        if states[0] == states[1] == states[2]:
            return 1.0
        elif states[0] == states[1] or states[1] == states[2] or states[0] == states[2]:
            return 0.5
        else:
            return 0.0
    
    def classify(
        self,
        measurements: ThreePhaseMeasurement,
        behavioral: BehavioralAssessment
    ) -> VagalProfile:
        """
        Полная классификация вагусного профиля (базовый протокол).
        
        Args:
            measurements: Три замера HRV
            behavioral: Поведенческая оценка
            
        Returns:
            VagalProfile: Итоговый профиль
        """
        # 1. Физиологическая доминанта (по baseline)
        physiological = self.classify_physiological_state(measurements.baseline)
        
        # 2. Внешняя презентация
        behavioral_state, _ = self.classify_behavioral_presentation(behavioral)
        
        # 3. Определяем псевдо-флаг
        is_pseudo = (
            behavioral_state == VagalState.VENTRAL and 
            physiological != VagalState.VENTRAL
        )
        
        # 4. Реакция на стресс
        stress_response = self.classify_stress_response(
            measurements.baseline, 
            measurements.stress
        )
        
        # 5. Скорость восстановления
        recovery_speed = self.calculate_recovery_speed(
            measurements.baseline,
            measurements.stress,
            measurements.recovery
        )
        
        # 6. Индекс реактивности
        reactivity = self.calculate_reactivity_index(
            measurements.baseline,
            measurements.stress
        )
        
        # 7. Когерентность
        coherence = self.calculate_coherence(
            physiological, 
            behavioral_state, 
            stress_response
        )
        
        # Определяем триггер, если указан в измерениях
        primary_trigger = measurements.trigger_type or TriggerType.UNKNOWN
        
        return VagalProfile(
            physiological_dominant=physiological,
            behavioral_presentation=behavioral_state,
            is_pseudo=is_pseudo,
            stress_response=stress_response,
            recovery_speed_percent=recovery_speed,
            reactivity_index=reactivity,
            coherence_score=coherence,
            primary_trigger=primary_trigger
        )
    
    def classify_with_triggers(
        self,
        multi_measurement: MultiTriggerMeasurement,
        behavioral: BehavioralAssessment
    ) -> VagalProfile:
        """
        Расширенная классификация с триггерным профилем.
        
        Args:
            multi_measurement: Измерения с несколькими триггерами
            behavioral: Поведенческая оценка
            
        Returns:
            VagalProfile: Профиль с триггерной картой
        """
        baseline = multi_measurement.baseline
        
        # 1. Физиологическая доминанта
        physiological = self.classify_physiological_state(baseline)
        
        # 2. Внешняя презентация
        behavioral_state, _ = self.classify_behavioral_presentation(behavioral)
        
        # 3. Псевдо-флаг
        is_pseudo = (
            behavioral_state == VagalState.VENTRAL and 
            physiological != VagalState.VENTRAL
        )
        
        # 4. Анализируем каждый триггер
        trigger_sensitivity_map = {}
        trigger_responses = {}
        max_reactivity = 0
        primary_trigger = TriggerType.UNKNOWN
        secondary_trigger = None
        dominant_stress_response = VagalState.SYMPATHETIC
        
        for test in multi_measurement.trigger_tests:
            # Рассчитываем реактивность на этот триггер
            reactivity = self.calculate_reactivity_index(baseline, test.stress_data)
            test.reactivity_score = reactivity
            
            # Определяем тип ответа
            test.response_type = self.classify_stress_response(baseline, test.stress_data)
            
            trigger_sensitivity_map[test.trigger_type] = reactivity
            trigger_responses[test.trigger_type] = test.response_type
        
        # 5. Находим главный и вторичный триггеры
        if trigger_sensitivity_map:
            sorted_triggers = sorted(
                trigger_sensitivity_map.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            if sorted_triggers:
                primary_trigger = sorted_triggers[0][0]
                max_reactivity = sorted_triggers[0][1]
                dominant_stress_response = trigger_responses.get(
                    primary_trigger, 
                    VagalState.SYMPATHETIC
                )
                
                if len(sorted_triggers) > 1:
                    # Вторичный триггер, если его реактивность >= 60% от первичного
                    if sorted_triggers[1][1] >= max_reactivity * 0.6:
                        secondary_trigger = sorted_triggers[1][0]
        
        # 6. Скорость восстановления (по финальному recovery или по среднему)
        recovery_speed = 50.0  # Дефолт
        if multi_measurement.final_recovery:
            # Берём самый сильный стресс для расчёта восстановления
            strongest_stress = None
            if multi_measurement.trigger_tests:
                strongest_test = max(
                    multi_measurement.trigger_tests,
                    key=lambda t: t.reactivity_score
                )
                strongest_stress = strongest_test.stress_data
            
            if strongest_stress:
                recovery_speed = self.calculate_recovery_speed(
                    baseline,
                    strongest_stress,
                    multi_measurement.final_recovery
                )
        
        # 7. Когерентность
        coherence = self.calculate_coherence(
            physiological,
            behavioral_state,
            dominant_stress_response
        )
        
        return VagalProfile(
            physiological_dominant=physiological,
            behavioral_presentation=behavioral_state,
            is_pseudo=is_pseudo,
            stress_response=dominant_stress_response,
            recovery_speed_percent=recovery_speed,
            reactivity_index=max_reactivity,
            coherence_score=coherence,
            primary_trigger=primary_trigger,
            secondary_trigger=secondary_trigger,
            trigger_sensitivity_map=trigger_sensitivity_map
        )
    
    def compare_trigger_responses(
        self,
        baseline: KubiosData,
        trigger_data: Dict[TriggerType, KubiosData]
    ) -> Dict[TriggerType, dict]:
        """
        Сравнительный анализ реакций на разные триггеры.
        
        Args:
            baseline: Базовый замер
            trigger_data: Словарь {триггер: данные при стрессе}
            
        Returns:
            Словарь с анализом по каждому триггеру
        """
        results = {}
        
        for trigger_type, stress_data in trigger_data.items():
            reactivity = self.calculate_reactivity_index(baseline, stress_data)
            response = self.classify_stress_response(baseline, stress_data)
            
            # Детальные изменения
            rmssd_drop = (stress_data.rmssd - baseline.rmssd) / baseline.rmssd * 100
            lfhf_change = stress_data.lf_hf_ratio - baseline.lf_hf_ratio
            tp_drop = (stress_data.total_power - baseline.total_power) / baseline.total_power * 100
            
            results[trigger_type] = {
                'reactivity_score': reactivity,
                'response_type': response,
                'rmssd_change_percent': rmssd_drop,
                'lf_hf_change': lfhf_change,
                'total_power_change_percent': tp_drop,
                'severity': 'high' if reactivity >= 50 else 'medium' if reactivity >= 25 else 'low'
            }
        
        return results


# Интерпретации триггеров
TRIGGER_INTERPRETATIONS = {
    TriggerType.ATTACHMENT: 
        "Система наиболее уязвима к угрозам привязанности. Отвержение, потеря близких, "
        "одиночество вызывают сильнейшую дисрегуляцию. Рекомендуется работа с безопасной "
        "привязанностью и проработка ранних отношенческих травм.",
    
    TriggerType.CONTROL:
        "Система наиболее уязвима к потере контроля. Неопределённость, хаос, невозможность "
        "влиять на ситуацию запускают сильную реакцию. Рекомендуется работа с толерантностью "
        "к неопределённости и развитие гибкости.",
    
    TriggerType.SAFETY:
        "Система наиболее уязвима к угрозам безопасности. Конфликты, агрессия, потенциальная "
        "опасность вызывают мощную активацию. Возможна история травмы насилия. "
        "Рекомендуется работа с безопасностью и границами.",
    
    TriggerType.IDENTITY:
        "Система наиболее уязвима к угрозам идентичности. Стыд, критика, обесценивание "
        "запускают сильную реакцию. Возможна история эмоционального насилия или нарциссической "
        "травмы. Рекомендуется работа с самоценностью.",
    
    TriggerType.BODY:
        "Система наиболее уязвима к телесным сигналам. Боль, болезнь, телесные ощущения "
        "вызывают дисрегуляцию. Возможна соматическая травма или медицинская история. "
        "Рекомендуется работа с интероцепцией и телесной безопасностью.",
}


# Интерпретации профилей
PROFILE_INTERPRETATIONS = {
    # Когерентные профили
    (VagalState.VENTRAL, VagalState.VENTRAL, False, VagalState.VENTRAL): 
        "Здоровая вагусная регуляция. Хорошая социальная адаптация, "
        "адекватная реакция на стресс, быстрое восстановление.",
    
    (VagalState.SYMPATHETIC, VagalState.SYMPATHETIC, False, VagalState.SYMPATHETIC):
        "Хроническая симпатическая активация. Возможна тревога, гипервигильность. "
        "Рекомендуется работа с регуляцией через вагусные практики.",
    
    (VagalState.DORSAL, VagalState.DORSAL, False, VagalState.DORSAL):
        "Дорсальное доминирование. Возможны диссоциация, оцепенение, депрессия. "
        "Требуется мягкая активация через безопасный контакт.",
    
    # Псевдо-профили
    (VagalState.SYMPATHETIC, VagalState.VENTRAL, True, VagalState.SYMPATHETIC):
        "Псевдо-вентральный профиль. Социальная маскировка при внутренней тревоге. "
        "Истощение ресурсов на поддержание фасада. Риск выгорания.",
    
    (VagalState.SYMPATHETIC, VagalState.VENTRAL, True, VagalState.DORSAL):
        "Псевдо-вентральный с дорсальным коллапсом. Фасад социальной адаптации, "
        "но при стрессе — уход в shutdown. Возможна скрытая травма.",
    
    (VagalState.DORSAL, VagalState.VENTRAL, True, VagalState.DORSAL):
        "Псевдо-вентральный при дорсальной базе. Функциональное замирание "
        "с социальной маской. Высокий риск диссоциативных состояний.",
    
    # Смешанные профили
    (VagalState.VENTRAL, VagalState.VENTRAL, False, VagalState.SYMPATHETIC):
        "Хорошая база с симпатической реактивностью. Адекватный ответ на угрозу, "
        "но возможна избыточная активация. Норма при определённых условиях.",
    
    (VagalState.VENTRAL, VagalState.VENTRAL, False, VagalState.DORSAL):
        "Вентральная база с дорсальным коллапсом при стрессе. "
        "Возможна травматическая реакция на специфические триггеры.",
    
    (VagalState.SYMPATHETIC, VagalState.SYMPATHETIC, False, VagalState.DORSAL):
        "Симпатическая гипервигильность с дорсальным провалом. "
        "Паттерн истощения: борьба-борьба-коллапс. Требуется стабилизация.",
}


def create_sample_kubios_data(
    rmssd: float = 35.0,
    sdnn: float = 45.0,
    lf_hf: float = 1.5,
    hf_power: float = 300.0,
    total_power: float = 1500.0
) -> KubiosData:
    """Вспомогательная функция для создания тестовых данных"""
    return KubiosData(
        mean_rr=850,
        sdnn=sdnn,
        rmssd=rmssd,
        pnn50=25.0,
        mean_hr=70,
        vlf_power=total_power * 0.3,
        lf_power=total_power * 0.4,
        hf_power=hf_power,
        lf_hf_ratio=lf_hf,
        total_power=total_power,
        sd1=rmssd * 0.7,
        sd2=sdnn * 1.2
    )
