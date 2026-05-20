from dataclasses import dataclass
from typing import List, Optional
from utils_typing import Entity, Event, Relation, dataclass

@dataclass
class BusinessEvent(Event):
    pass

@dataclass
class ConflictEvent(Event):
    pass

@dataclass
class ContactEvent(Event):
    pass

@dataclass
class JusticeEvent(Event):
    pass

@dataclass
class LifeEvent(Event):
    pass

@dataclass
class MovementEvent(Event):
    pass

@dataclass
class PersonnelEvent(Event):
    pass

@dataclass
class TransactionEvent(Event):
    pass

@dataclass
class AttackEvent(Event):
    pass

@dataclass
class VulnerabilityRelatedEvent(Event):
    pass

@dataclass
class ManufactureEvent(Event):
    pass

@dataclass
class FilmEvent(Event):
    pass

@dataclass
class MilitaryEvent(Event):
    pass

@dataclass
class MusicEvent(Event):
    pass

@dataclass
class OlympicsEvent(Event):
    pass

@dataclass
class OrganizationEvent(Event):
    pass

@dataclass
class PeopleEvent(Event):
    pass

@dataclass
class ProjectsEvent(Event):
    pass

@dataclass
class SportsEvent(Event):
    pass

@dataclass
class WineEvent(Event):
    pass


