%% FUNCTION Z2
% This matlab function returns value of Z2 for a given angle alpha. Z2 is 
% part of the equation of motion and is the coefficient in front of F2.
%
% input:
% - [rad] alpha
% - constants (module parameters)
% output: 
% - [] Z2
% 
% Creator: Anders van Riesen (a.vanriesen@student.utwente.nl)
% Created: 10-12-2017
% Last edited: 10-12-2017

function Z2 = Z2_func(alpha,b,L)
    
%     
%     % determine other variables
%     phi = phi_func(N_mod,alpha,constants);
%     l2 = l2_func(N_mod,alpha,constants);
%     S2 = S2_func(N_mod,alpha,constants);

    if alpha==pi
        psi=pi;
    elseif alpha==-pi
        psi=-pi;
    else
    % substitution functions f
        f1 = 2*b*L*sin(alpha);
        f2 = 2*b*L*(cos(alpha)+1);
        f3 = 2*b^2*(cos(alpha)+1);
        psi = 2*atan((-f1 - sqrt(f1.^2+f2.^2-f3.^2))./(f3-f2));
    end
    
    if alpha==pi
        phi=pi;
    elseif alpha==-pi
        phi=-pi;
    else
        % substitution functions g
        g1 = -2*b*L*sin(alpha);
        g2 = -2*b*L*(cos(alpha)+1);
        g3 = 2*b^2*(cos(alpha)+1);
        phi = 2*atan2(-g1 + sqrt(g1.^2+g2.^2-g3.^2),g3-g2);
    end

    S2 = b*sin(psi-alpha)./(L*sin(psi-phi));
    l2 = sqrt(b^2 + L^2 - 2*b*L*cos(phi));
%         
%     % determine Z1
    Z2 = -b*L*sin(phi)./l2.*S2;
   
end