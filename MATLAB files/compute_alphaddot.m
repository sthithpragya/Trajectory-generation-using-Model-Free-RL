function alphaddot = compute_alphaddot(N_mod,alpha,F1,F2,b,L)

    M = computeMM_separately(alpha);

    alpha_cell = {};
    for j = 1:N_mod
        alpha_cell{j} = alpha(j);
    end

    G = computeGG(alpha_cell{:});
    
    Q_forces = zeros(N_mod,1);
    for j = 1:N_mod%computation of the forces to apply
        Z1 = Z1_func(alpha(j),b(j),L(j));
        Z2 = Z2_func(alpha(j),b(j),L(j));
        
        Q_forces(j) = Z1*F1(j) + Z2*F2(j);
    end
    
    alphaddot = inv(M)*(Q_forces - G);
    
end
            