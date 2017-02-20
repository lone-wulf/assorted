function [tV,tF] = preprocessTarget(sourceV,sourceF)

x = sourceV(:,1);
xc = mean(x);
xdev = (max(x)-min(x))/2;
xii = x-x+1;% < (xc+ xdev);

y = sourceV(:,2);
yc = mean(y);
ydev = (max(y)-min(y))/2;
yii = (y < (yc + (0.8*ydev))).* (y > (yc-0.8*ydev));

z = sourceV(:,3);
zc = mean(z);
zdev = 0.15*(max(z)-min(z));
zii = z > zc - zdev;

ind = (xii.*yii.*zii)==1;
[tV,tF] = removePoints(sourceV,sourceF, ind);
tV = normalize(tV);