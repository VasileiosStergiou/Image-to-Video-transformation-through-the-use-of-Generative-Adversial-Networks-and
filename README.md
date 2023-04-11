# Thesis

Στο ακόλουθο link παρατίθεται ο κώδικας της διπλωματικής εργασίας,
ο οποίος καταλαμβάνει περίπου 30 GB και είναι εξίσου διαθέσιμος στο μηχάνημα Stilvi.

https://drive.google.com/drive/folders/1XidhaCdE6KxBAHzdE4krhCdX1313bq87?usp=share_link


------------------------------------------------- Set up για εκτέλεση του κώδικα ----------------------------------
                        
Για την εκτέλεση του κώδικα υπάρχουν 2 επιλογές:
 
            Σύνδεση στο μηχάνημα Stilvi (Ενδείκνυται ύστερα από προσωπική χρήση)

   Η χρήση του παραπάνω μηχανήματος γίνεται με χρήση του προγράμματος Filezilla
   με την εισαγωγή των εξής στοιχείων
   
   Αφού γίνει η σύνδεση,ο χρήστης πρέπει να εργαστεί μέσω του Anaconda
   που υπάρχει εγκατεστημένο στο μηχάνημα, καθώς μέσω αυτού μπορεί να
   εγκαταστεί τοπικά τις απαραίτητες βιβλιοθήκες της Python
   
   Στη παρούσα διπλωματική εργασία, υπήρχε ήδη set up των απαραίτητων βιβλιοθηκών
   από προγενέστερη διπλωματική εργασία, οπότε ο χρήστης αρκεί να εκτελέσει την 
   εντολή *conda activate zagori*, με το όνομα *zagori* να αποτελεί το υπάρχον από ήδη
   υπάρχον set up. Έτσι, ο χρήστης μπορεί να εκτελέσει πλέον τον απαραίτητο κώδικα.
   
   
                Εκτέλεση σε προσωπικό υπολογιστή χωρίς σύνδεση στο μηχάνημα Stilvi
           
          
Εάν ο χρήστης επιθυμεί να εκτελέσει τον κώδικα στον προσωπικό του υπολογιστή,
πρέπει να εκτελέσει την ακόλουθη εντολή για να εγκαταστήσει τα packages στο Anaconda
    
          conda env create -f environment_animation.yml
    
Το .yml αρχείο υπάρχει τόσο στον κώδικα που παρατίθεται στο link,όσο και στον υπάρχοντα
κώδικα στον λογαριασμό του μηχανήματος Stilvi.
    
    
    
----------------------------------------------  Εντολές -----------------------------------------------



                      Α. Εκπαίδεση (Training)
                      
Για την εκπαίδευση του μοντέλου στα datasets, αρχικά πρέπει να γίνει το κατάλληλο import
στο αρχείο run.py του κώδικα, πρωτού αυτό εκπαιδευτεί στο αντίστοιχο dataset.

> import load_dataset_taichi για εκπαίδευση στα βίντεο του Τaichi datasset

> import load_dataset_fashion για εκπαίδευση στα βίντεο του Fashion dataset


Στη συνέχεια, γίνεται εκτέλεση των ακόλουθων εντολών, αφότου τερματήσει η τρέχουσα εκπαίδεση
(Training)


> CUDA_VISIBLE_DEVICES=0 python run.py --config config/taichi.yaml --device_ids 0

> CUDA_VISIBLE_DEVICES=0 python run.py --config config/fashion.yaml --device_ids 0



Ο κώδικας διαθέτει εκ των προτέρων το Logger module (αρχείο train.py), το οποίο παράγει αντίστοιχο παράγει
αρχείο .txt με τη πορεία των perceptual, feature matching, generator και discriminator error
που αφορούν την εκπαίδευση των δομών του μοντέλου. 
Για την εξαγωγή των αντίστοιχων plots υπάρχει αντίστοιχο script.




                      Β. Ανακατασκευή βίντεο (Reconstruction)

Για την ανακατασκευή των βίντεο που εξάγωνονται από το μοντέλο FOMM στα σύνολα Taichi και Fashion:
ΣΗΜΕΙΩΣΗ: Ο εκτιμώμενος χρόνος εξαγωγής των βίντεο κυμαίνεται μεταξύ 1.5 - 2 ωρών.

