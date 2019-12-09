# HeHE-maker
Ett enkelt verktyg för att skapa en webbversion och en version för tryck av HeHE

## How-To
Lägg in alla sidor som en egen PDF i `/pages/`. Se till att numrera dem så att de hamnar i rätt ordning (1 högst upp, sen 2, sen 3 osv...).

`/scripts/hehemaker.py` går från topp till botten igenom alla PDF:er i `/pages/` och sätter ihop två versioner i `/papers/`; En version för webben (där alla sidor är ensamma och hamnar efter varandra) och en version som kan skickas till tryck.
