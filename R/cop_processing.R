# cop_processing.R
suppressWarnings(require(signal))

# --- 1. Definir parâmetros de cada ensaio -----------------
duration.s     <- c(60)
sampling.freq  <- c(100)

# --- 2. Garantir índices válidos ---------------------------
trial <- 1

# --- 3. Ajuste da duração ---------------------------------
n.desired <- min(length(X), duration.s[trial] * Fs)
X <- X[1:n.desired]
Y <- Y[1:n.desired]
time <- time[1:n.desired]

# --- 4. Centralização e remoção de tendência ---------------
X <- X - mean(X, na.rm = TRUE)
Y <- Y - mean(Y, na.rm = TRUE)
X <- residuals(lm(X ~ time))
Y <- residuals(lm(Y ~ time))
