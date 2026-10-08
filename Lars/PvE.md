# Programma van Eisen – Data-Diode

|                   |   |                                                                  |
|-------------------|---|------------------------------------------------------------------|
| Opgesteld door    | : | Projectgroep DataDiode                                           |
| Projectleider     | : | Jens van Winden                                                  |
| Projectleden      | : | Bart Sterrenburg, Ivo Bruinsma, Lars de Boorder, Issam Mahrik    |
| Begeleider        | : | Jens van Winden                                                  |
| Opdrachtgever     | : | Sentyron                                                         |
| Versie            | : | 1.0 (concept)                                                    |
| Datum van uitgifte| : | 06-10-2026                                                       |

## Versiebeheer

| Versie | Datum      | Wie              | Wat                                                                 |
|--------|------------|------------------|---------------------------------------------------------------------|
| 0.1    | 01-10-2026 | Bart Sterrenburg | Eerste opzet van de eisen (functioneel, security, prestatie, tests) |
| 1.0    | 06-10-2026 | Lars de Boorder  | Analyse van de wensen toegevoegd, prioriteiten aangepast aan de opdrachtgever, bron per eis, fasering en open vragen |

---

## 1. Inleiding

### 1.1 Doel van dit document

In dit document staan de eisen voor de data-diode die wij voor Sentyron bouwen. Bij elke eis staat waar hij vandaan komt, hoe belangrijk hij is en hoe we hem gaan testen. Het PvE is de basis voor het architectuurontwerp, het detailontwerp en het acceptatietestplan.

### 1.2 Wat bouwen we

Een data-diode laat data maar in één richting door. Wij bouwen een proof of concept (PoC) op een Z7 Nano-board met een Zynq 7000. Er zijn twee kanten:

- **Kant A (verzender):** een laptop of ander systeem dat data aanlevert aan de FPGA.
- **Kant B (ontvanger):** een systeem dat de data van de FPGA ontvangt via UDP.

Data gaat van A via de FPGA naar B. Kant B mag niets terugsturen naar de FPGA of naar A. De FPGA mag wel antwoorden aan de verzender, bijvoorbeeld voor een TCP-verbinding.

### 1.3 Afbakening: logische diode

Het Z7 Nano-board heeft gewone koperen Ethernetpoorten. Die kunnen fysiek altijd in beide richtingen werken. Een "echte" data-diode heeft vaak geen fysieke weg terug, bijvoorbeeld een glasvezel met alleen een zender. Onze PoC is daarom een **logische** diode: de FPGA-logica zorgt ervoor dat verkeer vanaf B wordt genegeerd en nergens terechtkomt.

In ons plan van aanpak staat dat eenrichtingsverkeer ook in de fysieke opzet wordt meegenomen. Na verder uitzoeken blijkt dat met deze hardware alleen logisch te kunnen. We leggen aan Sentyron voor of een logische diode voldoende is (zie hoofdstuk 6). In het eindverslag beschrijven we de restrisico's hiervan (eis PD-003).

Buiten de scope vallen (zie ook PvA §2.3): volledige cryptografische authenticatie, certificaatbeheer en een gegarandeerde snelheid van 1 Gb/s.

### 1.4 Prioriteiten (MoSCoW)

| Prioriteit | Betekenis                                                                 |
|------------|---------------------------------------------------------------------------|
| **Must**   | Moet erin. Zonder deze eis is de PoC niet geslaagd.                       |
| **Should** | Belangrijk en willen we halen, maar de PoC faalt niet zonder.             |
| **Could**  | Doen we alleen als de basis werkt en er tijd over is.                     |
| **Won't**  | Doen we in dit project bewust niet.                                       |

---

## 2. Analyse van de wensen van Sentyron

### 2.1 Bronnen

- **[G]** Gesprek met Sentyron op 10-09-2026 (aantekeningen in `Notes.md` in onze GitHub-repo).
- **[PvA]** Ons Plan van Aanpak Data-Diode.
- **[OB]** Eerste opzet van de eisen door Bart Sterrenburg (01-10-2026).

### 2.2 Wensen en wat ze voor ons betekenen