@dataclass
class Die(LifeEvent):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, instrument: Optional[List] = None, person: Optional[List] = None, place: Optional[List] = None, victim: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.instrument = instrument if instrument is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []
        self.victim = victim if victim is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Die(mention=\"{self.mention}\", agent={self.agent}, instrument={self.instrument}, person={self.person}, place={self.place}, victim={self.victim}, time={self.time})"


@dataclass
class Spread(Event):
    """A Spread Event occurs when a disease starts or continues to spread within a population."""
    def __init__(self, mention: str, information_source: Optional[List[str]] = None, population: Optional[List[str]] = None,
                 disease: Optional[List[str]] = None, value: Optional[List[str]] = None, trend: Optional[List[str]] = None,
                 place: Optional[List[str]] = None, time: Optional[List[str]] = None):
        self.mention = mention
        self.information_source = information_source if information_source is not None else []
        self.population = population if population is not None else []
        self.disease = disease if disease is not None else []
        self.value = value if value is not None else []
        self.trend = trend if trend is not None else []
        self.place = place if place is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Spread(mention='{self.mention}', information_source={self.information_source}, population={self.population}, disease={self.disease}, value={self.value}, trend={self.trend}, place={self.place}, time={self.time})"


@dataclass
class Infect(Event):
    """An Infect Event occurs when individuals become infected by a disease."""
    def __init__(self, mention: str, information_source: Optional[List[str]] = None, disease: Optional[List[str]] = None,
                 value: Optional[List[str]] = None, place: Optional[List[str]] = None, infected: Optional[List[str]] = None,
                 time: Optional[List[str]] = None):
        self.mention = mention
        self.information_source = information_source if information_source is not None else []
        self.disease = disease if disease is not None else []
        self.value = value if value is not None else []
        self.place = place if place is not None else []
        self.infected = infected if infected is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Infect(mention='{self.mention}', information_source={self.information_source}, disease={self.disease}, value={self.value}, place={self.place}, infected={self.infected}, time={self.time})"


@dataclass
class Death(Event):
    """A Death Event occurs when individuals die, typically due to disease."""
    def __init__(self, mention: str, information_source: Optional[List[str]] = None, disease: Optional[List[str]] = None,
                 value: Optional[List[str]] = None, trend: Optional[List[str]] = None, dead: Optional[List[str]] = None,
                 place: Optional[List[str]] = None, time: Optional[List[str]] = None):
        self.mention = mention
        self.information_source = information_source if information_source is not None else []
        self.disease = disease if disease is not None else []
        self.value = value if value is not None else []
        self.trend = trend if trend is not None else []
        self.dead = dead if dead is not None else []
        self.place = place if place is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Death(mention='{self.mention}', information_source={self.information_source}, disease={self.disease}, value={self.value}, trend={self.trend}, dead={self.dead}, place={self.place}, time={self.time})"


@dataclass
class Prevent(Event):
    """A Prevent Event occurs when actions are taken to prevent the spread or occurrence of a disease."""
    def __init__(self, mention: str, information_source: Optional[List[str]] = None, target: Optional[List[str]] = None,
                 disease: Optional[List[str]] = None, effectiveness: Optional[List[str]] = None,
                 means: Optional[List[str]] = None, agent: Optional[List[str]] = None):
        self.mention = mention
        self.information_source = information_source if information_source is not None else []
        self.target = target if target is not None else []
        self.disease = disease if disease is not None else []
        self.effectiveness = effectiveness if effectiveness is not None else []
        self.means = means if means is not None else []
        self.agent = agent if agent is not None else []

    def __repr__(self):
        return f"Prevent(mention='{self.mention}', information_source={self.information_source}, target={self.target}, disease={self.disease}, effectiveness={self.effectiveness}, means={self.means}, agent={self.agent})"


@dataclass
class Cure(Event):
    """A Cure Event occurs when individuals recover from a disease through medical intervention or treatment."""
    def __init__(self, mention: str, information_source: Optional[List[str]] = None, disease: Optional[List[str]] = None,
                 value: Optional[List[str]] = None, duration: Optional[List[str]] = None, facility: Optional[List[str]] = None,
                 place: Optional[List[str]] = None, effectiveness: Optional[List[str]] = None, cured: Optional[List[str]] = None,
                 means: Optional[List[str]] = None, time: Optional[List[str]] = None):
        self.mention = mention
        self.information_source = information_source if information_source is not None else []
        self.disease = disease if disease is not None else []
        self.value = value if value is not None else []
        self.duration = duration if duration is not None else []
        self.facility = facility if facility is not None else []
        self.place = place if place is not None else []
        self.effectiveness = effectiveness if effectiveness is not None else []
        self.cured = cured if cured is not None else []
        self.means = means if means is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Cure(mention='{self.mention}', information_source={self.information_source}, disease={self.disease}, value={self.value}, duration={self.duration}, facility={self.facility}, place={self.place}, effectiveness={self.effectiveness}, cured={self.cured}, means={self.means}, time={self.time})"


@dataclass
class Control(Event):
    """A Control Event occurs when efforts are made to manage or limit the spread or impact of a disease."""
    def __init__(self, mention: str, authority: Optional[List[str]] = None, information_source: Optional[List[str]] = None,
                 disease: Optional[List[str]] = None, subject: Optional[List[str]] = None, place: Optional[List[str]] = None,
                 means: Optional[List[str]] = None, effectiveness: Optional[List[str]] = None, time: Optional[List[str]] = None):
        self.mention = mention
        self.authority = authority if authority is not None else []
        self.information_source = information_source if information_source is not None else []
        self.disease = disease if disease is not None else []
        self.subject = subject if subject is not None else []
        self.place = place if place is not None else []
        self.means = means if means is not None else []
        self.effectiveness = effectiveness if effectiveness is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Control(mention='{self.mention}', authority={self.authority}, information_source={self.information_source}, disease={self.disease}, subject={self.subject}, place={self.place}, means={self.means}, effectiveness={self.effectiveness}, time={self.time})"


@dataclass
class Symptom(Event):
    """A Symptom Event occurs when specific symptoms or signs of a disease are observed in individuals."""
    def __init__(self, mention: str, information_source: Optional[List[str]] = None, disease: Optional[List[str]] = None,
                 duration: Optional[List[str]] = None, place: Optional[List[str]] = None, symptom: Optional[List[str]] = None,
                 time: Optional[List[str]] = None, person: Optional[List[str]] = None):
        self.mention = mention
        self.information_source = information_source if information_source is not None else []
        self.disease = disease if disease is not None else []
        self.duration = duration if duration is not None else []
        self.place = place if place is not None else []
        self.symptom = symptom if symptom is not None else []
        self.time = time if time is not None else []
        self.person = person if person is not None else []

    def __repr__(self):
        return f"Symptom(mention='{self.mention}', information_source={self.information_source}, disease={self.disease}, duration={self.duration}, place={self.place}, symptom={self.symptom}, time={self.time}, person={self.person})"


@dataclass
class Injure(LifeEvent):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, victim: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.victim = victim if victim is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Injure(mention=\"{self.mention}\", agent={self.agent}, instrument={self.instrument}, place={self.place}, victim={self.victim}, time={self.time})"


# @dataclass
# class Attack(ConflictEvent):
#     def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, attacker: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, target: Optional[List] = None, victim: Optional[List] = None, time: Optional[List] = None):
#         self.mention = mention if mention is not None else []
#         self.agent = agent if agent is not None else []
#         self.attacker = attacker if attacker is not None else []
#         self.instrument = instrument if instrument is not None else []
#         self.place = place if place is not None else []
#         self.target = target if target is not None else []
#         self.victim = victim if victim is not None else []
#         self.time = time if time is not None else []

#     def __repr__(self):
#         return f"Attack(mention=\"{self.mention}\", agent={self.agent}, attacker={self.attacker}, instrument={self.instrument}, place={self.place}, target={self.target}, victim={self.victim}, time={self.time})"


@dataclass
class Attack(ConflictEvent, Event):
    def __init__(self, mention: str, agent: Optional[List[str]] = None, assailant: Optional[List[str]] = None, attacker: Optional[List[str]] = None, instrument: Optional[List[str]] = None, means: Optional[List[str]] = None, place: Optional[List[str]] = None, target: Optional[List[str]] = None, victim: Optional[List[str]] = None,  time: Optional[List[str]] = None,  weapon: Optional[List[str]] = None):
        self.mention = mention
        self.agent = agent if agent is not None else []
        self.assailant = assailant if assailant is not None else []
        self.attacker = attacker if attacker is not None else []
        self.instrument = instrument if instrument is not None else []
        self.means = means if means is not None else []
        self.place = place if place is not None else []
        self.target = target if target is not None else []
        self.victim = victim if victim is not None else []
        self.time = time if time is not None else []
        self.weapon = weapon if weapon is not None else []
    def __repr__(self):
        return f"Attack(mention=\"{self.mention}\", agent={self.agent}, assailant={self.assailant}, attacker={self.attacker}, instrument={self.instrument}, means={self.means}, place={self.place}, target={self.target}, victim={self.victim}, time={self.time}, weapon={self.weapon})"


@dataclass
class Transport(MovementEvent):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, artifact: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, place: Optional[List] = None, vehicle: Optional[List] = None, victim: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.place = place if place is not None else []
        self.vehicle = vehicle if vehicle is not None else []
        self.victim = victim if victim is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Transport(mention=\"{self.mention}\", agent={self.agent}, artifact={self.artifact}, destination={self.destination}, origin={self.origin}, place={self.place}, vehicle={self.vehicle}, victim={self.victim}, time={self.time})"


@dataclass
class TransferMoney(TransactionEvent):
    def __init__(self, mention: Optional[List] = None, beneficiary: Optional[List] = None, giver: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None, money: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.giver = giver if giver is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []
        self.money = money if money is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"TransferMoney(mention=\"{self.mention}\", beneficiary={self.beneficiary}, giver={self.giver}, place={self.place}, recipient={self.recipient}, money={self.money}, time={self.time})"


@dataclass
class Sue(JusticeEvent):
    def __init__(self, mention: Optional[List] = None, adjudicator: Optional[List] = None, defendant: Optional[List] = None, place: Optional[List] = None, plaintiff: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.defendant = defendant if defendant is not None else []
        self.place = place if place is not None else []
        self.plaintiff = plaintiff if plaintiff is not None else []

    def __repr__(self):
        return f"Sue(mention=\"{self.mention}\", adjudicator={self.adjudicator}, defendant={self.defendant}, place={self.place}, plaintiff={self.plaintiff})"


@dataclass
class Convict(JusticeEvent):
    def __init__(self, mention: Optional[List] = None, adjudicator: Optional[List] = None, defendant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.defendant = defendant if defendant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Convict(mention=\"{self.mention}\", adjudicator={self.adjudicator}, defendant={self.defendant}, place={self.place})"


@dataclass
class Sentence(JusticeEvent):
    def __init__(self, mention: Optional[List] = None, adjudicator: Optional[List] = None, defendant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.defendant = defendant if defendant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Sentence(mention=\"{self.mention}\", adjudicator={self.adjudicator}, defendant={self.defendant}, place={self.place})"


@dataclass
class ChargeIndict(JusticeEvent):
    def __init__(self, mention: Optional[List] = None, adjudicator: Optional[List] = None, defendant: Optional[List] = None, place: Optional[List] = None, prosecutor: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.defendant = defendant if defendant is not None else []
        self.place = place if place is not None else []
        self.prosecutor = prosecutor if prosecutor is not None else []

    def __repr__(self):
        return f"ChargeIndict(mention=\"{self.mention}\", adjudicator={self.adjudicator}, defendant={self.defendant}, place={self.place}, prosecutor={self.prosecutor})"


@dataclass
class EndPosition(PersonnelEvent):
    def __init__(self, mention: Optional[List] = None, entity: Optional[List] = None, person: Optional[List] = None, place: Optional[List] = None, position: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []
        self.position = position if position is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"EndPosition(mention=\"{self.mention}\", entity={self.entity}, person={self.person}, place={self.place}, position={self.position}, time={self.time})"


@dataclass
class StartPosition(PersonnelEvent):
    def __init__(self, mention: Optional[List] = None, entity: Optional[List] = None, person: Optional[List] = None, place: Optional[List] = None, position: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []
        self.position = position if position is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"StartPosition(mention=\"{self.mention}\", entity={self.entity}, person={self.person}, place={self.place}, position={self.position}, time={self.time})"


@dataclass
class TransferOwnership(TransactionEvent):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, beneficiary: Optional[List] = None, buyer: Optional[List] = None, place: Optional[List] = None, seller: Optional[List] = None, giver: Optional[List] = None, recipient: Optional[List] = None, thing: Optional[List] = None, price: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.buyer = buyer if buyer is not None else []
        self.place = place if place is not None else []
        self.seller = seller if seller is not None else []
        self.giver = giver if giver is not None else []
        self.recipient = recipient if recipient is not None else []
        self.thing = thing if thing is not None else []
        self.price = price if price is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"TransferOwnership(mention=\"{self.mention}\", artifact={self.artifact}, beneficiary={self.beneficiary}, buyer={self.buyer}, place={self.place}, seller={self.seller}, giver={self.giver}, recipient={self.recipient}, thing={self.thing}, price={self.price}, time={self.time})"


@dataclass
class ArrestJail(JusticeEvent):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, person: Optional[List] = None, place: Optional[List] = None, crime: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []
        self.crime = crime if crime is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"ArrestJail(mention=\"{self.mention}\", agent={self.agent}, person={self.person}, place={self.place}, crime={self.crime}, time={self.time})"


@dataclass
class Demonstrate(ConflictEvent):
    def __init__(self, mention: Optional[List] = None, entity: Optional[List] = None, place: Optional[List] = None, police: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []
        self.police = police if police is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Demonstrate(mention=\"{self.mention}\", entity={self.entity}, place={self.place}, police={self.police}, time={self.time})"


@dataclass
class Appeal(JusticeEvent):
    def __init__(self, mention: Optional[List] = None, adjudicator: Optional[List] = None, place: Optional[List] = None, plaintiff: Optional[List] = None, defendant: Optional[List] = None, prosecutor: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.place = place if place is not None else []
        self.plaintiff = plaintiff if plaintiff is not None else []
        self.defendant = defendant if defendant is not None else []
        self.prosecutor = prosecutor if prosecutor is not None else []

    def __repr__(self):
        return f"Appeal(mention=\"{self.mention}\", adjudicator={self.adjudicator}, place={self.place}, plaintiff={self.plaintiff}, defendant={self.defendant}, prosecutor={self.prosecutor})"


@dataclass
class Execute(JusticeEvent):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, person: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Execute(mention=\"{self.mention}\", agent={self.agent}, person={self.person}, place={self.place})"


@dataclass
class Meet(ContactEvent):
    def __init__(self, mention: Optional[List] = None, entity: Optional[List] = None, place: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Meet(mention=\"{self.mention}\", entity={self.entity}, place={self.place}, time={self.time})"


@dataclass
class Nominate(PersonnelEvent):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, person: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Nominate(mention=\"{self.mention}\", agent={self.agent}, person={self.person}, place={self.place})"


@dataclass
class PhoneWrite(ContactEvent):
    def __init__(self, mention: Optional[List] = None, entity: Optional[List] = None, place: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"PhoneWrite(mention=\"{self.mention}\", entity={self.entity}, place={self.place}, time={self.time})"


@dataclass
class Elect(PersonnelEvent):
    def __init__(self, mention: Optional[List] = None, entity: Optional[List] = None, person: Optional[List] = None, place: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []
        self.agent = agent if agent is not None else []

    def __repr__(self):
        return f"Elect(mention=\"{self.mention}\", entity={self.entity}, person={self.person}, place={self.place}, agent={self.agent})"


@dataclass
class ReleaseParole(JusticeEvent):
    def __init__(self, mention: Optional[List] = None, entity: Optional[List] = None, person: Optional[List] = None, place: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []
        self.agent = agent if agent is not None else []

    def __repr__(self):
        return f"ReleaseParole(mention=\"{self.mention}\", entity={self.entity}, person={self.person}, place={self.place}, agent={self.agent})"


@dataclass
class TrialHearing(JusticeEvent):
    def __init__(self, mention: Optional[List] = None, adjudicator: Optional[List] = None, defendant: Optional[List] = None, place: Optional[List] = None, prosecutor: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.defendant = defendant if defendant is not None else []
        self.place = place if place is not None else []
        self.prosecutor = prosecutor if prosecutor is not None else []

    def __repr__(self):
        return f"TrialHearing(mention=\"{self.mention}\", adjudicator={self.adjudicator}, defendant={self.defendant}, place={self.place}, prosecutor={self.prosecutor})"


@dataclass
class Divorce(LifeEvent):
    def __init__(self, mention: Optional[List] = None, person: Optional[List] = None, place: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Divorce(mention=\"{self.mention}\", person={self.person}, place={self.place}, time={self.time})"


@dataclass
class Marry(LifeEvent):
    def __init__(self, mention: Optional[List] = None, person: Optional[List] = None, place: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Marry(mention=\"{self.mention}\", person={self.person}, place={self.place}, time={self.time})"


@dataclass
class Fine(JusticeEvent):
    def __init__(self, mention: Optional[List] = None, adjudicator: Optional[List] = None, entity: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Fine(mention=\"{self.mention}\", adjudicator={self.adjudicator}, entity={self.entity}, place={self.place})"


@dataclass
class Acquit(JusticeEvent):
    def __init__(self, mention: Optional[List] = None, adjudicator: Optional[List] = None, defendant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.defendant = defendant if defendant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Acquit(mention=\"{self.mention}\", adjudicator={self.adjudicator}, defendant={self.defendant}, place={self.place})"


@dataclass
class EndOrg(BusinessEvent):
    def __init__(self, mention: Optional[List] = None, org: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.org = org if org is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"EndOrg(mention=\"{self.mention}\", org={self.org}, place={self.place})"


@dataclass
class StartOrg(BusinessEvent):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, org: Optional[List] = None, place: Optional[List] = None, organization: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.org = org if org is not None else []
        self.place = place if place is not None else []
        self.organization = organization if organization is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"StartOrg(mention=\"{self.mention}\", agent={self.agent}, org={self.org}, place={self.place}, organization={self.organization}, time={self.time})"


@dataclass
class DeclareBankruptcy(BusinessEvent):
    def __init__(self, mention: Optional[List] = None, org: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.org = org if org is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"DeclareBankruptcy(mention=\"{self.mention}\", org={self.org}, place={self.place})"


@dataclass
class BeBorn(LifeEvent):
    def __init__(self, mention: Optional[List] = None, person: Optional[List] = None, place: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"BeBorn(mention=\"{self.mention}\", person={self.person}, place={self.place}, time={self.time})"


@dataclass
class Extradite(JusticeEvent):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, person: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.person = person if person is not None else []

    def __repr__(self):
        return f"Extradite(mention=\"{self.mention}\", agent={self.agent}, destination={self.destination}, origin={self.origin}, person={self.person})"


@dataclass
class Pardon(JusticeEvent):
    def __init__(self, mention: Optional[List] = None, adjudicator: Optional[List] = None, defendant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.defendant = defendant if defendant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Pardon(mention=\"{self.mention}\", adjudicator={self.adjudicator}, defendant={self.defendant}, place={self.place})"


@dataclass
class MergeOrg(BusinessEvent):
    def __init__(self, mention: Optional[List] = None, org: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.org = org if org is not None else []

    def __repr__(self):
        return f"MergeOrg(mention=\"{self.mention}\", org={self.org})"


@dataclass
class Databreach(AttackEvent):
    def __init__(self, mention: Optional[List] = None, attack_pattern: Optional[List] = None, attacker: Optional[List] = None, compromised_data: Optional[List] = None, damage_amount: Optional[List] = None, number_of_data: Optional[List] = None, number_of_victim: Optional[List] = None, place: Optional[List] = None, purpose: Optional[List] = None, time: Optional[List] = None, tool: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attack_pattern = attack_pattern if attack_pattern is not None else []
        self.attacker = attacker if attacker is not None else []
        self.compromised_data = compromised_data if compromised_data is not None else []
        self.damage_amount = damage_amount if damage_amount is not None else []
        self.number_of_data = number_of_data if number_of_data is not None else []
        self.number_of_victim = number_of_victim if number_of_victim is not None else []
        self.place = place if place is not None else []
        self.purpose = purpose if purpose is not None else []
        self.time = time if time is not None else []
        self.tool = tool if tool is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"Databreach(mention=\"{self.mention}\", attack_pattern={self.attack_pattern}, attacker={self.attacker}, compromised_data={self.compromised_data}, damage_amount={self.damage_amount}, number_of_data={self.number_of_data}, number_of_victim={self.number_of_victim}, place={self.place}, purpose={self.purpose}, time={self.time}, tool={self.tool}, victim={self.victim})"


@dataclass
class Phishing(AttackEvent):
    def __init__(self, mention: Optional[List] = None, attack_pattern: Optional[List] = None, attacker: Optional[List] = None, damage_amount: Optional[List] = None, place: Optional[List] = None, purpose: Optional[List] = None, time: Optional[List] = None, tool: Optional[List] = None, trusted_entity: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attack_pattern = attack_pattern if attack_pattern is not None else []
        self.attacker = attacker if attacker is not None else []
        self.damage_amount = damage_amount if damage_amount is not None else []
        self.place = place if place is not None else []
        self.purpose = purpose if purpose is not None else []
        self.time = time if time is not None else []
        self.tool = tool if tool is not None else []
        self.trusted_entity = trusted_entity if trusted_entity is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"Phishing(mention=\"{self.mention}\", attack_pattern={self.attack_pattern}, attacker={self.attacker}, damage_amount={self.damage_amount}, place={self.place}, purpose={self.purpose}, time={self.time}, tool={self.tool}, trusted_entity={self.trusted_entity}, victim={self.victim})"


@dataclass
class Ransom(AttackEvent):
    def __init__(self, mention: Optional[List] = None, attack_pattern: Optional[List] = None, attacker: Optional[List] = None, damage_amount: Optional[List] = None, payment_method: Optional[List] = None, place: Optional[List] = None, price: Optional[List] = None, time: Optional[List] = None, tool: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attack_pattern = attack_pattern if attack_pattern is not None else []
        self.attacker = attacker if attacker is not None else []
        self.damage_amount = damage_amount if damage_amount is not None else []
        self.payment_method = payment_method if payment_method is not None else []
        self.place = place if place is not None else []
        self.price = price if price is not None else []
        self.time = time if time is not None else []
        self.tool = tool if tool is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"Ransom(mention=\"{self.mention}\", attack_pattern={self.attack_pattern}, attacker={self.attacker}, damage_amount={self.damage_amount}, payment_method={self.payment_method}, place={self.place}, price={self.price}, time={self.time}, tool={self.tool}, victim={self.victim})"


@dataclass
class Patchvulnerability(VulnerabilityRelatedEvent):
    def __init__(self, mention: Optional[List] = None, cve: Optional[List] = None, issues_addressed: Optional[List] = None, patch: Optional[List] = None, patch_number: Optional[List] = None, releaser: Optional[List] = None, supported_platform: Optional[List] = None, time: Optional[List] = None, vulnerability: Optional[List] = None, vulnerable_system: Optional[List] = None, vulnerable_system_version: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.cve = cve if cve is not None else []
        self.issues_addressed = issues_addressed if issues_addressed is not None else []
        self.patch = patch if patch is not None else []
        self.patch_number = patch_number if patch_number is not None else []
        self.releaser = releaser if releaser is not None else []
        self.supported_platform = supported_platform if supported_platform is not None else []
        self.time = time if time is not None else []
        self.vulnerability = vulnerability if vulnerability is not None else []
        self.vulnerable_system = vulnerable_system if vulnerable_system is not None else []
        self.vulnerable_system_version = vulnerable_system_version if vulnerable_system_version is not None else []

    def __repr__(self):
        return f"Patchvulnerability(mention=\"{self.mention}\", cve={self.cve}, issues_addressed={self.issues_addressed}, patch={self.patch}, patch_number={self.patch_number}, releaser={self.releaser}, supported_platform={self.supported_platform}, time={self.time}, vulnerability={self.vulnerability}, vulnerable_system={self.vulnerable_system}, vulnerable_system_version={self.vulnerable_system_version})"


@dataclass
class Discovervulnerability(VulnerabilityRelatedEvent):
    def __init__(self, mention: Optional[List] = None, capabilities: Optional[List] = None, cve: Optional[List] = None, discoverer: Optional[List] = None, supported_platform: Optional[List] = None, time: Optional[List] = None, vulnerability: Optional[List] = None, vulnerable_system: Optional[List] = None, vulnerable_system_owner: Optional[List] = None, vulnerable_system_version: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.capabilities = capabilities if capabilities is not None else []
        self.cve = cve if cve is not None else []
        self.discoverer = discoverer if discoverer is not None else []
        self.supported_platform = supported_platform if supported_platform is not None else []
        self.time = time if time is not None else []
        self.vulnerability = vulnerability if vulnerability is not None else []
        self.vulnerable_system = vulnerable_system if vulnerable_system is not None else []
        self.vulnerable_system_owner = vulnerable_system_owner if vulnerable_system_owner is not None else []
        self.vulnerable_system_version = vulnerable_system_version if vulnerable_system_version is not None else []

    def __repr__(self):
        return f"Discovervulnerability(mention=\"{self.mention}\", capabilities={self.capabilities}, cve={self.cve}, discoverer={self.discoverer}, supported_platform={self.supported_platform}, time={self.time}, vulnerability={self.vulnerability}, vulnerable_system={self.vulnerable_system}, vulnerable_system_owner={self.vulnerable_system_owner}, vulnerable_system_version={self.vulnerable_system_version})"


@dataclass
class Broadcast(ContactEvent):
    def __init__(self, mention: Optional[List] = None, audience: Optional[List] = None, entity: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.audience = audience if audience is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Broadcast(mention=\"{self.mention}\", audience={self.audience}, entity={self.entity}, place={self.place})"


@dataclass
class Contact(Event):
    def __init__(self, mention: Optional[List] = None, entity: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Contact(mention=\"{self.mention}\", entity={self.entity}, place={self.place})"


@dataclass
class TransportPerson(MovementEvent):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, destination: Optional[List] = None, instrument: Optional[List] = None, origin: Optional[List] = None, person: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.destination = destination if destination is not None else []
        self.instrument = instrument if instrument is not None else []
        self.origin = origin if origin is not None else []
        self.person = person if person is not None else []

    def __repr__(self):
        return f"TransportPerson(mention=\"{self.mention}\", agent={self.agent}, destination={self.destination}, instrument={self.instrument}, origin={self.origin}, person={self.person})"


@dataclass
class Artifact(ManufactureEvent):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, artifact: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.artifact = artifact if artifact is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Artifact(mention=\"{self.mention}\", agent={self.agent}, artifact={self.artifact}, place={self.place})"


@dataclass
class TransportArtifact(MovementEvent):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, artifact: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []

    def __repr__(self):
        return f"TransportArtifact(mention=\"{self.mention}\", agent={self.agent}, artifact={self.artifact}, destination={self.destination}, origin={self.origin})"


@dataclass
class Correspondence(ContactEvent):
    def __init__(self, mention: Optional[List] = None, entity: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Correspondence(mention=\"{self.mention}\", entity={self.entity}, place={self.place})"


@dataclass
class Transaction(Event):
    def __init__(self, mention: Optional[List] = None, beneficiary: Optional[List] = None, giver: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.giver = giver if giver is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"Transaction(mention=\"{self.mention}\", beneficiary={self.beneficiary}, giver={self.giver}, place={self.place}, recipient={self.recipient})"


@dataclass
class Collaboration(BusinessEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Collaboration(mention=\"{self.mention}\")"


@dataclass
class Employment(BusinessEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Employment(mention=\"{self.mention}\")"


@dataclass
class EmploymentTenure(BusinessEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"EmploymentTenure(mention=\"{self.mention}\")"


@dataclass
class Financing(BusinessEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Financing(mention=\"{self.mention}\")"


@dataclass
class Investment(BusinessEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Investment(mention=\"{self.mention}\")"


@dataclass
class Layoff(BusinessEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Layoff(mention=\"{self.mention}\")"


@dataclass
class Sponsorship(BusinessEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Sponsorship(mention=\"{self.mention}\")"


@dataclass
class StartSubsidiary(BusinessEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"StartSubsidiary(mention=\"{self.mention}\")"


@dataclass
class Riot(ConflictEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Riot(mention=\"{self.mention}\")"


@dataclass
class SelfImmolation(ConflictEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"SelfImmolation(mention=\"{self.mention}\")"


@dataclass
class EMail(ContactEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"EMail(mention=\"{self.mention}\")"


@dataclass
class LetterCommunication(ContactEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"LetterCommunication(mention=\"{self.mention}\")"


@dataclass
class OnlineChat(ContactEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"OnlineChat(mention=\"{self.mention}\")"


@dataclass
class VideoChat(ContactEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"VideoChat(mention=\"{self.mention}\")"


@dataclass
class VoiceMail(ContactEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"VoiceMail(mention=\"{self.mention}\")"


@dataclass
class Education(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Education(mention=\"{self.mention}\")"


@dataclass
class DubbingPerformance(FilmEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"DubbingPerformance(mention=\"{self.mention}\")"


@dataclass
class FilmCrewGig(FilmEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"FilmCrewGig(mention=\"{self.mention}\")"


@dataclass
class FilmDistribution(FilmEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"FilmDistribution(mention=\"{self.mention}\")"


@dataclass
class FilmFestival(FilmEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"FilmFestival(mention=\"{self.mention}\")"


@dataclass
class FilmProduction(FilmEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"FilmProduction(mention=\"{self.mention}\")"


@dataclass
class Abortion(LifeEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Abortion(mention=\"{self.mention}\")"


@dataclass
class Homesick(LifeEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Homesick(mention=\"{self.mention}\")"


@dataclass
class Pregnancy(LifeEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Pregnancy(mention=\"{self.mention}\")"


@dataclass
class Sick(LifeEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Sick(mention=\"{self.mention}\")"


@dataclass
class Travel(LifeEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Travel(mention=\"{self.mention}\")"


@dataclass
class LeanManufacturing(ManufactureEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"LeanManufacturing(mention=\"{self.mention}\")"


@dataclass
class MilitaryCommand(MilitaryEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"MilitaryCommand(mention=\"{self.mention}\")"


@dataclass
class MilitaryService(MilitaryEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"MilitaryService(mention=\"{self.mention}\")"


@dataclass
class RecruitTraining(MilitaryEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"RecruitTraining(mention=\"{self.mention}\")"


@dataclass
class Recruitment(MilitaryEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Recruitment(mention=\"{self.mention}\")"


@dataclass
class Driving(MovementEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Driving(mention=\"{self.mention}\")"


@dataclass
class Parking(MovementEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Parking(mention=\"{self.mention}\")"


@dataclass
class Transportperson(MovementEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Transportperson(mention=\"{self.mention}\")"


@dataclass
class Compose(MusicEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Compose(mention=\"{self.mention}\")"


@dataclass
class Dance(MusicEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Dance(mention=\"{self.mention}\")"


@dataclass
class GroupMembership(MusicEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"GroupMembership(mention=\"{self.mention}\")"


@dataclass
class Sing(MusicEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Sing(mention=\"{self.mention}\")"


@dataclass
class TrackContribution(MusicEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"TrackContribution(mention=\"{self.mention}\")"


@dataclass
class ClosingCeremony(OlympicsEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"ClosingCeremony(mention=\"{self.mention}\")"


@dataclass
class OlympicAthleteAffiliation(OlympicsEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"OlympicAthleteAffiliation(mention=\"{self.mention}\")"


@dataclass
class OlympicMedalHonor(OlympicsEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"OlympicMedalHonor(mention=\"{self.mention}\")"


@dataclass
class OpeningCeremony(OlympicsEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"OpeningCeremony(mention=\"{self.mention}\")"


@dataclass
class DivisionOfLabour(OrganizationEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"DivisionOfLabour(mention=\"{self.mention}\")"


@dataclass
class Leadership(OrganizationEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Leadership(mention=\"{self.mention}\")"


@dataclass
class OrgCommunication(OrganizationEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"OrgCommunication(mention=\"{self.mention}\")"


@dataclass
class OrganizationBoardMembership(OrganizationEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"OrganizationBoardMembership(mention=\"{self.mention}\")"


@dataclass
class Appointment(PeopleEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Appointment(mention=\"{self.mention}\")"


@dataclass
class PlaceLived(PeopleEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"PlaceLived(mention=\"{self.mention}\")"


@dataclass
class Demotion(PersonnelEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Demotion(mention=\"{self.mention}\")"


@dataclass
class PerformanceAppraisal(PersonnelEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"PerformanceAppraisal(mention=\"{self.mention}\")"


@dataclass
class Promotion(PersonnelEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Promotion(mention=\"{self.mention}\")"


@dataclass
class Resignation(PersonnelEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Resignation(mention=\"{self.mention}\")"


@dataclass
class ProjectParticipation(ProjectsEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"ProjectParticipation(mention=\"{self.mention}\")"


@dataclass
class FairPlay(SportsEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"FairPlay(mention=\"{self.mention}\")"


@dataclass
class SportsTeamRoster(SportsEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"SportsTeamRoster(mention=\"{self.mention}\")"


@dataclass
class SportsTeamSeasonRecord(SportsEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"SportsTeamSeasonRecord(mention=\"{self.mention}\")"


@dataclass
class Tournament(SportsEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Tournament(mention=\"{self.mention}\")"


@dataclass
class Deposit(TransactionEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Deposit(mention=\"{self.mention}\")"


@dataclass
class MoneyLaundering(TransactionEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"MoneyLaundering(mention=\"{self.mention}\")"


@dataclass
class GrapeVarietyComposition(WineEvent):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"GrapeVarietyComposition(mention=\"{self.mention}\")"


@dataclass
class Testing(Event):
    def __init__(self, mention: Optional[List] = None, circumstances: Optional[List] = None, means: Optional[List] = None, product: Optional[List] = None, result: Optional[List] = None, tested_property: Optional[List] = None, tester: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.circumstances = circumstances if circumstances is not None else []
        self.means = means if means is not None else []
        self.product = product if product is not None else []
        self.result = result if result is not None else []
        self.tested_property = tested_property if tested_property is not None else []
        self.tester = tester if tester is not None else []

    def __repr__(self):
        return f"Testing(mention=\"{self.mention}\", circumstances={self.circumstances}, means={self.means}, product={self.product}, result={self.result}, tested_property={self.tested_property}, tester={self.tester})"


@dataclass
class Know(Event):
    def __init__(self, mention: Optional[List] = None, cognizer: Optional[List] = None, evidence: Optional[List] = None, instrument: Optional[List] = None, means: Optional[List] = None, phenomenon: Optional[List] = None, topic: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.cognizer = cognizer if cognizer is not None else []
        self.evidence = evidence if evidence is not None else []
        self.instrument = instrument if instrument is not None else []
        self.means = means if means is not None else []
        self.phenomenon = phenomenon if phenomenon is not None else []
        self.topic = topic if topic is not None else []

    def __repr__(self):
        return f"Know(mention=\"{self.mention}\", cognizer={self.cognizer}, evidence={self.evidence}, instrument={self.instrument}, means={self.means}, phenomenon={self.phenomenon}, topic={self.topic})"


@dataclass
class Telling(Event):
    def __init__(self, mention: Optional[List] = None, addressee: Optional[List] = None, message: Optional[List] = None, speaker: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.addressee = addressee if addressee is not None else []
        self.message = message if message is not None else []
        self.speaker = speaker if speaker is not None else []

    def __repr__(self):
        return f"Telling(mention=\"{self.mention}\", addressee={self.addressee}, message={self.message}, speaker={self.speaker})"


@dataclass
class Confronting_problem(Event):
    def __init__(self, mention: Optional[List] = None, activity: Optional[List] = None, experiencer: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.activity = activity if activity is not None else []
        self.experiencer = experiencer if experiencer is not None else []

    def __repr__(self):
        return f"Confronting_problem(mention=\"{self.mention}\", activity={self.activity}, experiencer={self.experiencer})"


@dataclass
class Hostile_encounter(Event):
    def __init__(self, mention: Optional[List] = None, instrument: Optional[List] = None, issue: Optional[List] = None, purpose: Optional[List] = None, side_1: Optional[List] = None, side_2: Optional[List] = None, sides: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.instrument = instrument if instrument is not None else []
        self.issue = issue if issue is not None else []
        self.purpose = purpose if purpose is not None else []
        self.side_1 = side_1 if side_1 is not None else []
        self.side_2 = side_2 if side_2 is not None else []
        self.sides = sides if sides is not None else []

    def __repr__(self):
        return f"Hostile_encounter(mention=\"{self.mention}\", instrument={self.instrument}, issue={self.issue}, purpose={self.purpose}, side_1={self.side_1}, side_2={self.side_2}, sides={self.sides})"


@dataclass
class Arriving(Event):
    def __init__(self, mention: Optional[List] = None, goal: Optional[List] = None, means: Optional[List] = None, path: Optional[List] = None, place: Optional[List] = None, purpose: Optional[List] = None, source: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.goal = goal if goal is not None else []
        self.means = means if means is not None else []
        self.path = path if path is not None else []
        self.place = place if place is not None else []
        self.purpose = purpose if purpose is not None else []
        self.source = source if source is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Arriving(mention=\"{self.mention}\", goal={self.goal}, means={self.means}, path={self.path}, place={self.place}, purpose={self.purpose}, source={self.source}, theme={self.theme})"


@dataclass
class Education_teaching(Event):
    def __init__(self, mention: Optional[List] = None, course: Optional[List] = None, fact: Optional[List] = None, role: Optional[List] = None, skill: Optional[List] = None, student: Optional[List] = None, subject: Optional[List] = None, teacher: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.course = course if course is not None else []
        self.fact = fact if fact is not None else []
        self.role = role if role is not None else []
        self.skill = skill if skill is not None else []
        self.student = student if student is not None else []
        self.subject = subject if subject is not None else []
        self.teacher = teacher if teacher is not None else []

    def __repr__(self):
        return f"Education_teaching(mention=\"{self.mention}\", course={self.course}, fact={self.fact}, role={self.role}, skill={self.skill}, student={self.student}, subject={self.subject}, teacher={self.teacher})"


@dataclass
class Receiving(Event):
    def __init__(self, mention: Optional[List] = None, donor: Optional[List] = None, recipient: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.donor = donor if donor is not None else []
        self.recipient = recipient if recipient is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Receiving(mention=\"{self.mention}\", donor={self.donor}, recipient={self.recipient}, theme={self.theme})"


@dataclass
class Deciding(Event):
    def __init__(self, mention: Optional[List] = None, cognizer: Optional[List] = None, decision: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.cognizer = cognizer if cognizer is not None else []
        self.decision = decision if decision is not None else []

    def __repr__(self):
        return f"Deciding(mention=\"{self.mention}\", cognizer={self.cognizer}, decision={self.decision})"


@dataclass
class Giving(Event):
    def __init__(self, mention: Optional[List] = None, offerer: Optional[List] = None, recipient: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.offerer = offerer if offerer is not None else []
        self.recipient = recipient if recipient is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Giving(mention=\"{self.mention}\", offerer={self.offerer}, recipient={self.recipient}, theme={self.theme})"


@dataclass
class Cause_to_make_progress(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, project: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.project = project if project is not None else []

    def __repr__(self):
        return f"Cause_to_make_progress(mention=\"{self.mention}\", agent={self.agent}, project={self.project})"


@dataclass
class Commitment(Event):
    def __init__(self, mention: Optional[List] = None, addressee: Optional[List] = None, message: Optional[List] = None, speaker: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.addressee = addressee if addressee is not None else []
        self.message = message if message is not None else []
        self.speaker = speaker if speaker is not None else []

    def __repr__(self):
        return f"Commitment(mention=\"{self.mention}\", addressee={self.addressee}, message={self.message}, speaker={self.speaker})"


@dataclass
class Manufacturing(Event):
    def __init__(self, mention: Optional[List] = None, factory: Optional[List] = None, instrument: Optional[List] = None, producer: Optional[List] = None, product: Optional[List] = None, resource: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.factory = factory if factory is not None else []
        self.instrument = instrument if instrument is not None else []
        self.producer = producer if producer is not None else []
        self.product = product if product is not None else []
        self.resource = resource if resource is not None else []

    def __repr__(self):
        return f"Manufacturing(mention=\"{self.mention}\", factory={self.factory}, instrument={self.instrument}, producer={self.producer}, product={self.product}, resource={self.resource})"


@dataclass
class Killing(Event):
    def __init__(self, mention: Optional[List] = None, cause: Optional[List] = None, instrument: Optional[List] = None, killer: Optional[List] = None, means: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.cause = cause if cause is not None else []
        self.instrument = instrument if instrument is not None else []
        self.killer = killer if killer is not None else []
        self.means = means if means is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"Killing(mention=\"{self.mention}\", cause={self.cause}, instrument={self.instrument}, killer={self.killer}, means={self.means}, victim={self.victim})"


@dataclass
class Causation(Event):
    def __init__(self, mention: Optional[List] = None, actor: Optional[List] = None, affected: Optional[List] = None, cause: Optional[List] = None, effect: Optional[List] = None, means: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.actor = actor if actor is not None else []
        self.affected = affected if affected is not None else []
        self.cause = cause if cause is not None else []
        self.effect = effect if effect is not None else []
        self.means = means if means is not None else []

    def __repr__(self):
        return f"Causation(mention=\"{self.mention}\", actor={self.actor}, affected={self.affected}, cause={self.cause}, effect={self.effect}, means={self.means})"


@dataclass
class Action(Event):
    def __init__(self, mention: Optional[List] = None, act: Optional[List] = None, agent: Optional[List] = None, domain: Optional[List] = None, manner: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.act = act if act is not None else []
        self.agent = agent if agent is not None else []
        self.domain = domain if domain is not None else []
        self.manner = manner if manner is not None else []

    def __repr__(self):
        return f"Action(mention=\"{self.mention}\", act={self.act}, agent={self.agent}, domain={self.domain}, manner={self.manner})"


@dataclass
class Cause_change_of_position_on_a_scale(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, attribute: Optional[List] = None, cause: Optional[List] = None, difference: Optional[List] = None, item: Optional[List] = None, value_1: Optional[List] = None, value_2: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.attribute = attribute if attribute is not None else []
        self.cause = cause if cause is not None else []
        self.difference = difference if difference is not None else []
        self.item = item if item is not None else []
        self.value_1 = value_1 if value_1 is not None else []
        self.value_2 = value_2 if value_2 is not None else []

    def __repr__(self):
        return f"Cause_change_of_position_on_a_scale(mention=\"{self.mention}\", agent={self.agent}, attribute={self.attribute}, cause={self.cause}, difference={self.difference}, item={self.item}, value_1={self.value_1}, value_2={self.value_2})"


@dataclass
class Sending(Event):
    def __init__(self, mention: Optional[List] = None, goal: Optional[List] = None, means: Optional[List] = None, recipient: Optional[List] = None, sender: Optional[List] = None, source: Optional[List] = None, theme: Optional[List] = None, transferors: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.goal = goal if goal is not None else []
        self.means = means if means is not None else []
        self.recipient = recipient if recipient is not None else []
        self.sender = sender if sender is not None else []
        self.source = source if source is not None else []
        self.theme = theme if theme is not None else []
        self.transferors = transferors if transferors is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"Sending(mention=\"{self.mention}\", goal={self.goal}, means={self.means}, recipient={self.recipient}, sender={self.sender}, source={self.source}, theme={self.theme}, transferors={self.transferors}, vehicle={self.vehicle})"


@dataclass
class Preventing_or_letting(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, event: Optional[List] = None, means: Optional[List] = None, potential_hindrance: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.event = event if event is not None else []
        self.means = means if means is not None else []
        self.potential_hindrance = potential_hindrance if potential_hindrance is not None else []

    def __repr__(self):
        return f"Preventing_or_letting(mention=\"{self.mention}\", agent={self.agent}, event={self.event}, means={self.means}, potential_hindrance={self.potential_hindrance})"


@dataclass
class Check(Event):
    def __init__(self, mention: Optional[List] = None, inspector: Optional[List] = None, means: Optional[List] = None, unconfirmed_content: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.inspector = inspector if inspector is not None else []
        self.means = means if means is not None else []
        self.unconfirmed_content = unconfirmed_content if unconfirmed_content is not None else []

    def __repr__(self):
        return f"Check(mention=\"{self.mention}\", inspector={self.inspector}, means={self.means}, unconfirmed_content={self.unconfirmed_content})"


@dataclass
class Statement(Event):
    def __init__(self, mention: Optional[List] = None, addressee: Optional[List] = None, medium: Optional[List] = None, message: Optional[List] = None, speaker: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.addressee = addressee if addressee is not None else []
        self.medium = medium if medium is not None else []
        self.message = message if message is not None else []
        self.speaker = speaker if speaker is not None else []

    def __repr__(self):
        return f"Statement(mention=\"{self.mention}\", addressee={self.addressee}, medium={self.medium}, message={self.message}, speaker={self.speaker})"


@dataclass
class Death(Event):
    def __init__(self, mention: Optional[List] = None, place: Optional[List] = None, time: Optional[List] = None, information_source: Optional[List] = None, disease: Optional[List] = None, value: Optional[List] = None, trend: Optional[List] = None, dead: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []###
        self.time = time if time is not None else []
        self.information_source = information_source if information_source is not None else []
        self.disease = disease if disease is not None else []
        self.value = value if value is not None else []
        self.trend = trend if trend is not None else []
        self.dead = dead if dead is not None else []

    def __repr__(self):
        return f"Death(mention=\"{self.mention}\", place={self.place}, time={self.time}, information_source={self.information_source}, disease={self.disease}, value={self.value}, trend={self.trend}, dead={self.dead})"


@dataclass
class Cure(Event):
    def __init__(self, mention: Optional[List] = None, affliction: Optional[List] = None, medication: Optional[List] = None, patient: Optional[List] = None, treatment: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.affliction = affliction if affliction is not None else []
        self.medication = medication if medication is not None else []
        self.patient = patient if patient is not None else []
        self.treatment = treatment if treatment is not None else []

    def __repr__(self):
        return f"Cure(mention=\"{self.mention}\", affliction={self.affliction}, medication={self.medication}, patient={self.patient}, treatment={self.treatment})"


@dataclass
class Revenge(Event):
    def __init__(self, mention: Optional[List] = None, avenger: Optional[List] = None, injured_party: Optional[List] = None, injury: Optional[List] = None, offender: Optional[List] = None, punishment: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.avenger = avenger if avenger is not None else []
        self.injured_party = injured_party if injured_party is not None else []
        self.injury = injury if injury is not None else []
        self.offender = offender if offender is not None else []
        self.punishment = punishment if punishment is not None else []

    def __repr__(self):
        return f"Revenge(mention=\"{self.mention}\", avenger={self.avenger}, injured_party={self.injured_party}, injury={self.injury}, offender={self.offender}, punishment={self.punishment})"


@dataclass
class Request(Event):
    def __init__(self, mention: Optional[List] = None, addressee: Optional[List] = None, medium: Optional[List] = None, message: Optional[List] = None, speaker: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.addressee = addressee if addressee is not None else []
        self.medium = medium if medium is not None else []
        self.message = message if message is not None else []
        self.speaker = speaker if speaker is not None else []

    def __repr__(self):
        return f"Request(mention=\"{self.mention}\", addressee={self.addressee}, medium={self.medium}, message={self.message}, speaker={self.speaker})"


@dataclass
class Assistance(Event):
    def __init__(self, mention: Optional[List] = None, benefited_party: Optional[List] = None, focal_entity: Optional[List] = None, goal: Optional[List] = None, helper: Optional[List] = None, means: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.benefited_party = benefited_party if benefited_party is not None else []
        self.focal_entity = focal_entity if focal_entity is not None else []
        self.goal = goal if goal is not None else []
        self.helper = helper if helper is not None else []
        self.means = means if means is not None else []

    def __repr__(self):
        return f"Assistance(mention=\"{self.mention}\", benefited_party={self.benefited_party}, focal_entity={self.focal_entity}, goal={self.goal}, helper={self.helper}, means={self.means})"


@dataclass
class Supply(Event):
    def __init__(self, mention: Optional[List] = None, imposed_purpose: Optional[List] = None, recipient: Optional[List] = None, supplier: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.imposed_purpose = imposed_purpose if imposed_purpose is not None else []
        self.recipient = recipient if recipient is not None else []
        self.supplier = supplier if supplier is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Supply(mention=\"{self.mention}\", imposed_purpose={self.imposed_purpose}, recipient={self.recipient}, supplier={self.supplier}, theme={self.theme})"


@dataclass
class Presence(Event):
    def __init__(self, mention: Optional[List] = None, circumstances: Optional[List] = None, duration: Optional[List] = None, entity: Optional[List] = None, inherent_purpose: Optional[List] = None, place: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.circumstances = circumstances if circumstances is not None else []
        self.duration = duration if duration is not None else []
        self.entity = entity if entity is not None else []
        self.inherent_purpose = inherent_purpose if inherent_purpose is not None else []
        self.place = place if place is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Presence(mention=\"{self.mention}\", circumstances={self.circumstances}, duration={self.duration}, entity={self.entity}, inherent_purpose={self.inherent_purpose}, place={self.place}, time={self.time})"


@dataclass
class Getting(Event):
    def __init__(self, mention: Optional[List] = None, means: Optional[List] = None, recipient: Optional[List] = None, source: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.means = means if means is not None else []
        self.recipient = recipient if recipient is not None else []
        self.source = source if source is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Getting(mention=\"{self.mention}\", means={self.means}, recipient={self.recipient}, source={self.source}, theme={self.theme})"


@dataclass
class Rite(Event):
    def __init__(self, mention: Optional[List] = None, member: Optional[List] = None, object: Optional[List] = None, type: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.member = member if member is not None else []
        self.object = object if object is not None else []
        self.type = type if type is not None else []

    def __repr__(self):
        return f"Rite(mention=\"{self.mention}\", member={self.member}, object={self.object}, type={self.type})"


@dataclass
class Wearing(Event):
    def __init__(self, mention: Optional[List] = None, body_location: Optional[List] = None, clothing: Optional[List] = None, wearer: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.body_location = body_location if body_location is not None else []
        self.clothing = clothing if clothing is not None else []
        self.wearer = wearer if wearer is not None else []

    def __repr__(self):
        return f"Wearing(mention=\"{self.mention}\", body_location={self.body_location}, clothing={self.clothing}, wearer={self.wearer})"


@dataclass
class Placing(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, cause: Optional[List] = None, location: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.cause = cause if cause is not None else []
        self.location = location if location is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Placing(mention=\"{self.mention}\", agent={self.agent}, cause={self.cause}, location={self.location}, theme={self.theme})"


@dataclass
class Research(Event):
    def __init__(self, mention: Optional[List] = None, field: Optional[List] = None, researcher: Optional[List] = None, topic: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.field = field if field is not None else []
        self.researcher = researcher if researcher is not None else []
        self.topic = topic if topic is not None else []

    def __repr__(self):
        return f"Research(mention=\"{self.mention}\", field={self.field}, researcher={self.researcher}, topic={self.topic})"


@dataclass
class Legality(Event):
    def __init__(self, mention: Optional[List] = None, action: Optional[List] = None, object: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.action = action if action is not None else []
        self.object = object if object is not None else []

    def __repr__(self):
        return f"Legality(mention=\"{self.mention}\", action={self.action}, object={self.object})"


@dataclass
class Change(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, attribute: Optional[List] = None, cause: Optional[List] = None, entity: Optional[List] = None, final_category: Optional[List] = None, final_value: Optional[List] = None, initial_category: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.attribute = attribute if attribute is not None else []
        self.cause = cause if cause is not None else []
        self.entity = entity if entity is not None else []
        self.final_category = final_category if final_category is not None else []
        self.final_value = final_value if final_value is not None else []
        self.initial_category = initial_category if initial_category is not None else []

    def __repr__(self):
        return f"Change(mention=\"{self.mention}\", agent={self.agent}, attribute={self.attribute}, cause={self.cause}, entity={self.entity}, final_category={self.final_category}, final_value={self.final_value}, initial_category={self.initial_category})"


@dataclass
class Using(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, instrument: Optional[List] = None, means: Optional[List] = None, purpose: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.instrument = instrument if instrument is not None else []
        self.means = means if means is not None else []
        self.purpose = purpose if purpose is not None else []

    def __repr__(self):
        return f"Using(mention=\"{self.mention}\", agent={self.agent}, instrument={self.instrument}, means={self.means}, purpose={self.purpose})"


@dataclass
class Connect(Event):
    def __init__(self, mention: Optional[List] = None, figures: Optional[List] = None, ground: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.figures = figures if figures is not None else []
        self.ground = ground if ground is not None else []

    def __repr__(self):
        return f"Connect(mention=\"{self.mention}\", figures={self.figures}, ground={self.ground})"


# @dataclass
# class Attack(Event):
#     def __init__(self, mention: Optional[List] = None, assailant: Optional[List] = None, means: Optional[List] = None, victim: Optional[List] = None, weapon: Optional[List] = None):
#         self.mention = mention if mention is not None else []
#         self.assailant = assailant if assailant is not None else []
#         self.means = means if means is not None else []
#         self.victim = victim if victim is not None else []
#         self.weapon = weapon if weapon is not None else []

#     def __repr__(self):
#         return f"Attack(mention=\"{self.mention}\", assailant={self.assailant}, means={self.means}, victim={self.victim}, weapon={self.weapon})"


@dataclass
class Motion(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, area: Optional[List] = None, cause: Optional[List] = None, distance: Optional[List] = None, goal: Optional[List] = None, means: Optional[List] = None, path: Optional[List] = None, source: Optional[List] = None, speed: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.area = area if area is not None else []
        self.cause = cause if cause is not None else []
        self.distance = distance if distance is not None else []
        self.goal = goal if goal is not None else []
        self.means = means if means is not None else []
        self.path = path if path is not None else []
        self.source = source if source is not None else []
        self.speed = speed if speed is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Motion(mention=\"{self.mention}\", agent={self.agent}, area={self.area}, cause={self.cause}, distance={self.distance}, goal={self.goal}, means={self.means}, path={self.path}, source={self.source}, speed={self.speed}, theme={self.theme})"


@dataclass
class Cost(Event):
    def __init__(self, mention: Optional[List] = None, asset: Optional[List] = None, goods: Optional[List] = None, intended_event: Optional[List] = None, payer: Optional[List] = None, rate: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.asset = asset if asset is not None else []
        self.goods = goods if goods is not None else []
        self.intended_event = intended_event if intended_event is not None else []
        self.payer = payer if payer is not None else []
        self.rate = rate if rate is not None else []

    def __repr__(self):
        return f"Cost(mention=\"{self.mention}\", asset={self.asset}, goods={self.goods}, intended_event={self.intended_event}, payer={self.payer}, rate={self.rate})"


@dataclass
class Traveling(Event):
    def __init__(self, mention: Optional[List] = None, area: Optional[List] = None, distance: Optional[List] = None, entity: Optional[List] = None, goal: Optional[List] = None, means: Optional[List] = None, path: Optional[List] = None, purpose: Optional[List] = None, traveler: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.area = area if area is not None else []
        self.distance = distance if distance is not None else []
        self.entity = entity if entity is not None else []
        self.goal = goal if goal is not None else []
        self.means = means if means is not None else []
        self.path = path if path is not None else []
        self.purpose = purpose if purpose is not None else []
        self.traveler = traveler if traveler is not None else []

    def __repr__(self):
        return f"Traveling(mention=\"{self.mention}\", area={self.area}, distance={self.distance}, entity={self.entity}, goal={self.goal}, means={self.means}, path={self.path}, purpose={self.purpose}, traveler={self.traveler})"


@dataclass
class Self_motion(Event):
    def __init__(self, mention: Optional[List] = None, direction: Optional[List] = None, distance: Optional[List] = None, goal: Optional[List] = None, path: Optional[List] = None, self_mover: Optional[List] = None, source: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.direction = direction if direction is not None else []
        self.distance = distance if distance is not None else []
        self.goal = goal if goal is not None else []
        self.path = path if path is not None else []
        self.self_mover = self_mover if self_mover is not None else []
        self.source = source if source is not None else []

    def __repr__(self):
        return f"Self_motion(mention=\"{self.mention}\", direction={self.direction}, distance={self.distance}, goal={self.goal}, path={self.path}, self_mover={self.self_mover}, source={self.source})"


@dataclass
class Commerce_pay(Event):
    def __init__(self, mention: Optional[List] = None, buyer: Optional[List] = None, goods: Optional[List] = None, money: Optional[List] = None, seller: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.buyer = buyer if buyer is not None else []
        self.goods = goods if goods is not None else []
        self.money = money if money is not None else []
        self.seller = seller if seller is not None else []

    def __repr__(self):
        return f"Commerce_pay(mention=\"{self.mention}\", buyer={self.buyer}, goods={self.goods}, money={self.money}, seller={self.seller})"


@dataclass
class Commerce_sell(Event):
    def __init__(self, mention: Optional[List] = None, buyer: Optional[List] = None, goods: Optional[List] = None, money: Optional[List] = None, seller: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.buyer = buyer if buyer is not None else []
        self.goods = goods if goods is not None else []
        self.money = money if money is not None else []
        self.seller = seller if seller is not None else []

    def __repr__(self):
        return f"Commerce_sell(mention=\"{self.mention}\", buyer={self.buyer}, goods={self.goods}, money={self.money}, seller={self.seller})"


@dataclass
class Destroying(Event):
    def __init__(self, mention: Optional[List] = None, cause: Optional[List] = None, destroyer: Optional[List] = None, means: Optional[List] = None, patient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.cause = cause if cause is not None else []
        self.destroyer = destroyer if destroyer is not None else []
        self.means = means if means is not None else []
        self.patient = patient if patient is not None else []

    def __repr__(self):
        return f"Destroying(mention=\"{self.mention}\", cause={self.cause}, destroyer={self.destroyer}, means={self.means}, patient={self.patient})"


@dataclass
class Committing_crime(Event):
    def __init__(self, mention: Optional[List] = None, crime: Optional[List] = None, instrument: Optional[List] = None, perpetrator: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.crime = crime if crime is not None else []
        self.instrument = instrument if instrument is not None else []
        self.perpetrator = perpetrator if perpetrator is not None else []

    def __repr__(self):
        return f"Committing_crime(mention=\"{self.mention}\", crime={self.crime}, instrument={self.instrument}, perpetrator={self.perpetrator})"


@dataclass
class Creating(Event):
    def __init__(self, mention: Optional[List] = None, cause: Optional[List] = None, created_entity: Optional[List] = None, creator: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.cause = cause if cause is not None else []
        self.created_entity = created_entity if created_entity is not None else []
        self.creator = creator if creator is not None else []

    def __repr__(self):
        return f"Creating(mention=\"{self.mention}\", cause={self.cause}, created_entity={self.created_entity}, creator={self.creator})"


@dataclass
class Process_end(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, cause: Optional[List] = None, final_subevent: Optional[List] = None, process: Optional[List] = None, state: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.cause = cause if cause is not None else []
        self.final_subevent = final_subevent if final_subevent is not None else []
        self.process = process if process is not None else []
        self.state = state if state is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Process_end(mention=\"{self.mention}\", agent={self.agent}, cause={self.cause}, final_subevent={self.final_subevent}, process={self.process}, state={self.state}, time={self.time})"


@dataclass
class Dispersal(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, cause: Optional[List] = None, goal_area: Optional[List] = None, individuals: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.cause = cause if cause is not None else []
        self.goal_area = goal_area if goal_area is not None else []
        self.individuals = individuals if individuals is not None else []

    def __repr__(self):
        return f"Dispersal(mention=\"{self.mention}\", agent={self.agent}, cause={self.cause}, goal_area={self.goal_area}, individuals={self.individuals})"


@dataclass
class Reveal_secret(Event):
    def __init__(self, mention: Optional[List] = None, addressee: Optional[List] = None, information: Optional[List] = None, speaker: Optional[List] = None, topic: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.addressee = addressee if addressee is not None else []
        self.information = information if information is not None else []
        self.speaker = speaker if speaker is not None else []
        self.topic = topic if topic is not None else []

    def __repr__(self):
        return f"Reveal_secret(mention=\"{self.mention}\", addressee={self.addressee}, information={self.information}, speaker={self.speaker}, topic={self.topic})"


@dataclass
class Adducing(Event):
    def __init__(self, mention: Optional[List] = None, medium: Optional[List] = None, role: Optional[List] = None, speaker: Optional[List] = None, specified_entity: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.medium = medium if medium is not None else []
        self.role = role if role is not None else []
        self.speaker = speaker if speaker is not None else []
        self.specified_entity = specified_entity if specified_entity is not None else []

    def __repr__(self):
        return f"Adducing(mention=\"{self.mention}\", medium={self.medium}, role={self.role}, speaker={self.speaker}, specified_entity={self.specified_entity})"


@dataclass
class Recovering(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, entity: Optional[List] = None, means: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.entity = entity if entity is not None else []
        self.means = means if means is not None else []

    def __repr__(self):
        return f"Recovering(mention=\"{self.mention}\", agent={self.agent}, entity={self.entity}, means={self.means})"


@dataclass
class Becoming(Event):
    def __init__(self, mention: Optional[List] = None, entity: Optional[List] = None, final_category: Optional[List] = None, final_quality: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.final_category = final_category if final_category is not None else []
        self.final_quality = final_quality if final_quality is not None else []

    def __repr__(self):
        return f"Becoming(mention=\"{self.mention}\", entity={self.entity}, final_category={self.final_category}, final_quality={self.final_quality})"


@dataclass
class Perception_active(Event):
    def __init__(self, mention: Optional[List] = None, direction: Optional[List] = None, perceiver_agentive: Optional[List] = None, phenomenon: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.direction = direction if direction is not None else []
        self.perceiver_agentive = perceiver_agentive if perceiver_agentive is not None else []
        self.phenomenon = phenomenon if phenomenon is not None else []

    def __repr__(self):
        return f"Perception_active(mention=\"{self.mention}\", direction={self.direction}, perceiver_agentive={self.perceiver_agentive}, phenomenon={self.phenomenon})"


@dataclass
class Removing(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, cause: Optional[List] = None, goal: Optional[List] = None, source: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.cause = cause if cause is not None else []
        self.goal = goal if goal is not None else []
        self.source = source if source is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Removing(mention=\"{self.mention}\", agent={self.agent}, cause={self.cause}, goal={self.goal}, source={self.source}, theme={self.theme})"


@dataclass
class Employment(Event):
    def __init__(self, mention: Optional[List] = None, employee: Optional[List] = None, employer: Optional[List] = None, field: Optional[List] = None, place_of_employment: Optional[List] = None, position: Optional[List] = None, task: Optional[List] = None, type: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.employee = employee if employee is not None else []
        self.employer = employer if employer is not None else []
        self.field = field if field is not None else []
        self.place_of_employment = place_of_employment if place_of_employment is not None else []
        self.position = position if position is not None else []
        self.task = task if task is not None else []
        self.type = type if type is not None else []

    def __repr__(self):
        return f"Employment(mention=\"{self.mention}\", employee={self.employee}, employer={self.employer}, field={self.field}, place_of_employment={self.place_of_employment}, position={self.position}, task={self.task}, type={self.type})"


@dataclass
class Defending(Event):
    def __init__(self, mention: Optional[List] = None, assailant: Optional[List] = None, defender: Optional[List] = None, instrument: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.assailant = assailant if assailant is not None else []
        self.defender = defender if defender is not None else []
        self.instrument = instrument if instrument is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"Defending(mention=\"{self.mention}\", assailant={self.assailant}, defender={self.defender}, instrument={self.instrument}, victim={self.victim})"


@dataclass
class Participation(Event):
    def __init__(self, mention: Optional[List] = None, event: Optional[List] = None, participants: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.event = event if event is not None else []
        self.participants = participants if participants is not None else []

    def __repr__(self):
        return f"Participation(mention=\"{self.mention}\", event={self.event}, participants={self.participants})"


@dataclass
class Communication(Event):
    def __init__(self, mention: Optional[List] = None, addressee: Optional[List] = None, interlocutors: Optional[List] = None, message: Optional[List] = None, speaker: Optional[List] = None, topic: Optional[List] = None, trigger: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.addressee = addressee if addressee is not None else []
        self.interlocutors = interlocutors if interlocutors is not None else []
        self.message = message if message is not None else []
        self.speaker = speaker if speaker is not None else []
        self.topic = topic if topic is not None else []
        self.trigger = trigger if trigger is not None else []

    def __repr__(self):
        return f"Communication(mention=\"{self.mention}\", addressee={self.addressee}, interlocutors={self.interlocutors}, message={self.message}, speaker={self.speaker}, topic={self.topic}, trigger={self.trigger})"


@dataclass
class Hold(Event):
    def __init__(self, mention: Optional[List] = None, entity: Optional[List] = None, manipulator: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.manipulator = manipulator if manipulator is not None else []

    def __repr__(self):
        return f"Hold(mention=\"{self.mention}\", entity={self.entity}, manipulator={self.manipulator})"


@dataclass
class Choosing(Event):
    def __init__(self, mention: Optional[List] = None, chosen: Optional[List] = None, cognizer: Optional[List] = None, possibilities: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.chosen = chosen if chosen is not None else []
        self.cognizer = cognizer if cognizer is not None else []
        self.possibilities = possibilities if possibilities is not None else []

    def __repr__(self):
        return f"Choosing(mention=\"{self.mention}\", chosen={self.chosen}, cognizer={self.cognizer}, possibilities={self.possibilities})"


@dataclass
class Judgment_communication(Event):
    def __init__(self, mention: Optional[List] = None, addressee: Optional[List] = None, communicator: Optional[List] = None, evaluee: Optional[List] = None, medium: Optional[List] = None, reason: Optional[List] = None, topic: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.addressee = addressee if addressee is not None else []
        self.communicator = communicator if communicator is not None else []
        self.evaluee = evaluee if evaluee is not None else []
        self.medium = medium if medium is not None else []
        self.reason = reason if reason is not None else []
        self.topic = topic if topic is not None else []

    def __repr__(self):
        return f"Judgment_communication(mention=\"{self.mention}\", addressee={self.addressee}, communicator={self.communicator}, evaluee={self.evaluee}, medium={self.medium}, reason={self.reason}, topic={self.topic})"


@dataclass
class Building(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, components: Optional[List] = None, created_entity: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.components = components if components is not None else []
        self.created_entity = created_entity if created_entity is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Building(mention=\"{self.mention}\", agent={self.agent}, components={self.components}, created_entity={self.created_entity}, place={self.place})"


@dataclass
class Coming_to_believe(Event):
    def __init__(self, mention: Optional[List] = None, cognizer: Optional[List] = None, content: Optional[List] = None, means: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.cognizer = cognizer if cognizer is not None else []
        self.content = content if content is not None else []
        self.means = means if means is not None else []

    def __repr__(self):
        return f"Coming_to_believe(mention=\"{self.mention}\", cognizer={self.cognizer}, content={self.content}, means={self.means})"


@dataclass
class Change_of_leadership(Event):
    def __init__(self, mention: Optional[List] = None, body: Optional[List] = None, new_leader: Optional[List] = None, old_leader: Optional[List] = None, old_order: Optional[List] = None, role: Optional[List] = None, selector: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.body = body if body is not None else []
        self.new_leader = new_leader if new_leader is not None else []
        self.old_leader = old_leader if old_leader is not None else []
        self.old_order = old_order if old_order is not None else []
        self.role = role if role is not None else []
        self.selector = selector if selector is not None else []

    def __repr__(self):
        return f"Change_of_leadership(mention=\"{self.mention}\", body={self.body}, new_leader={self.new_leader}, old_leader={self.old_leader}, old_order={self.old_order}, role={self.role}, selector={self.selector})"


@dataclass
class Departing(Event):
    def __init__(self, mention: Optional[List] = None, goal: Optional[List] = None, path: Optional[List] = None, source: Optional[List] = None, traveller: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.goal = goal if goal is not None else []
        self.path = path if path is not None else []
        self.source = source if source is not None else []
        self.traveller = traveller if traveller is not None else []

    def __repr__(self):
        return f"Departing(mention=\"{self.mention}\", goal={self.goal}, path={self.path}, source={self.source}, traveller={self.traveller})"


@dataclass
class Terrorism(Event):
    def __init__(self, mention: Optional[List] = None, act: Optional[List] = None, instrument: Optional[List] = None, terrorist: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.act = act if act is not None else []
        self.instrument = instrument if instrument is not None else []
        self.terrorist = terrorist if terrorist is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"Terrorism(mention=\"{self.mention}\", act={self.act}, instrument={self.instrument}, terrorist={self.terrorist}, victim={self.victim})"


@dataclass
class Process_start(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, event: Optional[List] = None, initial_subevent: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.event = event if event is not None else []
        self.initial_subevent = initial_subevent if initial_subevent is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Process_start(mention=\"{self.mention}\", agent={self.agent}, event={self.event}, initial_subevent={self.initial_subevent}, time={self.time})"


@dataclass
class Ratification(Event):
    def __init__(self, mention: Optional[List] = None, proposal: Optional[List] = None, ratifier: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.proposal = proposal if proposal is not None else []
        self.ratifier = ratifier if ratifier is not None else []

    def __repr__(self):
        return f"Ratification(mention=\"{self.mention}\", proposal={self.proposal}, ratifier={self.ratifier})"


@dataclass
class Convincing(Event):
    def __init__(self, mention: Optional[List] = None, addressee: Optional[List] = None, content: Optional[List] = None, speaker: Optional[List] = None, topic: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.addressee = addressee if addressee is not None else []
        self.content = content if content is not None else []
        self.speaker = speaker if speaker is not None else []
        self.topic = topic if topic is not None else []

    def __repr__(self):
        return f"Convincing(mention=\"{self.mention}\", addressee={self.addressee}, content={self.content}, speaker={self.speaker}, topic={self.topic})"


@dataclass
class Containing(Event):
    def __init__(self, mention: Optional[List] = None, container: Optional[List] = None, contents: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.container = container if container is not None else []
        self.contents = contents if contents is not None else []

    def __repr__(self):
        return f"Containing(mention=\"{self.mention}\", container={self.container}, contents={self.contents})"


@dataclass
class Labeling(Event):
    def __init__(self, mention: Optional[List] = None, entity: Optional[List] = None, label: Optional[List] = None, speaker: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.label = label if label is not None else []
        self.speaker = speaker if speaker is not None else []

    def __repr__(self):
        return f"Labeling(mention=\"{self.mention}\", entity={self.entity}, label={self.label}, speaker={self.speaker})"


@dataclass
class Influence(Event):
    def __init__(self, mention: Optional[List] = None, action: Optional[List] = None, agent: Optional[List] = None, behavior: Optional[List] = None, cognizer: Optional[List] = None, product: Optional[List] = None, situation: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.action = action if action is not None else []
        self.agent = agent if agent is not None else []
        self.behavior = behavior if behavior is not None else []
        self.cognizer = cognizer if cognizer is not None else []
        self.product = product if product is not None else []
        self.situation = situation if situation is not None else []

    def __repr__(self):
        return f"Influence(mention=\"{self.mention}\", action={self.action}, agent={self.agent}, behavior={self.behavior}, cognizer={self.cognizer}, product={self.product}, situation={self.situation})"


@dataclass
class Bodily_harm(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, body_part: Optional[List] = None, cause: Optional[List] = None, instrument: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.body_part = body_part if body_part is not None else []
        self.cause = cause if cause is not None else []
        self.instrument = instrument if instrument is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"Bodily_harm(mention=\"{self.mention}\", agent={self.agent}, body_part={self.body_part}, cause={self.cause}, instrument={self.instrument}, victim={self.victim})"


@dataclass
class Motion_directional(Event):
    def __init__(self, mention: Optional[List] = None, area: Optional[List] = None, direction: Optional[List] = None, goal: Optional[List] = None, path: Optional[List] = None, source: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.area = area if area is not None else []
        self.direction = direction if direction is not None else []
        self.goal = goal if goal is not None else []
        self.path = path if path is not None else []
        self.source = source if source is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Motion_directional(mention=\"{self.mention}\", area={self.area}, direction={self.direction}, goal={self.goal}, path={self.path}, source={self.source}, theme={self.theme})"


@dataclass
class Catastrophe(Event):
    def __init__(self, mention: Optional[List] = None, cause: Optional[List] = None, patient: Optional[List] = None, place: Optional[List] = None, undesirable_event: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.cause = cause if cause is not None else []
        self.patient = patient if patient is not None else []
        self.place = place if place is not None else []
        self.undesirable_event = undesirable_event if undesirable_event is not None else []

    def __repr__(self):
        return f"Catastrophe(mention=\"{self.mention}\", cause={self.cause}, patient={self.patient}, place={self.place}, undesirable_event={self.undesirable_event})"


@dataclass
class Bringing(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, area: Optional[List] = None, carrier: Optional[List] = None, goal: Optional[List] = None, source: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.area = area if area is not None else []
        self.carrier = carrier if carrier is not None else []
        self.goal = goal if goal is not None else []
        self.source = source if source is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Bringing(mention=\"{self.mention}\", agent={self.agent}, area={self.area}, carrier={self.carrier}, goal={self.goal}, source={self.source}, theme={self.theme})"


@dataclass
class Sign_agreement(Event):
    def __init__(self, mention: Optional[List] = None, agreement: Optional[List] = None, signatory: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agreement = agreement if agreement is not None else []
        self.signatory = signatory if signatory is not None else []

    def __repr__(self):
        return f"Sign_agreement(mention=\"{self.mention}\", agreement={self.agreement}, signatory={self.signatory})"


@dataclass
class Scrutiny(Event):
    def __init__(self, mention: Optional[List] = None, cognizer: Optional[List] = None, ground: Optional[List] = None, instrument: Optional[List] = None, phenomenon: Optional[List] = None, unwanted_entity: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.cognizer = cognizer if cognizer is not None else []
        self.ground = ground if ground is not None else []
        self.instrument = instrument if instrument is not None else []
        self.phenomenon = phenomenon if phenomenon is not None else []
        self.unwanted_entity = unwanted_entity if unwanted_entity is not None else []

    def __repr__(self):
        return f"Scrutiny(mention=\"{self.mention}\", cognizer={self.cognizer}, ground={self.ground}, instrument={self.instrument}, phenomenon={self.phenomenon}, unwanted_entity={self.unwanted_entity})"


@dataclass
class Commerce_buy(Event):
    def __init__(self, mention: Optional[List] = None, buyer: Optional[List] = None, goods: Optional[List] = None, seller: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.buyer = buyer if buyer is not None else []
        self.goods = goods if goods is not None else []
        self.seller = seller if seller is not None else []

    def __repr__(self):
        return f"Commerce_buy(mention=\"{self.mention}\", buyer={self.buyer}, goods={self.goods}, seller={self.seller})"


@dataclass
class Writing(Event):
    def __init__(self, mention: Optional[List] = None, addressee: Optional[List] = None, author: Optional[List] = None, instrument: Optional[List] = None, text: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.addressee = addressee if addressee is not None else []
        self.author = author if author is not None else []
        self.instrument = instrument if instrument is not None else []
        self.text = text if text is not None else []

    def __repr__(self):
        return f"Writing(mention=\"{self.mention}\", addressee={self.addressee}, author={self.author}, instrument={self.instrument}, text={self.text})"


@dataclass
class Arranging(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, configuration: Optional[List] = None, location: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.configuration = configuration if configuration is not None else []
        self.location = location if location is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Arranging(mention=\"{self.mention}\", agent={self.agent}, configuration={self.configuration}, location={self.location}, theme={self.theme})"


@dataclass
class Supporting(Event):
    def __init__(self, mention: Optional[List] = None, supported: Optional[List] = None, supporter: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.supported = supported if supported is not None else []
        self.supporter = supporter if supporter is not None else []

    def __repr__(self):
        return f"Supporting(mention=\"{self.mention}\", supported={self.supported}, supporter={self.supporter})"


@dataclass
class Conquering(Event):
    def __init__(self, mention: Optional[List] = None, conqueror: Optional[List] = None, means: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.conqueror = conqueror if conqueror is not None else []
        self.means = means if means is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Conquering(mention=\"{self.mention}\", conqueror={self.conqueror}, means={self.means}, theme={self.theme})"


@dataclass
class Response(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, responding_entity: Optional[List] = None, response: Optional[List] = None, trigger: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.responding_entity = responding_entity if responding_entity is not None else []
        self.response = response if response is not None else []
        self.trigger = trigger if trigger is not None else []

    def __repr__(self):
        return f"Response(mention=\"{self.mention}\", agent={self.agent}, responding_entity={self.responding_entity}, response={self.response}, trigger={self.trigger})"


@dataclass
class Competition(Event):
    def __init__(self, mention: Optional[List] = None, competition: Optional[List] = None, participants: Optional[List] = None, venue: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.competition = competition if competition is not None else []
        self.participants = participants if participants is not None else []
        self.venue = venue if venue is not None else []

    def __repr__(self):
        return f"Competition(mention=\"{self.mention}\", competition={self.competition}, participants={self.participants}, venue={self.venue})"


@dataclass
class Come_together(Event):
    def __init__(self, mention: Optional[List] = None, configuration: Optional[List] = None, individuals: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.configuration = configuration if configuration is not None else []
        self.individuals = individuals if individuals is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Come_together(mention=\"{self.mention}\", configuration={self.configuration}, individuals={self.individuals}, place={self.place})"


@dataclass
class Emergency(Event):
    def __init__(self, mention: Optional[List] = None, place: Optional[List] = None, undesirable_event: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.undesirable_event = undesirable_event if undesirable_event is not None else []

    def __repr__(self):
        return f"Emergency(mention=\"{self.mention}\", place={self.place}, undesirable_event={self.undesirable_event})"


@dataclass
class Expansion(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, dimension: Optional[List] = None, initial_size: Optional[List] = None, item: Optional[List] = None, result_size: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.dimension = dimension if dimension is not None else []
        self.initial_size = initial_size if initial_size is not None else []
        self.item = item if item is not None else []
        self.result_size = result_size if result_size is not None else []

    def __repr__(self):
        return f"Expansion(mention=\"{self.mention}\", agent={self.agent}, dimension={self.dimension}, initial_size={self.initial_size}, item={self.item}, result_size={self.result_size})"


@dataclass
class Arrest(Event):
    def __init__(self, mention: Optional[List] = None, authorities: Optional[List] = None, charges: Optional[List] = None, offense: Optional[List] = None, suspect: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.authorities = authorities if authorities is not None else []
        self.charges = charges if charges is not None else []
        self.offense = offense if offense is not None else []
        self.suspect = suspect if suspect is not None else []

    def __repr__(self):
        return f"Arrest(mention=\"{self.mention}\", authorities={self.authorities}, charges={self.charges}, offense={self.offense}, suspect={self.suspect})"


@dataclass
class Openness(Event):
    def __init__(self, mention: Optional[List] = None, barrier: Optional[List] = None, theme: Optional[List] = None, useful_location: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.barrier = barrier if barrier is not None else []
        self.theme = theme if theme is not None else []
        self.useful_location = useful_location if useful_location is not None else []

    def __repr__(self):
        return f"Openness(mention=\"{self.mention}\", barrier={self.barrier}, theme={self.theme}, useful_location={self.useful_location})"


@dataclass
class Becoming_a_member(Event):
    def __init__(self, mention: Optional[List] = None, group: Optional[List] = None, new_member: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.group = group if group is not None else []
        self.new_member = new_member if new_member is not None else []

    def __repr__(self):
        return f"Becoming_a_member(mention=\"{self.mention}\", group={self.group}, new_member={self.new_member})"


@dataclass
class Collaboration(Event):
    def __init__(self, mention: Optional[List] = None, partners: Optional[List] = None, undertaking: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.partners = partners if partners is not None else []
        self.undertaking = undertaking if undertaking is not None else []

    def __repr__(self):
        return f"Collaboration(mention=\"{self.mention}\", partners={self.partners}, undertaking={self.undertaking})"


@dataclass
class Earnings_and_losses(Event):
    def __init__(self, mention: Optional[List] = None, earner: Optional[List] = None, earnings: Optional[List] = None, goods: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.earner = earner if earner is not None else []
        self.earnings = earnings if earnings is not None else []
        self.goods = goods if goods is not None else []

    def __repr__(self):
        return f"Earnings_and_losses(mention=\"{self.mention}\", earner={self.earner}, earnings={self.earnings}, goods={self.goods})"


@dataclass
class Protest(Event):
    def __init__(self, mention: Optional[List] = None, addressee: Optional[List] = None, arguer: Optional[List] = None, content: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.addressee = addressee if addressee is not None else []
        self.arguer = arguer if arguer is not None else []
        self.content = content if content is not None else []

    def __repr__(self):
        return f"Protest(mention=\"{self.mention}\", addressee={self.addressee}, arguer={self.arguer}, content={self.content})"


@dataclass
class Resolve_problem(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, cause: Optional[List] = None, means: Optional[List] = None, problem: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.cause = cause if cause is not None else []
        self.means = means if means is not None else []
        self.problem = problem if problem is not None else []

    def __repr__(self):
        return f"Resolve_problem(mention=\"{self.mention}\", agent={self.agent}, cause={self.cause}, means={self.means}, problem={self.problem})"


@dataclass
class Exchange(Event):
    def __init__(self, mention: Optional[List] = None, exchanger_1: Optional[List] = None, exchanger_2: Optional[List] = None, exchangers: Optional[List] = None, theme_1: Optional[List] = None, theme_2: Optional[List] = None, themes: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.exchanger_1 = exchanger_1 if exchanger_1 is not None else []
        self.exchanger_2 = exchanger_2 if exchanger_2 is not None else []
        self.exchangers = exchangers if exchangers is not None else []
        self.theme_1 = theme_1 if theme_1 is not None else []
        self.theme_2 = theme_2 if theme_2 is not None else []
        self.themes = themes if themes is not None else []

    def __repr__(self):
        return f"Exchange(mention=\"{self.mention}\", exchanger_1={self.exchanger_1}, exchanger_2={self.exchanger_2}, exchangers={self.exchangers}, theme_1={self.theme_1}, theme_2={self.theme_2}, themes={self.themes})"


@dataclass
class Damaging(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, cause: Optional[List] = None, patient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.cause = cause if cause is not None else []
        self.patient = patient if patient is not None else []

    def __repr__(self):
        return f"Damaging(mention=\"{self.mention}\", agent={self.agent}, cause={self.cause}, patient={self.patient})"


@dataclass
class Criminal_investigation(Event):
    def __init__(self, mention: Optional[List] = None, incident: Optional[List] = None, investigator: Optional[List] = None, suspect: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.incident = incident if incident is not None else []
        self.investigator = investigator if investigator is not None else []
        self.suspect = suspect if suspect is not None else []

    def __repr__(self):
        return f"Criminal_investigation(mention=\"{self.mention}\", incident={self.incident}, investigator={self.investigator}, suspect={self.suspect})"


@dataclass
class Create_artwork(Event):
    def __init__(self, mention: Optional[List] = None, activity: Optional[List] = None, culture: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.activity = activity if activity is not None else []
        self.culture = culture if culture is not None else []

    def __repr__(self):
        return f"Create_artwork(mention=\"{self.mention}\", activity={self.activity}, culture={self.culture})"


@dataclass
class Getready(Event):
    def __init__(self, mention: Optional[List] = None, activity: Optional[List] = None, protagonist: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.activity = activity if activity is not None else []
        self.protagonist = protagonist if protagonist is not None else []

    def __repr__(self):
        return f"Getready(mention=\"{self.mention}\", activity={self.activity}, protagonist={self.protagonist})"


@dataclass
class Cause_to_amalgamate(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, part_1: Optional[List] = None, part_2: Optional[List] = None, parts: Optional[List] = None, whole: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.part_1 = part_1 if part_1 is not None else []
        self.part_2 = part_2 if part_2 is not None else []
        self.parts = parts if parts is not None else []
        self.whole = whole if whole is not None else []

    def __repr__(self):
        return f"Cause_to_amalgamate(mention=\"{self.mention}\", agent={self.agent}, part_1={self.part_1}, part_2={self.part_2}, parts={self.parts}, whole={self.whole})"


@dataclass
class Coming_to_be(Event):
    def __init__(self, mention: Optional[List] = None, components: Optional[List] = None, entity: Optional[List] = None, place: Optional[List] = None, time: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.components = components if components is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []
        self.time = time if time is not None else []

    def __repr__(self):
        return f"Coming_to_be(mention=\"{self.mention}\", components={self.components}, entity={self.entity}, place={self.place}, time={self.time})"


@dataclass
class Bearing_arms(Event):
    def __init__(self, mention: Optional[List] = None, protagonist: Optional[List] = None, weapon: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.protagonist = protagonist if protagonist is not None else []
        self.weapon = weapon if weapon is not None else []

    def __repr__(self):
        return f"Bearing_arms(mention=\"{self.mention}\", protagonist={self.protagonist}, weapon={self.weapon})"


@dataclass
class Practice(Event):
    def __init__(self, mention: Optional[List] = None, action: Optional[List] = None, agent: Optional[List] = None, occasion: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.action = action if action is not None else []
        self.agent = agent if agent is not None else []
        self.occasion = occasion if occasion is not None else []

    def __repr__(self):
        return f"Practice(mention=\"{self.mention}\", action={self.action}, agent={self.agent}, occasion={self.occasion})"


@dataclass
class Quarreling(Event):
    def __init__(self, mention: Optional[List] = None, arguer2: Optional[List] = None, arguers: Optional[List] = None, issue: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.arguer2 = arguer2 if arguer2 is not None else []
        self.arguers = arguers if arguers is not None else []
        self.issue = issue if issue is not None else []

    def __repr__(self):
        return f"Quarreling(mention=\"{self.mention}\", arguer2={self.arguer2}, arguers={self.arguers}, issue={self.issue})"


@dataclass
class Hindering(Event):
    def __init__(self, mention: Optional[List] = None, action: Optional[List] = None, hindrance: Optional[List] = None, protagonist: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.action = action if action is not None else []
        self.hindrance = hindrance if hindrance is not None else []
        self.protagonist = protagonist if protagonist is not None else []

    def __repr__(self):
        return f"Hindering(mention=\"{self.mention}\", action={self.action}, hindrance={self.hindrance}, protagonist={self.protagonist})"


@dataclass
class Social_event(Event):
    def __init__(self, mention: Optional[List] = None, attendees: Optional[List] = None, beneficiary: Optional[List] = None, host: Optional[List] = None, occasion: Optional[List] = None, social_event: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attendees = attendees if attendees is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.host = host if host is not None else []
        self.occasion = occasion if occasion is not None else []
        self.social_event = social_event if social_event is not None else []

    def __repr__(self):
        return f"Social_event(mention=\"{self.mention}\", attendees={self.attendees}, beneficiary={self.beneficiary}, host={self.host}, occasion={self.occasion}, social_event={self.social_event})"


@dataclass
class Control(Event):
    def __init__(self, mention: Optional[List] = None, controlling_variable: Optional[List] = None, dependent_variable: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.controlling_variable = controlling_variable if controlling_variable is not None else []
        self.dependent_variable = dependent_variable if dependent_variable is not None else []

    def __repr__(self):
        return f"Control(mention=\"{self.mention}\", controlling_variable={self.controlling_variable}, dependent_variable={self.dependent_variable})"


@dataclass
class Ingestion(Event):
    def __init__(self, mention: Optional[List] = None, ingestibles: Optional[List] = None, ingestor: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.ingestibles = ingestibles if ingestibles is not None else []
        self.ingestor = ingestor if ingestor is not None else []

    def __repr__(self):
        return f"Ingestion(mention=\"{self.mention}\", ingestibles={self.ingestibles}, ingestor={self.ingestor})"


@dataclass
class Emptying(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, cause: Optional[List] = None, source: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.cause = cause if cause is not None else []
        self.source = source if source is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Emptying(mention=\"{self.mention}\", agent={self.agent}, cause={self.cause}, source={self.source}, theme={self.theme})"


@dataclass
class Filling(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, cause: Optional[List] = None, goal: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.cause = cause if cause is not None else []
        self.goal = goal if goal is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Filling(mention=\"{self.mention}\", agent={self.agent}, cause={self.cause}, goal={self.goal}, theme={self.theme})"


@dataclass
class Theft(Event):
    def __init__(self, mention: Optional[List] = None, goods: Optional[List] = None, instrument: Optional[List] = None, means: Optional[List] = None, perpetrator: Optional[List] = None, source: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.goods = goods if goods is not None else []
        self.instrument = instrument if instrument is not None else []
        self.means = means if means is not None else []
        self.perpetrator = perpetrator if perpetrator is not None else []
        self.source = source if source is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"Theft(mention=\"{self.mention}\", goods={self.goods}, instrument={self.instrument}, means={self.means}, perpetrator={self.perpetrator}, source={self.source}, victim={self.victim})"


@dataclass
class Achieve(Event):
    def __init__(self, mention: Optional[List] = None, agent: Optional[List] = None, goal: Optional[List] = None, means: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.goal = goal if goal is not None else []
        self.means = means if means is not None else []

    def __repr__(self):
        return f"Achieve(mention=\"{self.mention}\", agent={self.agent}, goal={self.goal}, means={self.means})"


@dataclass
class Agree_or_refuse_to_act(Event):
    def __init__(self, mention: Optional[List] = None, proposed_action: Optional[List] = None, speaker: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.proposed_action = proposed_action if proposed_action is not None else []
        self.speaker = speaker if speaker is not None else []

    def __repr__(self):
        return f"Agree_or_refuse_to_act(mention=\"{self.mention}\", proposed_action={self.proposed_action}, speaker={self.speaker})"


@dataclass
class Positive_regulation(Event):
    def __init__(self, mention: Optional[List] = None, cause: Optional[List] = None, csite: Optional[List] = None, site: Optional[List] = None, theme: Optional[List] = None, theme2: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.cause = cause if cause is not None else []
        self.csite = csite if csite is not None else []
        self.site = site if site is not None else []
        self.theme = theme if theme is not None else []
        self.theme2 = theme2 if theme2 is not None else []

    def __repr__(self):
        return f"Positive_regulation(mention=\"{self.mention}\", cause={self.cause}, csite={self.csite}, site={self.site}, theme={self.theme}, theme2={self.theme2})"


@dataclass
class Phosphorylation(Event):
    def __init__(self, mention: Optional[List] = None, site: Optional[List] = None, theme: Optional[List] = None, cause: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.site = site if site is not None else []
        self.theme = theme if theme is not None else []
        self.cause = cause if cause is not None else []

    def __repr__(self):
        return f"Phosphorylation(mention=\"{self.mention}\", site={self.site}, theme={self.theme}, cause={self.cause})"


@dataclass
class Gene_expression(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Gene_expression(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Regulation(Event):
    def __init__(self, mention: Optional[List] = None, cause: Optional[List] = None, csite: Optional[List] = None, site: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.cause = cause if cause is not None else []
        self.csite = csite if csite is not None else []
        self.site = site if site is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Regulation(mention=\"{self.mention}\", cause={self.cause}, csite={self.csite}, site={self.site}, theme={self.theme})"


@dataclass
class Binding(Event):
    def __init__(self, mention: Optional[List] = None, site: Optional[List] = None, site2: Optional[List] = None, theme: Optional[List] = None, theme2: Optional[List] = None, theme3: Optional[List] = None, theme4: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.site = site if site is not None else []
        self.site2 = site2 if site2 is not None else []
        self.theme = theme if theme is not None else []
        self.theme2 = theme2 if theme2 is not None else []
        self.theme3 = theme3 if theme3 is not None else []
        self.theme4 = theme4 if theme4 is not None else []

    def __repr__(self):
        return f"Binding(mention=\"{self.mention}\", site={self.site}, site2={self.site2}, theme={self.theme}, theme2={self.theme2}, theme3={self.theme3}, theme4={self.theme4})"


@dataclass
class Localization(Event):
    def __init__(self, mention: Optional[List] = None, atloc: Optional[List] = None, theme: Optional[List] = None, toloc: Optional[List] = None, fromloc: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.atloc = atloc if atloc is not None else []
        self.theme = theme if theme is not None else []
        self.toloc = toloc if toloc is not None else []
        self.fromloc = fromloc if fromloc is not None else []

    def __repr__(self):
        return f"Localization(mention=\"{self.mention}\", atloc={self.atloc}, theme={self.theme}, toloc={self.toloc}, fromloc={self.fromloc})"


@dataclass
class Negative_regulation(Event):
    def __init__(self, mention: Optional[List] = None, cause: Optional[List] = None, csite: Optional[List] = None, site: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.cause = cause if cause is not None else []
        self.csite = csite if csite is not None else []
        self.site = site if site is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Negative_regulation(mention=\"{self.mention}\", cause={self.cause}, csite={self.csite}, site={self.site}, theme={self.theme})"


@dataclass
class Transcription(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Transcription(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Protein_catabolism(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Protein_catabolism(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Protein_modification(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Protein_modification(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Ubiquitination(Event):
    def __init__(self, mention: Optional[List] = None, cause: Optional[List] = None, site: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.cause = cause if cause is not None else []
        self.site = site if site is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Ubiquitination(mention=\"{self.mention}\", cause={self.cause}, site={self.site}, theme={self.theme})"


@dataclass
class Acetylation(Event):
    def __init__(self, mention: Optional[List] = None, site: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.site = site if site is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Acetylation(mention=\"{self.mention}\", site={self.site}, theme={self.theme})"


@dataclass
class Deacetylation(Event):
    def __init__(self, mention: Optional[List] = None, cause: Optional[List] = None, site: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.cause = cause if cause is not None else []
        self.site = site if site is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Deacetylation(mention=\"{self.mention}\", cause={self.cause}, site={self.site}, theme={self.theme})"


@dataclass
class Being_in_operation(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Being_in_operation(mention=\"{self.mention}\")"


@dataclass
class Carry_goods(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Carry_goods(mention=\"{self.mention}\")"


@dataclass
class Cause_to_be_included(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Cause_to_be_included(mention=\"{self.mention}\")"


@dataclass
class Rescuing(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Rescuing(mention=\"{self.mention}\")"


@dataclass
class Military_operation(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Military_operation(mention=\"{self.mention}\")"


@dataclass
class Besieging(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Besieging(mention=\"{self.mention}\")"


@dataclass
class Aiming(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Aiming(mention=\"{self.mention}\")"


@dataclass
class Reporting(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Reporting(mention=\"{self.mention}\")"


@dataclass
class Warning(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Warning(mention=\"{self.mention}\")"


@dataclass
class Expressing_publicly(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Expressing_publicly(mention=\"{self.mention}\")"


@dataclass
class Temporary_stay(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Temporary_stay(mention=\"{self.mention}\")"


@dataclass
class Cause_change_of_strength(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Cause_change_of_strength(mention=\"{self.mention}\")"


@dataclass
class Recording(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Recording(mention=\"{self.mention}\")"


@dataclass
class Surrendering(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Surrendering(mention=\"{self.mention}\")"


@dataclass
class Legal_rulings(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Legal_rulings(mention=\"{self.mention}\")"


@dataclass
class Escaping(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Escaping(mention=\"{self.mention}\")"


@dataclass
class Hiding_objects(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Hiding_objects(mention=\"{self.mention}\")"


@dataclass
class Name_conferral(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Name_conferral(mention=\"{self.mention}\")"


@dataclass
class Change_sentiment(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Change_sentiment(mention=\"{self.mention}\")"


@dataclass
class Lighting(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Lighting(mention=\"{self.mention}\")"


@dataclass
class Having_or_lacking_access(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Having_or_lacking_access(mention=\"{self.mention}\")"


@dataclass
class Rewards_and_punishments(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Rewards_and_punishments(mention=\"{self.mention}\")"


@dataclass
class Preserving(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Preserving(mention=\"{self.mention}\")"


@dataclass
class Renting(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Renting(mention=\"{self.mention}\")"


@dataclass
class Change_event_time(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Change_event_time(mention=\"{self.mention}\")"


@dataclass
class Award(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Award(mention=\"{self.mention}\")"


@dataclass
class Vocalizations(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Vocalizations(mention=\"{self.mention}\")"


@dataclass
class Use_firearm(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Use_firearm(mention=\"{self.mention}\")"


@dataclass
class Violence(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Violence(mention=\"{self.mention}\")"


@dataclass
class Surrounding(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Surrounding(mention=\"{self.mention}\")"


@dataclass
class Prison(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Prison(mention=\"{self.mention}\")"


@dataclass
class Publishing(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Publishing(mention=\"{self.mention}\")"


@dataclass
class Submitting_documents(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Submitting_documents(mention=\"{self.mention}\")"


@dataclass
class Releasing(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Releasing(mention=\"{self.mention}\")"


@dataclass
class Imposing_obligation(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Imposing_obligation(mention=\"{self.mention}\")"


@dataclass
class Scouring(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Scouring(mention=\"{self.mention}\")"


@dataclass
class Justifying(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Justifying(mention=\"{self.mention}\")"


@dataclass
class Expend_resource(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Expend_resource(mention=\"{self.mention}\")"


@dataclass
class Change_tool(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Change_tool(mention=\"{self.mention}\")"


@dataclass
class Breathing(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Breathing(mention=\"{self.mention}\")"


@dataclass
class Kidnapping(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Kidnapping(mention=\"{self.mention}\")"


@dataclass
class Reforming_a_system(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Reforming_a_system(mention=\"{self.mention}\")"


@dataclass
class Forming_relationships(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Forming_relationships(mention=\"{self.mention}\")"


@dataclass
class Giveup(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Giveup(mention=\"{self.mention}\")"


@dataclass
class Body_movement(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Body_movement(mention=\"{self.mention}\")"


@dataclass
class Robbery(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Robbery(mention=\"{self.mention}\")"


@dataclass
class Limiting(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Limiting(mention=\"{self.mention}\")"


@dataclass
class Institutionalization(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Institutionalization(mention=\"{self.mention}\")"


@dataclass
class Patrolling(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Patrolling(mention=\"{self.mention}\")"


@dataclass
class Risk(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Risk(mention=\"{self.mention}\")"


@dataclass
class Suspicion(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Suspicion(mention=\"{self.mention}\")"


@dataclass
class Incident(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Incident(mention=\"{self.mention}\")"


@dataclass
class Extradition(Event):
    def __init__(self, mention: Optional[List] = None):
        self.mention = mention if mention is not None else []

    def __repr__(self):
        return f"Extradition(mention=\"{self.mention}\")"


@dataclass
class Blood_vessel_development(Event):
    def __init__(self, mention: Optional[List] = None, atloc: Optional[List] = None, fromloc: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.atloc = atloc if atloc is not None else []
        self.fromloc = fromloc if fromloc is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Blood_vessel_development(mention=\"{self.mention}\", atloc={self.atloc}, fromloc={self.fromloc}, theme={self.theme})"


@dataclass
class Growth(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Growth(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Planned_process(Event):
    def __init__(self, mention: Optional[List] = None, instrument: Optional[List] = None, instrument2: Optional[List] = None, theme: Optional[List] = None, theme2: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.instrument = instrument if instrument is not None else []
        self.instrument2 = instrument2 if instrument2 is not None else []
        self.theme = theme if theme is not None else []
        self.theme2 = theme2 if theme2 is not None else []

    def __repr__(self):
        return f"Planned_process(mention=\"{self.mention}\", instrument={self.instrument}, instrument2={self.instrument2}, theme={self.theme}, theme2={self.theme2})"


@dataclass
class Cell_proliferation(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Cell_proliferation(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Development(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Development(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Synthesis(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Synthesis(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Remodeling(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Remodeling(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Catabolism(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Catabolism(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Breakdown(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Breakdown(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Pathway(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, participant2: Optional[List] = None, participant3: Optional[List] = None, participant4: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.participant2 = participant2 if participant2 is not None else []
        self.participant3 = participant3 if participant3 is not None else []
        self.participant4 = participant4 if participant4 is not None else []

    def __repr__(self):
        return f"Pathway(mention=\"{self.mention}\", participant={self.participant}, participant2={self.participant2}, participant3={self.participant3}, participant4={self.participant4})"


@dataclass
class Reproduction(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Reproduction(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Protein_processing(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Protein_processing(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Metabolism(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Metabolism(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Translation(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Translation(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Cell_division(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Cell_division(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Dissociation(Event):
    def __init__(self, mention: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Dissociation(mention=\"{self.mention}\", theme={self.theme})"


@dataclass
class Dna_methylation(Event):
    def __init__(self, mention: Optional[List] = None, site: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.site = site if site is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Dna_methylation(mention=\"{self.mention}\", site={self.site}, theme={self.theme})"


@dataclass
class Dephosphorylation(Event):
    def __init__(self, mention: Optional[List] = None, site: Optional[List] = None, theme: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.site = site if site is not None else []
        self.theme = theme if theme is not None else []

    def __repr__(self):
        return f"Dephosphorylation(mention=\"{self.mention}\", site={self.site}, theme={self.theme})"


@dataclass
class Dummy(Event):
    def __init__(self, mention: Optional[List] = None, perpind: Optional[List] = None, perporg: Optional[List] = None, target: Optional[List] = None, victim: Optional[List] = None, weapon: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.perpind = perpind if perpind is not None else []
        self.perporg = perporg if perporg is not None else []
        self.target = target if target is not None else []
        self.victim = victim if victim is not None else []
        self.weapon = weapon if weapon is not None else []

    def __repr__(self):
        return f"Dummy(mention=\"{self.mention}\", perpind={self.perpind}, perporg={self.perporg}, target={self.target}, victim={self.victim}, weapon={self.weapon})"


@dataclass
class Adverse_event(Event):
    def __init__(self, mention: Optional[List] = None, combination_drug: Optional[List] = None, effect: Optional[List] = None, subject: Optional[List] = None, subject_age: Optional[List] = None, subject_disorder: Optional[List] = None, subject_gender: Optional[List] = None, subject_population: Optional[List] = None, subject_race: Optional[List] = None, treatment: Optional[List] = None, treatment_disorder: Optional[List] = None, treatment_dosage: Optional[List] = None, treatment_drug: Optional[List] = None, treatment_duration: Optional[List] = None, treatment_freq: Optional[List] = None, treatment_route: Optional[List] = None, treatment_time_elapsed: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.combination_drug = combination_drug if combination_drug is not None else []
        self.effect = effect if effect is not None else []
        self.subject = subject if subject is not None else []
        self.subject_age = subject_age if subject_age is not None else []
        self.subject_disorder = subject_disorder if subject_disorder is not None else []
        self.subject_gender = subject_gender if subject_gender is not None else []
        self.subject_population = subject_population if subject_population is not None else []
        self.subject_race = subject_race if subject_race is not None else []
        self.treatment = treatment if treatment is not None else []
        self.treatment_disorder = treatment_disorder if treatment_disorder is not None else []
        self.treatment_dosage = treatment_dosage if treatment_dosage is not None else []
        self.treatment_drug = treatment_drug if treatment_drug is not None else []
        self.treatment_duration = treatment_duration if treatment_duration is not None else []
        self.treatment_freq = treatment_freq if treatment_freq is not None else []
        self.treatment_route = treatment_route if treatment_route is not None else []
        self.treatment_time_elapsed = treatment_time_elapsed if treatment_time_elapsed is not None else []

    def __repr__(self):
        return f"Adverse_event(mention=\"{self.mention}\", combination_drug={self.combination_drug}, effect={self.effect}, subject={self.subject}, subject_age={self.subject_age}, subject_disorder={self.subject_disorder}, subject_gender={self.subject_gender}, subject_population={self.subject_population}, subject_race={self.subject_race}, treatment={self.treatment}, treatment_disorder={self.treatment_disorder}, treatment_dosage={self.treatment_dosage}, treatment_drug={self.treatment_drug}, treatment_duration={self.treatment_duration}, treatment_freq={self.treatment_freq}, treatment_route={self.treatment_route}, treatment_time_elapsed={self.treatment_time_elapsed})"


@dataclass
class Potential_therapeutic_event(Event):
    def __init__(self, mention: Optional[List] = None, combination_drug: Optional[List] = None, effect: Optional[List] = None, subject: Optional[List] = None, subject_age: Optional[List] = None, subject_disorder: Optional[List] = None, subject_gender: Optional[List] = None, subject_population: Optional[List] = None, subject_race: Optional[List] = None, treatment: Optional[List] = None, treatment_disorder: Optional[List] = None, treatment_dosage: Optional[List] = None, treatment_drug: Optional[List] = None, treatment_duration: Optional[List] = None, treatment_freq: Optional[List] = None, treatment_route: Optional[List] = None, treatment_time_elapsed: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.combination_drug = combination_drug if combination_drug is not None else []
        self.effect = effect if effect is not None else []
        self.subject = subject if subject is not None else []
        self.subject_age = subject_age if subject_age is not None else []
        self.subject_disorder = subject_disorder if subject_disorder is not None else []
        self.subject_gender = subject_gender if subject_gender is not None else []
        self.subject_population = subject_population if subject_population is not None else []
        self.subject_race = subject_race if subject_race is not None else []
        self.treatment = treatment if treatment is not None else []
        self.treatment_disorder = treatment_disorder if treatment_disorder is not None else []
        self.treatment_dosage = treatment_dosage if treatment_dosage is not None else []
        self.treatment_drug = treatment_drug if treatment_drug is not None else []
        self.treatment_duration = treatment_duration if treatment_duration is not None else []
        self.treatment_freq = treatment_freq if treatment_freq is not None else []
        self.treatment_route = treatment_route if treatment_route is not None else []
        self.treatment_time_elapsed = treatment_time_elapsed if treatment_time_elapsed is not None else []

    def __repr__(self):
        return f"Potential_therapeutic_event(mention=\"{self.mention}\", combination_drug={self.combination_drug}, effect={self.effect}, subject={self.subject}, subject_age={self.subject_age}, subject_disorder={self.subject_disorder}, subject_gender={self.subject_gender}, subject_population={self.subject_population}, subject_race={self.subject_race}, treatment={self.treatment}, treatment_disorder={self.treatment_disorder}, treatment_dosage={self.treatment_dosage}, treatment_drug={self.treatment_drug}, treatment_duration={self.treatment_duration}, treatment_freq={self.treatment_freq}, treatment_route={self.treatment_route}, treatment_time_elapsed={self.treatment_time_elapsed})"


@dataclass
class life_die_deathcausedbyviolentevents(Event):
    def __init__(self, mention: Optional[List] = None, instrument: Optional[List] = None, killer: Optional[List] = None, place: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.instrument = instrument if instrument is not None else []
        self.killer = killer if killer is not None else []
        self.place = place if place is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"life_die_deathcausedbyviolentevents(mention=\"{self.mention}\", instrument={self.instrument}, killer={self.killer}, place={self.place}, victim={self.victim})"


@dataclass
class movement_transportartifact_hide(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, hidingplace: Optional[List] = None, origin: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.hidingplace = hidingplace if hidingplace is not None else []
        self.origin = origin if origin is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"movement_transportartifact_hide(mention=\"{self.mention}\", artifact={self.artifact}, hidingplace={self.hidingplace}, origin={self.origin}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class contact_commitmentpromiseexpressintent_Na(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_commitmentpromiseexpressintent_Na(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class justice_arrestjaildetain_arrestjaildetain(Event):
    def __init__(self, mention: Optional[List] = None, crime: Optional[List] = None, detainee: Optional[List] = None, jailer: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.crime = crime if crime is not None else []
        self.detainee = detainee if detainee is not None else []
        self.jailer = jailer if jailer is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"justice_arrestjaildetain_arrestjaildetain(mention=\"{self.mention}\", crime={self.crime}, detainee={self.detainee}, jailer={self.jailer}, place={self.place})"


@dataclass
class contact_discussion_meet(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"contact_discussion_meet(mention=\"{self.mention}\", participant={self.participant}, place={self.place})"


@dataclass
class life_injure_injurycausedbyviolentevents(Event):
    def __init__(self, mention: Optional[List] = None, injurer: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.injurer = injurer if injurer is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"life_injure_injurycausedbyviolentevents(mention=\"{self.mention}\", injurer={self.injurer}, instrument={self.instrument}, place={self.place}, victim={self.victim})"


@dataclass
class transaction_transferownership_Na(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, beneficiary: Optional[List] = None, giver: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.giver = giver if giver is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"transaction_transferownership_Na(mention=\"{self.mention}\", artifact={self.artifact}, beneficiary={self.beneficiary}, giver={self.giver}, place={self.place}, recipient={self.recipient})"


@dataclass
class justice_investigate_investigatecrime(Event):
    def __init__(self, mention: Optional[List] = None, crime: Optional[List] = None, defendant: Optional[List] = None, investigator: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.crime = crime if crime is not None else []
        self.defendant = defendant if defendant is not None else []
        self.investigator = investigator if investigator is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"justice_investigate_investigatecrime(mention=\"{self.mention}\", crime={self.crime}, defendant={self.defendant}, investigator={self.investigator}, place={self.place})"


@dataclass
class contact_collaborate_Na(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"contact_collaborate_Na(mention=\"{self.mention}\", participant={self.participant}, place={self.place})"


@dataclass
class government_agreements_violateagreement(Event):
    def __init__(self, mention: Optional[List] = None, otherparticipant: Optional[List] = None, place: Optional[List] = None, violator: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.otherparticipant = otherparticipant if otherparticipant is not None else []
        self.place = place if place is not None else []
        self.violator = violator if violator is not None else []

    def __repr__(self):
        return f"government_agreements_violateagreement(mention=\"{self.mention}\", otherparticipant={self.otherparticipant}, place={self.place}, violator={self.violator})"


@dataclass
class movement_transportperson_prevententry(Event):
    def __init__(self, mention: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, passenger: Optional[List] = None, preventer: Optional[List] = None, transporter: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.passenger = passenger if passenger is not None else []
        self.preventer = preventer if preventer is not None else []
        self.transporter = transporter if transporter is not None else []

    def __repr__(self):
        return f"movement_transportperson_prevententry(mention=\"{self.mention}\", destination={self.destination}, origin={self.origin}, passenger={self.passenger}, preventer={self.preventer}, transporter={self.transporter})"


@dataclass
class personnel_endposition_Na(Event):
    def __init__(self, mention: Optional[List] = None, employee: Optional[List] = None, place: Optional[List] = None, placeofemployment: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.employee = employee if employee is not None else []
        self.place = place if place is not None else []
        self.placeofemployment = placeofemployment if placeofemployment is not None else []

    def __repr__(self):
        return f"personnel_endposition_Na(mention=\"{self.mention}\", employee={self.employee}, place={self.place}, placeofemployment={self.placeofemployment})"


@dataclass
class contact_commandorder_broadcast(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_commandorder_broadcast(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class transaction_transfermoney_Na(Event):
    def __init__(self, mention: Optional[List] = None, beneficiary: Optional[List] = None, giver: Optional[List] = None, money: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.giver = giver if giver is not None else []
        self.money = money if money is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"transaction_transfermoney_Na(mention=\"{self.mention}\", beneficiary={self.beneficiary}, giver={self.giver}, money={self.money}, place={self.place}, recipient={self.recipient})"


@dataclass
class conflict_attack_selfdirectedbattle(Event):
    def __init__(self, mention: Optional[List] = None, attacker: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, target: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attacker = attacker if attacker is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.target = target if target is not None else []

    def __repr__(self):
        return f"conflict_attack_selfdirectedbattle(mention=\"{self.mention}\", attacker={self.attacker}, instrument={self.instrument}, place={self.place}, target={self.target})"


@dataclass
class justice_initiatejudicialprocess_Na(Event):
    def __init__(self, mention: Optional[List] = None, crime: Optional[List] = None, defendant: Optional[List] = None, judgecourt: Optional[List] = None, place: Optional[List] = None, prosecutor: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.crime = crime if crime is not None else []
        self.defendant = defendant if defendant is not None else []
        self.judgecourt = judgecourt if judgecourt is not None else []
        self.place = place if place is not None else []
        self.prosecutor = prosecutor if prosecutor is not None else []

    def __repr__(self):
        return f"justice_initiatejudicialprocess_Na(mention=\"{self.mention}\", crime={self.crime}, defendant={self.defendant}, judgecourt={self.judgecourt}, place={self.place}, prosecutor={self.prosecutor})"


@dataclass
class contact_prevarication_broadcast(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_prevarication_broadcast(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class conflict_attack_stealrobhijack(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, attacker: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, target: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.attacker = attacker if attacker is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.target = target if target is not None else []

    def __repr__(self):
        return f"conflict_attack_stealrobhijack(mention=\"{self.mention}\", artifact={self.artifact}, attacker={self.attacker}, instrument={self.instrument}, place={self.place}, target={self.target})"


@dataclass
class life_injure_illnessdegradationhungerthirst(Event):
    def __init__(self, mention: Optional[List] = None, place: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"life_injure_illnessdegradationhungerthirst(mention=\"{self.mention}\", place={self.place}, victim={self.victim})"


@dataclass
class contact_negotiate_meet(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"contact_negotiate_meet(mention=\"{self.mention}\", participant={self.participant}, place={self.place})"


@dataclass
class contact_threatencoerce_Na(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_threatencoerce_Na(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class life_die_Na(Event):
    def __init__(self, mention: Optional[List] = None, place: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"life_die_Na(mention=\"{self.mention}\", place={self.place}, victim={self.victim})"


@dataclass
class contact_commitmentpromiseexpressintent_broadcast(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_commitmentpromiseexpressintent_broadcast(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class personnel_elect_Na(Event):
    def __init__(self, mention: Optional[List] = None, candidate: Optional[List] = None, place: Optional[List] = None, voter: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.candidate = candidate if candidate is not None else []
        self.place = place if place is not None else []
        self.voter = voter if voter is not None else []

    def __repr__(self):
        return f"personnel_elect_Na(mention=\"{self.mention}\", candidate={self.candidate}, place={self.place}, voter={self.voter})"


@dataclass
class contact_mediastatement_broadcast(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_mediastatement_broadcast(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class contact_requestadvise_correspondence(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_requestadvise_correspondence(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class movement_transportartifact_disperseseparate(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"movement_transportartifact_disperseseparate(mention=\"{self.mention}\", artifact={self.artifact}, destination={self.destination}, origin={self.origin}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class government_legislate_legislate(Event):
    def __init__(self, mention: Optional[List] = None, governmentbody: Optional[List] = None, law: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.governmentbody = governmentbody if governmentbody is not None else []
        self.law = law if law is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"government_legislate_legislate(mention=\"{self.mention}\", governmentbody={self.governmentbody}, law={self.law}, place={self.place})"


@dataclass
class personnel_elect_winelection(Event):
    def __init__(self, mention: Optional[List] = None, candidate: Optional[List] = None, place: Optional[List] = None, voter: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.candidate = candidate if candidate is not None else []
        self.place = place if place is not None else []
        self.voter = voter if voter is not None else []

    def __repr__(self):
        return f"personnel_elect_winelection(mention=\"{self.mention}\", candidate={self.candidate}, place={self.place}, voter={self.voter})"


@dataclass
class movement_transportperson_preventexit(Event):
    def __init__(self, mention: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, passenger: Optional[List] = None, preventer: Optional[List] = None, transporter: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.passenger = passenger if passenger is not None else []
        self.preventer = preventer if preventer is not None else []
        self.transporter = transporter if transporter is not None else []

    def __repr__(self):
        return f"movement_transportperson_preventexit(mention=\"{self.mention}\", destination={self.destination}, origin={self.origin}, passenger={self.passenger}, preventer={self.preventer}, transporter={self.transporter})"


@dataclass
class conflict_yield_Na(Event):
    def __init__(self, mention: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None, yielder: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []
        self.yielder = yielder if yielder is not None else []

    def __repr__(self):
        return f"conflict_yield_Na(mention=\"{self.mention}\", place={self.place}, recipient={self.recipient}, yielder={self.yielder})"


@dataclass
class contact_negotiate_Na(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"contact_negotiate_Na(mention=\"{self.mention}\", participant={self.participant}, place={self.place})"


@dataclass
class government_agreements_Na(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"government_agreements_Na(mention=\"{self.mention}\", participant={self.participant}, place={self.place})"


@dataclass
class justice_judicialconsequences_extradite(Event):
    def __init__(self, mention: Optional[List] = None, crime: Optional[List] = None, defendant: Optional[List] = None, destination: Optional[List] = None, extraditer: Optional[List] = None, origin: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.crime = crime if crime is not None else []
        self.defendant = defendant if defendant is not None else []
        self.destination = destination if destination is not None else []
        self.extraditer = extraditer if extraditer is not None else []
        self.origin = origin if origin is not None else []

    def __repr__(self):
        return f"justice_judicialconsequences_extradite(mention=\"{self.mention}\", crime={self.crime}, defendant={self.defendant}, destination={self.destination}, extraditer={self.extraditer}, origin={self.origin})"


@dataclass
class personnel_endposition_firinglayoff(Event):
    def __init__(self, mention: Optional[List] = None, employee: Optional[List] = None, place: Optional[List] = None, placeofemployment: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.employee = employee if employee is not None else []
        self.place = place if place is not None else []
        self.placeofemployment = placeofemployment if placeofemployment is not None else []

    def __repr__(self):
        return f"personnel_endposition_firinglayoff(mention=\"{self.mention}\", employee={self.employee}, place={self.place}, placeofemployment={self.placeofemployment})"


@dataclass
class justice_investigate_Na(Event):
    def __init__(self, mention: Optional[List] = None, defendant: Optional[List] = None, investigator: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.defendant = defendant if defendant is not None else []
        self.investigator = investigator if investigator is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"justice_investigate_Na(mention=\"{self.mention}\", defendant={self.defendant}, investigator={self.investigator}, place={self.place})"


@dataclass
class government_agreements_acceptagreementcontractceasefire(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"government_agreements_acceptagreementcontractceasefire(mention=\"{self.mention}\", participant={self.participant}, place={self.place})"


@dataclass
class disaster_fireexplosion_fireexplosion(Event):
    def __init__(self, mention: Optional[List] = None, fireexplosionobject: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.fireexplosionobject = fireexplosionobject if fireexplosionobject is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"disaster_fireexplosion_fireexplosion(mention=\"{self.mention}\", fireexplosionobject={self.fireexplosionobject}, instrument={self.instrument}, place={self.place})"


@dataclass
class movement_transportperson_smuggleextract(Event):
    def __init__(self, mention: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, passenger: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.passenger = passenger if passenger is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"movement_transportperson_smuggleextract(mention=\"{self.mention}\", destination={self.destination}, origin={self.origin}, passenger={self.passenger}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class transaction_transaction_transfercontrol(Event):
    def __init__(self, mention: Optional[List] = None, beneficiary: Optional[List] = None, giver: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None, territoryorfacility: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.giver = giver if giver is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []
        self.territoryorfacility = territoryorfacility if territoryorfacility is not None else []

    def __repr__(self):
        return f"transaction_transaction_transfercontrol(mention=\"{self.mention}\", beneficiary={self.beneficiary}, giver={self.giver}, place={self.place}, recipient={self.recipient}, territoryorfacility={self.territoryorfacility})"


@dataclass
class transaction_transfermoney_giftgrantprovideaid(Event):
    def __init__(self, mention: Optional[List] = None, beneficiary: Optional[List] = None, giver: Optional[List] = None, money: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.giver = giver if giver is not None else []
        self.money = money if money is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"transaction_transfermoney_giftgrantprovideaid(mention=\"{self.mention}\", beneficiary={self.beneficiary}, giver={self.giver}, money={self.money}, place={self.place}, recipient={self.recipient})"


@dataclass
class movement_transportartifact_nonviolentthrowlaunch(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"movement_transportartifact_nonviolentthrowlaunch(mention=\"{self.mention}\", artifact={self.artifact}, destination={self.destination}, origin={self.origin}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class contact_commitmentpromiseexpressintent_correspondence(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_commitmentpromiseexpressintent_correspondence(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class conflict_attack_airstrikemissilestrike(Event):
    def __init__(self, mention: Optional[List] = None, attacker: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, target: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attacker = attacker if attacker is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.target = target if target is not None else []

    def __repr__(self):
        return f"conflict_attack_airstrikemissilestrike(mention=\"{self.mention}\", attacker={self.attacker}, instrument={self.instrument}, place={self.place}, target={self.target})"


@dataclass
class justice_judicialconsequences_Na(Event):
    def __init__(self, mention: Optional[List] = None, crime: Optional[List] = None, defendant: Optional[List] = None, judgecourt: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.crime = crime if crime is not None else []
        self.defendant = defendant if defendant is not None else []
        self.judgecourt = judgecourt if judgecourt is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"justice_judicialconsequences_Na(mention=\"{self.mention}\", crime={self.crime}, defendant={self.defendant}, judgecourt={self.judgecourt}, place={self.place})"


@dataclass
class government_formation_Na(Event):
    def __init__(self, mention: Optional[List] = None, founder: Optional[List] = None, gpe: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.founder = founder if founder is not None else []
        self.gpe = gpe if gpe is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"government_formation_Na(mention=\"{self.mention}\", founder={self.founder}, gpe={self.gpe}, place={self.place})"


@dataclass
class movement_transportperson_hide(Event):
    def __init__(self, mention: Optional[List] = None, hidingplace: Optional[List] = None, origin: Optional[List] = None, passenger: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.hidingplace = hidingplace if hidingplace is not None else []
        self.origin = origin if origin is not None else []
        self.passenger = passenger if passenger is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"movement_transportperson_hide(mention=\"{self.mention}\", hidingplace={self.hidingplace}, origin={self.origin}, passenger={self.passenger}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class justice_judicialconsequences_execute(Event):
    def __init__(self, mention: Optional[List] = None, crime: Optional[List] = None, defendant: Optional[List] = None, executioner: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.crime = crime if crime is not None else []
        self.defendant = defendant if defendant is not None else []
        self.executioner = executioner if executioner is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"justice_judicialconsequences_execute(mention=\"{self.mention}\", crime={self.crime}, defendant={self.defendant}, executioner={self.executioner}, place={self.place})"


@dataclass
class transaction_transaction_embargosanction(Event):
    def __init__(self, mention: Optional[List] = None, artifactmoney: Optional[List] = None, giver: Optional[List] = None, place: Optional[List] = None, preventer: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifactmoney = artifactmoney if artifactmoney is not None else []
        self.giver = giver if giver is not None else []
        self.place = place if place is not None else []
        self.preventer = preventer if preventer is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"transaction_transaction_embargosanction(mention=\"{self.mention}\", artifactmoney={self.artifactmoney}, giver={self.giver}, place={self.place}, preventer={self.preventer}, recipient={self.recipient})"


@dataclass
class conflict_attack_stabbing(Event):
    def __init__(self, mention: Optional[List] = None, attacker: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, target: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attacker = attacker if attacker is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.target = target if target is not None else []

    def __repr__(self):
        return f"conflict_attack_stabbing(mention=\"{self.mention}\", attacker={self.attacker}, instrument={self.instrument}, place={self.place}, target={self.target})"


@dataclass
class personnel_startposition_hiring(Event):
    def __init__(self, mention: Optional[List] = None, employee: Optional[List] = None, place: Optional[List] = None, placeofemployment: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.employee = employee if employee is not None else []
        self.place = place if place is not None else []
        self.placeofemployment = placeofemployment if placeofemployment is not None else []

    def __repr__(self):
        return f"personnel_startposition_hiring(mention=\"{self.mention}\", employee={self.employee}, place={self.place}, placeofemployment={self.placeofemployment})"


@dataclass
class conflict_yield_retreat(Event):
    def __init__(self, mention: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, retreater: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.retreater = retreater if retreater is not None else []

    def __repr__(self):
        return f"conflict_yield_retreat(mention=\"{self.mention}\", destination={self.destination}, origin={self.origin}, retreater={self.retreater})"


@dataclass
class transaction_transfermoney_embargosanction(Event):
    def __init__(self, mention: Optional[List] = None, giver: Optional[List] = None, money: Optional[List] = None, place: Optional[List] = None, preventer: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.giver = giver if giver is not None else []
        self.money = money if money is not None else []
        self.place = place if place is not None else []
        self.preventer = preventer if preventer is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"transaction_transfermoney_embargosanction(mention=\"{self.mention}\", giver={self.giver}, money={self.money}, place={self.place}, preventer={self.preventer}, recipient={self.recipient})"


@dataclass
class manufacture_artifact_build(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, instrument: Optional[List] = None, manufacturer: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.instrument = instrument if instrument is not None else []
        self.manufacturer = manufacturer if manufacturer is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"manufacture_artifact_build(mention=\"{self.mention}\", artifact={self.artifact}, instrument={self.instrument}, manufacturer={self.manufacturer}, place={self.place})"


@dataclass
class inspection_sensoryobserve_Na(Event):
    def __init__(self, mention: Optional[List] = None, observedentity: Optional[List] = None, observer: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.observedentity = observedentity if observedentity is not None else []
        self.observer = observer if observer is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"inspection_sensoryobserve_Na(mention=\"{self.mention}\", observedentity={self.observedentity}, observer={self.observer}, place={self.place})"


@dataclass
class justice_initiatejudicialprocess_trialhearing(Event):
    def __init__(self, mention: Optional[List] = None, crime: Optional[List] = None, defendant: Optional[List] = None, judgecourt: Optional[List] = None, place: Optional[List] = None, prosecutor: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.crime = crime if crime is not None else []
        self.defendant = defendant if defendant is not None else []
        self.judgecourt = judgecourt if judgecourt is not None else []
        self.place = place if place is not None else []
        self.prosecutor = prosecutor if prosecutor is not None else []

    def __repr__(self):
        return f"justice_initiatejudicialprocess_trialhearing(mention=\"{self.mention}\", crime={self.crime}, defendant={self.defendant}, judgecourt={self.judgecourt}, place={self.place}, prosecutor={self.prosecutor})"


@dataclass
class movement_transportperson_selfmotion(Event):
    def __init__(self, mention: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, transporter: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.transporter = transporter if transporter is not None else []

    def __repr__(self):
        return f"movement_transportperson_selfmotion(mention=\"{self.mention}\", destination={self.destination}, origin={self.origin}, transporter={self.transporter})"


@dataclass
class transaction_transferownership_purchase(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, beneficiary: Optional[List] = None, giver: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.giver = giver if giver is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"transaction_transferownership_purchase(mention=\"{self.mention}\", artifact={self.artifact}, beneficiary={self.beneficiary}, giver={self.giver}, place={self.place}, recipient={self.recipient})"


@dataclass
class contact_requestadvise_broadcast(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_requestadvise_broadcast(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class contact_commitmentpromiseexpressintent_meet(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_commitmentpromiseexpressintent_meet(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class movement_transportartifact_bringcarryunload(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"movement_transportartifact_bringcarryunload(mention=\"{self.mention}\", artifact={self.artifact}, destination={self.destination}, origin={self.origin}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class government_spy_spy(Event):
    def __init__(self, mention: Optional[List] = None, beneficiary: Optional[List] = None, observedentity: Optional[List] = None, place: Optional[List] = None, spy: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.observedentity = observedentity if observedentity is not None else []
        self.place = place if place is not None else []
        self.spy = spy if spy is not None else []

    def __repr__(self):
        return f"government_spy_spy(mention=\"{self.mention}\", beneficiary={self.beneficiary}, observedentity={self.observedentity}, place={self.place}, spy={self.spy})"


@dataclass
class government_vote_violationspreventvote(Event):
    def __init__(self, mention: Optional[List] = None, ballot: Optional[List] = None, candidate: Optional[List] = None, place: Optional[List] = None, preventer: Optional[List] = None, voter: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.ballot = ballot if ballot is not None else []
        self.candidate = candidate if candidate is not None else []
        self.place = place if place is not None else []
        self.preventer = preventer if preventer is not None else []
        self.voter = voter if voter is not None else []

    def __repr__(self):
        return f"government_vote_violationspreventvote(mention=\"{self.mention}\", ballot={self.ballot}, candidate={self.candidate}, place={self.place}, preventer={self.preventer}, voter={self.voter})"


@dataclass
class contact_discussion_Na(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"contact_discussion_Na(mention=\"{self.mention}\", participant={self.participant}, place={self.place})"


@dataclass
class transaction_transferownership_giftgrantprovideaid(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, beneficiary: Optional[List] = None, giver: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.giver = giver if giver is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"transaction_transferownership_giftgrantprovideaid(mention=\"{self.mention}\", artifact={self.artifact}, beneficiary={self.beneficiary}, giver={self.giver}, place={self.place}, recipient={self.recipient})"


@dataclass
class contact_commandorder_correspondence(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_commandorder_correspondence(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class conflict_attack_firearmattack(Event):
    def __init__(self, mention: Optional[List] = None, attacker: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, target: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attacker = attacker if attacker is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.target = target if target is not None else []

    def __repr__(self):
        return f"conflict_attack_firearmattack(mention=\"{self.mention}\", attacker={self.attacker}, instrument={self.instrument}, place={self.place}, target={self.target})"


@dataclass
class contact_prevarication_correspondence(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_prevarication_correspondence(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class conflict_attack_strangling(Event):
    def __init__(self, mention: Optional[List] = None, attacker: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, target: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attacker = attacker if attacker is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.target = target if target is not None else []

    def __repr__(self):
        return f"conflict_attack_strangling(mention=\"{self.mention}\", attacker={self.attacker}, instrument={self.instrument}, place={self.place}, target={self.target})"


@dataclass
class contact_requestadvise_Na(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_requestadvise_Na(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class artifactexistence_damagedestroy_destroy(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, destroyer: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destroyer = destroyer if destroyer is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"artifactexistence_damagedestroy_destroy(mention=\"{self.mention}\", artifact={self.artifact}, destroyer={self.destroyer}, instrument={self.instrument}, place={self.place})"


@dataclass
class movement_transportartifact_sendsupplyexport(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"movement_transportartifact_sendsupplyexport(mention=\"{self.mention}\", artifact={self.artifact}, destination={self.destination}, origin={self.origin}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class transaction_transaction_giftgrantprovideaid(Event):
    def __init__(self, mention: Optional[List] = None, beneficiary: Optional[List] = None, giver: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.giver = giver if giver is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"transaction_transaction_giftgrantprovideaid(mention=\"{self.mention}\", beneficiary={self.beneficiary}, giver={self.giver}, place={self.place}, recipient={self.recipient})"


@dataclass
class conflict_attack_Na(Event):
    def __init__(self, mention: Optional[List] = None, attacker: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, target: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attacker = attacker if attacker is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.target = target if target is not None else []

    def __repr__(self):
        return f"conflict_attack_Na(mention=\"{self.mention}\", attacker={self.attacker}, instrument={self.instrument}, place={self.place}, target={self.target})"


@dataclass
class personnel_endposition_quitretire(Event):
    def __init__(self, mention: Optional[List] = None, employee: Optional[List] = None, place: Optional[List] = None, placeofemployment: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.employee = employee if employee is not None else []
        self.place = place if place is not None else []
        self.placeofemployment = placeofemployment if placeofemployment is not None else []

    def __repr__(self):
        return f"personnel_endposition_quitretire(mention=\"{self.mention}\", employee={self.employee}, place={self.place}, placeofemployment={self.placeofemployment})"


@dataclass
class justice_initiatejudicialprocess_chargeindict(Event):
    def __init__(self, mention: Optional[List] = None, crime: Optional[List] = None, defendant: Optional[List] = None, judgecourt: Optional[List] = None, place: Optional[List] = None, prosecutor: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.crime = crime if crime is not None else []
        self.defendant = defendant if defendant is not None else []
        self.judgecourt = judgecourt if judgecourt is not None else []
        self.place = place if place is not None else []
        self.prosecutor = prosecutor if prosecutor is not None else []

    def __repr__(self):
        return f"justice_initiatejudicialprocess_chargeindict(mention=\"{self.mention}\", crime={self.crime}, defendant={self.defendant}, judgecourt={self.judgecourt}, place={self.place}, prosecutor={self.prosecutor})"


@dataclass
class life_injure_Na(Event):
    def __init__(self, mention: Optional[List] = None, injurer: Optional[List] = None, place: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.injurer = injurer if injurer is not None else []
        self.place = place if place is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"life_injure_Na(mention=\"{self.mention}\", injurer={self.injurer}, place={self.place}, victim={self.victim})"


@dataclass
class contact_requestadvise_meet(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_requestadvise_meet(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class government_formation_startgpe(Event):
    def __init__(self, mention: Optional[List] = None, founder: Optional[List] = None, gpe: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.founder = founder if founder is not None else []
        self.gpe = gpe if gpe is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"government_formation_startgpe(mention=\"{self.mention}\", founder={self.founder}, gpe={self.gpe}, place={self.place})"


@dataclass
class transaction_transfermoney_payforservice(Event):
    def __init__(self, mention: Optional[List] = None, beneficiary: Optional[List] = None, giver: Optional[List] = None, money: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.giver = giver if giver is not None else []
        self.money = money if money is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"transaction_transfermoney_payforservice(mention=\"{self.mention}\", beneficiary={self.beneficiary}, giver={self.giver}, money={self.money}, place={self.place}, recipient={self.recipient})"


@dataclass
class disaster_accidentcrash_accidentcrash(Event):
    def __init__(self, mention: Optional[List] = None, crashobject: Optional[List] = None, driverpassenger: Optional[List] = None, place: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.crashobject = crashobject if crashobject is not None else []
        self.driverpassenger = driverpassenger if driverpassenger is not None else []
        self.place = place if place is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"disaster_accidentcrash_accidentcrash(mention=\"{self.mention}\", crashobject={self.crashobject}, driverpassenger={self.driverpassenger}, place={self.place}, vehicle={self.vehicle})"


@dataclass
class contact_threatencoerce_meet(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_threatencoerce_meet(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class movement_transportperson_grantentryasylum(Event):
    def __init__(self, mention: Optional[List] = None, destination: Optional[List] = None, granter: Optional[List] = None, origin: Optional[List] = None, passenger: Optional[List] = None, transporter: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.destination = destination if destination is not None else []
        self.granter = granter if granter is not None else []
        self.origin = origin if origin is not None else []
        self.passenger = passenger if passenger is not None else []
        self.transporter = transporter if transporter is not None else []

    def __repr__(self):
        return f"movement_transportperson_grantentryasylum(mention=\"{self.mention}\", destination={self.destination}, granter={self.granter}, origin={self.origin}, passenger={self.passenger}, transporter={self.transporter})"


@dataclass
class contact_publicstatementinperson_broadcast(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_publicstatementinperson_broadcast(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class contact_discussion_correspondence(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"contact_discussion_correspondence(mention=\"{self.mention}\", participant={self.participant}, place={self.place})"


@dataclass
class movement_transportperson_disperseseparate(Event):
    def __init__(self, mention: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, passenger: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.passenger = passenger if passenger is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"movement_transportperson_disperseseparate(mention=\"{self.mention}\", destination={self.destination}, origin={self.origin}, passenger={self.passenger}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class movement_transportartifact_Na(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"movement_transportartifact_Na(mention=\"{self.mention}\", artifact={self.artifact}, destination={self.destination}, origin={self.origin}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class movement_transportperson_Na(Event):
    def __init__(self, mention: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, passenger: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.passenger = passenger if passenger is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"movement_transportperson_Na(mention=\"{self.mention}\", destination={self.destination}, origin={self.origin}, passenger={self.passenger}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class conflict_demonstrate_Na(Event):
    def __init__(self, mention: Optional[List] = None, demonstrator: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.demonstrator = demonstrator if demonstrator is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"conflict_demonstrate_Na(mention=\"{self.mention}\", demonstrator={self.demonstrator}, place={self.place})"


@dataclass
class life_injure_illnessdegradationphysical(Event):
    def __init__(self, mention: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"life_injure_illnessdegradationphysical(mention=\"{self.mention}\", victim={self.victim})"


@dataclass
class transaction_transfermoney_purchase(Event):
    def __init__(self, mention: Optional[List] = None, beneficiary: Optional[List] = None, giver: Optional[List] = None, money: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.giver = giver if giver is not None else []
        self.money = money if money is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"transaction_transfermoney_purchase(mention=\"{self.mention}\", beneficiary={self.beneficiary}, giver={self.giver}, money={self.money}, place={self.place}, recipient={self.recipient})"


@dataclass
class inspection_sensoryobserve_physicalinvestigateinspect(Event):
    def __init__(self, mention: Optional[List] = None, inspectedentity: Optional[List] = None, inspector: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.inspectedentity = inspectedentity if inspectedentity is not None else []
        self.inspector = inspector if inspector is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"inspection_sensoryobserve_physicalinvestigateinspect(mention=\"{self.mention}\", inspectedentity={self.inspectedentity}, inspector={self.inspector}, place={self.place})"


@dataclass
class manufacture_artifact_createmanufacture(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, instrument: Optional[List] = None, manufacturer: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.instrument = instrument if instrument is not None else []
        self.manufacturer = manufacturer if manufacturer is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"manufacture_artifact_createmanufacture(mention=\"{self.mention}\", artifact={self.artifact}, instrument={self.instrument}, manufacturer={self.manufacturer}, place={self.place})"


@dataclass
class contact_publicstatementinperson_Na(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_publicstatementinperson_Na(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class justice_judicialconsequences_convict(Event):
    def __init__(self, mention: Optional[List] = None, crime: Optional[List] = None, defendant: Optional[List] = None, judgecourt: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.crime = crime if crime is not None else []
        self.defendant = defendant if defendant is not None else []
        self.judgecourt = judgecourt if judgecourt is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"justice_judicialconsequences_convict(mention=\"{self.mention}\", crime={self.crime}, defendant={self.defendant}, judgecourt={self.judgecourt}, place={self.place})"


@dataclass
class contact_funeralvigil_meet(Event):
    def __init__(self, mention: Optional[List] = None, deceased: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.deceased = deceased if deceased is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"contact_funeralvigil_meet(mention=\"{self.mention}\", deceased={self.deceased}, participant={self.participant}, place={self.place})"


@dataclass
class government_formation_mergegpe(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"government_formation_mergegpe(mention=\"{self.mention}\", participant={self.participant}, place={self.place})"


@dataclass
class transaction_transfermoney_borrowlend(Event):
    def __init__(self, mention: Optional[List] = None, beneficiary: Optional[List] = None, giver: Optional[List] = None, money: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.giver = giver if giver is not None else []
        self.money = money if money is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"transaction_transfermoney_borrowlend(mention=\"{self.mention}\", beneficiary={self.beneficiary}, giver={self.giver}, money={self.money}, place={self.place}, recipient={self.recipient})"


@dataclass
class transaction_transaction_Na(Event):
    def __init__(self, mention: Optional[List] = None, beneficiary: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"transaction_transaction_Na(mention=\"{self.mention}\", beneficiary={self.beneficiary}, participant={self.participant}, place={self.place})"


@dataclass
class transaction_transferownership_embargosanction(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, giver: Optional[List] = None, place: Optional[List] = None, preventer: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.giver = giver if giver is not None else []
        self.place = place if place is not None else []
        self.preventer = preventer if preventer is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"transaction_transferownership_embargosanction(mention=\"{self.mention}\", artifact={self.artifact}, giver={self.giver}, place={self.place}, preventer={self.preventer}, recipient={self.recipient})"


@dataclass
class contact_threatencoerce_broadcast(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_threatencoerce_broadcast(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class conflict_attack_bombing(Event):
    def __init__(self, mention: Optional[List] = None, attacker: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, target: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attacker = attacker if attacker is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.target = target if target is not None else []

    def __repr__(self):
        return f"conflict_attack_bombing(mention=\"{self.mention}\", attacker={self.attacker}, instrument={self.instrument}, place={self.place}, target={self.target})"


@dataclass
class artifactexistence_damagedestroy_damage(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, damager: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.damager = damager if damager is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"artifactexistence_damagedestroy_damage(mention=\"{self.mention}\", artifact={self.artifact}, damager={self.damager}, instrument={self.instrument}, place={self.place})"


@dataclass
class contact_funeralvigil_Na(Event):
    def __init__(self, mention: Optional[List] = None, deceased: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.deceased = deceased if deceased is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"contact_funeralvigil_Na(mention=\"{self.mention}\", deceased={self.deceased}, participant={self.participant}, place={self.place})"


@dataclass
class contact_prevarication_Na(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_prevarication_Na(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class government_vote_Na(Event):
    def __init__(self, mention: Optional[List] = None, ballot: Optional[List] = None, candidate: Optional[List] = None, place: Optional[List] = None, result: Optional[List] = None, voter: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.ballot = ballot if ballot is not None else []
        self.candidate = candidate if candidate is not None else []
        self.place = place if place is not None else []
        self.result = result if result is not None else []
        self.voter = voter if voter is not None else []

    def __repr__(self):
        return f"government_vote_Na(mention=\"{self.mention}\", ballot={self.ballot}, candidate={self.candidate}, place={self.place}, result={self.result}, voter={self.voter})"


@dataclass
class movement_transportartifact_receiveimport(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"movement_transportartifact_receiveimport(mention=\"{self.mention}\", artifact={self.artifact}, destination={self.destination}, origin={self.origin}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class conflict_attack_invade(Event):
    def __init__(self, mention: Optional[List] = None, attacker: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, target: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attacker = attacker if attacker is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.target = target if target is not None else []

    def __repr__(self):
        return f"conflict_attack_invade(mention=\"{self.mention}\", attacker={self.attacker}, instrument={self.instrument}, place={self.place}, target={self.target})"


@dataclass
class contact_collaborate_correspondence(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"contact_collaborate_correspondence(mention=\"{self.mention}\", participant={self.participant}, place={self.place})"


@dataclass
class conflict_attack_biologicalchemicalpoisonattack(Event):
    def __init__(self, mention: Optional[List] = None, attacker: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, target: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attacker = attacker if attacker is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.target = target if target is not None else []

    def __repr__(self):
        return f"conflict_attack_biologicalchemicalpoisonattack(mention=\"{self.mention}\", attacker={self.attacker}, instrument={self.instrument}, place={self.place}, target={self.target})"


@dataclass
class life_die_nonviolentdeath(Event):
    def __init__(self, mention: Optional[List] = None, place: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"life_die_nonviolentdeath(mention=\"{self.mention}\", place={self.place}, victim={self.victim})"


@dataclass
class contact_collaborate_meet(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"contact_collaborate_meet(mention=\"{self.mention}\", participant={self.participant}, place={self.place})"


@dataclass
class personnel_startposition_Na(Event):
    def __init__(self, mention: Optional[List] = None, employee: Optional[List] = None, place: Optional[List] = None, placeofemployment: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.employee = employee if employee is not None else []
        self.place = place if place is not None else []
        self.placeofemployment = placeofemployment if placeofemployment is not None else []

    def __repr__(self):
        return f"personnel_startposition_Na(mention=\"{self.mention}\", employee={self.employee}, place={self.place}, placeofemployment={self.placeofemployment})"


@dataclass
class contact_negotiate_correspondence(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"contact_negotiate_correspondence(mention=\"{self.mention}\", participant={self.participant}, place={self.place})"


@dataclass
class conflict_yield_surrender(Event):
    def __init__(self, mention: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None, surrenderer: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []
        self.surrenderer = surrenderer if surrenderer is not None else []

    def __repr__(self):
        return f"conflict_yield_surrender(mention=\"{self.mention}\", place={self.place}, recipient={self.recipient}, surrenderer={self.surrenderer})"


@dataclass
class government_agreements_rejectnullifyagreementcontractceasefire(Event):
    def __init__(self, mention: Optional[List] = None, otherparticipant: Optional[List] = None, place: Optional[List] = None, rejecternullifier: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.otherparticipant = otherparticipant if otherparticipant is not None else []
        self.place = place if place is not None else []
        self.rejecternullifier = rejecternullifier if rejecternullifier is not None else []

    def __repr__(self):
        return f"government_agreements_rejectnullifyagreementcontractceasefire(mention=\"{self.mention}\", otherparticipant={self.otherparticipant}, place={self.place}, rejecternullifier={self.rejecternullifier})"


@dataclass
class transaction_transferownership_borrowlend(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, beneficiary: Optional[List] = None, giver: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.giver = giver if giver is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"transaction_transferownership_borrowlend(mention=\"{self.mention}\", artifact={self.artifact}, beneficiary={self.beneficiary}, giver={self.giver}, place={self.place}, recipient={self.recipient})"


@dataclass
class movement_transportartifact_preventexit(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, preventer: Optional[List] = None, transporter: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.preventer = preventer if preventer is not None else []
        self.transporter = transporter if transporter is not None else []

    def __repr__(self):
        return f"movement_transportartifact_preventexit(mention=\"{self.mention}\", artifact={self.artifact}, destination={self.destination}, origin={self.origin}, preventer={self.preventer}, transporter={self.transporter})"


@dataclass
class conflict_demonstrate_marchprotestpoliticalgathering(Event):
    def __init__(self, mention: Optional[List] = None, demonstrator: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.demonstrator = demonstrator if demonstrator is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"conflict_demonstrate_marchprotestpoliticalgathering(mention=\"{self.mention}\", demonstrator={self.demonstrator}, place={self.place})"


@dataclass
class movement_transportartifact_grantentry(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, transporter: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.transporter = transporter if transporter is not None else []

    def __repr__(self):
        return f"movement_transportartifact_grantentry(mention=\"{self.mention}\", artifact={self.artifact}, destination={self.destination}, origin={self.origin}, transporter={self.transporter})"


@dataclass
class government_vote_castvote(Event):
    def __init__(self, mention: Optional[List] = None, ballot: Optional[List] = None, candidate: Optional[List] = None, place: Optional[List] = None, result: Optional[List] = None, voter: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.ballot = ballot if ballot is not None else []
        self.candidate = candidate if candidate is not None else []
        self.place = place if place is not None else []
        self.result = result if result is not None else []
        self.voter = voter if voter is not None else []

    def __repr__(self):
        return f"government_vote_castvote(mention=\"{self.mention}\", ballot={self.ballot}, candidate={self.candidate}, place={self.place}, result={self.result}, voter={self.voter})"


@dataclass
class contact_commandorder_meet(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_commandorder_meet(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class contact_commandorder_Na(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_commandorder_Na(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class movement_transportperson_evacuationrescue(Event):
    def __init__(self, mention: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, passenger: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.passenger = passenger if passenger is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"movement_transportperson_evacuationrescue(mention=\"{self.mention}\", destination={self.destination}, origin={self.origin}, passenger={self.passenger}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class movement_transportartifact_smuggleextract(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"movement_transportartifact_smuggleextract(mention=\"{self.mention}\", artifact={self.artifact}, destination={self.destination}, origin={self.origin}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class contact_prevarication_meet(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_prevarication_meet(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class artifactexistence_damagedestroy_Na(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, damagerdestroyer: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.damagerdestroyer = damagerdestroyer if damagerdestroyer is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"artifactexistence_damagedestroy_Na(mention=\"{self.mention}\", artifact={self.artifact}, damagerdestroyer={self.damagerdestroyer}, instrument={self.instrument}, place={self.place})"


@dataclass
class manufacture_artifact_Na(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, instrument: Optional[List] = None, manufacturer: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.instrument = instrument if instrument is not None else []
        self.manufacturer = manufacturer if manufacturer is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"manufacture_artifact_Na(mention=\"{self.mention}\", artifact={self.artifact}, instrument={self.instrument}, manufacturer={self.manufacturer}, place={self.place})"


@dataclass
class contact_threatencoerce_correspondence(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_threatencoerce_correspondence(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class inspection_sensoryobserve_inspectpeopleorganization(Event):
    def __init__(self, mention: Optional[List] = None, inspectedentity: Optional[List] = None, inspector: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.inspectedentity = inspectedentity if inspectedentity is not None else []
        self.inspector = inspector if inspector is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"inspection_sensoryobserve_inspectpeopleorganization(mention=\"{self.mention}\", inspectedentity={self.inspectedentity}, inspector={self.inspector}, place={self.place})"


@dataclass
class movement_transportperson_bringcarryunload(Event):
    def __init__(self, mention: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, passenger: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.passenger = passenger if passenger is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"movement_transportperson_bringcarryunload(mention=\"{self.mention}\", destination={self.destination}, origin={self.origin}, passenger={self.passenger}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class movement_transportperson_fall(Event):
    def __init__(self, mention: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, passenger: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.passenger = passenger if passenger is not None else []

    def __repr__(self):
        return f"movement_transportperson_fall(mention=\"{self.mention}\", destination={self.destination}, origin={self.origin}, passenger={self.passenger})"


@dataclass
class manufacture_artifact_createintellectualproperty(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, instrument: Optional[List] = None, manufacturer: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.instrument = instrument if instrument is not None else []
        self.manufacturer = manufacturer if manufacturer is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"manufacture_artifact_createintellectualproperty(mention=\"{self.mention}\", artifact={self.artifact}, instrument={self.instrument}, manufacturer={self.manufacturer}, place={self.place})"


@dataclass
class contact_mediastatement_Na(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"contact_mediastatement_Na(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class movement_transportartifact_fall(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []

    def __repr__(self):
        return f"movement_transportartifact_fall(mention=\"{self.mention}\", artifact={self.artifact}, destination={self.destination}, origin={self.origin})"


@dataclass
class movement_transportartifact_prevententry(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, preventer: Optional[List] = None, transporter: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.preventer = preventer if preventer is not None else []
        self.transporter = transporter if transporter is not None else []

    def __repr__(self):
        return f"movement_transportartifact_prevententry(mention=\"{self.mention}\", artifact={self.artifact}, destination={self.destination}, origin={self.origin}, preventer={self.preventer}, transporter={self.transporter})"


@dataclass
class conflict_attack_setfire(Event):
    def __init__(self, mention: Optional[List] = None, attacker: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, target: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attacker = attacker if attacker is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.target = target if target is not None else []

    def __repr__(self):
        return f"conflict_attack_setfire(mention=\"{self.mention}\", attacker={self.attacker}, instrument={self.instrument}, place={self.place}, target={self.target})"


@dataclass
class inspection_sensoryobserve_monitorelection(Event):
    def __init__(self, mention: Optional[List] = None, monitor: Optional[List] = None, monitoredentity: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.monitor = monitor if monitor is not None else []
        self.monitoredentity = monitoredentity if monitoredentity is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"inspection_sensoryobserve_monitorelection(mention=\"{self.mention}\", monitor={self.monitor}, monitoredentity={self.monitoredentity}, place={self.place})"


@dataclass
class conflict_attack_hanging(Event):
    def __init__(self, mention: Optional[List] = None, attacker: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, target: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attacker = attacker if attacker is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.target = target if target is not None else []

    def __repr__(self):
        return f"conflict_attack_hanging(mention=\"{self.mention}\", attacker={self.attacker}, instrument={self.instrument}, place={self.place}, target={self.target})"


# @dataclass
# class Spread(Event):
#     def __init__(self, mention: Optional[List] = None):
#         self.mention = mention if mention is not None else []

#     def __repr__(self):
#         return f"Spread(mention=\"{self.mention}\")"


# @dataclass
# class Infect(Event):
#     def __init__(self, mention: Optional[List] = None):
#         self.mention = mention if mention is not None else []

#     def __repr__(self):
#         return f"Infect(mention=\"{self.mention}\")"


# @dataclass
# class Symptom(Event):
#     def __init__(self, mention: Optional[List] = None):
#         self.mention = mention if mention is not None else []

#     def __repr__(self):
#         return f"Symptom(mention=\"{self.mention}\")"


# @dataclass
# class Prevent(Event):
#     def __init__(self, mention: Optional[List] = None):
#         self.mention = mention if mention is not None else []

#     def __repr__(self):
#         return f"Prevent(mention=\"{self.mention}\")"


@dataclass
class Movement_Transportation_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, passengerartifact: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.passengerartifact = passengerartifact if passengerartifact is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"Movement_Transportation_Unspecified(mention=\"{self.mention}\", destination={self.destination}, origin={self.origin}, passengerartifact={self.passengerartifact}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class Medical_Intervention_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, patient: Optional[List] = None, place: Optional[List] = None, treater: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.patient = patient if patient is not None else []
        self.place = place if place is not None else []
        self.treater = treater if treater is not None else []

    def __repr__(self):
        return f"Medical_Intervention_Unspecified(mention=\"{self.mention}\", patient={self.patient}, place={self.place}, treater={self.treater})"


@dataclass
class Life_Die_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, killer: Optional[List] = None, place: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.killer = killer if killer is not None else []
        self.place = place if place is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"Life_Die_Unspecified(mention=\"{self.mention}\", killer={self.killer}, place={self.place}, victim={self.victim})"


@dataclass
class Cognitive_Inspection_SensoryObserve(Event):
    def __init__(self, mention: Optional[List] = None, instrument: Optional[List] = None, observedentity: Optional[List] = None, observer: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.instrument = instrument if instrument is not None else []
        self.observedentity = observedentity if observedentity is not None else []
        self.observer = observer if observer is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Cognitive_Inspection_SensoryObserve(mention=\"{self.mention}\", instrument={self.instrument}, observedentity={self.observedentity}, observer={self.observer}, place={self.place})"


@dataclass
class Contact_Contact_Broadcast(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None, topic: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []
        self.topic = topic if topic is not None else []

    def __repr__(self):
        return f"Contact_Contact_Broadcast(mention=\"{self.mention}\", communicator={self.communicator}, instrument={self.instrument}, place={self.place}, recipient={self.recipient}, topic={self.topic})"


@dataclass
class Conflict_Attack_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, attacker: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, target: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attacker = attacker if attacker is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.target = target if target is not None else []

    def __repr__(self):
        return f"Conflict_Attack_Unspecified(mention=\"{self.mention}\", attacker={self.attacker}, instrument={self.instrument}, place={self.place}, target={self.target})"


@dataclass
class Justice_ChargeIndict_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, defendant: Optional[List] = None, judgecourt: Optional[List] = None, place: Optional[List] = None, prosecutor: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.defendant = defendant if defendant is not None else []
        self.judgecourt = judgecourt if judgecourt is not None else []
        self.place = place if place is not None else []
        self.prosecutor = prosecutor if prosecutor is not None else []

    def __repr__(self):
        return f"Justice_ChargeIndict_Unspecified(mention=\"{self.mention}\", defendant={self.defendant}, judgecourt={self.judgecourt}, place={self.place}, prosecutor={self.prosecutor})"


@dataclass
class Contact_Contact_Meet(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None, topic: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []
        self.topic = topic if topic is not None else []

    def __repr__(self):
        return f"Contact_Contact_Meet(mention=\"{self.mention}\", participant={self.participant}, place={self.place}, topic={self.topic})"


@dataclass
class Contact_Contact_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None, topic: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []
        self.topic = topic if topic is not None else []

    def __repr__(self):
        return f"Contact_Contact_Unspecified(mention=\"{self.mention}\", participant={self.participant}, place={self.place}, topic={self.topic})"


@dataclass
class Life_Infect_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"Life_Infect_Unspecified(mention=\"{self.mention}\", victim={self.victim})"


@dataclass
class Transaction_ExchangeBuySell_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, acquiredentity: Optional[List] = None, giver: Optional[List] = None, paymentbarter: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.acquiredentity = acquiredentity if acquiredentity is not None else []
        self.giver = giver if giver is not None else []
        self.paymentbarter = paymentbarter if paymentbarter is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"Transaction_ExchangeBuySell_Unspecified(mention=\"{self.mention}\", acquiredentity={self.acquiredentity}, giver={self.giver}, paymentbarter={self.paymentbarter}, recipient={self.recipient})"


@dataclass
class GenericCrime_GenericCrime_GenericCrime(Event):
    def __init__(self, mention: Optional[List] = None, perpetrator: Optional[List] = None, place: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.perpetrator = perpetrator if perpetrator is not None else []
        self.place = place if place is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"GenericCrime_GenericCrime_GenericCrime(mention=\"{self.mention}\", perpetrator={self.perpetrator}, place={self.place}, victim={self.victim})"


@dataclass
class Justice_Sentence_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, defendant: Optional[List] = None, judgecourt: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.defendant = defendant if defendant is not None else []
        self.judgecourt = judgecourt if judgecourt is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Justice_Sentence_Unspecified(mention=\"{self.mention}\", defendant={self.defendant}, judgecourt={self.judgecourt}, place={self.place})"


@dataclass
class Justice_ArrestJailDetain_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, detainee: Optional[List] = None, jailer: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.detainee = detainee if detainee is not None else []
        self.jailer = jailer if jailer is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Justice_ArrestJailDetain_Unspecified(mention=\"{self.mention}\", detainee={self.detainee}, jailer={self.jailer}, place={self.place})"


@dataclass
class Life_Injure_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, bodypart: Optional[List] = None, injurer: Optional[List] = None, instrument: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.bodypart = bodypart if bodypart is not None else []
        self.injurer = injurer if injurer is not None else []
        self.instrument = instrument if instrument is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"Life_Injure_Unspecified(mention=\"{self.mention}\", bodypart={self.bodypart}, injurer={self.injurer}, instrument={self.instrument}, victim={self.victim})"


@dataclass
class Conflict_Attack_DetonateExplode(Event):
    def __init__(self, mention: Optional[List] = None, attacker: Optional[List] = None, explosivedevice: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None, target: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.attacker = attacker if attacker is not None else []
        self.explosivedevice = explosivedevice if explosivedevice is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
        self.target = target if target is not None else []

    def __repr__(self):
        return f"Conflict_Attack_DetonateExplode(mention=\"{self.mention}\", attacker={self.attacker}, explosivedevice={self.explosivedevice}, instrument={self.instrument}, place={self.place}, target={self.target})"


@dataclass
class ArtifactExistence_DamageDestroyDisableDismantle_DisableDefuse(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, disabler: Optional[List] = None, instrument: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.disabler = disabler if disabler is not None else []
        self.instrument = instrument if instrument is not None else []

    def __repr__(self):
        return f"ArtifactExistence_DamageDestroyDisableDismantle_DisableDefuse(mention=\"{self.mention}\", artifact={self.artifact}, disabler={self.disabler}, instrument={self.instrument})"


@dataclass
class Justice_InvestigateCrime_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, defendant: Optional[List] = None, investigator: Optional[List] = None, observedentity: Optional[List] = None, observer: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.defendant = defendant if defendant is not None else []
        self.investigator = investigator if investigator is not None else []
        self.observedentity = observedentity if observedentity is not None else []
        self.observer = observer if observer is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Justice_InvestigateCrime_Unspecified(mention=\"{self.mention}\", defendant={self.defendant}, investigator={self.investigator}, observedentity={self.observedentity}, observer={self.observer}, place={self.place})"


@dataclass
class ArtifactExistence_DamageDestroyDisableDismantle_Destroy(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, destroyer: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destroyer = destroyer if destroyer is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"ArtifactExistence_DamageDestroyDisableDismantle_Destroy(mention=\"{self.mention}\", artifact={self.artifact}, destroyer={self.destroyer}, instrument={self.instrument}, place={self.place})"


@dataclass
class Contact_RequestCommand_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, place: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.place = place if place is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"Contact_RequestCommand_Unspecified(mention=\"{self.mention}\", communicator={self.communicator}, place={self.place}, recipient={self.recipient})"


@dataclass
class Cognitive_IdentifyCategorize_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, identifiedobject: Optional[List] = None, identifiedrole: Optional[List] = None, identifier: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.identifiedobject = identifiedobject if identifiedobject is not None else []
        self.identifiedrole = identifiedrole if identifiedrole is not None else []
        self.identifier = identifier if identifier is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Cognitive_IdentifyCategorize_Unspecified(mention=\"{self.mention}\", identifiedobject={self.identifiedobject}, identifiedrole={self.identifiedrole}, identifier={self.identifier}, place={self.place})"


@dataclass
class Contact_Contact_Correspondence(Event):
    def __init__(self, mention: Optional[List] = None, participant: Optional[List] = None, place: Optional[List] = None, topic: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.participant = participant if participant is not None else []
        self.place = place if place is not None else []
        self.topic = topic if topic is not None else []

    def __repr__(self):
        return f"Contact_Contact_Correspondence(mention=\"{self.mention}\", participant={self.participant}, place={self.place}, topic={self.topic})"


@dataclass
class Movement_Transportation_Evacuation(Event):
    def __init__(self, mention: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, passengerartifact: Optional[List] = None, transporter: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.passengerartifact = passengerartifact if passengerartifact is not None else []
        self.transporter = transporter if transporter is not None else []

    def __repr__(self):
        return f"Movement_Transportation_Evacuation(mention=\"{self.mention}\", destination={self.destination}, origin={self.origin}, passengerartifact={self.passengerartifact}, transporter={self.transporter})"


@dataclass
class Justice_TrialHearing_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, defendant: Optional[List] = None, judgecourt: Optional[List] = None, place: Optional[List] = None, prosecutor: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.defendant = defendant if defendant is not None else []
        self.judgecourt = judgecourt if judgecourt is not None else []
        self.place = place if place is not None else []
        self.prosecutor = prosecutor if prosecutor is not None else []

    def __repr__(self):
        return f"Justice_TrialHearing_Unspecified(mention=\"{self.mention}\", defendant={self.defendant}, judgecourt={self.judgecourt}, place={self.place}, prosecutor={self.prosecutor})"


@dataclass
class Contact_RequestCommand_Meet(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"Contact_RequestCommand_Meet(mention=\"{self.mention}\", communicator={self.communicator}, recipient={self.recipient})"


@dataclass
class ArtifactExistence_ManufactureAssemble_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, components: Optional[List] = None, manufacturerassembler: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.components = components if components is not None else []
        self.manufacturerassembler = manufacturerassembler if manufacturerassembler is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"ArtifactExistence_ManufactureAssemble_Unspecified(mention=\"{self.mention}\", artifact={self.artifact}, components={self.components}, manufacturerassembler={self.manufacturerassembler}, place={self.place})"


@dataclass
class Justice_Convict_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, defendant: Optional[List] = None, judgecourt: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.defendant = defendant if defendant is not None else []
        self.judgecourt = judgecourt if judgecourt is not None else []

    def __repr__(self):
        return f"Justice_Convict_Unspecified(mention=\"{self.mention}\", defendant={self.defendant}, judgecourt={self.judgecourt})"


@dataclass
class Conflict_Demonstrate_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, demonstrator: Optional[List] = None, target: Optional[List] = None, topic: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.demonstrator = demonstrator if demonstrator is not None else []
        self.target = target if target is not None else []
        self.topic = topic if topic is not None else []

    def __repr__(self):
        return f"Conflict_Demonstrate_Unspecified(mention=\"{self.mention}\", demonstrator={self.demonstrator}, target={self.target}, topic={self.topic})"


@dataclass
class Justice_ReleaseParole_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, defendant: Optional[List] = None, judgecourt: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.defendant = defendant if defendant is not None else []
        self.judgecourt = judgecourt if judgecourt is not None else []

    def __repr__(self):
        return f"Justice_ReleaseParole_Unspecified(mention=\"{self.mention}\", defendant={self.defendant}, judgecourt={self.judgecourt})"


@dataclass
class ArtifactExistence_DamageDestroyDisableDismantle_Damage(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, damager: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.damager = damager if damager is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"ArtifactExistence_DamageDestroyDisableDismantle_Damage(mention=\"{self.mention}\", artifact={self.artifact}, damager={self.damager}, instrument={self.instrument}, place={self.place})"


@dataclass
class Personnel_EndPosition_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, employee: Optional[List] = None, placeofemployment: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.employee = employee if employee is not None else []
        self.placeofemployment = placeofemployment if placeofemployment is not None else []

    def __repr__(self):
        return f"Personnel_EndPosition_Unspecified(mention=\"{self.mention}\", employee={self.employee}, placeofemployment={self.placeofemployment})"


@dataclass
class Personnel_StartPosition_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, employee: Optional[List] = None, place: Optional[List] = None, placeofemployment: Optional[List] = None, position: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.employee = employee if employee is not None else []
        self.place = place if place is not None else []
        self.placeofemployment = placeofemployment if placeofemployment is not None else []
        self.position = position if position is not None else []

    def __repr__(self):
        return f"Personnel_StartPosition_Unspecified(mention=\"{self.mention}\", employee={self.employee}, place={self.place}, placeofemployment={self.placeofemployment}, position={self.position})"


@dataclass
class Cognitive_TeachingTrainingLearning_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, learner: Optional[List] = None, teachertrainer: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.learner = learner if learner is not None else []
        self.teachertrainer = teachertrainer if teachertrainer is not None else []

    def __repr__(self):
        return f"Cognitive_TeachingTrainingLearning_Unspecified(mention=\"{self.mention}\", learner={self.learner}, teachertrainer={self.teachertrainer})"


@dataclass
class Contact_ThreatenCoerce_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"Contact_ThreatenCoerce_Unspecified(mention=\"{self.mention}\", communicator={self.communicator}, recipient={self.recipient})"


@dataclass
class Contact_ThreatenCoerce_Correspondence(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"Contact_ThreatenCoerce_Correspondence(mention=\"{self.mention}\", communicator={self.communicator}, recipient={self.recipient})"


@dataclass
class Conflict_Defeat_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, defeated: Optional[List] = None, place: Optional[List] = None, victor: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.defeated = defeated if defeated is not None else []
        self.place = place if place is not None else []
        self.victor = victor if victor is not None else []

    def __repr__(self):
        return f"Conflict_Defeat_Unspecified(mention=\"{self.mention}\", defeated={self.defeated}, place={self.place}, victor={self.victor})"


@dataclass
class Control_ImpedeInterfereWith_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, impeder: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.impeder = impeder if impeder is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"Control_ImpedeInterfereWith_Unspecified(mention=\"{self.mention}\", impeder={self.impeder}, place={self.place})"


@dataclass
class Cognitive_Research_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, place: Optional[List] = None, researcher: Optional[List] = None, subject: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.researcher = researcher if researcher is not None else []
        self.subject = subject if subject is not None else []

    def __repr__(self):
        return f"Cognitive_Research_Unspecified(mention=\"{self.mention}\", place={self.place}, researcher={self.researcher}, subject={self.subject})"


@dataclass
class ArtifactExistence_DamageDestroyDisableDismantle_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, damagerdestroyer: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.damagerdestroyer = damagerdestroyer if damagerdestroyer is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"ArtifactExistence_DamageDestroyDisableDismantle_Unspecified(mention=\"{self.mention}\", artifact={self.artifact}, damagerdestroyer={self.damagerdestroyer}, instrument={self.instrument}, place={self.place})"


@dataclass
class Movement_Transportation_IllegalTransportation(Event):
    def __init__(self, mention: Optional[List] = None, destination: Optional[List] = None, passengerartifact: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.destination = destination if destination is not None else []
        self.passengerartifact = passengerartifact if passengerartifact is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"Movement_Transportation_IllegalTransportation(mention=\"{self.mention}\", destination={self.destination}, passengerartifact={self.passengerartifact}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class Justice_Acquit_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, defendant: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.defendant = defendant if defendant is not None else []

    def __repr__(self):
        return f"Justice_Acquit_Unspecified(mention=\"{self.mention}\", defendant={self.defendant})"


@dataclass
class Contact_RequestCommand_Correspondence(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, recipient: Optional[List] = None, topic: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.recipient = recipient if recipient is not None else []
        self.topic = topic if topic is not None else []

    def __repr__(self):
        return f"Contact_RequestCommand_Correspondence(mention=\"{self.mention}\", communicator={self.communicator}, recipient={self.recipient}, topic={self.topic})"


@dataclass
class ArtifactExistence_DamageDestroyDisableDismantle_Dismantle(Event):
    def __init__(self, mention: Optional[List] = None, artifact: Optional[List] = None, components: Optional[List] = None, dismantler: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifact = artifact if artifact is not None else []
        self.components = components if components is not None else []
        self.dismantler = dismantler if dismantler is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []

    def __repr__(self):
        return f"ArtifactExistence_DamageDestroyDisableDismantle_Dismantle(mention=\"{self.mention}\", artifact={self.artifact}, components={self.components}, dismantler={self.dismantler}, instrument={self.instrument}, place={self.place})"


@dataclass
class Movement_Transportation_PreventPassage(Event):
    def __init__(self, mention: Optional[List] = None, destination: Optional[List] = None, origin: Optional[List] = None, passengerartifact: Optional[List] = None, preventer: Optional[List] = None, transporter: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.destination = destination if destination is not None else []
        self.origin = origin if origin is not None else []
        self.passengerartifact = passengerartifact if passengerartifact is not None else []
        self.preventer = preventer if preventer is not None else []
        self.transporter = transporter if transporter is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"Movement_Transportation_PreventPassage(mention=\"{self.mention}\", destination={self.destination}, origin={self.origin}, passengerartifact={self.passengerartifact}, preventer={self.preventer}, transporter={self.transporter}, vehicle={self.vehicle})"


@dataclass
class Conflict_Demonstrate_DemonstrateWithViolence(Event):
    def __init__(self, mention: Optional[List] = None, demonstrator: Optional[List] = None, regulator: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.demonstrator = demonstrator if demonstrator is not None else []
        self.regulator = regulator if regulator is not None else []

    def __repr__(self):
        return f"Conflict_Demonstrate_DemonstrateWithViolence(mention=\"{self.mention}\", demonstrator={self.demonstrator}, regulator={self.regulator})"


@dataclass
class Disaster_Crash_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, crashobject: Optional[List] = None, place: Optional[List] = None, vehicle: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.crashobject = crashobject if crashobject is not None else []
        self.place = place if place is not None else []
        self.vehicle = vehicle if vehicle is not None else []

    def __repr__(self):
        return f"Disaster_Crash_Unspecified(mention=\"{self.mention}\", crashobject={self.crashobject}, place={self.place}, vehicle={self.vehicle})"


@dataclass
class Contact_RequestCommand_Broadcast(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"Contact_RequestCommand_Broadcast(mention=\"{self.mention}\", communicator={self.communicator}, recipient={self.recipient})"


@dataclass
class Disaster_DiseaseOutbreak_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, place: Optional[List] = None, victim: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.victim = victim if victim is not None else []

    def __repr__(self):
        return f"Disaster_DiseaseOutbreak_Unspecified(mention=\"{self.mention}\", place={self.place}, victim={self.victim})"


@dataclass
class Contact_ThreatenCoerce_Broadcast(Event):
    def __init__(self, mention: Optional[List] = None, communicator: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.communicator = communicator if communicator is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"Contact_ThreatenCoerce_Broadcast(mention=\"{self.mention}\", communicator={self.communicator}, recipient={self.recipient})"


@dataclass
class Transaction_Donation_Unspecified(Event):
    def __init__(self, mention: Optional[List] = None, artifactmoney: Optional[List] = None, giver: Optional[List] = None, recipient: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.artifactmoney = artifactmoney if artifactmoney is not None else []
        self.giver = giver if giver is not None else []
        self.recipient = recipient if recipient is not None else []

    def __repr__(self):
        return f"Transaction_Donation_Unspecified(mention=\"{self.mention}\", artifactmoney={self.artifactmoney}, giver={self.giver}, recipient={self.recipient})"
