clc
clear all

[sourceV, sourceF] = read_ply('Source_1.ply');
[targetV, targetF] = read_ply('Template_1.ply');

tV = targetV;
[sourceV,sourceF] = preprocessSource(sourceV, sourceF);
[targetV,targetF] = preprocessTarget(targetV, targetF);

figure(1)
[scenter, sradii, sevecs,sv, schi2] = fit_ellipsoid(sourceV,sourceF);
figure(1),
[tcenter, tradii, tevecs, tv, tchi2] = fit_ellipsoid(targetV,targetF);
tevecs = tevecs';
sevecs = sevecs';
R = sevecs\tevecs;
s1 = sourceV-repmat(mean(sourceV),size(sourceV,1),1);
transV = s1*R + repmat(mean(targetV),size(sourceV,1),1);

radS = mean(sourceV) - scenter';
radV = mean(targetV) - tcenter';

T = diag(sign(radV./radS));
transV = transV*T;

%[transV,targetpV]=Preall(targetV,transV,);
%figure(3),
%[tcenter, tradii, tevecs, tv, tchi2] = fit_ellipsoid(transV,sourceF);

mn = mean(tV);
transV = normalize(transV);
Maxtarget=max(tV)-min(tV);
Maxsource=max(transV)-min(transV);
D=Maxtarget./Maxsource;
D=[D(1,1) 0 0;0 D(1,2) 0; 0 0 D(1,3)];
transV=transV*D;
transV = transV + repmat(mn, size(transV,1),1);
tv = transV(1:100:end,:);
figure(2),
[tcenter, tradii, tevecs, tv, tchi2] = fit_ellipsoid(transV,sourceF);

write_ply(transV, sourceF,'registered.ply');