| ID   | Wat Sentyron wil                                                                 | Bron | Wat betekent dit voor ons                                                                                   |
|------|----------------------------------------------------------------------------------|------|-------------------------------------------------------------------------------------------------------------|
| W-01 | De ontvanger kan niet terugsturen naar de FPGA. De FPGA mag wel terugsturen naar de verzender. | [G]  | Dit is de kern van het project. Alles wat via kant B binnenkomt moet worden genegeerd. Kant A mag wel tweerichtingsverkeer hebben. |
| W-02 | Tussen verzender en FPGA uiteindelijk TCP, maar beginnen met UDP. Van FPGA naar ontvanger UDP. | [G]  | Eerst een simpele UDP-datastroom laten werken. TCP is een volgende stap. Naar B altijd UDP, want UDP heeft geen antwoord van de ontvanger nodig. |
| W-03 | Een andere verzender moet geweigerd worden. Vooraf bepalen wie de verzender is. Wie de ontvanger is maakt niet uit. | [G]  | De FPGA moet de verzender kunnen herkennen (bijvoorbeeld IP-adres of een ID). De ontvanger hoeft niet gecontroleerd te worden. |
| W-04 | Niet vastbijten in de authenticatie. Datastroom is belangrijker.                  | [G]  | Authenticatie krijgt een lagere prioriteit dan de datastroom. We zorgen wel dat er een onderbouwde aanpak is. |
| W-05 | 1 Gb/s is geen harde eis, een PoC is goed genoeg.                                 | [G]  | Snelheid is niet het belangrijkste. Wij hebben als groep 100 Mb/s als minimum gekozen (PvA §3).               |
| W-06 | Zynq 7000 Z7 Nano gebruiken.                                                      | [G]  | Het board ligt vast.                                                                                        |
| W-07 | Libraries gebruiken mag.                                                          | [G]  | We mogen open-sourcecomponenten gebruiken, maar leggen vast welke (bron en jaar).                           |
| W-08 | Prototype: laten zien dat er iets binnenkomt, met een LED of een simulatie.       | [G]  | Voor het prototype is een simpele demonstratie genoeg.                                                      |
| W-09 | Extra's als de basis werkt: bepaalde data filteren, videostream.                  | [G]  | Alleen als alles werkt. Deze krijgen prioriteit Could.                                                      |

### 2.3 Conclusie van de analyse

Uit het gesprek blijkt dat Sentyron vooral wil zien dat een FPGA eenrichtingsverkeer kan afdwingen. De datastroom van A naar B en het blokkeren van verkeer vanaf B zijn daarom **Must**. De controle van de verzender is wel een wens (W-03), maar Sentyron zegt zelf dat we ons er niet in moeten vastbijten (W-04). Daarom is een onderbouwde aanpak voor de verzendercontrole Must, en het echt weigeren van een onbekende verzender Should. Dit sluit aan bij het hoofddoel in ons PvA (§2.2). Snelheid en extra's komen pas na de basis.

---

## 3. Eisen

De kolom *Test* verwijst naar de tests in hoofdstuk 5. De nummers uit de eerste opzet [OB] zijn waar mogelijk aangehouden.

### 3.1 Functionele eisen (FR)

| ID      | Eis                                                                                                   | Prio   | Bron        | Test        |
|---------|-------------------------------------------------------------------------------------------------------|--------|-------------|-------------|
| FR-001  | Het systeem kan data (payload) van kant A naar kant B doorsturen.                                     | Must   | W-01, W-02  | T-01        |
| FR-002a | De verbinding tussen verzender en FPGA werkt met UDP.                                                 | Must   | W-02        | T-01        |
| FR-002b | De verbinding tussen verzender en FPGA werkt met TCP.                                                 | Should | W-02        | T-01        |
| FR-003  | De FPGA stuurt data naar kant B alleen als UDP over IPv4 en Ethernet.                                  | Must   | W-02        | T-01, T-04  |
| FR-004  | Het MAC-adres, IP-adres en de UDP-poort van de ontvanger zijn vooraf vast ingesteld. Daardoor is geen ARP-antwoord van B nodig. | Must | W-01 | T-04 |
| FR-005  | Er is een uitgewerkte en onderbouwde aanpak voor het controleren van de verzender.                    | Must   | W-03, W-04, PvA §2.2 | Review |
| FR-006  | Alleen een vooraf ingestelde verzender (allowlist) kan een sessie starten. Een onbekende verzender wordt geweigerd en er gaat dan niets naar B. | Should | W-03 | T-02, T-03 |
| FR-007  | Data die binnenkomt voordat de verzender is toegelaten, wordt weggegooid.                             | Should | W-03        | T-03        |
| FR-008  | De handshake bevat minimaal een protocolversie en een verzender-ID. Dit is een PoC en geen volwaardige beveiliging. | Should | W-03, W-04 | T-02 |
| FR-009  | Elk UDP-pakket naar B bevat een volgnummer en de lengte van de payload, zodat B kan zien of er data mist. | Should | [OB]     | T-01, T-04  |

