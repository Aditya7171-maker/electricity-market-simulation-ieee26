IEEE RTS-24 Electricity Market Simulation:
Single Hour Copper-Plate Economic Dispatch using Pyomo

This project implements a single-hour electricity market clearing model using the generator data from the IEEE Reliability Test System.

The model determines the least-cost generator dispatch, market clearing price, and market welfare metrics using linear optimization.

The implementation is written in Python using Pyomo and solved with GLPK.

Power System Dataset

The generator parameters are based on the dataset described in:

An Updated Version of the IEEE RTS 24‑Bus System for Electricity Market and Power System Operation Studies

This dataset is widely used in academic research for:

electricity market studies

economic dispatch problems

optimal power flow models

congestion analysis

Model Overview

The electricity market is modeled as a copper-plate system, meaning:

there are no transmission constraints

power can flow freely between all buses

the system behaves like a single node market

The system operator clears the market by solving a cost minimization problem.

Simulation Assumptions
Time Horizon

Single hourly market clearing.

Selected hour:
Hour 18

System Demand
Demand = 2650.5 MW

This value is taken from the RTS load profile.

Demand is assumed to be perfectly inelastic.

Wind Generation

Installed wind capacity:

1200 MW

Wind availability assumed:

40%

Available wind generation used in the model:

Wind Output = 480 MW

Wind marginal cost assumed:

0 $/MWh
Consumer Bid Price

To evaluate consumer surplus, a simplified demand bid price is assumed:

Bid Price = 100 $/MWh

This represents the maximum willingness to pay for electricity.

Model Outputs

The optimization determines:

• optimal generator dispatch
• market clearing price
• total generation cost
• producer profits
• consumer surplus
• social welfare

Simulation Results
Market Clearing Price
13.32 $/MWh

The clearing price equals the marginal cost of the marginal generator required to meet demand.

Total Generation Cost
$16,268.56
Generator Dispatch
Generator	Dispatch (MW)
U2	100.5
U6	155
U7	155
U8	400
U9	400
U10	300
U11	310
U12	350
Wind	480

High cost generators remain offline.

This demonstrates the merit-order dispatch principle used in real electricity markets.

Market Welfare Metrics
Producer Profit

Generators with cost below the market price earn profit:

Profit=(MarketPrice−Cost)×Generation

Example:

Generator	Profit
U8	2920
U9	3140
U10	3996
Consumer Surplus
Consumer Surplus=(Bid Price−Market Price)×Demand

Result:

Consumer Surplus = $229,745
Social Welfare

Total welfare in the market is defined as:

Social Welfare = Consumer Surplus + Producer Profit

Result:

Social Welfare = $248,781
Visualizations

The project generates three market analysis plots.

Generator Dispatch

Shows how much power each generator produces.

Merit Order Curve

Displays generators sorted by marginal cost with cumulative capacity.

This illustrates the supply curve of the electricity market.

Generator Cost vs Dispatch

Compares generator marginal cost with dispatch level and highlights the market clearing price.

Tools Used

Python libraries used:

Pyomo
GLPK
Pandas
Matplotlib

These tools allow formulation, solution, and visualization of the electricity market model
