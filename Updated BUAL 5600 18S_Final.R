# ============ Question 1 ============
# Package
library(gpairs)
library("leaps")

data(state)
state1<-data.frame(state.x77,row.names=state.abb,check.names=T)
summary(state1)

# Part 1
gpairs(state1)

# Part 2
full<-lm(Life.Exp~., data=state1)
summary(full)

# Part 3
# Accessing a best subset model using original data
best.subset <- regsubsets(Life.Exp~., data=state1)
best.subset.summary <- summary(best.subset)
best.subset.by.adjr2 <- which.max(best.subset.summary$adjr2)
best.subset.by.cp <- which.min(best.subset.summary$cp)
best.subset.by.bic <- which.min(best.subset.summary$bic)

# Create plots for choosing the best model
par(mfrow=c(2,2))
plot(best.subset$rss, xlab="Number of Variables", ylab="RSS", type="l")
plot(best.subset.summary$adjr2, xlab="Number of Variables", ylab="Adjusted RSq", type="l")
points(best.subset.by.adjr2, best.subset.summary$adjr2[best.subset.by.adjr2], col="red", cex =2, pch =20)
plot(best.subset.summary$cp, xlab="Number of Variables", ylab="CP", type="l")
points(best.subset.by.cp, best.subset.summary$cp[best.subset.by.cp], col="red", cex =2, pch =20)
plot(best.subset.summary$bic, xlab="Number of Variables", ylab="BIC", type="l")
points(best.subset.by.bic, best.subset.summary$bic[best.subset.by.bic], col="red", cex =2, pch =20)

# Part 4
# Accessing a best subset model using logged data
best.subset1 <- regsubsets(Life.Exp~log(Population+1)+Income+log(Illiteracy+1)+Murder+HS.Grad+Frost+log(Area+1), data=state1)
best.subset.summary1 <- summary(best.subset1)
summary(best.subset1)
best.subset1.by.adjr2 <- which.max(best.subset.summary1$adjr2)
best.subset1.by.cp <- which.min(best.subset.summary1$cp)
best.subset1.by.bic <- which.min(best.subset.summary1$bic)

### Now, I put the maximum number of predictor=5, Please change the 'nvmax'.
par(mfrow=c(2,2))
plot(best.subset1$rss, xlab="Number of Variables", ylab="RSS", type="l")
plot(best.subset.summary1$adjr2, xlab="Number of Variables", ylab="Adjusted RSq", type="l")
points(best.subset1.by.adjr2, best.subset.summary1$adjr2[best.subset1.by.adjr2], col="red", cex =2, pch =20)
plot(best.subset.summary1$cp, xlab="Number of Variables", ylab="CP", type="l")
points(best.subset1.by.cp, best.subset.summary1$cp[best.subset1.by.cp], col="red", cex =2, pch =20)
plot(best.subset.summary1$bic, xlab="Number of Variables", ylab="BIC", type="l")
points(best.subset1.by.bic, best.subset.summary1$bic[best.subset1.by.bic], col="red", cex =2, pch =20)

# Part 5
## Best model using original variable
best1<-lm(Life.Exp~., data=state1)
summary(best1)

## Best model using logged variable
best2<-lm(Life.Exp ~ Population + Murder + HS.Grad + Frost , data=state1)
summary(best2)

## Compare models
anova(best1, best2,best.subset1)


# Part 7
# Prediction
# replace best to name of your best model
library(tibble)
new.df1<-tibble(Population = 23000, Murder = 2, HS.Grad = 45, Frost=70)
predict(best2, new.df1, interval = "confidence")
predict(best2, new.df1, interval = "prediction")


# ============ Question 2 : Shrinkage models============
# Packages
install.packages("doParallel")
library("doParallel")
library("glmnet")

# loading data

attach(data)
str(data)
summary(data)
cor(Age, Height)

