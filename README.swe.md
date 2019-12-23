# HeHE-maker
*Denna version ~~kan vara något~~ är väldigt utdaterad. För en fullständig guide, se `README.md`*

**HeHE-maker** är ett enkelt verktyg för att skapa en webbversion och en version för tryck av HeHE, och lite andra saker, som kan köras i kommandotolken med Python. För att skapa en ny upplaga av HeHE, börja med att sätta ihop varje sida i valfritt programm, allt från MS Paint till OpenOffice fungerar, bara sätt in texten på mallarna du fått av Picasso och exportera varje sida som en PDF i en annars tom mapp. Se till att de hamnar i rätt ordning, dvs. förstasidan högst upp, följt av andra sidan osv. (förslagsvis genom att namnge dem till 01.pdf, 02.pdf, 03.pdf etc etc). Antalet sidor måste som standard vara = 0 (mod 4) för att programmet ska fungera!

### Vad fan är en kommandotolk?
Du vet den där svarta rutan eliiite haxxors använder i filmer? Aa men den. Kan sökas fram på Windows, och är du på Linux kan du nog ignorera denna guiden helt.

### Tips
Följande kommandon behöver du för att använda HeHE-maker:

* `cd`: Change Directory, så du navigerar dig mellan filer
* Högerklick: Klistrar in det du kopierat i kommandotolken. Effektivt!

That's it!

## Python
Python är ett bra programmeringsspråk som är relativt lätt att köra lokalt på din dator. Installera via https://www.python.org/downloads/ och följ anvisningarna. Glöm inte kontrollera att allt funkar genom att skriva `python -v` i kommandotolken!

OBS: Om du inte låter python skapa en miljövariabel (PATH-variable) vid installation kan du komma att behöva fixa runt lite för att köra scriptet.

## Krav
Kräver paketet `pdfrw` för att fungera. Installera genom att köra `pip install pdfrw`.

## Så kör du programmet
Följ installationsguiden ovan. När du gjort det, ladda ner detta projektet. Öppna kommandotolken och navigera till `/hehe-maker/`-mappen (om du inte vill lägga till en PATH-variabel) och skriv in `hehe-maker.py "<input>" "<output>"` där du ersätter `<input>` med sökvägen till mappen där du sparat dina sidor och `<output>` med sökvägen till den plats du vill spara dina tidningar. Tryck `Enter` och klart!

Har du en webbversion som du vill göra om till en printversion är det bara att köra programmet precis som du hade gjort om du haft en mapp full med olika sidor.

### Flaggor
Flaggor kan användas för att ändra vad HeHE-maker gör. Nedan följer en lista. Bara skriv in efter `hehe-maker.py`! Blanda dessa flaggor på egen risk.

* Är denna listan inte hjälpsam nog? Skriv `-h` eller `--help`!
* Man kan förtrycka kravet på att man ska kunna trycka allt på ett jämnt antal uppslag genom att lägga till flaggan `-f` eller `--force` före `input`.
* Skulle du istället vilja konvertera från en printversion till en webbversion, använd `-s` eller `--split` före `input` (det är ej nödvändigt att använda `-f` samtidigt).
* Vill du ta bort en eller flera sidor kan du använda `-rm` eller `--remove`, följt av sidnummret eller sidnummerna. Exempel: Du vill ta bort första och sista sidan. Då skriver du helt enkelt in `hehe-maker.py -rm 1 12 "<sökväg till input>" "<sökväg till output>"`!
* Om du vill sätta in filer i en existerande PDF kan du använda `-ins` eller `--insert` följt av sökvägen till mappen där allt du vill sätta in ligger, samt på vilket index detta ska sättas in med hjälp av flaggan `-i` (eller `--index`). Exempelvis kan man göra så här för att lägga in två sidor som ligger i mappen på sökvägen `\xxx\` på andrasidan: `hehe-maker.py -ins "\xxx\" -i 2 "<sökväg till input>" "<sökväg till output>"`.

## Varför
Att sitta och göra denna tidningen i PowerPoint som Redaktionen '19 är inte optimalt.

## TODO
Rimligen kan scriptet även anpassas för att köras på en hemsida, vilket är ett framtida projekt. Även installationen kan göras enklare. Ny flagga för att sätta in en sida i en PDF kan också behövas