### 3.2 Eenrichtingseisen (ER)

| ID      | Eis                                                                                                   | Prio   | Bron       | Test             |
|---------|-------------------------------------------------------------------------------------------------------|--------|------------|------------------|
| ER-001  | Verkeer dat via kant B binnenkomt, komt niet bij de software (PS), de payloadlogica of bij kant A.    | Must   | W-01       | T-05, R-01       |
| ER-002  | Kant B verstuurt geen ARP, ICMP, TCP, DHCP of IPv6, alleen de UDP-pakketten uit FR-003.               | Must   | W-01       | T-04, T-06       |
| ER-003  | Er is geen bridge, router, NAT of IP-forwarding tussen kant A en kant B.                              | Must   | W-01       | T-05, T-06, R-01 |
| ER-004  | Ontvangen signalen van kant B (RX) worden zo vroeg mogelijk genegeerd. Er is geen buffer, interrupt, DMA of software die deze data kan lezen. | Must | W-01 | T-05, R-01 |
| ER-005  | Beheer van het board (bijvoorbeeld SSH of een webinterface) is niet bereikbaar via kant B.             | Must   | W-01       | T-06             |
| ER-006  | Pause frames van kant B hebben geen invloed op kant A. Flow control op B staat uit waar dat kan.      | Should | W-01       | T-05             |
| ER-007  | Linkstatus en statistieken van kant B worden niet teruggegeven aan de verzender.                      | Should | W-01       | T-05             |
| ER-008  | Logbestanden bevatten geen payload en geen token van de verzender.                                     | Could  | [OB]       | Review           |

### 3.3 Prestatie-eisen (PR)

| ID      | Eis                                                                                                   | Prio   | Bron            | Test |
|---------|-------------------------------------------------------------------------------------------------------|--------|-----------------|------|
| PR-001  | De doorvoersnelheid van A naar B is minimaal 100 Mb/s.                                                | Must   | W-05, PvA §3    | T-09 |
| PR-002  | Als de hardware het ondersteunt, meten we ook de snelheid bij 1 Gb/s.                                  | Could  | W-05            | T-09 |
| PR-003  | Bij elke snelheidsmeting leggen we ook het pakketverlies vast.                                         | Should | [OB]            | T-09 |
| PR-004  | Als een buffer vol is, worden alleen hele pakketten weggegooid (of wacht de verzender). Er gaan geen halve pakketten naar B. | Should | [OB] | T-07 |

### 3.4 Randvoorwaarden (RV)

| ID      | Eis                                                                                                   | Prio   | Bron       | Test   |
|---------|-------------------------------------------------------------------------------------------------------|--------|------------|--------|
| RV-001  | De oplossing draait op het Z7 Nano-board met Zynq 7000.                                                | Must   | W-06       | T-01   |
| RV-002  | Van elke gebruikte library of open-sourcecomponent leggen we de bron, het jaar en de licentie vast.    | Must   | W-07       | Review |
| RV-003  | Code, FPGA-project en testscripts staan in GitHub, zodat het project opnieuw te bouwen is.             | Should | [PvA §1.2] | T-10   |
| RV-004  | Na een reset of opstart stuurt de FPGA niets naar B totdat alles goed is ingesteld (fail-closed).      | Should | [OB]       | T-08   |

De hardwaredetails van het board (welke Ethernet-PHY, hoe de poorten aangesloten zijn, welke snelheden mogelijk zijn) zoeken we uit in het Ethernet-onderzoek (Jira DD-24). De punten HW-001 t/m HW-007 uit de eerste opzet [OB] gebruiken we daar als checklist.

### 3.5 Prototype en oplevering (PD)