# Part 1
# Training data
x <- model.matrix(Weight ~ Age + Height, data = data[1:900, ])
y <- data[1:900, ]$Weight
# Testing Data
x.test <- model.matrix(Weight ~ Age + Height, data = data[901:1034, ])
y.test <- data[901:1034, ]$Weight
registerDoParallel(6); getDoParWorkers()

# Part 2
lm.fit <-  lm(Weight ~ Age + Height, data = data[1:900, ])
summary(lm.fit)
lm.pred <-  predict(lm.fit, newx = x.test)
LM.MSE <- mean((y - lm.pred)^2)
LM.MSE

lm.test.r2 <-  1 - mean((y - lm.pred)^2) / mean((y.test - mean(y.test))^2)
lm.test.r2

# Part 3
cv.ridge <-  cv.glmnet(x, y, type.measure="mse", alpha=0, parallel=T)
## alpha =1 for lasso only, alpha = 0 for ridge only, and 0<alpha<1 to blend ridge & lasso penalty !!!!
plot(cv.ridge)
coef(cv.ridge)
sqrt(cv.ridge$cvm[cv.ridge$lambda == cv.ridge$lambda.1se])

#plot variable feature coefficients against the shrinkage parameter lambda.
glmmod <-glmnet(x, y, alpha = 0)
plot(glmmod, xvar="lambda")
grid()

# report the model coefficient estimates
coef(glmmod)[, 1]

cv.glmmod <- cv.glmnet(x, y, alpha=0)
plot(cv.glmmod)
mod.ridge <-  cv.glmnet(x, y, alpha = 0, thresh = 1e-12, parallel = T)
lambda.best1 <-  mod.ridge$lambda.min
lambda.best1

ridge.pred <-  predict(mod.ridge, newx = x.test, s = lambda.best1)
ridge.MSE <- mean((y.test - ridge.pred)^2)
ridge.MSE
ridge.test.r2 <-  1 - mean((y.test - ridge.pred)^2)/mean((y.test - mean(y.test))^2)
ridge.test.r2

# Part 4
mod.lasso <-  cv.glmnet(x, y, alpha = 1, thresh = 1e-12, parallel = T)

# report the model coefficient estimates
coef(mod.lasso)[,1]

## alpha =1 for lasso only, alpha = 0 for ridge only, and 0<alpha<1 for elastic net, a blend ridge & lasso penalty !!!!
lambda.best2 <- mod.lasso$lambda.min
lambda.best2

lasso.pred <- predict(mod.lasso, newx = x.test, s = lambda.best2)
LASSO.MSE <- mean((y.test - lasso.pred)^2)
LASSO.MSE
lasso.test.r2 <-  1 - mean((y.test - lasso.pred)^2)/mean((y.test - mean(y.test))^2)
lasso.test.r2
# Part 5
barplot(c(lm.test.r2, lasso.test.r2, ridge.test.r2), col = "red", names.arg = c("OLS", "LASSO", "Ridge"), main = "Testing Data Derived R-squared")

library(knitr) #  kable function to convert tabular R-results into Rmd tables
# create table as data frame
MSE_Table = data.frame(LM=LM.MSE, LASSO=LASSO.MSE, Ridge=ridge.MSE)

# convert to markdown
kable(MSE_Table, format="pandoc", caption="Test Dataset SSE Results", align=c("c", "c", "c"))

# ============ Question 3 : Logistic Regression============
# Packages
install.packages('tidyverse')
install.packages('modelr')
install.packages('broom') 

library(tidyverse)  # data manipulation and visualization
library(modelr)     # provides easy pipeline modeling functions
library(broom)      # helps to tidy up model outputs

# Load data 
(default <- as_tibble(ISLR::Default))
summary(default)

# Part 1
# Examine association 
# Creating plot using plot() function
plot(default$default, default$student)
plot(default$default, default$balance)
plot(default$default, default$income)

# Althernative way to create plots
install.packages('cowplot')
library(cowplot)
mosaicplot(student~default, data=default, color=TRUE)
ggplot(default, aes(x = default, y = balance)) +
  geom_boxplot() + theme_bw()
