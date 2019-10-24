import os
import time

def ustvari_razrede():
	with open("pot_do_mape_za_test.txt","r") as f:
		pot = f.read()  # dejansko pot do mape za test shrani v spremenljivko "pot"
	razredi = []
	for razred in os.listdir(pot):
		razredi.append(razred)  # v seznam "razredi" dodaj imena vseh podmap v mapi za test
	return razredi

def pripravi_test_datoteke(razredi):
	if not os.path.isdir("./batch"):
		os.mkdir("batch")  # ce mapa ne obstaja, jo ustvari
	if not os.path.isdir("./rezultati_testiranj"):
		os.mkdir("rezultati_testiranj")  # ce mapa ne obstaja, jo ustvari
	with open("pot_do_label_image.txt","r") as f:
		label_image = f.read()  # pot do datoteke "label_image.py" shrani v "label_image"
	with open("pot_do_mape_z_modelom.txt","r") as f:
		model = f.read()  # pot do mape "tmp", ki vsebuje model
	pot_graf = model.strip() + "/output_graph.pb"  # pot do modela shrani v "pot_graf"
	pot_oznake = model.strip() + "/output_labels.txt"  # pot do oznak shrani v "pot_oznake"
	with open("pot_do_mape_za_test.txt","r") as f:
		pot = f.read()  # pot do mape za test shrani v spremenljivko "pot"
	poti = []
	for a in os.listdir(pot):
		poti.append(os.path.join(pot, a))  # pot vsake podmape v mapi za test dodaj na seznam: "poti"

	# Za vsak razred naredi .bat datoteko, ki bo testirala vse slike v tem razredu
	for k, r in enumerate(razredi):
		sablona = open("sablona.txt", 'r')  # preberi sablono, in v njej spremeni kar je potrebno (glede na razred)
		vrste = []
		for v in sablona:
			v = v.replace("RAZRED", r.strip())  # v sabloni zamenjaj "RAZRED" s trenutnim razredom
			v = v.replace("POT", poti[k])  # v sabloni zamenjaj "POT" s trenutno potjo do razreda
			v = v.replace("LABEL", label_image)  # v sabloni zamenjaj "LABEL" s potjo do datoteke "label_image.py"
			v = v.replace("GRAF", pot_graf)  # v sabloni zamenjaj "GRAF" s potjo do modela
			v = v.replace("OZNAKE", pot_oznake)  # v sabloni zamenjaj "OZNAKE" s potjo do datoteke z oznakami v mapi "tmp"
			vrste.append(v)  # vse vrstice iz sablone s spremembami pripni v seznam "vrste"
		sablona.close()
		file = f"Test_{r}".strip()+".bat"  # ustvari ime za posamezno .bat datoteko
		dat = open(file, 'w')
		for i in vrste:
			dat.write(i)  # vsako vrstico iz seznama "vrste" prepisi v .bat datoteko
		dat.close()
		vrste = []  # izprazni seznam "vrste"
		os.rename(f"./{file}", f"./batch/{file}")  # .bat datoteka se prestavi v mapo "batch"

def testiraj():
	# za vsako .bat datoteko naredi:
	for i in os.listdir("./batch"):
		program = os.path.join("./batch", i)  # definiraj pot do .bat datoteke
		os.startfile(program)  # zazeni posamezno .bat datoteko


pripravi_test_datoteke(ustvari_razrede())
time.sleep(1)
testiraj()
