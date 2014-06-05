- outer loop :
    get le BLER depuis la table
    si le BLER > target du prof => augmente le BLER de la target du device concerne
    sinon                       => diminue
    
-inner loop :
    reutiliser la table BLER/SNR pour obtenir la target sur laquelle se basent les decisions
    
    
-open loop :
    # We use the N = 1.3 because of the high Ep of the nodeB which allow the signal to cross
    # obstacles therefore to have a lower distance to the UE
    # Computation of the measured power at the UE
    RxLevNodeB = EpNodeB + Gue + GnodeB - ( 20 log10(2200) + 20 * 1.4 * log10(d1) -27.55)
    
    # from RxLevNodeB and EpNodeB we deduce a new d=d2 based on fsl with n = 1.3
    
    20 * 1.3 * log10(d2) = EpNodeB + Gue + GnodeB - 20 * log10(2200) + 27.55
    log10(d2) = (-RxLevNodeB + EpNodeB + Gue + GnodeB - 20 * log10(2200) + 27.55) / (20 * 1.3)
    d2 = 10**( (-RxLevNodeB + EpNodeB + Gue + GnodeB - 20 * log10(2200) + 27.55) / (20 * 1.3) )
            
    # At the NodeB in UL we receive
    emitted_power_to_reach = NodeBSensitivity - Gue - GnodeB + ( 20 * log10(2200) + 20 * 1.3 * log10(d2) - 27.55)
    # The initial EpUe computation 
    EpUe_init = NodeBSensitivity - Gue - GnodeB + ( 20 * log10(2200) + 20 * 1.3 * log10(d1) - 27.55)
    
    # At this point EpUe_init should be lower than emitted_power to reach


    # validation example :
    # lets consider a device located at 60 meters of distance from the NodeB
    # => d1 = 60
    RxLevNodeB = 50 + 0 + 0 - ( 20log10(2200) - 20*1.4*log10(60) - 27.55)
    RxLevNodeB = -39 dBm
    
    d2 = 10**( (20 + 0 +0 - 20log10(2200) + 27.55) / (20*1.3) )
    d2 = 81.58 m
    
    EpUe_init = -100 + 0 + 0 + ( 20*log10(2200) + 20*1.3*log10(60) - 27.55)
    EpUe_init = -14 dBm
    
    emitted_power_to_reach = -100 + 0 + 0 + ( 20*log10(2200) + 20*1.3*log10(82) - 27.55 )
    emitted_power_to_reach = -11 dBm
    
    # We can see the difference between the initial Ep computed by the UE and the real one
