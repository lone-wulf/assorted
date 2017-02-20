function plotmesh(sourceV, sourceF, targetV, targetF)
sF = sourceF;
sV = sourceV;

if (nargin<3)
    targetV = sV;
    targetF = sF;
end
trisurf(sF,sV(:,1),sV(:,2),sV(:,3), 'FaceColor', 'cyan','FaceAlpha', 0.8);
%plot of the meshes
h=trisurf(sF,sV(:,1),sV(:,2),sV(:,3),0.3,'Edgecolor','none');
hold
light
lighting phong;
set(gca, 'visible', 'off')
set(gcf,'Color',[1 1 0.88])
view(90,90)
set(gca,'DataAspectRatio',[1 1 1],'PlotBoxAspectRatio',[1 1 1]);
tttt=trisurf(targetF,targetV(:,1),targetV(:,2),targetV(:,3),'Facecolor','m','Edgecolor','none');
alpha(0.5)