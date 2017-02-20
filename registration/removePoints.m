function [sV,sF] = removePoints(sourceV,sourceF, ind)

kk = cumsum(ind);
sf = sourceF(all(ind(sourceF),2),:);
sV = sourceV(ind,:);
sF = kk(sf);