# Comments while tuning the optimal network

## 1 Character initiële config
layers= Conv(96, 96, 32) Pool(48, 48, 32) Conv(48, 48, 64) PoolConv(24, 24, 64) Dense(512)
epochs = 30
number of images = 2000
test % = 0.2 
padding = 'equal'
filters = (3, 3)
aantal filters = 32 64 (aantal stijgt met de diepte van het netwerk)
learning_rate = 0.001 (default)
optimizer = adam

## Run 1: acc 0.32
Netwerk veranderingen: 
- None

Analyse:
- Overfitting is super hoog en acc on test zeer laag

## Run 2: acc 0.20
Netwerk veranderingen: 
- padding is op valid gezet, dit doet zorgt ervoor dat het netwerk minder complexer wordt

Analyse:
- Overfitting is super hoog en acc on test zeer laag
erfitting is super hoog en acc on test zeer laag

## Run 3: acc 0.42
Netwerk veranderingen: 
- Aan de fully connected layer heb is een dropout van 0.5 toegevoegd
- Dit om overfitting tegen te gaan. Door random weights op 0 te zetten probeer je te verkomen dat het netwerk te lang blijft hangen bij slechte weight settings. 
- Padding is terug op same gezet. Volgens Standford lecture van Andrej Karpathy is het best om dit te doen, zodanig dat je niet direct een te klein netwerk hebt qua width and height

Analyse:
- Overfitting is nu pas na epoch 15, dus dropout doet zijn werk, maar nog niet voldoende

## Run 4: acc 0.39
Netwerk veranderingen: 
- Extra dropout toegevgoed voor conv layers: 0.25 aan layer 1 en 0.3 aan conv layer 2. De eerste conv bevat de initiële input data, dus dropout mag niet te groot zijn anders verliezen we te veel info in het begin van de ketting 

Analyse:
- Hoewel de acc lager is dan vorige run is de overfitting minder in die zin dat 
  de trainingsacc niet 100% na 30 epochs. 

## Run 5: acc 0.86
Netwerk veranderingen: 
- Extra conv2d layer toegevoegd met 96 filters
- filters van convs veranderd naar 5X5. Er gaat dus op een grote oppervlak naar features gekeken worden.
  Je zou dus kunnen zeggen dat het model daardoor generieker zou moeten worden om zo overfitting tegen te gaan
- Verdubbelen het aantal epoch naar 60, want acc bleef binnen de eerste 20 laag

Analyse:
- ACC is veel hoger. Beetje raar wel dat een extra layer niet voor nog meer overfitting heeft gezorgd, want model complexiteit is vergroot.
- ACC overfitting na epoch 30
- Loss overfitting na epoch 20

## Run 6: acc 0.72
Netwerk veranderingen:
-  Dropout toegevoegd aan eerste conv layer om te zien of overfitting danlager is
Analyse:
- ACC is lager, maar overfitting start veel later (epoch 40, wel nog overfitting of validation loss vanaf epoch 30

## Run 7: acc 0.05
Netwerk veranderingen:
-  l1 regulariation toegevoegd aan alle conv layers l1 0.001 and dropout conv1 weggedaan
Analyse:
- Super slecht

## Run 8: acc 0.92
Netwerk veranderingen:
-  aantal filters gehalveerd en training en test data verdubbeld!
Analyse:
- Super goed! Wel nog validation loss overfitting, maar pas heel laat. Zie metrics.png

## Run 9: acc 0.92
Netwerk veranderingen:
-  dropout aan laatste conv layer toegevoegd en meer 40 epochs ipv 30. 
Analyse:
- Nog hogere acc en minder overfitting.

## 2 Character initiële config
layers= Conv(96, 96, 32) Pool(48, 48, 32) Conv(48, 48, 64) PoolConv(24, 24, 64) Dense(512)
epochs = 30
number of images = 2000
test % = 0.2 
padding = 'equal'
filters = (3, 3)
aantal filters = 32 64 (aantal stijgt met de diepte van het netwerk)
learning_rate = 0.001 (default)
optimizer = adam

## Run 1: acc 0.05
Netwerk veranderingen: 
- Beste netwerk van 1 char genomen

Analyse:
- Trainingset is volledig gememoriseerd... 

## Run 1: acc 0.05
Netwerk veranderingen: 
- Dense layer bevatte minder nodes dan de ouput, dus info verlies. Staat nu op 1024

Analyse:
- Trainingset is volledig gememoriseerd... 

## Sequence van twee cijfers. Minder complexe uitdaging dan 2 letters
## Run 1:  0.34
Netwerk veranderingen: 
- Start met configuratie beste netwerk 1 letter, enkel is laatste layer wel 100 want 10*10 combinaties 

Analyse:
- Trainingsdata overfit redelijk snel naar 70% na tien epochs waar test acc 33% is.  

## Run 2: 0.81
Netwerk veranderingen: 
- Dropout toegevoegd aan alle layers

Analyse:
- Blijft overfitten. Dropout is al overal toegevoegd, dus ga eens proberen met 10000 ipv 5000 images. 
- 10000 images convergeert niet zelfs niet na 50 epochs + duurt te lang. Data augmentation gebruiken, zo blijft rekenkracht/tijd hetzelfde.
- Hoe meer categorieën er zijn hoe meer trainingsdata nodig, zodanig dat elke combinatie minstens n keer kan voorkomen. 

## Run 3: 0.00
Netwerk veranderingen: 
- Data augmentation toegevoegd, dus er wordt nu gewerkt met generators. 
- rotation_range=30 -> 15 graden rotatie van image
- width_shift_range=0.1 -> 
- height_shift_range=0.1,
- shear_range=0.2

Analyse:
- Convergeert niet te veel augmentation

## Run 4: 0.87
Netwerk veranderingen: 
- Data augmentation toegevoegd, dus er wordt nu gewerkt met generators. 
- rotation_range=5 -> 5 graden rotatie van image

Analyse:
- Veel minder overfitting, volgende run ook shear range toevoegen. Is een slecht idee, want vervormt te veel! Graden naar 10 aangepast

## Run 5: 0.81
Netwerk veranderingen: 
- rotation_range=10-> 10 graden rotatie van image

Analyse:
- Veel minder overfitting, volgende run ook shear range toevoegen. Is een slecht idee, want vervormt te veel! Graden naar 10 aangepast






