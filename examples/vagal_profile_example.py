"""
Пример использования классификатора вагусных профилей.

Демонстрация различных профилей на основе данных Kubios.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.services.vagal_profile import (
    VagalProfileClassifier,
    KubiosData,
    BehavioralAssessment,
    ThreePhaseMeasurement,
    MultiTriggerMeasurement,
    TriggerTestResult,
    TriggerType,
    create_sample_kubios_data,
)


def example_healthy_ventral():
    """
    Пример 1: Здоровый вентральный профиль (V-V-V)
    
    Человек с хорошей вагусной регуляцией:
    - Высокий RMSSD в покое
    - Умеренная реакция на стресс
    - Быстрое восстановление
    """
    print("=" * 60)
    print("ПРИМЕР 1: Здоровый вентральный профиль")
    print("=" * 60)
    
    # Данные из Kubios
    baseline = KubiosData(
        mean_rr=900,
        sdnn=55,
        rmssd=48,           # Высокий - хороший вагусный тонус
        pnn50=30,
        mean_hr=67,
        vlf_power=500,
        lf_power=600,
        hf_power=500,       # Высокий HF
        lf_hf_ratio=1.2,    # Сбалансированный
        total_power=1600,
        sd1=34,
        sd2=65
    )
    
    stress = KubiosData(
        mean_rr=780,
        sdnn=42,
        rmssd=35,           # Умеренное снижение
        pnn50=22,
        mean_hr=77,
        vlf_power=450,
        lf_power=700,
        hf_power=350,
        lf_hf_ratio=2.0,
        total_power=1500,
        sd1=25,
        sd2=52
    )
    
    recovery = KubiosData(
        mean_rr=880,
        sdnn=52,
        rmssd=45,           # Почти полное восстановление
        pnn50=28,
        mean_hr=68,
        vlf_power=480,
        lf_power=580,
        hf_power=480,
        lf_hf_ratio=1.2,
        total_power=1540,
        sd1=32,
        sd2=62
    )
    
    behavioral = BehavioralAssessment(
        eye_contact=5,
        voice_prosody=4,
        facial_expressivity=5,
        social_engagement=5,
        body_relaxation=4
    )
    
    measurements = ThreePhaseMeasurement(
        baseline=baseline,
        stress=stress,
        recovery=recovery,
        recovery_time_seconds=120
    )
    
    classifier = VagalProfileClassifier()
    profile = classifier.classify(measurements, behavioral)
    
    print(f"Формула профиля: {profile}")
    print(f"Скорость восстановления: {profile.recovery_speed_percent:.1f}%")
    print(f"Индекс реактивности: {profile.reactivity_index:.1f}")
    print(f"Когерентность: {profile.coherence_score:.1f}")
    print(f"\nИнтерпретация: {profile.get_interpretation()}")
    print()


def example_pseudo_ventral():
    """
    Пример 2: Псевдо-вентральный профиль (S-V(p)-D)
    
    Человек выглядит социально адаптированным, но:
    - Физиологически в симпатической активации
    - При стрессе уходит в дорсальный коллапс
    - Медленное восстановление
    """
    print("=" * 60)
    print("ПРИМЕР 2: Псевдо-вентральный профиль (маскировка)")
    print("=" * 60)
    
    baseline = KubiosData(
        mean_rr=720,
        sdnn=32,
        rmssd=18,           # Низкий - симпатика
        pnn50=8,
        mean_hr=83,
        vlf_power=400,
        lf_power=600,
        hf_power=120,       # Низкий HF
        lf_hf_ratio=5.0,    # Высокий - симпатическое доминирование
        total_power=1120,
        sd1=13,
        sd2=38
    )
    
    stress = KubiosData(
        mean_rr=700,
        sdnn=25,
        rmssd=15,
        pnn50=5,
        mean_hr=86,
        vlf_power=350,
        lf_power=500,
        hf_power=80,
        lf_hf_ratio=6.2,
        total_power=930,
        sd1=11,
        sd2=30
    )
    
    # Плохое восстановление
    recovery = KubiosData(
        mean_rr=710,
        sdnn=28,
        rmssd=16,           # Почти не восстановился
        pnn50=6,
        mean_hr=85,
        vlf_power=380,
        lf_power=550,
        hf_power=100,
        lf_hf_ratio=5.5,
        total_power=1030,
        sd1=12,
        sd2=33
    )
    
    # НО! Внешне выглядит хорошо (социальная маска)
    behavioral = BehavioralAssessment(
        eye_contact=4,
        voice_prosody=4,
        facial_expressivity=4,
        social_engagement=5,
        body_relaxation=4,      # Кажется расслабленным
        reports_anxiety=True    # Но сам отмечает тревогу
    )
    
    measurements = ThreePhaseMeasurement(
        baseline=baseline,
        stress=stress,
        recovery=recovery,
        recovery_time_seconds=300  # Долгое восстановление
    )
    
    classifier = VagalProfileClassifier()
    profile = classifier.classify(measurements, behavioral)
    
    print(f"Формула профиля: {profile}")
    print(f"Скорость восстановления: {profile.recovery_speed_percent:.1f}%")
    print(f"Индекс реактивности: {profile.reactivity_index:.1f}")
    print(f"Когерентность: {profile.coherence_score:.1f}")
    print(f"\nИнтерпретация: {profile.get_interpretation()}")
    print()


def example_dorsal_shutdown():
    """
    Пример 3: Дорсальный профиль (D-D-D)
    
    Человек в состоянии shutdown:
    - Очень низкая вариабельность
    - Слабая реакция на стресс
    - Минимальное восстановление
    """
    print("=" * 60)
    print("ПРИМЕР 3: Дорсальный shutdown")
    print("=" * 60)
    
    baseline = KubiosData(
        mean_rr=850,
        sdnn=12,            # ОЧЕНЬ низкий
        rmssd=22,           # Парадокс: не очень низкий
        pnn50=15,
        mean_hr=71,
        vlf_power=100,
        lf_power=150,
        hf_power=100,
        lf_hf_ratio=1.5,
        total_power=350,    # ОЧЕНЬ низкий Total Power
        sd1=8,              # Плоская Пуанкаре
        sd2=15,
        sample_entropy=0.8  # Низкая энтропия
    )
    
    # Минимальная реакция на стресс (система "не отвечает")
    stress = KubiosData(
        mean_rr=840,
        sdnn=11,
        rmssd=21,           # Почти не изменился
        pnn50=14,
        mean_hr=72,
        vlf_power=95,
        lf_power=140,
        hf_power=95,
        lf_hf_ratio=1.5,
        total_power=330,
        sd1=7,
        sd2=14,
        sample_entropy=0.75
    )
    
    recovery = KubiosData(
        mean_rr=845,
        sdnn=11,
        rmssd=21,
        pnn50=14,
        mean_hr=71,
        vlf_power=98,
        lf_power=145,
        hf_power=98,
        lf_hf_ratio=1.5,
        total_power=341,
        sd1=7,
        sd2=14,
        sample_entropy=0.78
    )
    
    behavioral = BehavioralAssessment(
        eye_contact=2,
        voice_prosody=2,
        facial_expressivity=1,
        social_engagement=2,
        body_relaxation=2,
        reports_dissociation=True,
        reports_numbness=True
    )
    
    measurements = ThreePhaseMeasurement(
        baseline=baseline,
        stress=stress,
        recovery=recovery,
        recovery_time_seconds=180
    )
    
    classifier = VagalProfileClassifier()
    profile = classifier.classify(measurements, behavioral)
    
    print(f"Формула профиля: {profile}")
    print(f"Скорость восстановления: {profile.recovery_speed_percent:.1f}%")
    print(f"Индекс реактивности: {profile.reactivity_index:.1f}")
    print(f"Когерентность: {profile.coherence_score:.1f}")
    print(f"\nИнтерпретация: {profile.get_interpretation()}")
    print()


def example_sympathetic_with_dorsal_collapse():
    """
    Пример 4: Симпатика с дорсальным провалом (S-S-D)
    
    Человек в хронической тревоге, который при сильном стрессе
    "проваливается" в оцепенение.
    """
    print("=" * 60)
    print("ПРИМЕР 4: Симпатика с дорсальным коллапсом")
    print("=" * 60)
    
    baseline = KubiosData(
        mean_rr=700,
        sdnn=35,
        rmssd=16,
        pnn50=6,
        mean_hr=86,
        vlf_power=500,
        lf_power=800,
        hf_power=100,
        lf_hf_ratio=8.0,    # Высокий - гипервигильность
        total_power=1400,
        sd1=11,
        sd2=42
    )
    
    # Резкий провал при стрессе
    stress = KubiosData(
        mean_rr=820,        # Парадоксальное замедление
        sdnn=18,
        rmssd=12,
        pnn50=3,
        mean_hr=73,
        vlf_power=200,
        lf_power=300,
        hf_power=50,
        lf_hf_ratio=6.0,
        total_power=550,    # Резкое падение - коллапс
        sd1=8,
        sd2=22
    )
    
    recovery = KubiosData(
        mean_rr=730,
        sdnn=30,
        rmssd=14,
        pnn50=5,
        mean_hr=82,
        vlf_power=450,
        lf_power=700,
        hf_power=90,
        lf_hf_ratio=7.8,
        total_power=1240,
        sd1=10,
        sd2=36
    )
    
    behavioral = BehavioralAssessment(
        eye_contact=3,
        voice_prosody=2,
        facial_expressivity=2,
        social_engagement=2,
        body_relaxation=1,
        reports_anxiety=True
    )
    
    measurements = ThreePhaseMeasurement(
        baseline=baseline,
        stress=stress,
        recovery=recovery,
        recovery_time_seconds=240
    )
    
    classifier = VagalProfileClassifier()
    profile = classifier.classify(measurements, behavioral)
    
    print(f"Формула профиля: {profile}")
    print(f"Скорость восстановления: {profile.recovery_speed_percent:.1f}%")
    print(f"Индекс реактивности: {profile.reactivity_index:.1f}")
    print(f"Когерентность: {profile.coherence_score:.1f}")
    print(f"\nИнтерпретация: {profile.get_interpretation()}")
    print()


def print_threshold_reference():
    """Справочник пороговых значений"""
    print("=" * 60)
    print("СПРАВОЧНИК ПОРОГОВЫХ ЗНАЧЕНИЙ")
    print("=" * 60)
    print("""
    RMSSD (мс) - маркер парасимпатики:
    ├─ > 42    → Вентральный (хороший тонус)
    ├─ 20-42   → Переходная зона
    └─ < 20    → Симпатика/Дорсал (сниженный тонус)
    
    LF/HF ratio - баланс:
    ├─ > 2.0   → Симпатическое доминирование
    ├─ 0.5-2.0 → Сбалансированный
    └─ < 0.5   → Парасимпатическое доминирование
    
    SDNN (мс) - общая вариабельность:
    ├─ > 50    → Хорошая
    ├─ 30-50   → Умеренная
    ├─ 15-30   → Сниженная
    └─ < 15    → Очень низкая (возможен D)
    
    Total Power (мс²):
    └─ < 500   → Возможно дорсальное состояние
    
    Маркеры дорсального (D) паттерна:
    • SDNN < 15 при нормальном RMSSD
    • Total Power < 500
    • Плоская Пуанкаре (SD1 < 10, SD2 < 20)
    • Низкая энтропия (< 1.0)
    • Минимальная реактивность на стресс
    """)


def example_multi_trigger_testing():
    """
    Пример 5: Мульти-триггерное тестирование
    
    Один человек тестируется на 5 разных типов триггеров,
    чтобы определить, к чему он наиболее уязвим.
    """
    print("=" * 60)
    print("ПРИМЕР 5: Мульти-триггерное тестирование")
    print("=" * 60)
    
    # Общий baseline
    baseline = KubiosData(
        mean_rr=820,
        sdnn=45,
        rmssd=38,
        pnn50=25,
        mean_hr=73,
        vlf_power=450,
        lf_power=550,
        hf_power=400,
        lf_hf_ratio=1.4,
        total_power=1400,
        sd1=27,
        sd2=54
    )
    
    # Тест на ПРИВЯЗАННОСТЬ (Ta) - СИЛЬНАЯ РЕАКЦИЯ
    stress_attachment = KubiosData(
        mean_rr=720,
        sdnn=28,
        rmssd=18,           # Сильное падение!
        pnn50=8,
        mean_hr=83,
        vlf_power=400,
        lf_power=650,
        hf_power=150,
        lf_hf_ratio=4.3,    # Резкий рост
        total_power=1200,
        sd1=13,
        sd2=35
    )
    
    # Тест на КОНТРОЛЬ (Tc) - умеренная реакция
    stress_control = KubiosData(
        mean_rr=780,
        sdnn=38,
        rmssd=30,           # Умеренное снижение
        pnn50=18,
        mean_hr=77,
        vlf_power=420,
        lf_power=580,
        hf_power=320,
        lf_hf_ratio=1.8,
        total_power=1320,
        sd1=21,
        sd2=46
    )
    
    # Тест на БЕЗОПАСНОСТЬ (Ts) - средняя реакция
    stress_safety = KubiosData(
        mean_rr=750,
        sdnn=35,
        rmssd=28,
        pnn50=15,
        mean_hr=80,
        vlf_power=400,
        lf_power=600,
        hf_power=280,
        lf_hf_ratio=2.1,
        total_power=1280,
        sd1=20,
        sd2=42
    )
    
    # Тест на ИДЕНТИЧНОСТЬ (Ti) - ВТОРАЯ ПО СИЛЕ РЕАКЦИЯ
    stress_identity = KubiosData(
        mean_rr=740,
        sdnn=30,
        rmssd=22,           # Сильное падение
        pnn50=10,
        mean_hr=81,
        vlf_power=380,
        lf_power=620,
        hf_power=200,
        lf_hf_ratio=3.1,
        total_power=1200,
        sd1=15,
        sd2=38
    )
    
    # Тест на ТЕЛЕСНОЕ (Tb) - слабая реакция
    stress_body = KubiosData(
        mean_rr=800,
        sdnn=42,
        rmssd=35,           # Небольшое снижение
        pnn50=22,
        mean_hr=75,
        vlf_power=440,
        lf_power=540,
        hf_power=380,
        lf_hf_ratio=1.4,
        total_power=1360,
        sd1=25,
        sd2=50
    )
    
    # Финальное восстановление
    final_recovery = KubiosData(
        mean_rr=810,
        sdnn=43,
        rmssd=36,
        pnn50=24,
        mean_hr=74,
        vlf_power=445,
        lf_power=545,
        hf_power=390,
        lf_hf_ratio=1.4,
        total_power=1380,
        sd1=26,
        sd2=52
    )
    
    # Поведенческая оценка
    behavioral = BehavioralAssessment(
        eye_contact=4,
        voice_prosody=4,
        facial_expressivity=4,
        social_engagement=4,
        body_relaxation=3,
        reports_anxiety=True
    )
    
    # Собираем мульти-триггерные измерения
    multi_measurement = MultiTriggerMeasurement(
        baseline=baseline,
        trigger_tests=[
            TriggerTestResult(trigger_type=TriggerType.ATTACHMENT, stress_data=stress_attachment),
            TriggerTestResult(trigger_type=TriggerType.CONTROL, stress_data=stress_control),
            TriggerTestResult(trigger_type=TriggerType.SAFETY, stress_data=stress_safety),
            TriggerTestResult(trigger_type=TriggerType.IDENTITY, stress_data=stress_identity),
            TriggerTestResult(trigger_type=TriggerType.BODY, stress_data=stress_body),
        ],
        final_recovery=final_recovery
    )
    
    classifier = VagalProfileClassifier()
    profile = classifier.classify_with_triggers(multi_measurement, behavioral)
    
    print(f"Формула профиля: {profile}")
    print(f"Полная формула: {profile.get_full_formula()}")
    print(f"Скорость восстановления: {profile.recovery_speed_percent:.1f}%")
    print(f"Максимальная реактивность: {profile.reactivity_index:.1f}")
    print(f"Когерентность: {profile.coherence_score:.1f}")
    print()
    print(profile.get_trigger_report())
    print()
    print(f"Интерпретация:\n{profile.get_interpretation()}")
    print()


def print_trigger_reference():
    """Справочник типов триггеров"""
    print("=" * 60)
    print("СПРАВОЧНИК ТРИГГЕРНЫХ ТИПОВ")
    print("=" * 60)
    print("""
    Ta - ПРИВЯЗАННОСТЬ (Attachment)
    ├─ Отвержение, потеря, одиночество
    ├─ "Меня бросят", "Я никому не нужен"
    └─ Связь: ранние нарушения привязанности
    
    Tc - КОНТРОЛЬ (Control)
    ├─ Неопределённость, хаос, беспомощность
    ├─ "Я ничего не могу сделать", "Всё выходит из-под контроля"
    └─ Связь: травмы беспомощности, learned helplessness
    
    Ts - БЕЗОПАСНОСТЬ (Safety)
    ├─ Угроза, агрессия, конфликт
    ├─ "Мне угрожают", "Я в опасности"
    └─ Связь: физическое насилие, угрозы жизни
    
    Ti - ИДЕНТИЧНОСТЬ (Identity)
    ├─ Стыд, обесценивание, критика
    ├─ "Я плохой", "Я недостаточно хорош"
    └─ Связь: эмоциональное насилие, нарциссическая травма
    
    Tb - ТЕЛЕСНОЕ (Body)
    ├─ Боль, болезнь, телесные ощущения
    ├─ "Моё тело меня подводит"
    └─ Связь: медицинская травма, соматические расстройства
    """)


if __name__ == "__main__":
    print_threshold_reference()
    print()
    print_trigger_reference()
    print()
    
    example_healthy_ventral()
    example_pseudo_ventral()
    example_dorsal_shutdown()
    example_sympathetic_with_dorsal_collapse()
    example_multi_trigger_testing()
    
    print("=" * 60)
    print("Все профили успешно классифицированы!")
    print("=" * 60)
