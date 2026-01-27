"""
Обзор всех клинических профилей и их связи с психопатологией.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.services.clinical_profiles import (
    CLINICAL_PROFILES,
    DISORDER_PROFILE_MAP,
    ClinicalCategory,
    get_profile,
)


def print_all_profiles_table():
    """Таблица всех профилей"""
    print("=" * 80)
    print("ВСЕ 27 ВАГУСНЫХ ПРОФИЛЕЙ")
    print("=" * 80)
    print()
    
    # Группируем по физиологической доминанте
    for dom in ["V", "S", "D"]:
        dom_name = {"V": "ВЕНТРАЛЬНАЯ", "S": "СИМПАТИЧЕСКАЯ", "D": "ДОРСАЛЬНАЯ"}[dom]
        print(f"\n{'─' * 80}")
        print(f"  {dom_name} ДОМИНАНТА ({dom}-X-X)")
        print(f"{'─' * 80}")
        
        for formula, profile in CLINICAL_PROFILES.items():
            if formula.startswith(dom) or formula.startswith(f"{dom}-V(p)"):
                categories = ", ".join([c.value for c in profile.primary_categories[:2]])
                print(f"\n  {formula:12} │ {profile.name}")
                print(f"               │ Категории: {categories}")
                print(f"               │ Частота: {profile.prevalence}")


def print_disorder_map():
    """Карта расстройств → профили"""
    print("\n" + "=" * 80)
    print("ГДЕ ИСКАТЬ РАССТРОЙСТВА")
    print("=" * 80)
    
    for disorder, profiles in DISORDER_PROFILE_MAP.items():
        print(f"\n🔍 {disorder}")
        print(f"   Профили: {', '.join(profiles)}")


def print_hidden_symptoms_guide():
    """Гид по скрытым симптомам"""
    print("\n" + "=" * 80)
    print("ЧТО МОЖЕТ БЫТЬ СКРЫТО В КАЖДОМ ПРОФИЛЕ")
    print("=" * 80)
    
    for formula, profile in CLINICAL_PROFILES.items():
        if profile.hidden_symptoms:
            print(f"\n{formula} ({profile.name}):")
            for symptom in profile.hidden_symptoms:
                print(f"  ⚠️  {symptom}")


def print_pseudo_profiles():
    """Псевдо-профили — особая опасность"""
    print("\n" + "=" * 80)
    print("ПСЕВДО-ПРОФИЛИ: МАСКА НЕ СООТВЕТСТВУЕТ ФИЗИОЛОГИИ")
    print("=" * 80)
    print("""
    (p) = pseudo — внешняя вентральная презентация при НЕ-вентральной физиологии.
    Человек выглядит адаптированным, но внутри — другое состояние.
    """)
    
    pseudo_profiles = [
        "S-V(p)-V", "S-V(p)-S", "S-V(p)-D",
        "D-V(p)-V", "D-V(p)-S", "D-V(p)-D"
    ]
    
    for formula in pseudo_profiles:
        profile = get_profile(formula)
        if profile:
            print(f"\n{'─' * 60}")
            print(f"  {formula}: {profile.name}")
            print(f"{'─' * 60}")
            print(f"  Физиология: {profile.physiology}")
            print(f"  Презентация: {profile.presentation}")
            print(f"  Скрытое:")
            for h in profile.hidden_symptoms[:2]:
                print(f"    • {h}")
            print(f"  Риски: {', '.join(profile.risks[:2])}")


def print_defense_mechanisms():
    """Защитные механизмы по профилям"""
    print("\n" + "=" * 80)
    print("ЗАЩИТНЫЕ МЕХАНИЗМЫ")
    print("=" * 80)
    
    mechanisms = {}
    for formula, profile in CLINICAL_PROFILES.items():
        for mech in profile.defense_mechanisms:
            if mech not in mechanisms:
                mechanisms[mech] = []
            mechanisms[mech].append(formula)
    
    for mech, profiles in sorted(mechanisms.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n{mech}")
        print(f"  └─ {', '.join(profiles[:5])}")


def print_clinical_summary():
    """Клиническое резюме"""
    print("\n" + "=" * 80)
    print("КЛИНИЧЕСКОЕ РЕЗЮМЕ: ОСНОВНЫЕ ПАТТЕРНЫ")
    print("=" * 80)
    
    print("""
    
    ┌─────────────────────────────────────────────────────────────────────┐
    │                        ТРЕВОЖНЫЙ СПЕКТР                              │
    │                                                                      │
    │  S-S-S    Классическое ГТР, паника, гипервигильность               │
    │  S-V(p)-S Скрытая тревога за маской — "успешный невротик"          │
    │  V-S-S    Тревога с ресурсной базой — хороший прогноз              │
    │  S-S-D    Тревога → истощение → коллапс                            │
    └─────────────────────────────────────────────────────────────────────┘
    
    ┌─────────────────────────────────────────────────────────────────────┐
    │                      ДЕПРЕССИВНЫЙ СПЕКТР                            │
    │                                                                      │
    │  D-D-D    Тяжёлая депрессия, ступор, кататония                     │
    │  D-D-S    Депрессия с паническими атаками                          │
    │  D-S-S    Ажитированная депрессия (высокий суицидальный риск!)     │
    │  D-S-D    Дисфорическая депрессия                                  │
    │  S-D-D    Тревожное истощение → депрессия                          │
    └─────────────────────────────────────────────────────────────────────┘
    
    ┌─────────────────────────────────────────────────────────────────────┐
    │                   ДИССОЦИАТИВНЫЙ СПЕКТР                             │
    │                                                                      │
    │  V-V-D    Диссоциация при триггере (на здоровой базе)              │
    │  S-V(p)-D Псевдо-адаптация с коллапсом — ПТСР                       │
    │  D-V(p)-D Глубокая функциональная диссоциация                      │
    │  D-V(p)-V Жизнь на автопилоте, деперсонализация                    │
    └─────────────────────────────────────────────────────────────────────┘
    
    ┌─────────────────────────────────────────────────────────────────────┐
    │                    ПСИХОСОМАТИКА                                    │
    │                                                                      │
    │  S-V(p)-V Подавленная тревога → тело "говорит"                     │
    │  S-V(p)-S Тревога в теле (соматизация)                             │
    │  S-D-D    Тревога без осознания → хронические боли                 │
    │  Механизм: когда психика не может выразить — выражает тело         │
    └─────────────────────────────────────────────────────────────────────┘
    
    ┌─────────────────────────────────────────────────────────────────────┐
    │                 ОКР / ОБСЕССИИ                                       │
    │                                                                      │
    │  S-S-S    Тревога → контроль → ритуалы                             │
    │  V-S-S    ОКР с хорошим прогнозом (есть ресурс)                    │
    │  Механизм: ритуал как способ управлять невыносимой тревогой        │
    └─────────────────────────────────────────────────────────────────────┘
    
    ┌─────────────────────────────────────────────────────────────────────┐
    │                НАРЦИССИЧЕСКИЙ СПЕКТР                                │
    │                                                                      │
    │  S-V(p)-V Компенсаторный нарциссизм (грандиозная маска)            │
    │  D-V(p)-D Дефицитарный/пустой нарциссизм                           │
    │  Механизм: Ложное Я защищает от невыносимых переживаний            │
    └─────────────────────────────────────────────────────────────────────┘
    
    ┌─────────────────────────────────────────────────────────────────────┐
    │                ПОГРАНИЧНЫЙ СПЕКТР                                   │
    │                                                                      │
    │  S-V(p)-D Нестабильность: маска → тревога → коллапс                │
    │  S-S-D    Тревога → паника → отключение                            │
    │  D-S-D    Дисфория → взрыв → опустошение                           │
    │  Механизм: нестабильность регуляции, расщепление                   │
    └─────────────────────────────────────────────────────────────────────┘
    
    ┌─────────────────────────────────────────────────────────────────────┐
    │                ШИЗОИДНЫЙ / ИЗБЕГАЮЩИЙ                               │
    │                                                                      │
    │  V-D-V    Здоровая интроверсия (есть ресурс)                       │
    │  V-D-D    Глубокая изоляция при наличии возможностей               │
    │  D-D-D    Тотальный уход                                            │
    │  Механизм: контакт = опасность → безопасность в изоляции           │
    └─────────────────────────────────────────────────────────────────────┘
    
    ┌─────────────────────────────────────────────────────────────────────┐
    │                ИСТЕРИЧЕСКОЕ / КОНВЕРСИОННОЕ                         │
    │                                                                      │
    │  S-V(p)-D "La belle indifférence" — спокойствие при симптомах      │
    │  S-S-D    Конверсионные обмороки                                    │
    │  Механизм: тело выражает то, что психика не может                  │
    └─────────────────────────────────────────────────────────────────────┘
    """)


def print_risk_stratification():
    """Стратификация рисков"""
    print("\n" + "=" * 80)
    print("СТРАТИФИКАЦИЯ РИСКОВ")
    print("=" * 80)
    
    high_risk = []
    moderate_risk = []
    
    for formula, profile in CLINICAL_PROFILES.items():
        risks_text = " ".join(profile.risks).lower()
        if "суицид" in risks_text or "госпитализация" in risks_text:
            high_risk.append((formula, profile.name, profile.risks))
        elif "срыв" in risks_text or "острые" in risks_text:
            moderate_risk.append((formula, profile.name, profile.risks))
    
    print("\n🔴 ВЫСОКИЙ РИСК (требует особого внимания):")
    for f, n, r in high_risk:
        print(f"   {f}: {n}")
        print(f"      Риски: {', '.join(r)}")
    
    print("\n🟡 УМЕРЕННЫЙ РИСК:")
    for f, n, r in moderate_risk:
        print(f"   {f}: {n}")


if __name__ == "__main__":
    print_all_profiles_table()
    print_pseudo_profiles()
    print_disorder_map()
    print_clinical_summary()
    print_risk_stratification()
    print_hidden_symptoms_guide()
    
    print("\n" + "=" * 80)
    print("Обзор завершён")
    print("=" * 80)
