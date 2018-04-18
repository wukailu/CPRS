%% ================== Part 4: Multidimensional Outliers ===================
%  We will now use the code from the previous part and apply it to a 
%  harder problem in which more features describe each datapoint and only 
%  some features indicate whether a point is an outlier.
%

%  Loads the second dataset. You should now have the
%  variables X, Xval, yval in your environment
clear;
load('CF.mat');
X = log(value+0.01);
R = has_value;

%  Apply the same steps to the larger dataset
[mu sigma2] = estimateGaussian(X,R);

%  Training set 
p = multivariateGaussian(X, mu', sigma2');



epsilon = 0.05

fprintf('# Outliers found with eps = %.2f: %d\n\n', epsilon, sum(p(R==1) < epsilon));

has_value &= p >= epsilon;

save("-mat","clean.mat","has_value","value","problems","users");