ggplot(default, aes(x = default, y = income)) +
  geom_boxplot() + theme_bw()

# Part 2
# Split the whole sample into a training set(60%) and testing set(40%)
set.seed(123)
sample <- sample(c(TRUE, FALSE), nrow(default), replace = T, prob = c(0.6,0.4))
train <- default[sample, ]
test <- default[!sample, ]

# Part 3
# Simple logistic regression
model1 <- glm(default ~ balance, family = "binomial", data = train)
summary(model1)
#### Additional Plot
#default %>%
#  mutate(prob = ifelse(default == "Yes", 1, 0)) %>%
#  ggplot(aes(balance, prob)) +
#  geom_point(alpha = .15) +
#  geom_smooth(method = "glm", method.args = list(family = "binomial")) +
#  ggtitle("Logistic regression model fit") +
#  xlab("Balance") +
#ylab("Probability of Default")

# Assession coefficients
tidy(model1)
exp(coef(model1))

model2 <- glm(default ~ student, family = "binomial", data = train)
summary(model2)
tidy(model2)
exp(coef(model2))

model3 <- glm(default ~ income, family = "binomial", data = train)
summary(model3)
tidy(model3)
exp(coef(model3))

# Part 4
# Making prediction
predict(model1, data.frame(balance = c(1000, 2000)), type = "response")
predict(model2, data.frame(student = factor(c("Yes", "No"))), type = "response")
predict(model3, data.frame(income = c(50, 70)), type = "response")

# Part 5
# Multiple logistic regression
model4<- glm(default ~ balance + income + student, family = "binomial", data = train)
summary(model4)
tidy(model4)
exp(coef(model4))

# Part 6
new.df <- tibble(balance = 1500, income = 40, student = c("Yes", "No"))
predict(model4, new.df, type = "response")

# Model evaluation
## Goodness of fit test using Chi-square
anova(model1, model2, model3, test = "Chisq")
anova(model1, model4, test = "Chisq")

## R-square
install.packages("pscl")
library(pscl)
mr<-list(model1 = pscl::pR2(model1)["McFadden"],
         model2 = pscl::pR2(model2)["McFadden"],
         model3 = pscl::pR2(model3)["McFadden"],
         model4 = pscl::pR2(model4)["McFadden"])
mr
## Residual
# Model 1
model1_data <- augment(model1) %>% 
  mutate(index = 1:n())

#### Additional plot
#ggplot(model1_data, aes(index, .std.resid, color = default)) + 
#  geom_point(alpha = .5) +
#  geom_ref_line(h = 3)

model1_data %>% 
  filter(abs(.std.resid) > 3)

# Cook's distance
plot(model1, which = 4, id.n = 5)
model1_data %>% 
  top_n(5, .cooksd)

# Model 2
model2_data <- augment(model2) %>% 
  mutate(index = 1:n())

model2_data %>% 
  filter(abs(.std.resid) > 3)

# Cook's distance
plot(model2, which = 4, id.n = 5)
model2_data %>% 
  top_n(5, .cooksd)


# Model 3
model3_data <- augment(model3) %>% 
  mutate(index = 1:n())

model3_data %>% 
  filter(abs(.std.resid) > 3)

# Cook's distance
plot(model3, which = 4, id.n = 5)
model3_data %>% 
  top_n(5, .cooksd)

# Model 4
model4_data <- augment(model4) %>% 
  mutate(index = 1:n())

model4_data %>% 
  filter(abs(.std.resid) > 3)

# Cook's distance
plot(model4, which = 4, id.n = 5)
model4_data %>% 
  top_n(5, .cooksd)


# Validation of predicted values
test.predicted.m1 <- predict(model1, newdata = test, type = "response")
test.predicted.m2 <- predict(model2, newdata = test, type = "response")
test.predicted.m3 <- predict(model3, newdata = test, type = "response")
test.predicted.m4 <- predict(model4, newdata = test, type = "response")

