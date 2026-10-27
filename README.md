# Credit-Economic-Scenario-Generator (CESG)

**Why CESG?**
No vibe coding, all things elegantly and concisely coded based on classic financial mathematics, ensuring code interpretability and execution efficiency.

**Building Block 1: Credit Yield Martingale Tester**
**Objective**: After thousands of timesteps of Monte Carlo simulation, you may want to check whether the simulated credit yield output passes martingale test to ensure the model generates appropriate scenarios for risk-neutral pricing. 
**Theory**: Under risk-neutral measure, deflated asset prices are always martingale.
**Methodology**: The program constructed a Constant Maturity Index (CMI, namely, the value of an investment portfolio where corporate bonds held are always have a same equivalent time to maturity (or term) based on the simulated credit yields. Then, the CMIs are deflated by multiplying by the simulated risk-free deflator of the corresponding market to get the deflated CMIs. By comparing the time series of deflated CMI to the initial wealth (here, it is set to be 1), we can know whether the simulation passes the martingale test.
**Caution**: When constructing the realized transition proportion matrix, two methods are adopted: 1. Take the geometric average of the rating transition matrices of the last timepoint and the current timepoint. 2. Take the matrix multiplication of the rating transition matrices of the last timepoint and the current timepoint, then take the matrix square root of the multiplication.

**Next Development Step**: Develop the full JLT model logic for credit economic scenario generator. The current martingale tester will act as a quality assessment tool!

I am open to any further discussions on stochastic modeling, risk management and quantitative research!
