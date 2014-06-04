- modif the table of BLER/SNR used to match the umts values
- modif open_loop
    utiliser deux N de Friis different.
       => premier N = 1.4 pour calculer une puissance initial d'emission selon le vrai d
       =>deuxieme N = 1.3 pour calculer un deuxieme d theorique 
       =>deuxieme N pour calculer a partir du d theorique le emitted_power_to_reach
       
- outer loop :
    get le BLER depuis la table
    si le BLER > target du prof => augmente le BLER de la target du device concerne
    sinon                       => diminue
    
-inner loop :
    reutiliser la table BLER/SNR pour obtenir la target sur laquelle se basent les decisions   
