library(plotly)
library(dplyr)

f <- function(x){return(1/(1+exp(-x)))}
fprime <- function(x){return(f(x)*(1-f(x)))}
loss <- function(t,y){return(0.5*(t-y)^2)}

data <- matrix(c(0,0,0,0,1,0,1,0,0,1,1,1), nrow = 4, byrow = TRUE)
inputs <- data[,-3]
targets <- data[,3]

W <- matrix(rep(seq(2.5, 8.5, 0.01), 2), nrow = 601, ncol=2)
err_v <- matrix(nrow = 601, ncol = 601)
for (i in 1:nrow(W)){
  err <- c()
  for (k in 1:nrow(W)){
    w <- c(W[i, 1], W[k, 2])
    for (n in 1:nrow(inputs)){
      z <- c(w, 8.314263) %*% c(inputs[n,], -1)
      y <- f(z)
      err[n] <- loss(targets[n],y)
    }
    err_v[i, k] <- mean(err)
    
  }
}

fig <- plot_ly(x = W[,1], y = W[,2], z = err_v, scene = list(
  xaxis = list(title = "w1"),
  yaxis = list(title = "w2"),
  zaxis = list(title = "error")
)) %>% add_surface()

api_create(fig, filename = "error_sruface")


