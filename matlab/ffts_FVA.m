%testar FFT

function [frq_mefx,frq_mefy] = ffts_FVA(x,y,fs,cor);

%  y=Ankle_ML;
%  fs=1000;

T = 1/fs; % T = dt = time increment

%remove trend and mean value of data y
aa = detrend(y,0);

%discrete Fourier transform (DFT) of vector aa;
Z = fft (aa,length(aa)); %length(aa) is the N-point fft

% Calculating the magnitude of the fft
%For a complex vector Z, Z.*conj(Z) is the same as (abs(Z)).^2. That is, multiplying a complex number by its conjugate gives you the magnitude squared.
Pyy1 = Z.*conj (Z); %multiplies Z by its complex conjugate; 

% scale the fft 
Pyy = Pyy1*T/length(aa); 

%normalized power 
Pyyn= Pyy/(max(Pyy)); 

% evently spaced frequency vector with NumUniqePts points
g1 = (0:1/(T*length(Pyy)):2);
%g1 length is up to 5 because fft is symmetric and so, the last part of
%signal was cutted, because it contains the same content frequencies

% figure
% NumUniquePts = ceil(1+length(Pyy)/2);
% % evently spaced frequency vector with NumUniqePts points
% g1 = (0 : NumUniquePts-1)*fs/length(Pyy); % frequency vector
% 
% subplot(212),plot(g1,Pyyn(1:length(g1)),'g'),grid on,hold on, ylabel('pot. norm')
% %subplot(211),plot((1:length(y))./fs,y),hold on
% title('sinal (tempo)')

% since FFT is symmetric through away second half of fft
gg = (0:1/(T*length(Pyy)):fs/2); 

P = Pyyn(1:length(gg));         % potência de 0 até frequência de Nyquist
frq_mefy= sum(gg.*P)./sum(P);        % frequência média


bb = detrend(x,0);


Zb = fft (bb,length(bb));
Pxx = Zb.*conj (Zb);
Pxx = Pxx*T/length(bb);
Pxxn= Pxx/(max(Pxx));

% subplot(212),plot (g1,Pxxn(1:length(g1)),'b'),grid on,hold on, ylabel('PSD (normalized to the maximum)')
% xlabel('Frequency [Hz]'),title('FFT'), legend('can2','can1')
% subplot(211),plotyy((1:length(x))./fs,detrend(x),(1:length(y))./fs,detrend(y));

% % [hAx,hLine1,hLine2]=plotyy...
% % ylim(hAx(1),[mean(x)-2 mean(x)+2]) % left y-axis
% % ylim(hAx(2),[mean(y)-2 mean(y)+2]) % right y-axis

%title('sinal')


PP = Pxxn(1:length(gg));         % potência de 0 até frequência de Nyquist
frq_mefx= sum(gg.*PP)./sum(PP);        % frequência média

%close