list(
  model1 = table(test$default, test.predicted.m1 > 0.5) %>% prop.table() %>% round(3),
  model2 = table(test$default, test.predicted.m2 > 0.5) %>% prop.table() %>% round(3),
  model3 = table(test$default, test.predicted.m3 > 0.5) %>% prop.table() %>% round(3),
  model4 = table(test$default, test.predicted.m4 > 0.5) %>% prop.table() %>% round(3)
)

# MSE
test %>%
  mutate(m1.pred = ifelse(test.predicted.m1 > 0.5, "Yes", "No"),
         m2.pred = ifelse(test.predicted.m2 > 0.5, "Yes", "No"),
         m3.pred = ifelse(test.predicted.m3 > 0.5, "Yes", "No"),
         m4.pred = ifelse(test.predicted.m4 > 0.5, "Yes", "No")) %>%
  summarise(m1.error = mean(default != m1.pred),
            m2.error = mean(default != m2.pred),
            m3.error = mean(default != m3.pred),
            m4.error = mean(default != m4.pred))

# ============ Question 4 : Poisson Regression============

# =======Data cleaning=========
# subset variables of interest from NELS data 
nels.var <- c("F1S10B","BYS12","BYS31A", "BYCNCPT1", "BYSES", "BYTXCOMP", "F1S51") 

# create new dataset with only variables of interest
count.data <- nels[nels.var]
# change names of variables
names(count.data) <- c("skipped", "sex", "race", "self.con1", "ses", "achievement",
                       "F1S51")
summary(count.data)

# Part 2
plot(count.data$skipped, ylab="Counts", xlab="# of skipped")

# =======Data cleaning continued=========
# change sex so that female = 0
count.data$skipped<-as.integer(count.data$skipped)
count.data$male <- ifelse(count.data$sex==2, 0,count.data$sex)
# recode college plans variable to 0 = no, 1= yes,
count.data$college <- count.data$F1S51
count.data$college[count.data$F1S51==1] <- 0
count.data$college[count.data$F1S51==2 | count.data$F1S51==3 | count.data$F1S51==4 |
                     count.data$F1S51==5] <- 1
# make race variable a factor and name the levels
count.data$race <- factor(count.data$race, levels=1:5, labels=c("asian", "hispanic",
                                                                "black", "white", "nat.american"))
# make white the comparison race group
count.data$race <- relevel(count.data$race, ref = 4)
# create new dataset without missing data
count.data <- na.omit(count.data)
# mean center continuous variables
count.data$self.con1<-as.numeric(count.data$self.con1)
count.data$self.con1.m <- scale(count.data$self.con1, center = TRUE, scale = FALSE)
count.data$ses.m <- scale(count.data$ses, center = TRUE, scale = FALSE)
count.data$achievement<-as.numeric(count.data$achievement)
count.data$achievement.m <- scale(count.data$achievement, center = TRUE, scale = FALSE) 
# =======END Data cleaning=========

summary(count.data)
str(count.data)

# part 3 : possible models
# based on your answer in part 2. 
# regression model
model1 <- glm(skipped ~ male + race + college + self.con1.m + ses.m + achievement.m,
            data = count.data)
# logistic model
model2 <- glm(skipped ~ male + race + college + self.con1.m + ses.m + achievement.m,
              data = count.data, family = binomial)
# poisson regression
model3 <- glm(skipped ~ male + race + college + self.con1.m + ses.m + achievement.m,
                data = count.data, family = poisson)
# Part 3
# summary of results
summary(model1)
summary(model2)
summary(model3)

# AIC values
AIC(model1)
AIC(model2)
AIC(model3)
# BIC values
BIC(model1)
BIC(model2)
BIC(model3)

# Part 4
# Overdisperson
plot(fitted(model3),(count.data$skipped-fitted(model3))^2,xlab=expression(hat(mu)),ylab=expression((y-hat(mu))^2))
abline(0,1)
(dp <- sum(residuals(model3,type="pearson")^2)/model3$df.res)
summary(model3,dispersion=dp)

