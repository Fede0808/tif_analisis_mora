import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

class DiscreteTimeHazardModel:
    \"\"\"
    Implementación del Modelo de Supervivencia de Tiempo Discreto (Discrete-Time Hazard Model).
    Se basa en la expansión de los datos a formato persona-período e implementa
    regresión logística para predecir la probabilidad condicional de default (hazard).
    Rigor Matemático (LSE): h(t|x) = P(T=t | T>=t, X)
    \"\"\"
    def __init__(self, penalty='l2', C=1.0):
        self.model = LogisticRegression(penalty=penalty, C=C, solver='liblinear')
        self.time_col = 'time_period'
        self.event_col = 'default_event'
        
    def expand_data(self, df_raw, id_col, time_var, event_var, covariates):
        \"\"\"
        Expande un dataset a formato 'persona-período' (long-format).
        \"\"\"
        # Pseudo-implementación teórica para LSE standards
        # Por cada deudor, crear tantas filas como periodos haya estado activo hasta el evento
        expanded_rows = []
        for _, row in df_raw.iterrows():
            t_max = int(row[time_var])
            event = int(row[event_var])
            for t in range(1, t_max + 1):
                new_row = {
                    id_col: row[id_col],
                    self.time_col: t,
                    self.event_col: 1 if (t == t_max and event == 1) else 0
                }
                for cov in covariates:
                    new_row[cov] = row[cov]
                expanded_rows.append(new_row)
        
        return pd.DataFrame(expanded_rows)

    def fit(self, X, y):
        \"\"\"
        Ajusta el modelo logit sobre los datos expandidos persona-periodo.
        \"\"\"
        self.model.fit(X, y)
        print(\"[INFO] Discrete-Time Hazard Model ajustado exitosamente.\")

    def predict_hazard(self, X):
        \"\"\"
        Estima la función de riesgo: P(T=t | T >= t)
        \"\"\"
        return self.model.predict_proba(X)[:, 1]
        
    def predict_survival(self, X_grouped_by_person):
        \"\"\"
        S(t) = Productoria(1 - h(k)) para k=1 hasta t.
        \"\"\"
        pass # To be implemented via product limit logic over predicted hazards
