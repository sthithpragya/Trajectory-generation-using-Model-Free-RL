function [F1,F2] = compute_forces(N_mod,alpha,alphaddot,b,L,Fmin)

    M = computeMM_separately(alpha);

    alpha_cell = {};
    for j = 1:N_mod
        alpha_cell{j} = alpha(j);
    end

    G = computeGG(alpha_cell{:});

    Q = M*alphaddot + G;%torque to produce

    for j = 1:N_mod%computation of the forces to apply
        Z1 = Z1_func(alpha(j),b(j),L(j));
        Z2 = Z2_func(alpha(j),b(j),L(j));

        if Q(j) >= (Z1+Z2)*Fmin
             fr = Fmin;
             fl = (Q(j) - Z2*Fmin)/Z1;
        else
             fl = Fmin;
             fr = (Q(j) - Z1*Fmin)/Z2;
        end
        F1(j) = fl;
        F2(j) = fr;

    end
end
            