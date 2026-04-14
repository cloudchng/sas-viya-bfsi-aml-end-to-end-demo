package stage_5_prioritization / inline;
    /*
      SAS Viya AML Multi-Layered Shield: Phase 5 Prioritization
      This script calculates a weighted Global Alert Value to reduce noise.
    */
    method execute(
        double EM_EVENTPROBABILITY,
        char is_pep,
        char country_risk_level,
        double amount,
        double turnover_ratio,
        in_out double Global_Alert_Value,
        in_out char Alert_Priority
    );
        dcl double base_score;
        dcl double risk_additives;

        /* 1. Model Contribution (Max 50 points) */
        /* Note: Scale model probability to a 0-50 range.
           EM_EVENTPROBABILITY = Propability of Suspicious (Target=1). */
        base_score = EM_EVENTPROBABILITY * 50;

        /* 2. Risk Overlays (Additives) */
        risk_additives = 0;

        /* PEP Match (+25) */
        if (trim(is_pep) = 'High' or trim(is_pep) = 'YES') then risk_additives = risk_additives + 25;

        /* High Risk Country (+25) */
        if (trim(country_risk_level) = 'High') then risk_additives = risk_additives + 25;

        /* High Turnover Ratio (> 0.7 indicates suspicious activity relative to profile) (+15) */
        if (turnover_ratio > 0.7) then risk_additives = risk_additives + 15;

        /* High Amount Outlier (> 100k) (+10) */
        if (amount > 100000) then risk_additives = risk_additives + 10;

        /* 3. Final Calculation */
        Global_Alert_Value = base_score + risk_additives;

        /* Cap at 100 */
        if (Global_Alert_Value > 100) then Global_Alert_Value = 100;

        /* 4. Priority Assignment (Fixed Hierarchy & Thresholds) */
        if (Global_Alert_Value >= 85) then
            Alert_Priority = 'URGENT';
        else if (Global_Alert_Value >= 65) then
            Alert_Priority = 'High';
        else if (Global_Alert_Value >= 45) then
            Alert_Priority = 'Medium-High';
        else if (Global_Alert_Value >= 25) then
            Alert_Priority = 'Medium';
        else
            Alert_Priority = 'Low'; /* Noise reduction baseline */

        /* Logic for "Noise Reduction" is now handled in the priority else block above */
    end;
endpackage;
