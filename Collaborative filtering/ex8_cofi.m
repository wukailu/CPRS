%% Machine Learning Online Class
%  Exercise 8 | Anomaly Detection and Collaborative Filtering
%
%  Instructions
%  ------------
%
%  This file contains code that helps you get started on the
%  exercise. You will need to complete the following functions:
%
%     estimateGaussian.m
%     selectThreshold.m
%     cofiCostFunc.m
%
%  For this exercise, you will not need to change any code in this file,
%  or any other files other than those mentioned above.
%

%% ================== Part 7: Learning Movie Ratings ====================
%  Now, you will train the collaborative filtering model on a movie rating 
%  dataset of 1682 movies and 943 users
%

num_features = 20;%might be changed
pX=[];
pY=[];
pYval=[];
eps = 0.3;% error allowed
for lambda = 0:5:100 

fprintf('\nTraining collaborative filtering with lambda = %d... \n',lambda);

%  Load data
load ('final.mat');
Y = Y';
R = R';
Yval = Yval';
Ytest = Ytest';
Rval = Rval';
Rtest = Rtest';
Y(R==1) += 0.01;
Y(R==1) = log(Y(R==1));
Yval(Rval==1) += 0.01;
Yval(Rval==1) = log(Yval(Rval==1));

fprintf('checking data');
pos = find(R == 1);
fprintf('min value = %.5f', min(Y(pos)) );

%  Y is a 1682x943 matrix, containing ratings (1-5) of 1682 movies by 
%  943 users
%
%  R is a 1682x943 matrix, where R(i,j) = 1 if and only if user j gave a
%  rating to movie i

%  Normalize Ratings
%[Ynorm, Ymean] = normalizeRatings(Y, R);
Ynorm = Y;

%  Useful Values
num_users = size(Y, 2);
num_movies = size(Y, 1);

% Set Initial Parameters (Theta, X)
X = randn(num_movies, num_features);
Theta = randn(num_users, num_features);

initial_parameters = [X(:); Theta(:)];

% Set options for fmincg
options = optimset('GradObj', 'on', 'MaxIter', 100);

% Set Regularization
theta = fmincg (@(t)(cofiCostFunc(t, Ynorm, R, num_users, num_movies, ...
                                num_features, lambda)), ...
                initial_parameters, options);

% Unfold the returned theta back into U and W
X = reshape(theta(1:num_movies*num_features), num_movies, num_features);
Theta = reshape(theta(num_movies*num_features+1:end), ...
                num_users, num_features);

fprintf('Recommender system learning completed.\n');

%% ================== Part 8: Recommendation for you ====================
%  After training the model, you can now make recommendations by computing
%  the predictions matrix.
%

p = X * Theta';

pX = [pX lambda];

ratio = sum(sum( (((p>Y*(1-eps))&(p<Y*(1+eps)))|(abs(exp(Y)-exp(p))<=2) )(R==1) )) / sum(sum( R==1 ));
pY = [pY ratio];

ratio = sum(sum( (((p>Yval*(1-eps))&(p<Yval*(1+eps)))|(abs(exp(Yval)-exp(p))<=2) )(Rval==1) )) / sum(sum( Rval==1 ));
pYval = [pYval ratio];

end

plot(pX,pY,pX,pYval);
% save('result.mat','p','X','Theta');

% 50 feature lambda 23  92.25%/64.70%
% 30 feature lambda 15  91.56%/67.40%