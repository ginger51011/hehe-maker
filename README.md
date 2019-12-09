# HeHE-maker
Ett enkelt verktyg för att skapa en webbversion och en version för tryck av HeHE som kan köras i kommandotolken med Python. Börja med att sätta ihop varje sida i valfritt programm, allt från MS Paint till OpenOffice fungerar, bara sätt in texten på mallarna du fått av Picasso och exportera varje sida som en PDF i en annars tom mapp. Se till att de hamnar i rätt ordning, dvs. förstasidan högst upp, följt av andra sidan osv. (förslagsvis genom att namnge dem till 1.pdf, 2.pdf, 3.pdf etc etc). Antalet sidor måste vara = 0 (mod 4) för att programmet ska fungera!

### Vad fan är en kommandotolk?
Du vet den där svarta rutan eliiite haxxors använder i filmer? Aa men den. Kan sökas fram på Windows, och är du på Linux kan du nog ignorera denna guiden helt.

### Tips
Följande kommandon behöver du för att använda HeHE-maker:

`cd`: Change Directory, så du navigerar dig mellan filer
Högerklick: Klistrar in det du kopierat i kommandotolken. Effektivt!

That's it!

## Python
Python är ett bra programmeringsspråk som är relativt lätt att köra lokalt på din dator. Installera via https://www.python.org/downloads/ och följ anvisningarna. Glöm inte kontrollera att allt funkar genom att skriva `python -v` i kommandotolken!

## Så kör du programmet
Följ installationsguiden ovan. När du gjort det, ladda ner detta projektet. Öppna kommandotolken och navigera till `hehe-maker` och skriv in `python hehemaker.py "<input>" "<output>"` där du ersätter `<input>` med sökvägen till mappen där du sparat dina sidor och `<output>` med sökvägen till den plats du vill spara dina tidningar. Tryck `Enter` och klart!

## Varför
Att sitta och göra denna tidningen i PowerPoint som Redaktionen '19 är inte optimalt.

## TODO
Fixa enklare installation, öka mångsidigheten till att klara av NollEguiden med, förslagsvis med fler flags.

Rimligen kan scriptet även anpassas för att köras på en hemsida, vilket är ett framtida projekt.
