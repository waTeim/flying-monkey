module kalman;
import StateSpace;
import Distributions;

export newModel,initialGuess,predict,update,extractMeanFromState,extractVarianceFromState;

function initialGuess(observations::Array{Float64,1},varianceEstimate::Array{Float64,1})
   return Distributions.MvNormal(copy(observations),copy(varianceEstimate))
end

function newModel(processVariance::Float64,observationVariance::Float64)
   M_p::Matrix{Float64} = eye(3);
   M_v::Matrix{Float64} = eye(3)*processVariance;
   O_p::Matrix{Float64} = eye(3);
   O_v::Matrix{Float64} = eye(3)*observationVariance;

   return StateSpace.LinearGaussianSSM(M_p,M_v,O_p,O_v);
end

function update(model,predictedState,observations)
   return StateSpace.update(model,predictedState,copy(observations));
end

function predict(model,state)
   return StateSpace.predict(model,state)
end

function extractMeanFromState(state)
   return Distributions.mean(state)
end

function extractVarianceFromState(state)
   return Distributions.var(state)
end

end