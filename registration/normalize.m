function normPoints = normalize(Points)

pmean = mean(Points);

pmin = min(Points);
pmax = max(Points);
denom = max(pmax-pmin);
rows = size(Points,1);
mmean = repmat(pmean, rows,1);
normPoints = (Points-mmean)/denom;

