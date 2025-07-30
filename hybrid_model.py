import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
from deap import base, creator, tools, algorithms
import random


class HybridSalesPredictor:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.model = None
        self.best_params = None

    def _fuzzy_preprocess(self, X):
        """Fuzzy logic feature engineering"""
        X = X.copy()
        # Fuzzy rules for feature enrichment
        X['price_demand'] = np.where(
            X['price'] < X['price'].median(),
            np.sqrt(X['price_max'] - X['price']),
            np.log(X['price'] + 1)
        )
        X['promo_effect'] = np.where(
            X['promotion'] > 0,
            X['promotion'] * 1.5,
            X['seasonality'] * 0.8
        )
        return X

    def train(self, X, y):
        # Fuzzy preprocessing
        X = self._fuzzy_preprocess(X)
        X = self.scaler.fit_transform(X)

        # Genetic Algorithm optimization
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()
        toolbox.register("attr_float", random.uniform, 0.001, 0.1)  # learning rate
        toolbox.register("attr_int", random.randint, 5, 50)  # hidden layers
        toolbox.register("individual", tools.initCycle, creator.Individual,
                         (toolbox.attr_float, toolbox.attr_int), n=1)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("mate", tools.cxBlend, alpha=0.5)
        toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
        toolbox.register("select", tools.selTournament, tournsize=3)

        def evaluate(individual):
            lr, layers = individual[0], int(individual[1])
            model = MLPRegressor(
                hidden_layer_sizes=(layers,),
                learning_rate_init=lr,
                max_iter=500,
                early_stopping=True
            )
            model.fit(X[:800], y[:800])  # 80% training
            return (model.score(X[800:], y[800:]),  # 20% validation

                    toolbox.register("evaluate", evaluate)

                    pop = toolbox.population(n=15)
            algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=10, verbose=False)

            # Get best individual
            best = tools.selBest(pop, k=1)[0]
            self.best_params = {
                'learning_rate': best[0],
                'hidden_layers': int(best[1])
            }

            # Train final model
            self.model = MLPRegressor(
                hidden_layer_sizes=(self.best_params['hidden_layers'],),
                learning_rate_init=self.best_params['learning_rate'],
                max_iter=2000,
                early_stopping=True
            )
            self.model.fit(X, y)

    def predict(self, X):
        X = self._fuzzy_preprocess(X)
        X = self.scaler.transform(X)
        return self.model.predict(X)