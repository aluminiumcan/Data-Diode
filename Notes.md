
gebruik van interface rx tx op de datadiode

----------------------------------

1. Uiteindelijk TCP van communicatie 
Beginnen met UDP

Over waar de verbinding mag:
De fpga kan wel terugsturen naar de verzender maar de ontvanger kan niet sturen naar de fpga

Tussen verzender en fpga is TCP en van fpga naar ontvanger is UDP.

2. 1 GB/s is geen harde eis. POC is goed genoeg

3. Als je het opeens verbind met een andere verzender dan moet hij  de verbinding weigeren. Dus voorag bepalen wie de verzender is. De ontvanger maakt niet uit wie de verzender is, dus gewoon via udp.

4. zynq 7000 Z7 NANO
Er is een github met documentatie


5. Communicatie project:
Stuur maar op als je een PVA of iets hebt.
Graag de mijlpalen doorgeven.
Bij struikelblokken stuur een mail.

6. Documentatie:
- Wat school vraagt.

7. Pioriteit:
   Bijt je niet aan de authenticatie vast. Datastroom is belangrijker.


Over prototype: 
Gewoon dat er iets binnenkomt. Een link dat een ledje aan gaat of een simulatie.

Over taken
- Splitten van component of split hardware en software in taken
- gebruik van libraries

Extras:
- bepaalde data filteren als het werkt
- videostram

gastles is 22e 