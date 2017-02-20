function [sV,sF] = preprocessSource(sourceV,sourceF)

%sourceV = normalize(sourceV);
x = sourceV(:,1);
xc = mean(x);
xdev = 0.60*(max(x)-min(x))/2;
xii = abs(x-xc) < xdev; 

y = sourceV(:,2);
yc = mean(y);
ydev = (max(y)-min(y))/2;
yii = (y < (yc + (0.40*ydev))).* (y > (yc-0.6*ydev)) ; 

z = sourceV(:,3);
zc = mean(z);
zdev = (max(z)-min(z))/2;
zii = z-zc < 0.4*zdev; 

ind = (xii.*yii.*zii)==1;
[sV,sF] = removePoints(sourceV,sourceF, ind);
sV = normalize(sV);