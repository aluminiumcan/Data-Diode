# LD4 — Bewijs: actief handelen op verandering in planning en risico's

Doel: aantonen dat wij veranderingen in planning en risico's zien en daar aantoonbaar op bijsturen.
Bijhouden na elke sprint (en zodra er iets verandert). Verwijs vanuit het beoordelingsformulier naar dit bestand en naar de Jira-issues.

Jira: project DD, epic **DD-23 Risico's en planningswijzigingen**.

---

## 1. Planningswijzigingen

Per wijziging: wat zagen we, wat was de oorzaak, wat hebben we aangepast, wat was het effect.

| # | Datum | Week | Wat veranderde / wat zagen we | Oorzaak | Aanpassing | Gecommuniceerd aan | Jira |
|---|-------|------|-------------------------------|---------|------------|--------------------|------|
| 1 | 2026-10-01 | 1.5 | Achterstand op de planning | (invullen) | Scope sprint 1 ingekort: eerst DD-9, DD-7, DD-24. Testplannen (DD-8, DD-10) naar sprint 2. Extra's en authenticatie uitgesteld. | (Sentyron: datum mail invullen, zie DD-41) | DD-42 |

> Invullen door de groep: de echte oorzaak van de achterstand en de Jira-key. De gedane aanpassing hierboven is het voorstel; pas aan als jullie het anders hebben gedaan.

---

## 2. Risicolijst

Kans en impact: laag / middel / hoog. Status: open / bewaakt / opgetreden / opgelost.

| Jira | Risico | Kans | Impact | Maatregel | Eigenaar | Status | Laatst bijgewerkt |
|------|--------|------|--------|-----------|----------|--------|-------------------|
| DD-32 | Geen bruikbaar Ethernet-component voor de Z7 Nano | middel | hoog | Bestaande open-sourcecomponenten zoeken; terugval: Zynq-PS (ARM) voor netwerk | | open | 2026-10-01 |
| DD-33 | TCP-stack te zwaar/complex voor FPGA-logica | hoog | middel | Eerst UDP (toegestaan door opdrachtgever), TCP later | | open | 2026-10-01 |
| DD-34 | Doorvoersnelheid haalt 100 Mb/s niet | middel | middel | Vroeg meten, niet pas aan het eind | | open | 2026-10-01 |
| DD-35 | Eenrichtingsverkeer niet aantoonbaar | middel | hoog | Ontwerpkeuze onderbouwen en testen | | open | 2026-10-01 |
| DD-36 | Te lang vastzitten aan authenticatie | middel | middel | Eerst basisdatastroom, authenticatie daarna | | open | 2026-10-01 |
| DD-43 | Achterstand op planning | hoog | middel | Scope inkorten, prioriteiten (zie planningswijziging 1) | | opgetreden | 2026-10-01 |

> Kans/impact zijn een eerste inschatting van Claude; de groep moet ze bevestigen of aanpassen. Eigenaar nog invullen.

---

## 3. Sprintoverzicht (kort, per sprint)

Wordt ook gebruikt als "overzicht van sprints" voor de beoordeling (Scrum).

| Sprint | Periode | Sprintdoel | Gepland | Af | Niet af + waarom | Retro: wat verbeteren we |
|--------|---------|------------|---------|----|------------------|--------------------------|
| 1 | 1.5–1.6 | Ontwerp staat, Ethernet-component gekozen | | | | |
| 2 | 1.7–1.8 | Alfa: data via UDP naar ontvanger | | | | |

---

## 4. Sjabloon voor een nieuwe wijziging

```
Datum / week:
Wat zagen we:
Oorzaak:
Gevolg als we niets doen:
Wat hebben we aangepast (concreet):
Wie is geïnformeerd en hoe (mail/overleg + datum):
Effect achteraf (volgende sprint invullen):
Jira-issue:
```

## 5. Bewijs bewaren
- Screenshot van het Jira-bord/de burndown aan het eind van elke sprint
- Mails/notulen aan en van Sentyron (dat is ook bewijs voor LD5)
- Dit bestand, bij elke wijziging bijgewerkt met datum
