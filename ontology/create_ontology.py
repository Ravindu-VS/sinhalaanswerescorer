"""
OWL Ontology for Anuradhapura Period - Sri Lankan History.
This creates and saves the ontology using Owlready2.
"""
from owlready2 import *
import os

def create_ontology():
    """Create the Anuradhapura history ontology."""
    onto = get_ontology("http://sinhala-history.org/anuradhapura.owl")

    with onto:
        # ==================== CLASSES ====================
        class HistoricalEntity(Thing): pass
        class Ruler(HistoricalEntity): pass
        class Location(HistoricalEntity): pass
        class Structure(HistoricalEntity): pass
        class Event(HistoricalEntity): pass
        class TimePeriod(HistoricalEntity): pass
        class Religion(HistoricalEntity): pass
        class AdministrativeUnit(HistoricalEntity): pass

        # Sub-classes
        class Tank(Structure): pass
        class Canal(Structure): pass
        class Stupa(Structure): pass
        class Monastery(Structure): pass
        class MonasticOrder(HistoricalEntity): pass
        class Battle(Event): pass
        class Invasion(Event): pass

        # ==================== OBJECT PROPERTIES ====================
        class built_by(ObjectProperty):
            domain = [Structure]
            range = [Ruler]

        class ruled_during(ObjectProperty):
            domain = [Ruler]
            range = [TimePeriod]

        class located_in(ObjectProperty):
            domain = [Structure]
            range = [Location]

        class part_of(ObjectProperty):
            domain = [AdministrativeUnit]
            range = [AdministrativeUnit]

        class introduced_by(ObjectProperty):
            domain = [Religion]
            range = [Ruler]

        class associated_with(ObjectProperty):
            domain = [HistoricalEntity]
            range = [HistoricalEntity]

        class fought_in(ObjectProperty):
            domain = [Ruler]
            range = [Battle]

        class succeeded_by(ObjectProperty):
            domain = [Ruler]
            range = [Ruler]

        class founded_by(ObjectProperty):
            domain = [MonasticOrder]
            range = [Ruler]

        # ==================== DATA PROPERTIES ====================
        class reign_start(DataProperty, FunctionalProperty):
            domain = [Ruler]
            range = [str]

        class reign_end(DataProperty, FunctionalProperty):
            domain = [Ruler]
            range = [str]

        class significance_si(DataProperty, FunctionalProperty):
            domain = [HistoricalEntity]
            range = [str]

        class significance_en(DataProperty, FunctionalProperty):
            domain = [HistoricalEntity]
            range = [str]

        # ==================== INDIVIDUALS ====================

        # --- Locations ---
        anuradhapura = Location("Anuradhapura")
        anuradhapura.significance_si = "අනුරාධපුරය - ශ්‍රී ලංකාවේ පළමු අගනුවර"
        anuradhapura.significance_en = "First capital of Sri Lanka"

        polonnaruwa = Location("Polonnaruwa")
        polonnaruwa.significance_si = "පොළොන්නරුව - අනුරාධපුරයෙන් පසු අගනුවර"

        mihintale = Location("Mihintale")
        mihintale.significance_si = "මිහින්තලේ - බුදුදහම හඳුන්වාදුන් ස්ථානය"

        # --- Time Periods ---
        early_period = TimePeriod("EarlyPeriod_377BCE_to_100CE")
        early_period.significance_si = "මුල් කාලය - රාජධානිය ස්ථාපනය"

        middle_period = TimePeriod("MiddlePeriod_100CE_to_500CE")
        middle_period.significance_si = "මධ්‍ය කාලය - ජලාශ ශිෂ්ටාචාරය"

        late_period = TimePeriod("LatePeriod_500CE_to_1017CE")
        late_period.significance_si = "අවසාන කාලය - පරිහානිය"

        # --- Rulers ---
        pandukabhaya = Ruler("Pandukabhaya")
        pandukabhaya.reign_start = "437 BCE"
        pandukabhaya.reign_end = "367 BCE"
        pandukabhaya.significance_si = "පණ්ඩුකාභය - අනුරාධපුර නිර්මාතෘ"
        pandukabhaya.ruled_during = [early_period]

        devanampiya_tissa = Ruler("Devanampiya_Tissa")
        devanampiya_tissa.reign_start = "247 BCE"
        devanampiya_tissa.reign_end = "207 BCE"
        devanampiya_tissa.significance_si = "දේවානම්පිය තිස්ස - බුදුදහම රාජ්‍ය ආගම කළ රජු"
        devanampiya_tissa.ruled_during = [early_period]

        dutugemunu = Ruler("Dutugemunu")
        dutugemunu.reign_start = "161 BCE"
        dutugemunu.reign_end = "137 BCE"
        dutugemunu.significance_si = "දුටුගැමුණු - ලංකාව එක්සේසත් කළ වීර රජු"
        dutugemunu.ruled_during = [early_period]

        vattagamani = Ruler("Vattagamani_Abhaya")
        vattagamani.reign_start = "29 BCE"
        vattagamani.reign_end = "17 BCE"
        vattagamani.significance_si = "වට්ටගාමිණී අභය - අභයගිරිය ස්ථාපකයා"

        vasabha = Ruler("Vasabha")
        vasabha.reign_start = "67 CE"
        vasabha.reign_end = "111 CE"
        vasabha.significance_si = "වසභ - ජලාශ 11ක් හා ඇළ 12ක් ඉදිකළ රජු"
        vasabha.ruled_during = [middle_period]

        mahasena = Ruler("Mahasena")
        mahasena.reign_start = "274 CE"
        mahasena.reign_end = "301 CE"
        mahasena.significance_si = "මහාසේන - මින්නේරිය වැව හා ජේතවනාරාමය ඉදිකළ රජු"
        mahasena.ruled_during = [middle_period]

        dhatusena = Ruler("Dhatusena")
        dhatusena.reign_start = "455 CE"
        dhatusena.reign_end = "473 CE"
        dhatusena.significance_si = "ධාතුසේන - කලා වැව හා ජය ගඟ ඉදිකළ රජු"
        dhatusena.ruled_during = [middle_period]

        mahinda_v = Ruler("Mahinda_V")
        mahinda_v.reign_start = "982 CE"
        mahinda_v.reign_end = "1017 CE"
        mahinda_v.significance_si = "මහින්ද V - අනුරාධපුරයේ අවසාන රජු"
        mahinda_v.ruled_during = [late_period]

        # --- Tanks ---
        abhaya_wewa = Tank("Abhaya_Wewa")
        abhaya_wewa.significance_si = "අභය වැව - පළමු ප්‍රධාන ජලාශය"
        abhaya_wewa.located_in = [anuradhapura]

        tissa_wewa = Tank("Tissa_Wewa")
        tissa_wewa.built_by = [devanampiya_tissa]
        tissa_wewa.significance_si = "තිස්ස වැව"
        tissa_wewa.located_in = [anuradhapura]

        nuwara_wewa = Tank("Nuwara_Wewa")
        nuwara_wewa.significance_si = "නුවර වැව - නගර ජල සම්පාදනය"
        nuwara_wewa.located_in = [anuradhapura]

        kala_wewa = Tank("Kala_Wewa")
        kala_wewa.built_by = [dhatusena]
        kala_wewa.significance_si = "කලා වැව - ධාතුසේන විසින් ඉදිකළ මහා ජලාශය"

        minneriya_wewa = Tank("Minneriya_Wewa")
        minneriya_wewa.built_by = [mahasena]
        minneriya_wewa.significance_si = "මින්නේරිය වැව - මහාසේන රජු විසින් ඉදිකළ ජලාශය"

        # --- Canals ---
        jaya_ganga = Canal("Jaya_Ganga")
        jaya_ganga.built_by = [dhatusena]
        jaya_ganga.significance_si = "ජය ගඟ (යෝද ඇල) - සැතපුම් 54 දිග ඇළ මාර්ගය"
        jaya_ganga.associated_with = [kala_wewa]

        # --- Stupas ---
        thuparamaya = Stupa("Thuparamaya")
        thuparamaya.built_by = [devanampiya_tissa]
        thuparamaya.significance_si = "ථූපාරාමය - ශ්‍රී ලංකාවේ පළමු දාගැබ"
        thuparamaya.located_in = [anuradhapura]

        ruwanwelisaya = Stupa("Ruwanwelisaya")
        ruwanwelisaya.built_by = [dutugemunu]
        ruwanwelisaya.significance_si = "රුවන්වැලිසෑය - දුටුගැමුණු රජු ඉදිකළ මහා ස්තූපය"
        ruwanwelisaya.located_in = [anuradhapura]

        jetavanarama = Stupa("Jetavanarama")
        jetavanarama.built_by = [mahasena]
        jetavanarama.significance_si = "ජේතවනාරාමය - එකල ලෝකයේ තුන්වන උසම ගොඩනැගිල්ල"
        jetavanarama.located_in = [anuradhapura]

        abhayagiri_stupa = Stupa("Abhayagiri_Stupa")
        abhayagiri_stupa.built_by = [vattagamani]
        abhayagiri_stupa.significance_si = "අභයගිරි ස්තූපය"
        abhayagiri_stupa.located_in = [anuradhapura]

        # --- Sacred Sites ---
        sri_maha_bodhi = Structure("Sri_Maha_Bodhi")
        sri_maha_bodhi.significance_si = "ශ්‍රී මහා බෝධිය - ලෝකයේ පැරණිතම ලේඛනගත රෝපිත වෘක්ෂය"
        sri_maha_bodhi.located_in = [anuradhapura]
        sri_maha_bodhi.associated_with = [devanampiya_tissa]

        # --- Monastic Orders ---
        mahavihara = MonasticOrder("Mahavihara")
        mahavihara.significance_si = "මහාවිහාරය - ස්ථවිරවාදී බෞද්ධ නිකාය"

        abhayagiri_order = MonasticOrder("Abhayagiri_Nikaya")
        abhayagiri_order.founded_by = [vattagamani]
        abhayagiri_order.significance_si = "අභයගිරි නිකාය"

        jetavana_order = MonasticOrder("Jetavana_Nikaya")
        jetavana_order.founded_by = [mahasena]
        jetavana_order.significance_si = "ජේතවන නිකාය"

        # --- Religion ---
        buddhism = Religion("Theravada_Buddhism")
        buddhism.introduced_by = [devanampiya_tissa]
        buddhism.significance_si = "ථේරවාද බුදුදහම - රාජ්‍ය ආගම"

        # --- Events ---
        battle_with_elara = Battle("Battle_of_Vijithapura")
        battle_with_elara.significance_si = "දුටුගැමුණු-එළාර යුද්ධය"
        dutugemunu.fought_in = [battle_with_elara]

        chola_invasion = Invasion("Chola_Invasion_1017")
        chola_invasion.significance_si = "ක්‍රි.ව. 1017 චෝල ආක්‍රමණය - අනුරාධපුරයේ පරිහානිය"
        chola_invasion.associated_with = [mahinda_v]

        # --- Administrative Units ---
        kingdom = AdministrativeUnit("Anuradhapura_Kingdom")
        kingdom.significance_si = "අනුරාධපුර රාජධානිය"

        province = AdministrativeUnit("Province_Rata")
        province.part_of = [kingdom]
        province.significance_si = "රට - පළාත් මට්ටමේ පරිපාලන ඒකකය"

        village = AdministrativeUnit("Village_Gama")
        village.part_of = [province]
        village.significance_si = "ගම - ග්‍රාම මට්ටමේ පරිපාලන ඒකකය"

    return onto


def save_ontology(onto, filepath):
    """Save the ontology to a file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    onto.save(file=filepath, format="rdfxml")
    print(f"Ontology saved to: {filepath}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import ONTOLOGY_FILE
    onto = create_ontology()
    save_ontology(onto, ONTOLOGY_FILE)
    print(f"Classes: {list(onto.classes())}")
    print(f"Individuals: {list(onto.individuals())}")
