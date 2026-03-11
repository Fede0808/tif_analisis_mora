import torch
import torch.nn as nn

class TraCeR(nn.Module):
    \"\"\"
    TraCeR (Trajectory-based Clustering and Representation) Architecture.
    Basado conceptualmente en la arquitectura de arXiv orientada a capturar
    covariables longitudinales para modelos dinámicos (como riesgo crediticio).
    
    Estructura LSE-Standard:
    1. Temporal Encoder (RNN/LSTM o Temporal Convolutions)
    2. Representation Space (Latent Embedding)
    3. Hazard Classifier (Fully Connected) -> h(t)
    \"\"\"
    def __init__(self, input_dim, hidden_dim=64, latent_dim=32, num_layers=2):
        super(TraCeR, self).__init__()
        
        # 1. Temporal Encoder
        # Procesa la serie temporal de estados del deudor (Situaciones 1-6)
        self.lstm = nn.LSTM(
            input_size=input_dim, 
            hidden_size=hidden_dim, 
            num_layers=num_layers,
            batch_first=True
        )
        
        # 2. Latent Representation Space
        self.fc_latent = nn.Linear(hidden_dim, latent_dim)
        self.relu = nn.ReLU()
        
        # 3. Hazard Head
        # Mapea el vector latente a la probabilidad de default del siguiente periodo
        self.hazard_head = nn.Sequential(
            nn.Linear(latent_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid() # Output: h(t | X_hist)
        )

    def forward(self, x):
        \"\"\"
        Forward pass de TraCeR con datos longitudinales.
        x form shape: (batch_size, sequence_length, features)
        \"\"\"
        # Entrenando el Temporal Encoder
        # lstm_out shape: (batch_size, seq_len, hidden_dim)
        lstm_out, (h_n, c_n) = self.lstm(x)
        
        # Tomando el ultimo estado oculto secuencial (o pooling general) para el instante t
        # Para predicciones dinamicas a cada tiempo t, podríamos usar todo lstm_out
        # Aquí simplificamos usando la representación del instante final (o último evento)
        last_hidden = lstm_out[:, -1, :] 
        
        # Espacio Latente (Clustering / embedding space en un full TraCeR paper)
        latent_repr = self.relu(self.fc_latent(last_hidden))
        
        # Predicción de Riesgo
        hazard_prob = self.hazard_head(latent_repr)
        
        return hazard_prob, latent_repr