> CUDA_VISIBLE_DEVICES=0 python run.py --config config/taichi.yaml --mode reconstruction --checkpoint log/TAICHI/FULLMODEL/00000149-checkpoint.pth.tar --device_ids 0 

> CUDA_VISIBLE_DEVICES=0 python run.py --config config/fashion.yaml --mode reconstruction --checkpoint /home/vtagka/AlphaPose/MYANIME/log/FASHION/FULLMODEL/00000099-     checkpoint.pth.tar --device_ids 0

Για την εξαγωγή των αντίστοιχων bar plots υπάρχει αντίστοιχο script, όπως και για τα plots του training.
Η χρησιμότητα και ο τρόπος χρήσης των scripts που κατασκευάστηκαν εξηγείται στη παρακάτω ενότητα.

Στα *.yaml* αρχεία υπάρχουν σημαντικές παραμέτροι που αφορούν το μοντέλο, όπως για παράδειγμα:

> ο ρυθμός μάθησης (learing rate)

> οι εποχές εκπαίδευσης (epoches)

τις οποίες μπορεί να μεταβάλει ο χρήστης





------------------------------ Κώδικας για εξαγωγή απαραίτητων γραφικών παραστάσεων --------------------------------



       Γραφικές παραστάσεις για τα μεγέθη AED,L1 και SSIM μέσω του compare_plots.py

Για την εξαγωγή των συγκρίσεων μεταξύ της αρχικής τιμής και της νέας τιμής των μεγεθών μετά την
μετα-επεξεργασία των βίντεο, χρησιμοποιείται το αρχείο compare_plots.py με τον εξής τρόπο:

i. Αρχικά ο χρήστης μπορεί να δημιουργήσει ή να πάρει το ήδη έτοιμο directory "Results Post Poisson "
που παρατίθεται σε αυτό το Github repository. Μέσα σε αυτό υπάρχουν έτοιμες οι κατηγορίες αποτελεσμάτων
με την μορφή directories.

Π.χ το directory No_Poisson_Gauss προσδιορίζει ότι τα αποτελέσματα αυτά αφορούν την εφαρμογή μόνο Γκαουσιανού φίλτρου.
Για τα datasets Taichi και Fashion, που επίσης υπάρχουν με τη μορφή direcories.

> ΣΗΜΕΙΩΣΗ: Το script *compare_plots.py* πρέπει να είναι στο ίδιο μέρος με το "Results Post Poisson " για να τρέξει.

ii. Οι μετρικές εξάγωνται και αποθηκεύονται σε αντίστοιχα αρχεία .txt, 
μέσω του κώδικα που έχει προστεθεί στο αρχείο reconstruction.py.

ΣΗΜΕΙΩΣΗ: τα .txt που δεν φέρουν τη κατάληξη "_poisson" 
πρόκεινται για τις αρχικές τιμές των μετρικών, δηλαδή χωρίς την εφαρμογή μετασχηματισμών. 

> AED_per_video

> aed_per_video_poisson



> L1_per_video

> L1_per_video_poisson


> ssims

> ssims_poisson


Ο χρήστης, στη συνέχεια, πρέπει να τα μεταφέρει στο κατάλληλο fashion ή taichi directory,
ανάλογα με τους μετασχηματισμούς που έχει εφαρμώσει στα βίντεο.

iii. Με την εκτέλεση python compare_plots.py δημιουργούνται τα κατάλληλα directories
που περιέχουν τα bar plots για καθεμία από τις συγκρίσεις.

     Γραφικές παραστάσεις για τα perceptual,feature_matching,generator-discriminator error μέσω του plots.py
     
Αφότου εκπαιδευτεί το μοντέλο FOMM, στο directory που βρίσκεται το αρχείο run.py εξάγεται ένα αρχείο log_''.txt,
στο οποίο η κατάληξη του είναι αυτή του πιο πρόσφατου dataset στο οποίο εκπαιδεύτηκε.
Στο αρχείο αυτό καταγράφονται οι τιμές των  perceptual,feature_matching,generator-discriminator error, χωρισμένες με κόμμα.

Ο κώδικας του *plots.py*  διαβάζει από το log αρχείο και εξάγει τις γραφικές παραστάσεις, στις οποίες εφαρμώζεται παράλληλα
curve fitting, προκειμένου να είναι πιο ακριβής η προσέγγιση του σφάλματος εκπαίδευσης στις εποχές.