| ID      | Eis                                                                                                   | Prio   | Bron        | Test   |
|---------|-------------------------------------------------------------------------------------------------------|--------|-------------|--------|
| PD-001  | Het prototype laat zien dat data bij de FPGA binnenkomt, met een LED of een simulatie.                 | Must   | W-08        | Demo   |
| PD-002  | De werking van de PoC wordt gedemonstreerd aan Sentyron.                                               | Must   | PvA §2.2    | Demo   |
| PD-003  | Het eindverslag beschrijft de restrisico's, waaronder dat de koperpoorten fysiek in twee richtingen kunnen werken. | Must | §1.3, [OB] | Review |

### 3.6 Extra's

| ID      | Eis                                                                                                   | Prio   | Bron       |
|---------|-------------------------------------------------------------------------------------------------------|--------|------------|
| EX-001  | De FPGA kan bepaalde data filteren.                                                                    | Could  | W-09       |
| EX-002  | Er kan een videostream van A naar B worden gestuurd.                                                   | Could  | W-09       |
| EX-003  | Volledige cryptografische authenticatie en certificaatbeheer.                                          | Won't  | PvA §2.3   |
| EX-004  | Een gegarandeerde doorvoersnelheid van 1 Gb/s.                                                         | Won't  | W-05, PvA §2.3 |

---

## 4. Fasering

Volgens onze huidige sprintplanning werken we de eisen in deze volgorde uit. De planning kan nog veranderen.

| Fase                    | Eisen                                                                 |
|-------------------------|-----------------------------------------------------------------------|
| Sprint 2 + alfa (week 1.9) | FR-001, FR-002a, FR-003, FR-004, ER-001 t/m ER-005, RV-001, RV-002 |
| Sprint 3                | FR-002b (TCP), FR-009                                                 |
| Sprint 4                | FR-005 t/m FR-008 (verzendercontrole), ER-006, ER-007                |
| Sprint 5                | PR-001 t/m PR-004, RV-003, RV-004                                     |
| Sprint 6                | Acceptatietest, PD-002, PD-003                                        |
| Als er tijd over is     | EX-001, EX-002, PR-002, ER-008                                        |

---

## 5. Verificatie

Hoe we de tests precies uitvoeren, beschrijven we in het acceptatietestplan (Jira DD-8). Hier staat alleen welke tests er zijn.

| ID    | Test                                                                     |
|-------|--------------------------------------------------------------------------|
| T-01  | Geldige datastroom van A naar B                                          |
| T-02  | Onbekende verzender wordt geweigerd                                      |
| T-03  | Data vóór toelating en foute handshakes                                  |
| T-04  | Controle van de pakketten die op B aankomen                              |
| T-05  | Verkeer naar kant B sturen en controleren dat het nergens aankomt        |
| T-06  | Geen beheer via B en geen bridge/router tussen A en B                    |
| T-07  | Overbelasting en gedrag bij volle buffers                                |
| T-08  | Reset en opstarten (fail-closed)                                         |
| T-09  | Snelheidsmeting                                                          |
| T-10  | Project opnieuw bouwen vanuit GitHub                                     |
| R-01  | Review van hardware en FPGA-ontwerp: kan RX van B ergens komen?          |

---

## 6. Open vragen voor Sentyron

1. Is een logische diode met koperen Ethernetpoorten voldoende, of verwacht Sentyron een fysieke scheiding (zie §1.3)?
2. Het minimum van 100 Mb/s komt uit ons PvA en niet uit het gesprek. Vindt Sentyron dit een goede ondergrens?
3. Hoe moet de verzender herkend worden: is een vast IP- of MAC-adres genoeg, of willen ze een ID of token in de handshake?
4. Wat voor soort data moet er uiteindelijk door de diode (bestanden, losse berichten, een stream)?

---

## Bronnen

- Sentyron. (2026, 10 september). *Gesprek met de opdrachtgever* [Aantekeningen in `Notes.md`, GitHub-repository aluminiumcan/Data-Diode].
- Projectgroep DataDiode. (2026). *Plan van Aanpak – Data-Diode*. Hogeschool Rotterdam.
- Sterrenburg, B. (2026, 1 oktober). *Requirements – FPGA-data-diode PoC* [Eerste opzet, bijlage bij Jira DD-7].
