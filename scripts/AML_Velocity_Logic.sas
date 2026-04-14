package stage_1_velocity / inline;
    /*
      SAS Viya AML Multi-Layered Shield: Phase 1 Velocity Logic
      Flag if transaction consumes > 70% of expected monthly turnover.
    */
    method execute(double turnover_ratio, in_out double velocity_flag);
        if (turnover_ratio > 0.7) then velocity_flag = 1;
        else velocity_flag = 0;
    end;
endpackage;
