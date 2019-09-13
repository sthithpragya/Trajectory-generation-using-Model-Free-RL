function MM = computeMM_separately(a)
    N_mod = length(a);
    alpha = {};
    for j = 1:N_mod
        alpha{j} = a(j);
    end
    M = computeMxyga(alpha{:});
    R = computeR(alpha{:});
    MM=zeros(N_mod,N_mod);
    Mmod = zeros(N_mod,N_mod,N_mod);
    for i = 1:N_mod
        Mmod(:,:,i)=transpose(R(:,:,i))*M(:,:,i)*R(:,:,i); %Matrice d'inertie coordonn�e g�n�rale module i
        MM=MM+Mmod(:,:,i); %MM matrice d'inertie globale du syst�me
    end
    
    if true
        M_head = computeMxyg_head(alpha{:});
        R_head = computeR_head(alpha{:});
        MM = MM + transpose(R_head)*M_head*R_head; 
    end
    
end